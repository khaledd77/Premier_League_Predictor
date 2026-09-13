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
        return "<div class='placeholder'>⚠️ Please select two different teams to run a match prediction.</div>"

    result = predict_match(home_team, away_team)

    outcomes = [
        (home_team, result["home_win"] * 100, TEAM_LOGOS.get(home_team, DEFAULT_LOGO), "Home Win"),
        ("Draw", result["draw"] * 100, "", "Draw"),
        (away_team, result["away_win"] * 100, TEAM_LOGOS.get(away_team, DEFAULT_LOGO), "Away Win"),
    ]

    best_outcome = max(outcomes, key=lambda x: x[1])
    best_label = best_outcome[0]

    cards_html = ""
    for label, pct, logo_url, subtitle in outcomes:
        is_best = "highlight-card" if label == best_label else ""
        badge_tag = '<span class="favored-badge">FAVORED</span>' if label == best_label else ''
        img_tag = f'<img src="{logo_url}" width="38" style="margin-bottom:8px;">' if logo_url else '<div style="height:38px;"></div>'

        cards_html += (
            f'<div class="prob-card {is_best}">'
            f'{badge_tag}'
            f'{img_tag}'
            f'<div class="card-title">{label}</div>'
            f'<div class="card-subtitle">{subtitle}</div>'
            f'<div class="card-pct">{pct:.1f}%</div>'
            f'<div class="mini-bar-track"><div class="mini-bar-fill {is_best}" style="width:{pct:.1f}%;"></div></div>'
            f'</div>'
        )

    return (
        f'<div class="result-wrapper">'
        f'<div class="prediction-header">Match Forecast: <strong>{best_label} favored</strong></div>'
        f'<div class="cards-grid">{cards_html}</div>'
        f'</div>'
    )


# --- INTUITIVE & MODERN CSS STYLING ---
# --- LIGHT PURPLE BACKGROUND & UI STYLING ---
css = """
<style>
/* Main App Background */
.stApp {
    background-color: #F4E8F7 !important;
}

/* Header Styling */
#title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #4A1252;
    margin-bottom: 0px;
}

#subtitle {
    text-align: center;
    font-size: 16px;
    color: #6A3A73;
    margin-bottom: 25px;
}

/* Matchup Header Card */
.vs-banner {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: #FFFFFF;
    border: 2px solid #822C8E;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(74, 18, 82, 0.08);
}

.vs-team {
    text-align: center;
    font-weight: 700;
    color: #4A1252;
    font-size: 16px;
}

.vs-badge {
    background: #6B1D78;
    color: #00ff85;
    font-weight: 900;
    font-size: 18px;
    padding: 8px 16px;
    border-radius: 50%;
    box-shadow: 0 2px 8px rgba(107, 29, 120, 0.2);
}

/* Prediction Output Box */
.result-wrapper {
    margin-top: 20px;
    padding: 20px;
    background: #FFFFFF;
    border-radius: 16px;
    border: 2px solid #822C8E;
    box-shadow: 0 4px 15px rgba(74, 18, 82, 0.1);
}

.prediction-header {
    text-align: center;
    font-size: 20px;
    color: #4A1252;
    margin-bottom: 20px;
}

.prediction-header strong {
    color: #38003c;
    background: #00ff85;
    padding: 3px 10px;
    border-radius: 6px;
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.prob-card {
    position: relative;
    background: #FAF3FC;
    border: 2px solid #E2C7E8;
    border-radius: 12px;
    padding: 15px 10px;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.prob-card:hover {
    transform: translateY(-3px);
}

.prob-card.highlight-card {
    border-color: #822C8E;
    background: #F3DCF7;
    box-shadow: 0 4px 12px rgba(130, 44, 142, 0.15);
}

.favored-badge {
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    background: #6B1D78;
    color: #00ff85;
    font-size: 10px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 10px;
    letter-spacing: 0.5px;
}

.card-title {
    font-size: 16px;
    font-weight: 700;
    color: #4A1252;
    margin-top: 5px;
}

.card-subtitle {
    font-size: 12px;
    color: #666;
    margin-bottom: 8px;
}

.card-pct {
    font-size: 24px;
    font-weight: 800;
    color: #38003c;
    margin-bottom: 10px;
}

.mini-bar-track {
    width: 100%;
    height: 8px;
    background: #E2C7E8;
    border-radius: 4px;
    overflow: hidden;
}

.mini-bar-fill {
    height: 100%;
    background: #AC71B8;
    border-radius: 4px;
}

.mini-bar-fill.highlight-card {
    background: #00ff85;
}

.placeholder {
    margin-top: 20px;
    padding: 25px;
    text-align: center;
    font-size: 16px;
    color: #5A2A63;
    border: 2px dashed #822C8E;
    border-radius: 14px;
    background: #FFFFFF;
}

/* Streamlit Button Override */
div.stButton > button:first-child {
    background-color: #6B1D78 !important;
    color: #00ff85 !important;
    border: none !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    padding: 12px 0px !important;
}

div.stButton > button:first-child:hover {
    background-color: #4A1252 !important;
    color: #00ff85 !important;
    box-shadow: 0 4px 12px rgba(107, 29, 120, 0.3);
}

@media (max-width: 600px) {
    .cards-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# --- STREAMLIT USER INTERFACE ---
st.markdown("<h1 id='title'>Premier League Match Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p id='subtitle'>Select teams to analyze win probabilities powered by Machine Learning</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("HOME TEAM", options=teams, index=teams.index("Chelsea") if "Chelsea" in teams else 0)

with col2:
    away_team = st.selectbox("AWAY TEAM", options=teams, index=teams.index("Fulham") if "Fulham" in teams else 0)

# Dynamic VS Matchup Header
vs_html = f"""
<div class="vs-banner">
    <div class="vs-team">
        <img src="{TEAM_LOGOS.get(home_team, DEFAULT_LOGO)}" width="45"><br>
        {home_team}
    </div>
    <div class="vs-badge">VS</div>
    <div class="vs-team">
        <img src="{TEAM_LOGOS.get(away_team, DEFAULT_LOGO)}" width="45"><br>
        {away_team}
    </div>
</div>
"""
st.html(vs_html)

predict_clicked = st.button("RUN PREDICTION", type="primary", use_container_width=True)

if predict_clicked:
    html_output = render_results(home_team, away_team)
    st.html(html_output)
else:
    st.html("<div class='placeholder'>Select two teams above and click <strong>RUN PREDICTION</strong> to see probabilities.</div>")