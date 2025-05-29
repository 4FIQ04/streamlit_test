import streamlit as st
import requests

# Font selection
font_options = {
    "Sans Serif": "Arial, Harlow Solid Italic",
    "Serif": "Georgia, serif",
    "Monospace": "Courier New, monospace"
}
selected_font = st.selectbox("Choose your preferred font style:", list(font_options.keys()))
font_family = font_options[selected_font]

# Custom CSS with selected font and colorful background
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

# Title
st.markdown('<div class="title">💸 MYR Currency Exchange</div>', unsafe_allow_html=True)

# User name input
user_name = st.text_input("What's your name?", "Guest")
st.markdown(f'<div class="username">👋 Welcome, <strong>{user_name}</strong>! Hope you\'re having a fantastic day!</div>', unsafe_allow_html=True)

# Custom message input
user_message = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('📢 Your Message:', user_message)

# Fetch exchange rates
st.subheader('💱 Currency Conversion (Base: MYR)')
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    rates = data['rates']

    # Dropdown to select a currency
    currency_list = sorted(rates.keys())
    selected_currency = st.selectbox('Select a currency to convert MYR to:', currency_list)

    # Input amount
    amount = st.number_input('Enter amount in MYR:', min_value=0.0, value=1.0)

    # Conversion result
    result = amount * rates[selected_currency]
    st.success(f"{amount:.2f} MYR = {result:.2f} {selected_currency}")

    # Optional: Show all rates
    with st.expander("See all exchange rates (JSON)"):
        st.json(rates)

else:
    st.error("Failed to fetch exchange rates from API.")
