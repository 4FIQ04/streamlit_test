import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

# ========== Streamlit UI Setup ==========
st.set_page_config(page_title="Weather Forecast Dashboard", layout="centered")

st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #1565c0;
        padding-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: #424242;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌤️ Weather Forecast Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Check the latest weather trends by city</div>', unsafe_allow_html=True)

# ========== User Inputs ==========
user_name = st.text_input("Your Name:", "Guest")
st.markdown(f"👋 Hello, **{user_name}**! Let's check the weather.")

city = st.text_input("Enter a city name:", "Kuala Lumpur")
api_key = st.text_input("Enter your WeatherAPI Key:", type="password")

# ========== WeatherAPI Data Fetch Function ==========
@st.cache_data
def get_weatherapi_data(city_name, key):
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={city_name}&days=5&aqi=no&alerts=no"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ========== API Call and Display ==========
if st.button("Get Forecast"):
    if not api_key or api_key.lower() == "password":
        st.warning("⚠️ Please enter a **valid** WeatherAPI Key (not 'password').")
    else:
        data = get_weatherapi_data(city, api_key)

        if "error" in data:
            st.error(f"API Error: {data['error']}")
        elif "location" not in data or "forecast" not in data:
            st.error("❌ City not found or API response incomplete.")
        else:
            location = data["location"]
            st.success(f"✅ Showing 5-day forecast for **{location['name']}**, {location['country']}")

            # Parse forecast data
            forecast_days = data["forecast"]["forecastday"]
            forecast_data = []

            for day in forecast_days:
                for hour in day["hour"]:
                    forecast_data.append({
                        "datetime": hour["time"],
                        "temperature": hour["temp_c"],
                        "humidity": hour["humidity"],
                        "condition": hour["condition"]["text"]
                    })

            df = pd.DataFrame(forecast_data)
            df["datetime"] = pd.to_datetime(df["datetime"])

            # ========== Visualization 1: Temperature Line Chart ==========
            st.subheader("🌡️ Temperature Over Time")
            line_chart = alt.Chart(df).mark_line(point=True).encode(
                x='datetime:T',
                y='temperature:Q',
                tooltip=['datetime', 'temperature']
            ).properties(width=700, height=400)
            st.altair_chart(line_chart)

            # ========== Visualization 2: Humidity Bar Chart ==========
            st.subheader("💧 Humidity Levels")
            bar_chart = alt.Chart(df).mark_bar().encode(
                x='datetime:T',
                y='humidity:Q',
                color=alt.value('#4fc3f7'),
                tooltip=['datetime', 'humidity']
            ).properties(width=700, height=400)
            st.altair_chart(bar_chart)

            # ========== Forecast Table ==========
            with st.expander("🔍 Show forecast table"):
                st.dataframe(df)


