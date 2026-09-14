import os
import pickle
import urllib.parse
from collections import defaultdict, deque

import pandas as pd
import requests
import streamlit as st

# Set Page Config
st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="centered",
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


# ==========================================
# 2. TEAM LOGOS DICTIONARY & HELPERS
# ==========================================
TEAM_LOGOS = {
    "arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "aston villa": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg",
    "bournemouth": "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg",
    "brentford": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
    "brighton": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
    "brighton & hove albion": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
    "burnley": "https://upload.wikimedia.org/wikipedia/en/6/62/Burnley_F.C._logo.svg",
    "cardiff": "https://upload.wikimedia.org/wikipedia/en/3/3c/Cardiff_City_crest.svg",
    "cardiff city": "https://upload.wikimedia.org/wikipedia/en/3/3c/Cardiff_City_crest.svg",
    "chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "crystal palace": "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg",
    "everton": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
    "fulham": "https://upload.wikimedia.org/wikipedia/en/7/70/Fulham_FC_%28shield%29.svg",
    "huddersfield": "https://upload.wikimedia.org/wikipedia/en/7/7d/Huddersfield_Town_A.F.C._logo.svg",
    "huddersfield town": "https://upload.wikimedia.org/wikipedia/en/7/7d/Huddersfield_Town_A.F.C._logo.svg",
    "ipswich": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town_FC_logo.svg",
    "ipswich town": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town_FC_logo.svg",
    "leeds": "https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg",
    "leeds united": "https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg",
    "leicester": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
    "leicester city": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
    # "liverpool" intentionally omitted for now — the previously used file showed an
    # outdated crest and the correct current-season URL hasn't been confirmed yet.
    # Falls back to the colored initials badge below until this is filled in.
    "luton": "https://upload.wikimedia.org/wikipedia/en/9/9d/LutonTownFC2009.svg",
    "luton town": "https://upload.wikimedia.org/wikipedia/en/9/9d/LutonTownFC2009.svg",
    "manchester city": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "manchester united": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "newcastle": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "newcastle united": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "norwich": "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City_FC_logo.svg",
    "norwich city": "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City_FC_logo.svg",
    "nott'm forest": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg",
    "nottingham forest": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg",
    "sheffield united": "https://upload.wikimedia.org/wikipedia/en/9/9c/Sheffield_United_FC_logo.svg",
    "sheffield utd": "https://upload.wikimedia.org/wikipedia/en/9/9c/Sheffield_United_FC_logo.svg",
    "southampton": "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg",
    "stoke": "https://upload.wikimedia.org/wikipedia/en/2/29/Stoke_City_FC.svg",
    "stoke city": "https://upload.wikimedia.org/wikipedia/en/2/29/Stoke_City_FC.svg",
    "sunderland": "https://upload.wikimedia.org/wikipedia/en/7/77/Logo_Sunderland.svg",
    "swansea": "https://upload.wikimedia.org/wikipedia/en/f/f9/Swansea_City_AFC_logo.svg",
    "swansea city": "https://upload.wikimedia.org/wikipedia/en/f/f9/Swansea_City_AFC_logo.svg",
    "tottenham": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "tottenham hotspur": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "watford": "https://upload.wikimedia.org/wikipedia/en/e/e2/Watford.svg",
    "west brom": "https://upload.wikimedia.org/wikipedia/en/8/8b/West_Bromwich_Albion.svg",
    "west bromwich albion": "https://upload.wikimedia.org/wikipedia/en/8/8b/West_Bromwich_Albion.svg",
    "west ham": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "west ham united": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "wolves": "https://upload.wikimedia.org/wikipedia/en/c/fc/Wolverhampton_Wanderers.svg",
    "wolverhampton wanderers": "https://upload.wikimedia.org/wikipedia/en/c/fc/Wolverhampton_Wanderers.svg",
}

TEAM_COLORS = {
    "arsenal": "#EF0107",
    "aston villa": "#670E36",
    "bournemouth": "#DA291C",
    "brentford": "#E30613",
    "brighton & hove albion": "#0057B8",
    "burnley": "#6C1D45",
    "cardiff city": "#0070B5",
    "chelsea": "#034694",
    "crystal palace": "#1B458F",
    "everton": "#003399",
    "fulham": "#CC0000",
    "huddersfield town": "#0E63AD",
    "ipswich town": "#0044A9",
    "leeds united": "#1D428A",
    "leicester city": "#003090",
    "liverpool": "#C8102E",
    "luton town": "#F78F1E",
    "manchester city": "#6CABDD",
    "manchester united": "#DA291C",
    "newcastle united": "#241F20",
    "norwich city": "#FFF200",
    "nottingham forest": "#DD0000",
    "sheffield united": "#EE2737",
    "southampton": "#D71920",
    "stoke city": "#E03A3E",
    "sunderland": "#EB172F",
    "swansea city": "#121212",
    "tottenham hotspur": "#132257",
    "watford": "#FBEE23",
    "west bromwich albion": "#122F67",
    "west ham united": "#7A263A",
    "wolverhampton wanderers": "#FDB913",
}


def get_team_logo(team_name: str) -> str:
    """Safely retrieves team logo URL regardless of spacing or capitalization.
    Returns None if no URL is on file for this team (triggers the badge fallback)."""
    clean_name = str(team_name).strip().lower()
    return TEAM_LOGOS.get(clean_name)


def get_fallback_badge_uri(team_name: str) -> str:
    """Builds a self-contained SVG badge (no network needed) used whenever the real
    logo is missing or fails a reachability check."""
    color = TEAM_COLORS.get(team_name.strip().lower(), "#666666")
    initials = "".join(w[0] for w in team_name.split()[:3]).upper()
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
        f"<circle cx='50' cy='50' r='48' fill='{color}'/>"
        f"<text x='50' y='63' font-size='34' font-weight='800' fill='white' "
        f"text-anchor='middle' font-family='Arial, sans-serif'>{initials}</text>"
        f"</svg>"
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg)


@st.cache_data(ttl=86400, show_spinner=False)
def url_is_reachable(url: str) -> bool:
    """Checks a URL server-side, in Python — this is what actually decides which
    image to show. Nothing here depends on browser JavaScript, so there is no inline
    onerror handler for Streamlit's HTML sanitizer to strip out."""
    try:
        resp = requests.head(url, timeout=4, allow_redirects=True)
        if resp.status_code >= 400:
            # Some servers (including some Wikimedia paths) don't support HEAD properly
            resp = requests.get(url, timeout=4, stream=True)
        return resp.status_code < 400
    except requests.RequestException:
        return False


def render_team_image(team_name: str, size: int = 60) -> str:
    """Returns a single <img> tag pointing at whichever source is actually valid,
    decided in Python before any HTML is generated."""
    logo_url = get_team_logo(team_name)

    if logo_url and url_is_reachable(logo_url):
        src = logo_url
    else:
        src = get_fallback_badge_uri(team_name)

    return f'<img src="{src}" width="{size}" height="{size}" style="object-fit: contain;" />'


# ==========================================
# 3. CUSTOM CSS STYLING
# ==========================================
css = """
<style>
.stApp {
    background-color: #38003c !important;
}

#title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 0px;
}

#subtitle {
    text-align: center;
    font-size: 16px;
    color: #E8DBED !important;
    margin-bottom: 25px;
    opacity: 0.9;
}

div[data-testid="stSelectbox"] label p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}

div[data-baseweb="select"] > div:first-child {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1.5px solid #6B1D78 !important;
}

div[data-baseweb="select"] * {
    color: #38003c !important;
    font-weight: 600 !important;
    fill: #38003c !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

li[role="option"],
div[role="option"] {
    background-color: #ffffff !important;
    color: #38003c !important;
}

li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #f4e8f7 !important;
    color: #38003c !important;
}

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

# ==========================================
# 4. APP UI & LOGIC
# ==========================================
st.markdown(
    '<div id="title">Premier League Match Predictor</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div id="subtitle">Select teams to analyze win probabilities powered by'
    " Machine Learning</div>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox(
        "HOME TEAM", teams_list,
        index=teams_list.index("Chelsea") if "Chelsea" in teams_list else 0,
    )
with col2:
    away_team = st.selectbox(
        "AWAY TEAM", teams_list,
        index=teams_list.index("Fulham") if "Fulham" in teams_list else 1,
    )

st.markdown(
    f"""
    <div class="vs-banner">
        <div style="text-align: center;">
            {render_team_image(home_team, 60)}
            <div class="vs-team">{home_team}</div>
        </div>
        <div class="vs-badge">VS</div>
        <div style="text-align: center;">
            {render_team_image(away_team, 60)}
            <div class="vs-team">{away_team}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("RUN PREDICTION", use_container_width=True):

    if home_team == away_team:
        st.markdown(
            '<div class="placeholder">Please select two different teams.</div>',
            unsafe_allow_html=True,
        )
    else:
        result = predict_match(home_team, away_team)

        prob_home = result["home_win"] * 100
        prob_draw = result["draw"] * 100
        prob_away = result["away_win"] * 100

        favored = home_team if prob_home > prob_away else away_team

        home_highlight = "highlight-card" if favored == home_team else ""
        home_badge = (
            '<div class="favored-badge">FAVORED</div>'
            if favored == home_team
            else ""
        )

        away_highlight = "highlight-card" if favored == away_team else ""
        away_badge = (
            '<div class="favored-badge">FAVORED</div>'
            if favored == away_team
            else ""
        )

        home_bar_class = f"mini-bar-fill {home_highlight}"
        away_bar_class = f"mini-bar-fill {away_highlight}"

        st.markdown(
            f"""
            <div class="result-wrapper">
                <div class="prediction-header">Match Forecast: <strong>{favored} favored</strong></div>
                <div class="cards-grid">
                    <div class="prob-card {home_highlight}">{home_badge}
                        {render_team_image(home_team, 36)}
                        <div class="card-title">{home_team}</div>
                        <div class="card-subtitle">Home Win</div>
                        <div class="card-pct">{prob_home:.1f}%</div>
                        <div class="mini-bar-track">
                            <div class="{home_bar_class}" style="width: {prob_home:.1f}%;"></div>
                        </div>
                    </div>
                    <div class="prob-card">
                        <div class="card-title">Draw</div>
                        <div class="card-subtitle">Equal Points</div>
                        <div class="card-pct">{prob_draw:.1f}%</div>
                        <div class="mini-bar-track">
                            <div class="mini-bar-fill" style="width: {prob_draw:.1f}%;"></div>
                        </div>
                    </div>
                    <div class="prob-card {away_highlight}">{away_badge}
                        {render_team_image(away_team, 36)}
                        <div class="card-title">{away_team}</div>
                        <div class="card-subtitle">Away Win</div>
                        <div class="card-pct">{prob_away:.1f}%</div>
                        <div class="mini-bar-track">
                            <div class="{away_bar_class}" style="width: {prob_away:.1f}%;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <div class="placeholder">
            Select two teams above and click <strong>RUN PREDICTION</strong> to see probabilities.
        </div>
        """,
        unsafe_allow_html=True,
    )