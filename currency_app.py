import requests
import streamlit as st

# Function to validate currency code
def is_valid_currency(code):
    return isinstance(code, str) and len(code) == 3

# Function to perform currency conversion
def convert_currency(amount, from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("result") != "success":
            return None, f"API Error: {data.get('error-type', 'Unknown error')}"

        rates = data.get("rates", {})
        if to_currency not in rates:
            return None, "Target currency not found."

        rate = rates[to_currency]
        result = amount * rate
        return result, None

    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit UI
st.title("💱 Currency Converter App")

name = st.text_input("Enter your name:")
amount = st.number_input("Enter amount to convert:", min_value=0.0, format="%.2f")
from_currency = st.text_input("Enter source currency code (e.g., USD):").upper()
to_currency = st.text_input("Enter target currency code (e.g., EUR):").upper()

if st.button("Convert"):
    if not name or not is_valid_currency(from_currency) or not is_valid_currency(to_currency):
        st.warning("Please enter a valid name and 3-letter currency codes.")
    else:
        result, error = convert_currency(amount, from_currency, to_currency)
        if error:
            st.error(error)
        else:
            st.success(f"Hello {name}, {amount} {from_currency} = {result:.2f} {to_currency}")
