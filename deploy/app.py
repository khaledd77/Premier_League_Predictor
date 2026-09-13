import streamlit as st

# Set Page Config
st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="centered"
)

# ==========================================
# 1. TEAM LOGOS DICTIONARY & HELPER
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
    "liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
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

def get_team_logo(team_name: str) -> str:
    """Safely retrieves team logo URL regardless of spacing or capitalization."""
    clean_name = str(team_name).strip().lower()
    fallback_logo = "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png"
    return TEAM_LOGOS.get(clean_name, fallback_logo)

# ==========================================
# 2. CUSTOM CSS STYLING
# ==========================================
css = """
<style>
/* Dark Premier League Purple Background */
.stApp {
    background-color: #38003c !important;
}

/* White Header Styling */
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

/* Dropdown Labels (HOME TEAM / AWAY TEAM) in White */
div[data-testid="stSelectbox"] label p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}

/* 1. Main Dropdown Input Box (Closed State) */
div[data-baseweb="select"] > div:first-child {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1.5px solid #6B1D78 !important;
}

/* Force all text, icons, and values inside the input box to Dark Purple */
div[data-baseweb="select"] * {
    color: #38003c !important;
    font-weight: 600 !important;
    fill: #38003c !important;
}

/* 2. Pop-up Dropdown Options List Container (Open State) */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Individual items inside the dropdown list */
li[role="option"],
div[role="option"] {
    background-color: #ffffff !important;
    color: #38003c !important;
}

/* Hover & Active state for items in the list */
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #f4e8f7 !important;
    color: #38003c !important;
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

# ==========================================
# 3. APP UI & LOGIC
# ==========================================
st.markdown('<div id="title">Premier League Match Predictor</div>', unsafe_allow_html=True)
st.markdown('<div id="subtitle">Select teams to analyze win probabilities powered by Machine Learning</div>', unsafe_allow_html=True)

# List of teams sorted alphabetically
teams_list = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", 
    "Burnley", "Cardiff City", "Chelsea", "Crystal Palace", "Everton", "Fulham", 
    "Huddersfield Town", "Ipswich Town", "Leeds United", "Leicester City", "Liverpool", 
    "Luton Town", "Manchester City", "Manchester United", "Newcastle United", "Norwich City", 
    "Nottingham Forest", "Sheffield United", "Southampton", "Stoke City", "Sunderland", 
    "Swansea City", "Tottenham Hotspur", "Watford", "West Bromwich Albion", "West Ham United", 
    "Wolverhampton Wanderers"
]

col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("HOME TEAM", teams_list, index=0)
with col2:
    away_team = st.selectbox("AWAY TEAM", teams_list, index=1)

# Display Team Logos Banner
home_logo = get_team_logo(home_team)
away_logo = get_team_logo(away_team)

st.markdown(
    f"""
    <div class="vs-banner">
        <div style="text-align: center;">
            <img src="{home_logo}" width="60" height="60" style="object-fit: contain;" />
            <div class="vs-team">{home_team}</div>
        </div>
        <div class="vs-badge">VS</div>
        <div style="text-align: center;">
            <img src="{away_logo}" width="60" height="60" style="object-fit: contain;" />
            <div class="vs-team">{away_team}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Run Prediction Button & Results Container
if st.button("RUN PREDICTION", use_container_width=True):
    # Place your actual model inference logic here
    # Example placeholder values for output verification:
    prob_home = 48.5
    prob_draw = 26.2
    prob_away = 25.3
    
    favored = home_team if prob_home > prob_away else away_team
    
    st.markdown(
        f"""
        <div class="result-wrapper">
            <div class="prediction-header">Match Forecast: <strong>{favored} favored</strong></div>
            <div class="cards-grid">
                <div class="prob-card {'highlight-card' if favored == home_team else ''}">
                    {'<div class="favored-badge">FAVORED</div>' if favored == home_team else ''}
                    <img src="{home_logo}" width="36" height="36" style="object-fit: contain;" />
                    <div class="card-title">{home_team}</div>
                    <div class="card-subtitle">Home Win</div>
                    <div class="card-pct">{prob_home}%</div>
                    <div class="mini-bar-track">
                        <div class="mini-bar-fill {'highlight-card' if favored == home_team else ''}" style="width: {prob_home}%;"></div>
                    </div>
                </div>
                <div class="prob-card">
                    <div class="card-title">Draw</div>
                    <div class="card-subtitle">Equal Points</div>
                    <div class="card-pct">{prob_draw}%</div>
                    <div class="mini-bar-track">
                        <div class="mini-bar-fill" style="width: {prob_draw}%;"></div>
                    </div>
                </div>
                <div class="prob-card {'highlight-card' if favored == away_team else ''}">
                    {'<div class="favored-badge">FAVORED</div>' if favored == away_team else ''}
                    <img src="{away_logo}" width="36" height="36" style="object-fit: contain;" />
                    <div class="card-title">{away_team}</div>
                    <div class="card-subtitle">Away Win</div>
                    <div class="card-pct">{prob_away}%</div>
                    <div class="mini-bar-track">
                        <div class="mini-bar-fill {'highlight-card' if favored == away_team else ''}" style="width: {prob_away}%;"></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="placeholder">
            Select two teams above and click <strong>RUN PREDICTION</strong> to see probabilities.
        </div>
        """,
        unsafe_allow_html=True
    )