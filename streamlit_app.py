import streamlit as st
import requests
import pandas as pd
import altair as alt

# ========== Setup ==========
# Font options for UI customization
font_options = {
    "Sans Serif": "Arial, sans-serif",
    "Serif": "Georgia, serif",
    "Monospace": "Courier New, monospace"
}
selected_font = st.selectbox("Choose your preferred font style:", list(font_options.keys()))
font_family = font_options[selected_font]

# ========== Custom CSS ==========
st.markdown(f"""
    <style>
        body {{
            background: linear-gradient(to right, #ffe0b2, #ffccbc);
            font-family: {font_family};
        }}
        .stApp {{
            background: linear-gradient(to right, #fceabb, #f8b500);
            padding: 20px;
            border-radius: 10px;
        }}
        .title {{
            font-size: 36px;
            font-weight: bold;
            color: #4e342e;
            font-family: {font_family};
        }}
        .username {{
            font-weight: bold;
            font-size: 20px;
            color: #5d4037;
        }}
    </style>
""", unsafe_allow_html=True)

# ========== Title ==========
st.markdown('<div class="title">💸 MYR Currency Exchange Dashboard</div>', unsafe_allow_html=True)

# ========== Inputs ==========
user_name = st.text_input("What's your name?", "Guest")
st.markdown(f'<div class="username">👋 Welcome, <strong>{user_name}</strong>! Hope you\'re having a fantastic day!</div>', unsafe_allow_html=True)

user_message = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('📢 Your Message:', user_message)

# ========== Fetch Exchange Rates ==========
st.subheader('💱 Currency Conversion (Base: MYR)')

@st.cache_data
def get_exchange_rates():
    try:
        response = requests.get('https://api.vatcomply.com/rates?base=MYR')
        response.raise_for_status()
        return response.json()['rates']
    except Exception as e:
        st.error(f"Failed to fetch exchange rates: {e}")
        return {}

rates = get_exchange_rates()

if rates:
    # Dropdown to select a currency
    currency_list = sorted(rates.keys())
    selected_currency = st.selectbox('Select a currency to convert MYR to:', currency_list)

    # Input amount
    amount = st.number_input('Enter amount in MYR:', min_value=0.0, value=1.0)

    # Conversion
    result = amount * rates[selected_currency]
    st.success(f"{amount:.2f} MYR = {result:.2f} {selected_currency}")

    # ========== Visualization 1: Top 10 Rates Bar Chart ==========
    st.subheader("📊 Top 10 Exchange Rates")
    rate_df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"]).sort_values(by="Rate", ascending=False).head(10)

    bar_chart = alt.Chart(rate_df).mark_bar().encode(
        x=alt.X('Rate:Q'),
        y=alt.Y('Currency:N', sort='-x'),
        color=alt.value('#ff7043')
    ).properties(width=600)

    st.altair_chart(bar_chart)

    # ========== Visualization 2: Line Chart of Example Rates ==========
    st.subheader("📈 Example Line Chart (USD, EUR, GBP)")
    selected = ['USD', 'EUR', 'GBP']
    line_df = pd.DataFrame({cur: [rates[cur]] for cur in selected}, index=['Today'])
    st.line_chart(line_df)

    # Optional: Show raw JSON
    with st.expander("See full exchange rates (JSON)"):
        st.json(rates)


