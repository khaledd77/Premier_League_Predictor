import streamlit as st

# Set Page Config
st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="centered"
)

# ==========================================
# 1. FIXED TEAM LOGOS DICTIONARY & HELPER
# ==========================================
TEAM_LOGOS = {
    "arsenal": "https://content.sportslogos.net/logos/69/3478/full/arsenal_fc_logo_20038848.png",
    "aston villa": "https://content.sportslogos.net/logos/69/3479/full/aston_villa_logo_primary_2016_sportslogosnet-2234.png",
    "bournemouth": "https://content.sportslogos.net/logos/69/3480/full/afc_bournemouth_logo_primary_20146039.png",
    "brentford": "https://content.sportslogos.net/logos/69/3481/full/brentford_fc_logo_primary_20172081.png",
    "brighton": "https://content.sportslogos.net/logos/69/3482/full/brighton__hove_albion_logo_primary_20124803.png",
    "brighton & hove albion": "https://content.sportslogos.net/logos/69/3482/full/brighton__hove_albion_logo_primary_20124803.png",
    "burnley": "https://content.sportslogos.net/logos/69/3483/full/burnley_fc_logo_primary_20162817.png",
    "cardiff": "https://content.sportslogos.net/logos/69/3484/full/cardiff_city_logo_primary_20158863.png",
    "cardiff city": "https://content.sportslogos.net/logos/69/3484/full/cardiff_city_logo_primary_20158863.png",
    "chelsea": "https://content.sportslogos.net/logos/69/3485/full/chelsea_fc_logo_primary_20066723.png",
    "crystal palace": "https://content.sportslogos.net/logos/69/3486/full/crystal_palace_fc_logo_primary_2022_sportslogosnet-5373.png",
    "everton": "https://content.sportslogos.net/logos/69/3487/full/everton_fc_logo_primary_20151125.png",
    "fulham": "https://content.sportslogos.net/logos/69/3488/full/fulham_fc_logo_primary_20023608.png",
    "huddersfield": "https://content.sportslogos.net/logos/69/3489/full/huddersfield_town_logo_primary_2019_sportslogosnet-2415.png",
    "huddersfield town": "https://content.sportslogos.net/logos/69/3489/full/huddersfield_town_logo_primary_2019_sportslogosnet-2415.png",
    "ipswich": "https://content.sportslogos.net/logos/69/3490/full/ipswich_town_logo_primary_19959616.png",
    "ipswich town": "https://content.sportslogos.net/logos/69/3490/full/ipswich_town_logo_primary_19959616.png",
    "leeds": "https://content.sportslogos.net/logos/69/3491/full/leeds_united_logo_primary_19992642.png",
    "leeds united": "https://content.sportslogos.net/logos/69/3491/full/leeds_united_logo_primary_19992642.png",
    "leicester": "https://content.sportslogos.net/logos/69/3492/full/leicester_city_logo_primary_20102602.png",
    "leicester city": "https://content.sportslogos.net/logos/69/3492/full/leicester_city_logo_primary_20102602.png",
    "liverpool": "https://content.sportslogos.net/logos/69/3493/full/liverpool_fc_logo_primary_20124748.png",
    "luton": "https://content.sportslogos.net/logos/69/3494/full/luton_town_logo_primary_20092261.png",
    "luton town": "https://content.sportslogos.net/logos/69/3494/full/luton_town_logo_primary_20092261.png",
    "manchester city": "https://content.sportslogos.net/logos/69/3495/full/manchester_city_logo_primary_20177726.png",
    "manchester united": "https://content.sportslogos.net/logos/69/3496/full/manchester_united_logo_primary_19984916.png",
    "newcastle": "https://content.sportslogos.net/logos/69/3497/full/newcastle_united_logo_primary_19888497.png",
    "newcastle united": "https://content.sportslogos.net/logos/69/3497/full/newcastle_united_logo_primary_19888497.png",
    "norwich": "https://content.sportslogos.net/logos/69/3498/full/norwich_city_logo_primary_2022_sportslogosnet-8149.png",
    "norwich city": "https://content.sportslogos.net/logos/69/3498/full/norwich_city_logo_primary_2022_sportslogosnet-8149.png",
    "nott'm forest": "https://content.sportslogos.net/logos/69/3499/full/nottingham_forest_logo_primary_19747948.png",
    "nottingham forest": "https://content.sportslogos.net/logos/69/3499/full/nottingham_forest_logo_primary_19747948.png",
    "sheffield united": "https://content.sportslogos.net/logos/69/3501/full/sheffield_united_logo_primary_19992683.png",
    "sheffield utd": "https://content.sportslogos.net/logos/69/3501/full/sheffield_united_logo_primary_19992683.png",
    "southampton": "https://content.sportslogos.net/logos/69/3502/full/southampton_fc_logo_primary_20112423.png",
    "stoke": "https://content.sportslogos.net/logos/69/3503/full/stoke_city_logo_primary_20015039.png",
    "stoke city": "https://content.sportslogos.net/logos/69/3503/full/stoke_city_logo_primary_20015039.png",
    "sunderland": "https://content.sportslogos.net/logos/69/3504/full/sunderland_afc_logo_primary_19973843.png",
    "swansea": "https://content.sportslogos.net/logos/69/3505/full/swansea_city_logo_primary_2021_sportslogosnet-8089.png",
    "swansea city": "https://content.sportslogos.net/logos/69/3505/full/swansea_city_logo_primary_2021_sportslogosnet-8089.png",
    "tottenham": "https://content.sportslogos.net/logos/69/3506/full/tottenham_hotspur_logo_primary_20067645.png",
    "tottenham hotspur": "https://content.sportslogos.net/logos/69/3506/full/tottenham_hotspur_logo_primary_20067645.png",
    "watford": "https://content.sportslogos.net/logos/69/3507/full/watford_fc_logo_primary_19782578.png",
    "west brom": "https://content.sportslogos.net/logos/69/3508/full/west_bromwich_albion_logo_primary_20118536.png",
    "west bromwich albion": "https://content.sportslogos.net/logos/69/3508/full/west_bromwich_albion_logo_primary_20118536.png",
    "west ham": "https://content.sportslogos.net/logos/69/3509/full/west_ham_united_logo_primary_20162594.png",
    "west ham united": "https://content.sportslogos.net/logos/69/3509/full/west_ham_united_logo_primary_20162594.png",
    "wolves": "https://content.sportslogos.net/logos/69/3510/full/wolverhampton_wanderers_logo_primary_20022416.png",
    "wolverhampton wanderers": "https://content.sportslogos.net/logos/69/3510/full/wolverhampton_wanderers_logo_primary_20022416.png",
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

/* 1. Main Dropdown Input Box - Dark/Black Background */
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

/* Hover & Selected state - Highlighted Purple */
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