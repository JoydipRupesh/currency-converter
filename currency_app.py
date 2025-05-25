import streamlit as st
from forex_python.converter import CurrencyRates
from datetime import datetime

# App title
st.set_page_config(page_title="Currency Converter 💱", page_icon="💱")
st.title("🌍 Currency Converter")

# Get currency rates using forex-python
cr = CurrencyRates()

# Get currency codes from a base (e.g., USD)
currency_codes = list(cr.get_rates('USD').keys())

# Include USD itself
currency_codes.append('USD')

# Remove duplicates (just in case) and sort alphabetically
currency_codes = sorted(set(currency_codes))

# Currency input options
from_currency = st.selectbox("🔻 From Currency", currency_codes, index=currency_codes.index("USD"))
to_currency = st.selectbox("🔺 To Currency", currency_codes, index=currency_codes.index("BDT"))

# Amount input
amount = st.number_input("💰 Enter amount", min_value=0.0, format="%.2f")

# Convert on button click
if st.button("Convert 💱"):
    try:
        converted_amount = cr.convert(from_currency, to_currency, amount)
        st.success(f"✅ {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")

# Footer
st.caption(f"🕒 Exchange rates updated live | Powered by forex-python")
