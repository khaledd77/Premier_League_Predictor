import pickle
from collections import defaultdict, deque

import pandas as pd
import gradio as gr

with open("predictor_artifacts.pkl", "rb") as f:
    artifacts = pickle.load(f)

model = artifacts["model"]
features = artifacts["features"]
encoder = artifacts["encoder"]
teams = artifacts["teams"]

team_stats = defaultdict(lambda: {"goals_scored": [], "goals_conceded": []})
team_stats.update(artifacts["team_stats"])

last5 = defaultdict(lambda: deque(maxlen=5))
for team, results in artifacts["last5"].items():
    last5[team] = deque(results, maxlen=5)

h2h = defaultdict(lambda: {"home_wins": 0, "draws": 0, "away_wins": 0})
h2h.update(artifacts["h2h"])


def predict_match(home_team, away_team):

    home_avg_scored = sum(team_stats[home_team]["goals_scored"]) / len(
        team_stats[home_team]["goals_scored"]
    )

    home_avg_conceded = sum(team_stats[home_team]["goals_conceded"]) / len(
        team_stats[home_team]["goals_conceded"]
    )

    away_avg_scored = sum(team_stats[away_team]["goals_scored"]) / len(
        team_stats[away_team]["goals_scored"]
    )

    away_avg_conceded = sum(team_stats[away_team]["goals_conceded"]) / len(
        team_stats[away_team]["goals_conceded"]
    )

    home_last5 = last5[home_team]
    away_last5 = last5[away_team]

    home_wins = home_last5.count("W")
    home_draws = home_last5.count("D")
    home_losses = home_last5.count("L")

    away_wins = away_last5.count("W")
    away_draws = away_last5.count("D")
    away_losses = away_last5.count("L")

    h2h_home_wins = 0
    h2h_draws = 0
    h2h_away_wins = 0

    if (home_team, away_team) in h2h:

        h2h_home_wins = h2h[(home_team, away_team)]["home_wins"]
        h2h_draws = h2h[(home_team, away_team)]["draws"]
        h2h_away_wins = h2h[(home_team, away_team)]["away_wins"]

    elif (away_team, home_team) in h2h:

        h2h_home_wins = h2h[(away_team, home_team)]["away_wins"]
        h2h_draws = h2h[(away_team, home_team)]["draws"]
        h2h_away_wins = h2h[(away_team, home_team)]["home_wins"]

    X = pd.DataFrame([[
        home_avg_scored,
        home_avg_conceded,
        home_wins,
        home_draws,
        home_losses,
        away_avg_scored,
        away_avg_conceded,
        away_wins,
        away_draws,
        away_losses,
        h2h_home_wins,
        h2h_draws,
        h2h_away_wins
    ]], columns=features)

    probabilities = model.predict_proba(X)[0]

    return {
        "home_win": probabilities[2],
        "draw": probabilities[1],
        "away_win": probabilities[0]
    }


def predict_for_gui(home_team, away_team):

    if home_team == away_team:
        return "<div class='placeholder'>Please select two different teams.</div>"

    result = predict_match(home_team, away_team)

    outcomes = [
        (home_team, result["home_win"] * 100),
        ("Draw", result["draw"] * 100),
        (away_team, result["away_win"] * 100),
    ]

    best_label = max(outcomes, key=lambda x: x[1])[0]

    rows = ""
    for label, pct in outcomes:
        is_best = "highlight" if label == best_label else ""
        rows += f"""
        <div class="outcome-row {is_best}">
            <div class="outcome-label">{label}</div>
            <div class="bar-track">
                <div class="bar-fill {is_best}" style="width:{pct:.1f}%;"></div>
            </div>
            <div class="outcome-pct">{pct:.1f}%</div>
        </div>
        """

    return f"""
    <div class='result-box'>
        <div class='favored-tag'>Most Likely: <strong>{best_label}</strong></div>
        {rows}
    </div>
    """


css = """
body {
    background: white;
}

#title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1565c0;
}

#subtitle {
    text-align: center;
    font-size: 20px;
    color: #555;
}

.team-dropdown {
    font-size: 20px !important;
}

#predict-button {
    font-size: 24px !important;
    font-weight: bold;
    height: 65px;
    background: #1565c0 !important;
    color: white !important;
}

.result-box {
    margin-top: 25px;
    padding: 30px;
    border: 2px solid #1565c0;
    border-radius: 15px;
    background: #f5f9ff;
}

.placeholder {
    margin-top: 25px;
    padding: 30px;
    text-align: center;
    font-size: 18px;
    color: #888;
    border: 2px dashed #ccc;
    border-radius: 15px;
}

.favored-tag {
    text-align: center;
    font-size: 20px;
    color: #555;
    margin-bottom: 25px;
}

.favored-tag strong {
    color: #0d47a1;
}

.outcome-row {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 18px;
}

.outcome-label {
    min-width: 140px;
    font-size: 18px;
    font-weight: bold;
    color: #1565c0;
    text-align: right;
}

.bar-track {
    flex: 1;
    height: 28px;
    background: #e3ecf7;
    border-radius: 14px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: #90a4c4;
    border-radius: 14px;
}

.bar-fill.highlight {
    background: #1565c0;
}

.outcome-row.highlight .outcome-label {
    color: #0d47a1;
}

.outcome-pct {
    min-width: 60px;
    font-size: 18px;
    font-weight: bold;
    color: #333;
}

.outcome-row.highlight .outcome-pct {
    color: #0d47a1;
    font-size: 20px;
}

@media (max-width: 600px) {

    #title {
        font-size: 28px;
        line-height: 1.2;
    }

    #subtitle {
        font-size: 15px;
        line-height: 1.4;
        padding: 0 10px;
    }

    .team-dropdown {
        font-size: 16px !important;
    }

    #predict-button {
        font-size: 19px !important;
        height: 55px;
    }

    .result-box {
        padding: 20px;
    }

    .outcome-label {
        min-width: 90px;
        font-size: 14px;
    }

    .outcome-pct {
        min-width: 45px;
        font-size: 14px;
    }

    .bar-track {
        height: 22px;
    }
}
"""


with gr.Blocks(title="Premier League Match Predictor") as demo:

    gr.Markdown(
        "# ⚽ Premier League Match Predictor",
        elem_id="title"
    )

    gr.Markdown(
        "Predict the outcome of a Premier League match using Machine Learning",
        elem_id="subtitle"
    )

    with gr.Row():

        home_team = gr.Dropdown(
            choices=teams,
            label="HOME TEAM",
            value="Chelsea",
            elem_classes="team-dropdown"
        )

        away_team = gr.Dropdown(
            choices=teams,
            label="AWAY TEAM",
            value="Fulham",
            elem_classes="team-dropdown"
        )

    predict_button = gr.Button(
        "⚽ PREDICT MATCH",
        variant="primary",
        elem_id="predict-button"
    )

    prediction = gr.HTML(
        value="<div class='placeholder'>Select two teams and click Predict to see the odds.</div>"
    )

    predict_button.click(
        fn=predict_for_gui,
        inputs=[home_team, away_team],
        outputs=prediction
    )


demo.launch()