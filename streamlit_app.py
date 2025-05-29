import streamlit as st
import requests

# Custom CSS for colorful background and text styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #ffecd2, #fcb69f);
            color: #000000;
        }
        .stApp {
            background: linear-gradient(to right, #89f7fe, #66a6ff);
            padding: 20px;
            border-radius: 10px;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #222222;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">💸 MYR Currency Exchange</div>', unsafe_allow_html=True)

# User name input
user_name = st.text_input("What's your name?", "Guest")
st.write(f"👋 Welcome, **{user_name}**! Hope you're having a great day!")

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
