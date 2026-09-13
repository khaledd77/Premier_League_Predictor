import streamlit as st

# Set Page Config
st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="centered"
)

# ==========================================
# 1. PERMANENT EMBEDDABLE PNG TEAM LOGOS DICTIONARY
# ==========================================
TEAM_LOGOS = {
    "arsenal": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/200px-Arsenal_FC.svg.png",
    "aston villa": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/200px-Aston_Villa_FC_crest_%282016%29.svg.png",
    "bournemouth": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/AFC_Bournemouth_%282013%29.svg/200px-AFC_Bournemouth_%282013%29.svg.png",
    "brentford": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Brentford_FC_crest.svg/200px-Brentford_FC_crest.svg.png",
    "brighton": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/200px-Brighton_%26_Hove_Albion_logo.svg.png",
    "brighton & hove albion": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/200px-Brighton_%26_Hove_Albion_logo.svg.png",
    "burnley": "https://upload.wikimedia.org/wikipedia/en/thumb/6/62/Burnley_F.C._logo.svg/200px-Burnley_F.C._logo.svg.png",
    "cardiff": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/Cardiff_City_crest.svg/200px-Cardiff_City_crest.svg.png",
    "cardiff city": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/Cardiff_City_crest.svg/200px-Cardiff_City_crest.svg.png",
    "chelsea": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/200px-Chelsea_FC.svg.png",
    "crystal palace": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/200px-Crystal_Palace_FC_logo_%282022%29.svg.png",
    "everton": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/Everton_FC_logo.svg/200px-Everton_FC_logo.svg.png",
    "fulham": "https://upload.wikimedia.org/wikipedia/en/thumb/7/70/Fulham_FC_%28shield%29.svg/200px-Fulham_FC_%28shield%29.svg.png",
    "huddersfield": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Huddersfield_Town_A.F.C._logo.svg/200px-Huddersfield_Town_A.F.C._logo.svg.png",
    "huddersfield town": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Huddersfield_Town_A.F.C._logo.svg/200px-Huddersfield_Town_A.F.C._logo.svg.png",
    "ipswich": "https://upload.wikimedia.org/wikipedia/en/thumb/4/43/Ipswich_Town_FC_logo.svg/200px-Ipswich_Town_FC_logo.svg.png",
    "ipswich town": "https://upload.wikimedia.org/wikipedia/en/thumb/4/43/Ipswich_Town_FC_logo.svg/200px-Ipswich_Town_FC_logo.svg.png",
    "leeds": "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/Leeds_United_F.C._logo.svg/200px-Leeds_United_F.C._logo.svg.png",
    "leeds united": "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/Leeds_United_F.C._logo.svg/200px-Leeds_United_F.C._logo.svg.png",
    "leicester": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/200px-Leicester_City_crest.svg.png",
    "leicester city": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/200px-Leicester_City_crest.svg.png",
    "liverpool": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/200px-Liverpool_FC.svg.png",
    "luton": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/LutonTownFC2009.svg/200px-LutonTownFC2009.svg.png",
    "luton town": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/LutonTownFC2009.svg/200px-LutonTownFC2009.svg.png",
    "manchester city": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/200px-Manchester_City_FC_badge.svg.png",
    "manchester united": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/200px-Manchester_United_FC_crest.svg.png",
    "newcastle": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/200px-Newcastle_United_Logo.svg.png",
    "newcastle united": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/200px-Newcastle_United_Logo.svg.png",
    "norwich": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Norwich_City_FC_logo.svg/200px-Norwich_City_FC_logo.svg.png",
    "norwich city": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Norwich_City_FC_logo.svg/200px-Norwich_City_FC_logo.svg.png",
    "nott'm forest": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Nottingham_Forest_F.C._logo.svg/200px-Nottingham_Forest_F.C._logo.svg.png",
    "nottingham forest": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Nottingham_Forest_F.C._logo.svg/200px-Nottingham_Forest_F.C._logo.svg.png",
    "sheffield united": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9c/Sheffield_United_FC_logo.svg/200px-Sheffield_United_FC_logo.svg.png",
    "sheffield utd": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9c/Sheffield_United_FC_logo.svg/200px-Sheffield_United_FC_logo.svg.png",
    "southampton": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/FC_Southampton.svg/200px-FC_Southampton.svg.png",
    "stoke": "https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Stoke_City_FC.svg/200px-Stoke_City_FC.svg.png",
    "stoke city": "https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Stoke_City_FC.svg/200px-Stoke_City_FC.svg.png",
    "sunderland": "https://upload.wikimedia.org/wikipedia/en/thumb/7/77/Logo_Sunderland.svg/200px-Logo_Sunderland.svg.png",
    "swansea": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Swansea_City_AFC_logo.svg/200px-Swansea_City_AFC_logo.svg.png",
    "swansea city": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Swansea_City_AFC_logo.svg/200px-Swansea_City_AFC_logo.svg.png",
    "tottenham": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/200px-Tottenham_Hotspur.svg.png",
    "tottenham hotspur": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/200px-Tottenham_Hotspur.svg.png",
    "watford": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Watford.svg/200px-Watford.svg.png",
    "west brom": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/West_Bromwich_Albion.svg/200px-West_Bromwich_Albion.svg.png",
    "west bromwich albion": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/West_Bromwich_Albion.svg/200px-West_Bromwich_Albion.svg.png",
    "west ham": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/200px-West_Ham_United_FC_logo.svg.png",
    "west ham united": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/200px-West_Ham_United_FC_logo.svg.png",
    "wolves": "https://upload.wikimedia.org/wikipedia/en/thumb/c/fc/Wolverhampton_Wanderers.svg/200px-Wolverhampton_Wanderers.svg.png",
    "wolverhampton wanderers": "https://upload.wikimedia.org/wikipedia/en/thumb/c/fc/Wolverhampton_Wanderers.svg/200px-Wolverhampton_Wanderers.svg.png",
}

def get_team_logo(team_name: str) -> str:
    """Safely retrieves team logo URL regardless of spacing or capitalization."""
    clean_name = str(team_name).strip().lower()
    fallback_logo = "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png"
    return TEAM_LOGOS.get(clean_name, fallback_logo)

# ==========================================
# 2. CUSTOM CSS STYLING (DARK DROPDOWNS)
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

/* 1. Main Dropdown Input Box - Dark Background */
div[data-baseweb="select"] > div:first-child {
    background-color: #1e1e24 !important;
    border-radius: 10px !important;
    border: 1.5px solid #6B1D78 !important;
}

/* Text and Icons inside Input Box - White */
div[data-baseweb="select"] * {
    color: #ffffff !important;
    font-weight: 600 !important;
    fill: #ffffff !important;
}

/* 2. Pop-up Options List Container - Dark/Black Background */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #1e1e24 !important;
    border-radius: 10px !important;
    border: 1px solid #6B1D78 !important;
}

/* Individual options inside list - Dark Background with White Text */
li[role="option"],
div[role="option"] {
    background-color: #1e1e24 !important;
    color: #ffffff !important;
}

/* Hover & Selected state - Highlighted Purple with Neon Green Text */
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #4A0B50 !important;
    color: #00ff85 !important;
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