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

# --- OFFICIAL PREMIER LEAGUE TEAM CREST LOGOS (UPDATED & RELIABLE SVGs) ---
TEAM_LOGOS = {
    "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Aston Villa": (
        "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg"
    ),
    "Bournemouth": (
        "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg"
    ),
    "Brentford": (
        "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg"
    ),
    "Brighton": (
        "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg"
    ),
    "Brighton & Hove Albion": (
        "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg"
    ),
    "Burnley": (
        "https://upload.wikimedia.org/wikipedia/en/6/62/Burnley_F.C._logo.svg"
    ),
    "Chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "Crystal Palace": (
        "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg"
    ),
    "Everton": (
        "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg"
    ),
    "Fulham": (
        "https://upload.wikimedia.org/wikipedia/en/7/70/Fulham_FC_%28shield%29.svg"
    ),
    "Huddersfield Town": (
        "https://upload.wikimedia.org/wikipedia/en/7/7d/Huddersfield_Town_A.F.C._logo.svg"
    ),
    "Ipswich": (
        "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town_FC_logo.svg"
    ),
    "Ipswich Town": (
        "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town_FC_logo.svg"
    ),
    "Leicester": (
        "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg"
    ),
    "Leicester City": (
        "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg"
    ),
    "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
    "Luton Town": (
        "https://upload.wikimedia.org/wikipedia/en/9/9d/LutonTownFC2009.svg"
    ),
    "Manchester City": (
        "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"
    ),
    "Manchester United": (
        "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"
    ),
    "Newcastle United": (
        "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg"
    ),
    "Norwich City": (
        "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City_FC_logo.svg"
    ),
    "Nottingham Forest": (
        "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg"
    ),
    "Southampton": (
        "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"
    ),
    "Stoke City": (
        "https://upload.wikimedia.org/wikipedia/en/2/29/Stoke_City_FC.svg"
    ),
    "Tottenham": (
        "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"
    ),
    "West Ham": (
        "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg"
    ),
    "Wolves": (
        "https://upload.wikimedia.org/wikipedia/en/c/fc/Wolverhampton_Wanderers.svg"
    ),
    "Wolverhampton Wanderers": (
        "https://upload.wikimedia.org/wikipedia/en/c/fc/Wolverhampton_Wanderers.svg"
    ),
}
DEFAULT_LOGO = (
    "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png"
)
PL_LION_LOGO = "https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg"

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
    return (
        "<div class='placeholder'>⚠️ Please select two different teams to run a"
        " match prediction.</div>"
    )

  result = predict_match(home_team, away_team)

  outcomes = [
      (
          home_team,
          result["home_win"] * 100,
          TEAM_LOGOS.get(home_team, DEFAULT_LOGO),
          "Home Win",
      ),
      ("Draw", result["draw"] * 100, "", "Draw"),
      (
          away_team,
          result["away_win"] * 100,
          TEAM_LOGOS.get(away_team, DEFAULT_LOGO),
          "Away Win",
      ),
  ]

  best_outcome = max(outcomes, key=lambda x: x[1])
  best_label = best_outcome[0]

  cards_html = ""
  for label, pct, logo_url, subtitle in outcomes:
    is_best = "highlight-card" if label == best_label else ""
    badge_tag = (
        '<span class="favored-badge">FAVORED</span>'
        if label == best_label
        else ""
    )
    img_tag = (
        f'<img src="{logo_url}" width="38" style="margin-bottom:8px;'
        ' object-fit:contain;">'
        if logo_url
        else '<div style="height:38px;"></div>'
    )

    cards_html += (
        f'<div class="prob-card {is_best}">'
        f"{badge_tag}"
        f"{img_tag}"
        f'<div class="card-title">{label}</div>'
        f'<div class="card-subtitle">{subtitle}</div>'
        f'<div class="card-pct">{pct:.1f}%</div>'
        '<div class="mini-bar-track"><div class="mini-bar-fill'
        f' {is_best}" style="width:{pct:.1f}%;"></div></div>'
        "</div>"
    )

  return (
      '<div class="result-wrapper">'
      '<div class="prediction-header">Match Forecast:'
      f" <strong>{best_label} favored</strong></div>"
      f'<div class="cards-grid">{cards_html}</div>'
      "</div>"
  )


# --- DARK PURPLE BACKGROUND WITH WHITE DROPDOWNS & NEON GREEN BUTTON ---
css = """
<style>
/* Dark Premier League Purple Background */
.stApp {
    background-color: #38003c !important;
}

/* Title Header Container with Lion Logo */
.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 5px;
}

#title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF !important;
    margin: 0px;
}

#subtitle {
    text-align: center;
    font-size: 16px;
    color: #E8DBED !important;
    margin-bottom: 25px;
    opacity: 0.9;
}

/* Dropdown Labels (HOME TEAM / AWAY TEAM) in White */
div[data-testid="stSelectbox"] label p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}

/* Style the Select Box inputs to be White */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #38003c !important;
    border-radius: 10px !important;
    border: 1.5px solid #6B1D78 !important;
}

/* Ensure selected option text is dark purple */
div[data-baseweb="select"] * {
    color: #38003c !important;
    font-weight: 600 !important;
}

/* Matchup Header Card */
.vs-banner {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: #4A0B50;
    border: 2px solid #6B1D78;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.vs-team {
    text-align: center;
    font-weight: 700;
    color: #FFFFFF !important;
    font-size: 16px;
}

.vs-badge {
    background: #00ff85;
    color: #38003c;
    font-weight: 900;
    font-size: 18px;
    padding: 8px 16px;
    border-radius: 50%;
    box-shadow: 0 2px 8px rgba(0, 255, 133, 0.3);
}

/* Prediction Output Box */
.result-wrapper {
    margin-top: 20px;
    padding: 20px;
    background: #4A0B50;
    border-radius: 16px;
    border: 2px solid #6B1D78;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.prediction-header {
    text-align: center;
    font-size: 20px;
    color: #FFFFFF !important;
    margin-bottom: 20px;
}

.prediction-header strong {
    color: #38003c !important;
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
    background: #38003c;
    border: 1.5px solid #6B1D78;
    border-radius: 12px;
    padding: 15px 10px;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.prob-card:hover {
    transform: translateY(-3px);
}

.prob-card.highlight-card {
    border-color: #00ff85;
    background: #500C57;
    box-shadow: 0 4px 12px rgba(0, 255, 133, 0.2);
}

.favored-badge {
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    background: #00ff85;
    color: #38003c;
    font-size: 10px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 10px;
    letter-spacing: 0.5px;
}

.card-title {
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF !important;
    margin-top: 5px;
}

.card-subtitle {
    font-size: 12px;
    color: #E8DBED !important;
    margin-bottom: 8px;
}

.card-pct {
    font-size: 24px;
    font-weight: 800;
    color: #00ff85 !important;
    margin-bottom: 10px;
}

.mini-bar-track {
    width: 100%;
    height: 8px;
    background: #250028;
    border-radius: 4px;
    overflow: hidden;
}

.mini-bar-fill {
    height: 100%;
    background: #8A409A;
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
    color: #FFFFFF !important;
    border: 2px dashed #6B1D78;
    border-radius: 14px;
    background: #4A0B50;
}

/* Neon Green Action Button */
div.stButton > button:first-child {
    background-color: #00ff85 !important;
    color: #38003c !important;
    border: none !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    padding: 12px 0px !important;
}

div.stButton > button:first-child:hover {
    background-color: #00e676 !important;
    color: #250028 !important;
    box-shadow: 0 4px 15px rgba(0, 255, 133, 0.4);
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
header_html = f"""
<div class="header-container">
    <img src="{PL_LION_LOGO}" width="50" height="50" style="object-fit: contain;">
    <h1 id="title">Premier League Match Predictor</h1>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
st.markdown(
    '<p id="subtitle">Select teams to analyze win probabilities powered by'
    " Machine Learning</p>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
  home_team = st.selectbox(
      "HOME TEAM",
      options=teams,
      index=teams.index("Chelsea") if "Chelsea" in teams else 0,
  )

with col2:
  away_team = st.selectbox(
      "AWAY TEAM",
      options=teams,
      index=teams.index("Fulham") if "Fulham" in teams else 0,
  )

# Dynamic VS Matchup Header
vs_html = f"""
<div class="vs-banner">
    <div class="vs-team">
        <img src="{TEAM_LOGOS.get(home_team, DEFAULT_LOGO)}" width="45" height="45" style="object-fit: contain;"><br>
        {home_team}
    </div>
    <div class="vs-badge">VS</div>
    <div class="vs-team">
        <img src="{TEAM_LOGOS.get(away_team, DEFAULT_LOGO)}" width="45" height="45" style="object-fit: contain;"><br>
        {away_team}
    </div>
</div>
"""
st.html(vs_html)

predict_clicked = st.button(
    "RUN PREDICTION", type="primary", use_container_width=True
)

if predict_clicked:
  html_output = render_results(home_team, away_team)
  st.html(html_output)
else:
  st.html(
      "<div class='placeholder'>Select two teams above and click <strong>RUN"
      " PREDICTION</strong> to see probabilities.</div>"
  )