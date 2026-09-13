import os
import pickle
from collections import defaultdict, deque

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="centered"
)

# ==========================================
# 1. LOAD MODEL ARTIFACTS
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "predictor_artifacts.pkl")

with open(MODEL_PATH, "rb") as f:
    artifacts = pickle.load(f)

model = artifacts["model"]
features = artifacts["features"]
encoder = artifacts["encoder"]
teams_list = artifacts["teams"]

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
            home_avg_scored, home_avg_conceded,
            home_wins, home_draws, home_losses,
            away_avg_scored, away_avg_conceded,
            away_wins, away_draws, away_losses,
            h2h_home_wins, h2h_draws, h2h_away_wins,
        ]],
        columns=features,
    )

    probabilities = model.predict_proba(X)[0]

    return {
        "home_win": probabilities[2],
        "draw": probabilities[1],
        "away_win": probabilities[0],
    }


# ==========================================
# 2. TEAM BADGES (self-contained, no external requests)
# ==========================================
TEAM_BADGES = {
    "Arsenal": ("ARS", "#EF0107"),
    "Aston Villa": ("AVL", "#670E36"),
    "Bournemouth": ("BOU", "#DA291C"),
    "Brentford": ("BRE", "#E30613"),
    "Brighton & Hove Albion": ("BHA", "#0057B8"),
    "Burnley": ("BUR", "#6C1D45"),
    "Cardiff City": ("CAR", "#0070B5"),
    "Chelsea": ("CHE", "#034694"),
    "Crystal Palace": ("CRY", "#1B458F"),
    "Everton": ("EVE", "#003399"),
    "Fulham": ("FUL", "#CC0000"),
    "Huddersfield Town": ("HUD", "#0E63AD"),
    "Ipswich Town": ("IPS", "#0044A9"),
    "Leeds United": ("LEE", "#1D428A"),
    "Leicester City": ("LEI", "#003090"),
    "Liverpool": ("LIV", "#C8102E"),
    "Luton Town": ("LUT", "#F78F1E"),
    "Manchester City": ("MCI", "#6CABDD"),
    "Manchester United": ("MUN", "#DA291C"),
    "Newcastle United": ("NEW", "#241F20"),
    "Norwich City": ("NOR", "#FFF200"),
    "Nottingham Forest": ("NFO", "#DD0000"),
    "Sheffield United": ("SHU", "#EE2737"),
    "Southampton": ("SOU", "#D71920"),
    "Stoke City": ("STO", "#E03A3E"),
    "Sunderland": ("SUN", "#EB172F"),
    "Swansea City": ("SWA", "#121212"),
    "Tottenham Hotspur": ("TOT", "#132257"),
    "Watford": ("WAT", "#FBEE23"),
    "West Bromwich Albion": ("WBA", "#122F67"),
    "West Ham United": ("WHU", "#7A263A"),
    "Wolverhampton Wanderers": ("WOL", "#FDB913"),
}


def render_badge(team_name: str, size: int = 60) -> str:
    initials, color = TEAM_BADGES.get(team_name, ("?", "#666666"))
    font_size = int(size * 0.36)
    return f"""
    <div style="
        width:{size}px; height:{size}px; border-radius:50%;
        background:{color}; display:flex; align-items:center;
        justify-content:center; margin:0 auto;
        border: 2px solid rgba(255,255,255,0.4);
    ">
        <span style="color:#ffffff; font-weight:800; font-size:{font_size}px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);">{initials}</span>
    </div>
    """


# ==========================================
# 3. CUSTOM CSS STYLING
# ==========================================
css = """
<style>
.stApp { background-color: #38003c !important; }

#title {
    text-align: center; font-size: 38px; font-weight: 800;
    color: #FFFFFF !important; margin-bottom: 0px;
}
#subtitle {
    text-align: center; font-size: 16px; color: #E8DBED !important;
    margin-bottom: 25px; opacity: 0.9;
}

div[data-testid="stSelectbox"] label p {
    color: #FFFFFF !important; font-weight: 700 !important; font-size: 14px !important;
}
div[data-baseweb="select"] > div:first-child {
    background-color: #1e1e24 !important; border-radius: 10px !important;
    border: 1.5px solid #6B1D78 !important;
}
div[data-baseweb="select"] * {
    color: #ffffff !important; font-weight: 600 !important; fill: #ffffff !important;
}
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
    background-color: #1e1e24 !important; border-radius: 10px !important;
    border: 1px solid #6B1D78 !important;
}
li[role="option"], div[role="option"] {
    background-color: #1e1e24 !important; color: #ffffff !important;
}
li[role="option"]:hover, li[role="option"][aria-selected="true"] {
    background-color: #4A0B50 !important; color: #00ff85 !important;
}

.vs-banner {
    display: flex; align-items: center; justify-content: space-around;
    background: #4A0B50; border: 2px solid #6B1D78; border-radius: 16px;
    padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.vs-team { text-align: center; font-weight: 700; color: #FFFFFF !important; font-size: 16px; margin-top: 8px; }
.vs-badge {
    background: #00ff85; color: #38003c; font-weight: 900; font-size: 18px;
    padding: 8px 16px; border-radius: 50%; box-shadow: 0 2px 8px rgba(0,255,133,0.3);
}

.result-wrapper {
    margin-top: 20px; padding: 20px; background: #4A0B50; border-radius: 16px;
    border: 2px solid #6B1D78; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.prediction-header { text-align: center; font-size: 20px; color: #FFFFFF !important; margin-bottom: 20px; }
.prediction-header strong {
    color: #38003c !important; background: #00ff85; padding: 3px 10px; border-radius: 6px;
}

.cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
.prob-card {
    position: relative; background: #38003c; border: 1.5px solid #6B1D78;
    border-radius: 12px; padding: 15px 10px; text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.prob-card:hover { transform: translateY(-3px); }
.prob-card.highlight-card {
    border-color: #00ff85; background: #500C57; box-shadow: 0 4px 12px rgba(0,255,133,0.2);
}
.favored-badge {
    position: absolute; top: -10px; left: 50%; transform: translateX(-50%);
    background: #00ff85; color: #38003c; font-size: 10px; font-weight: 800;
    padding: 2px 8px; border-radius: 10px; letter-spacing: 0.5px;
}
.card-title { font-size: 16px; font-weight: 700; color: #FFFFFF !important; margin-top: 8px; }
.card-subtitle { font-size: 12px; color: #E8DBED !important; margin-bottom: 8px; }
.card-pct { font-size: 24px; font-weight: 800; color: #00ff85 !important; margin-bottom: 10px; }

.mini-bar-track { width: 100%; height: 8px; background: #250028; border-radius: 4px; overflow: hidden; }
.mini-bar-fill { height: 100%; background: #8A409A; border-radius: 4px; }
.mini-bar-fill.highlight-card { background: #00ff85; }

.placeholder {
    margin-top: 20px; padding: 25px; text-align: center; font-size: 16px;
    color: #FFFFFF !important; border: 2px dashed #6B1D78; border-radius: 14px;
    background: #4A0B50;
}

div.stButton > button:first-child {
    background-color: #00ff85 !important; color: #38003c !important; border: none !important;
    font-size: 18px !important; font-weight: bold !important; border-radius: 10px !important;
    padding: 12px 0px !important;
}
div.stButton > button:first-child:hover {
    background-color: #00e676 !important; color: #250028 !important;
    box-shadow: 0 4px 15px rgba(0,255,133,0.4);
}

@media (max-width: 600px) {
    .cards-grid { grid-template-columns: 1fr; }
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 4. APP UI & LOGIC
# ==========================================
st.markdown('<div id="title">Premier League Match Predictor</div>', unsafe_allow_html=True)
st.markdown('<div id="subtitle">Select teams to analyze win probabilities powered by Machine Learning</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("HOME TEAM", teams_list, index=teams_list.index("Chelsea") if "Chelsea" in teams_list else 0)
with col2:
    away_team = st.selectbox("AWAY TEAM", teams_list, index=teams_list.index("Fulham") if "Fulham" in teams_list else 1)

home_badge = render_badge(home_team, size=60)
away_badge = render_badge(away_team, size=60)

st.markdown(
    f"""
    <div class="vs-banner">
        <div>{home_badge}<div class="vs-team">{home_team}</div></div>
        <div class="vs-badge">VS</div>
        <div>{away_badge}<div class="vs-team">{away_team}</div></div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("RUN PREDICTION", use_container_width=True):

    if home_team == away_team:
        st.markdown(
            '<div class="placeholder">Please select two different teams.</div>',
            unsafe_allow_html=True
        )
    else:
        result = predict_match(home_team, away_team)

        prob_home = result["home_win"] * 100
        prob_draw = result["draw"] * 100
        prob_away = result["away_win"] * 100

        favored = home_team if prob_home > prob_away else away_team

        home_small = render_badge(home_team, size=36)
        away_small = render_badge(away_team, size=36)

        st.markdown(
            f"""
            <div class="result-wrapper">
                <div class="prediction-header">Match Forecast: <strong>{favored} favored</strong></div>
                <div class="cards-grid">
                    <div class="prob-card {'highlight-card' if favored == home_team else ''}">
                        {'<div class="favored-badge">FAVORED</div>' if favored == home_team else ''}
                        {home_small}
                        <div class="card-title">{home_team}</div>
                        <div class="card-subtitle">Home Win</div>
                        <div class="card-pct">{prob_home:.1f}%</div>
                        <div class="mini-bar-track">
                            <div class="mini-bar-fill {'highlight-card' if favored == home_team else ''}" style="width: {prob_home:.1f}%;"></div>
                        </div>
                    </div>
                    <div class="prob-card">
                        <div style="height:36px;"></div>
                        <div class="card-title">Draw</div>
                        <div class="card-subtitle">Equal Points</div>
                        <div class="card-pct">{prob_draw:.1f}%</div>
                        <div class="mini-bar-track">
                            <div class="mini-bar-fill" style="width: {prob_draw:.1f}%;"></div>
                        </div>
                    </div>
                    <div class="prob-card {'highlight-card' if favored == away_team else ''}">
                        {'<div class="favored-badge">FAVORED</div>' if favored == away_team else ''}
                        {away_small}
                        <div class="card-title">{away_team}</div>
                        <div class="card-subtitle">Away Win</div>
                        <div class="card-pct">{prob_away:.1f}%</div>
                        <div class="mini-bar-track">
                            <div class="mini-bar-fill {'highlight-card' if favored == away_team else ''}" style="width: {prob_away:.1f}%;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.markdown(
        '<div class="placeholder">Select two teams above and click <strong>RUN PREDICTION</strong> to see probabilities.</div>',
        unsafe_allow_html=True
    )