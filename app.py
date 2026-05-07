import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
import base64
import os
from dotenv import load_dotenv

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- CSS (MAIN MAGIC) ----------------
st.markdown("""
<style>

body {
    background-color: #013a63;
}

.stApp {
    background-color: #013a63;
}

.block-container {
    padding-top: 1rem !important;
}

/* HEADER */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:22px;
    font-weight:600;
    margin-bottom:10px;
}
.block-container {
    padding-top: 1rem !important;
}

/* INFO BAR */
.info-box {
    background:#e8f0ff;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}

/* CARD STYLE */
.card {
    background:white;
    padding:20px;
    border-radius:25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* SMALL CARD */
.small-card {
    background:white;
    padding:15px;
    border-radius:12px;
    text-align:center;
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
}

/* ALERT */
.alert {
    background:#fff4e5;
    padding:15px;
    border-radius:10px;
    color:#a85b00;
    font-weight:500;
}

</style>
""", unsafe_allow_html=True)

# ---------------- API ----------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

loc_icon = get_base64_image(r"Data\location.png")
search_icon = get_base64_image(r"Data\search.png")
gps_icon = get_base64_image(r"Data\gps.png")
wind_icon = get_base64_image(r"Data\wind.png")
sunrise_icon = get_base64_image(r"Data\sunrise.png")
sunset_icon = get_base64_image(r"Data\sunset.png")

def get_condition_image_base64(icon_code):
    mapping = {
        '01d': 'sunny.png',
        '01n': 'clear night.png',
        '02d': 'partly-cloudy.png',
        '02n': 'partly-cloudy.png',
        '03d': 'cloudy.png',
        '03n': 'cloudy.png',
        '04d': 'cloudy.png',
        '04n': 'cloudy.png',
        '09d': 'light-rain.png',
        '09n': 'light-rain.png',
        '10d': 'light-rain.png',
        '10n': 'light-rain.png',
        '11d': 'thunderstorm.png',
        '11n': 'thunderstorm.png',
        '13d': 'snowflake.png',
        '13n': 'snowflake.png',
        '50d': 'fog.png',
        '50n': 'fog.png'
    }
    filename = mapping.get(icon_code, 'sunny.png')
    try:
        return get_base64_image(rf"Data\condition\{filename}")
    except:
        return ""

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

# ---------------- STATE ----------------
if "city" not in st.session_state:
    st.session_state.city = "Bhubaneswar"

if "search" not in st.session_state:
    st.session_state.search = False

# ---------------- HEADER & CARD CSS FIXES ----------------
st.markdown("""
<style>

/* HEADER CARD */
div[data-testid="stHorizontalBlock"]:has(.header-marker) {
    background:white;
    padding:12px 20px;  /* reduce side padding */
    border-radius:25px;
    box-shadow:10px 14px 6px rgba(0,0,0,0.09);
    margin-top:30px;
    margin-bottom:10px;
}

/* REMOVE COLUMN PADDING (important) */
div[data-testid="column"] {
    padding: 0 !important;
}

/* LEFT TEXT */
div[data-testid="stHorizontalBlock"]:has(.header-marker) 
div[data-testid="column"]:nth-child(1) {
    display:flex;
    align-items:center;
}

/* RIGHT BUTTON COLUMN */
div[data-testid="stHorizontalBlock"]:has(.header-marker) 
div[data-testid="column"]:nth-child(2) {
    display:flex;
    justify-content:flex-end;
    align-items:center;
}

/* FORCE BUTTON TO EXTREME RIGHT */
div.stButton {
    width:100%;
    display:flex;
    justify-content:flex-end;
}

div.stButton > button {
    margin-right:0;
}

/* MAIN CARDS CSS FIX */
div[data-testid="column"]:has(.card-marker) {
    background: white;
    padding: 20px !important;
    border-radius: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# HEADER BLOCK

col1, col2 = st.columns([40,1])

with col1:
    st.markdown(f"""
    <div class="header-marker" style="
        display:flex;
        align-items:center;
        gap:8px;
        font-size:20px;
        font-weight:500;
        padding-bottom:15px
    ">
        <img src="data:image/jpeg;base64,{loc_icon}" width="18">
        {st.session_state.city.title()}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <style>
    /* Anchor to the entire header card so we can perfectly right-align */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) {{
        position: relative !important;
    }}
    /* Remove paddings from the button wrapper */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) div.stButton {{
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* Position the button relative to the header card itself */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        width: 20px !important;
        height: 20px !important;
        min-width: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        position: absolute !important;
        transform: translateY(-50%) !important;
        margin: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button:hover {{
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button:focus {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button:active {{
        background: transparent !important;
        border: none !important;
    }}
    /* Render image OVER the transparent button */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button::after {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/png;base64,{search_icon}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        pointer-events: none;
    }}
    /* Hide button text */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button p {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    if st.button("\u200B", key="search_btn"):
        st.session_state.search = not st.session_state.search

# ---------------- SEARCH ----------------
def submit_search():
    new_city = st.session_state.search_input.strip()
    if new_city:
        st.session_state.city = new_city
        st.session_state.search = False

if st.session_state.search:
    st.text_input("Search city and press Enter", key="search_input", on_change=submit_search)


city = st.session_state.city

# ---------------- FETCH ----------------
data = get_weather(city)
forecast = get_forecast(city)

if str(data.get("cod")) != "200":
    st.error("Error fetching weather")
else:

    # ---------------- MAIN CARDS ----------------
    col1, col2, col3 = st.columns([1.8, 1.4, 1.2], gap="large")

    # WEATHER CARD
    with col1:
        icon = data['weather'][0]['icon']
        icon_b64 = get_condition_image_base64(icon)
        desc = data['weather'][0]['description'].title()
        temp = int(data['main']['temp'])
        pressure = data['main']['pressure']
        visibility = data['visibility'] // 1000
        humidity = data['main']['humidity']
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 260px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div style="font-weight: 600; font-size: 18px; margin-bottom: 5px; color: #111; display: flex; align-items: center; gap: 6px;">
                        <img src="data:image/png;base64,{gps_icon}" width="24"> {city}
                    </div>
                    <div style="font-size: 48px; font-weight: bold; line-height: 1.2; color: #111;">{temp}°<span style="font-size: 24px;">C</span></div>
                    <div style="font-size: 16px; margin-top: 5px; color: #555;">{desc}</div>
                </div>
                <div>
                    <img src="data:image/png;base64,{icon_b64}" width="120" style="margin-top: -10px;">
                </div>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 25px;">
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 5px; text-align: center;">
                    <div style="font-size: 14px; color: #666;">Pressure</div>
                    <div style="font-size: 22px; color: #0d6efd; font-weight: 800;">{pressure} mb</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 5px; text-align: center;">
                    <div style="font-size: 14px; color: #666;">Visibility</div>
                    <div style="font-size: 22px; color: #0d6efd; font-weight: 800;">{visibility} km</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 5px; text-align: center;">
                    <div style="font-size: 14px; color: #666;">Humidity</div>
                    <div style="font-size: 22px; color: #0d6efd; font-weight: 800;">{humidity}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # WIND CARD
    with col2:
        speed = data['wind']['speed']
        pct = min(int(speed * 10), 100)
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 260px; display: flex; flex-direction: column;">
            <div style="font-weight: 600; font-size: 18px; margin-bottom: 20px; color: #111; display: flex; align-items: center; gap: 8px;"><img src="data:image/png;base64,{wind_icon}" width="24"> Wind Info</div>
            <div style="font-size: 42px; font-weight: bold; color: #0d6efd; line-height: 1;">{speed} <span style="font-size: 24px; font-weight: 500;">m/s</span></div>
            <div style="font-size: 16px; margin-top: auto; margin-bottom: 8px; color: #555;">Wind Speed</div>
            <div style="width: 100%; background-color: #e9ecef; border-radius: 4px; height: 10px; margin-bottom: 10px;">
                <div style="width: {pct}%; background-color: #0d6efd; height: 10px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 20px; font-weight: 600; color: #111;">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)

    # SUN CARD
    with col3:
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 260px; display: flex; flex-direction: column; justify-content: center;">
            <div>
                <div style="font-size: 18px; margin-bottom: 8px; font-weight: 500; color: #111; display: flex; align-items: center; gap: 8px;"><img src="data:image/png;base64,{sunrise_icon}" width="24"> Sunrise:</div>
                <div style="font-size: 28px; font-weight: bold; padding-left: 32px; color: #111;">{sunrise}</div>
            </div>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
            <div>
                <div style="font-size: 18px; margin-bottom: 8px; font-weight: 500; color: #111; display: flex; align-items: center; gap: 8px;"><img src="data:image/png;base64,{sunset_icon}" width="24"> Sunset:</div>
                <div style="font-size: 28px; font-weight: bold; padding-left: 32px; color: #111;">{sunset}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)