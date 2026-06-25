import os

import requests
import streamlit as st
from dotenv import load_dotenv

from app_functions import build_currency_list, convert

load_dotenv()

st.title("Convertisseur de devises")

API_KEY = os.getenv("EXCHANGERATE_API_KEY")
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR"


@st.cache_data(ttl=3600)  # évite de re-appeler l'API à chaque interaction (1h de cache)
def get_rates():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()["conversion_rates"]


rates = get_rates()
currencies = build_currency_list(rates, extra_currencies=["GBP", "CAD"])

if "from_currency" not in st.session_state:
    st.session_state.from_currency = currencies[0]
if "to_currency" not in st.session_state:
    st.session_state.to_currency = currencies[1]
if "history" not in st.session_state:
    st.session_state.history = []


def swap_currencies():
    st.session_state.from_currency, st.session_state.to_currency = (
        st.session_state.to_currency,
        st.session_state.from_currency,
    )


amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
from_currency = st.selectbox("De :", currencies, key="from_currency")
to_currency = st.selectbox("Vers :", currencies, key="to_currency")

st.button("Inverser les devises", on_click=swap_currencies)

if st.button("Convertir"):
    try:
        result = convert(amount, from_currency, to_currency, rates)
    except ValueError as e:
        st.error(str(e))
    else:
        conversion = f"{amount} {from_currency} = {result:.2f} {to_currency}"
        st.success(conversion)
        st.session_state.history.append(conversion)

if st.session_state.history:
    st.subheader("Historique des conversions")
    for entry in reversed(st.session_state.history):
        st.write(entry)
    if st.button("Effacer l'historique"):
        st.session_state.history = []
        st.rerun()
