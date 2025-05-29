import streamlit as st
import requests

st.title('💱 MYR Currency Converter')

# Fetch rates
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    rates = data['rates']

    # Dropdown for selecting target currency
    currency_list = sorted(rates.keys())
    selected_currency = st.selectbox("Select currency to convert MYR to:", currency_list)

    # Input for amount in MYR
    amount = st.number_input("Enter amount in MYR:", min_value=0.0, value=1.0)

    # Perform conversion
    result = amount * rates[selected_currency]
    st.success(f"{amount:.2f} MYR = {result:.2f} {selected_currency}")

else:
    st.error("Failed to fetch exchange rates.")

