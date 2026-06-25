import streamlit as st

st.title("Convertisseur de devises")

rates = {
    "EUR": 1,
    "USD": 1.1,
    "JPY": 130
}

amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
from_currency = st.selectbox("De :", rates.keys())
to_currency = st.selectbox("Vers :", rates.keys())

if st.button("Convertir"):
    result = amount * rates[to_currency] / rates[from_currency]
    st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
