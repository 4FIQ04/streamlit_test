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
api_key = st.text_input("Enter your OpenWeatherMap API Key:", type="password")

# ========== Weather Data Fetch Function ==========
@st.cache_data
def get_weather_data(city_name, key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ========== API Call and Error Handling ==========

if st.button("Get Forecast"):
    if not api_key:
        st.warning("Please provide a valid OpenWeatherMap API Key.")
    else:
        data = get_weather_data(city, api_key)

        if "error" in data:
            st.error(f"API Error: {data['error']}")
        elif data.get("cod") != "200":
            st.error("City not found or API returned an error.")
        else:
            st.success(f"Showing 5-day forecast for {data['city']['name']}, {data['city']['country']}")

            # Parse and prepare data
            forecast_data = []
            for item in data['list']:
                forecast_data.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "condition": item["weather"][0]["description"].title()
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

            # ========== Optional: Forecast Table ==========
            with st.expander("🔍 Show forecast table"):
                st.dataframe(df)



    # Optional: Show raw JSON
    with st.expander("See full exchange rates (JSON)"):
        st.json(rates)


