import os
import pickle
from collections import defaultdict, deque

import pandas as pd
import streamlit as st

# Set Streamlit Page Title & Configuration
st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="centered",
)

# --- OFFICIAL PREMIER LEAGUE TEAM CREST LOGOS ---
TEAM_LOGOS = {
    "Arsenal": "https://resources.premierleague.com/premierleague/badges/50/t3.png",
    "Aston Villa": "https://resources.premierleague.com/premierleague/badges/50/t7.png",
    "Bournemouth": "https://resources.premierleague.com/premierleague/badges/50/t91.png",
    "Brentford": "https://resources.premierleague.com/premierleague/badges/50/t94.png",
    "Brighton": "https://resources.premierleague.com/premierleague/badges/50/t36.png",
    "Chelsea": "https://resources.premierleague.com/premierleague/badges/50/t8.png",
    "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/50/t9.png",
    "Everton": "https://resources.premierleague.com/premierleague/badges/50/t11.png",
    "Fulham": "https://resources.premierleague.com/premierleague/badges/50/t54.png",
    "Ipswich": "https://resources.premierleague.com/premierleague/badges/50/t40.png",
    "Leicester": "https://resources.premierleague.com/premierleague/badges/50/t13.png",
    "Liverpool": "https://resources.premierleague.com/premierleague/badges/50/t14.png",
    "Manchester City": "https://resources.premierleague.com/premierleague/badges/50/t43.png",
    "Manchester United": "https://resources.premierleague.com/premierleague/badges/50/t1.png",
    "Newcastle United": "https://resources.premierleague.com/premierleague/badges/50/t4.png",
    "Nottingham Forest": "https://resources.premierleague.com/premierleague/badges/50/t17.png",
    "Southampton": "https://resources.premierleague.com/premierleague/badges/50/t20.png",
    "Tottenham": "https://resources.premierleague.com/premierleague/badges/50/t6.png",
    "West Ham": "https://resources.premierleague.com/premierleague/badges/50/t21.png",
    "Wolves": "https://resources.premierleague.com/premierleague/badges/50/t39.png"
}
DEFAULT_LOGO = "https://resources.premierleague.com/premierleague/badges/50/t-default.png"

# --- FILE PATH RESOLUTION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "predictor_artifacts.pkl")

with open(MODEL_PATH, "rb") as f:
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

    X = pd.DataFrame(
        [[
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
            h2h_away_wins,
        ]],
        columns=features,
    )

    probabilities = model.predict_proba(X)[0]

    return {
        "home_win": probabilities[2],
        "draw": probabilities[1],
        "away_win": probabilities[0],
    }


def render_results(home_team, away_team):
    if home_team == away_team:
        return "<div class='placeholder'>Please select two different teams.</div>"

    result = predict_match(home_team, away_team)

    outcomes = [
        (home_team, result["home_win"] * 100, TEAM_LOGOS.get(home_team, DEFAULT_LOGO)),
        ("Draw", result["draw"] * 100, ""),
        (away_team, result["away_win"] * 100, TEAM_LOGOS.get(away_team, DEFAULT_LOGO)),
    ]

    best_label = max(outcomes, key=lambda x: x[1])[0]

    rows = ""
    for label, pct, logo_url in outcomes:
        is_best = "highlight" if label == best_label else ""
        img_tag = f'<img src="{logo_url}" width="26" style="vertical-align:middle; margin-right:8px;">' if logo_url else ''
        
        rows += (
            f'<div class="outcome-row {is_best}">'
            f'<div class="outcome-label">{img_tag}{label}</div>'
            f'<div class="bar-track">'
            f'<div class="bar-fill {is_best}" style="width:{pct:.1f}%;"></div>'
            f'</div>'
            f'<div class="outcome-pct">{pct:.1f}%</div>'
            f'</div>'
        )

    return (
        f'<div class="result-box">'
        f'<div class="favored-tag">Most Likely: <strong>{best_label}</strong></div>'
        f'{rows}'
        f'</div>'
    )


# --- OFFICIAL PREMIER LEAGUE CSS STYLING ---
# --- LIGHTER PREMIER LEAGUE PURPLE CSS STYLING ---
css = """
<style>
/* Main Title & Subtitle */
#title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #6B1D78;
    letter-spacing: -0.5px;
}

#subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

/* Prediction Result Card */
.result-box {
    margin-top: 25px;
    padding: 30px;
    border: 2px solid #6B1D78;
    border-radius: 16px;
    background: #FAEFFC;
    box-shadow: 0 4px 12px rgba(107, 29, 120, 0.08);
}

.placeholder {
    margin-top: 25px;
    padding: 30px;
    text-align: center;
    font-size: 18px;
    color: #777;
    border: 2px dashed #6B1D78;
    border-radius: 16px;
    background: #fafafa;
}

.favored-tag {
    text-align: center;
    font-size: 20px;
    color: #6B1D78;
    margin-bottom: 25px;
    font-weight: 600;
}

.favored-tag strong {
    color: #38003c;
    background: #00ff85;
    padding: 4px 12px;
    border-radius: 6px;
}

/* Progress Bars & Rows */
.outcome-row {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 18px;
}

.outcome-label {
    min-width: 160px;
    font-size: 18px;
    font-weight: 700;
    color: #6B1D78;
    text-align: right;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.bar-track {
    flex: 1;
    height: 28px;
    background: #EED7F2;
    border-radius: 14px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: #B484BC;
    border-radius: 14px;
    transition: width 0.5s ease;
}

/* Winning / Most Likely Bar Highlight */
.bar-fill.highlight {
    background: #00ff85;
}

.outcome-row.highlight .outcome-label {
    color: #6B1D78;
}

.outcome-pct {
    min-width: 65px;
    font-size: 18px;
    font-weight: 700;
    color: #6B1D78;
}

.outcome-row.highlight .outcome-pct {
    color: #6B1D78;
    font-size: 20px;
}

/* Streamlit Button Override */
div.stButton > button:first-child {
    background-color: #6B1D78 !important;
    color: #00ff85 !important;
    border: none !important;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    padding: 12px 0px !important;
}

div.stButton > button:first-child:hover {
    background-color: #52145D !important;
    color: #00ff85 !important;
    box-shadow: 0 4px 10px rgba(107, 29, 120, 0.3);
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# --- STREAMLIT USER INTERFACE ---
st.markdown("<h1 id='title'>Premier League Match Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p id='subtitle'>Predict the outcome of a Premier League match using Machine Learning</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("HOME TEAM", options=teams, index=teams.index("Chelsea") if "Chelsea" in teams else 0)
    st.image(TEAM_LOGOS.get(home_team, DEFAULT_LOGO), width=50)

with col2:
    away_team = st.selectbox("AWAY TEAM", options=teams, index=teams.index("Fulham") if "Fulham" in teams else 0)
    st.image(TEAM_LOGOS.get(away_team, DEFAULT_LOGO), width=50)

predict_clicked = st.button("PREDICT MATCH", type="primary", use_container_width=True)

if predict_clicked:
    html_output = render_results(home_team, away_team)
    st.html(html_output)
else:
    st.html("<div class='placeholder'>Select two teams and click Predict to see the odds.</div>")