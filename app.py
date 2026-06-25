import os

import requests
import streamlit as st
from dotenv import load_dotenv

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

amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
from_currency = st.selectbox("De :", rates.keys())
to_currency = st.selectbox("Vers :", rates.keys())


#AVANT
#if st.button("Convertir"):
    #result = amount * rates[to_currency] / rates[from_currency]
    #st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")


if st.button("Convertir"): #il s'execute quand user cliquise qur bouton
      if amount <= 0:      # on verifie que amount ne sois pas inferireur ou = à zero
          st.error("Le montant doit être supérieur à zéro.")  #afficher message d'erreur rouge (st.error), STOP

      elif from_currency == to_currency:                        # si devis a = devise b
          st.error("Les deux devises ne peuvent pas être identiques.")  # affihcer message erreur

      else:                                    # sinon
          result = amount * rates[to_currency] / rates[from_currency] #on ramene en euro ( devise de reference) puis on convertis en devise cible
          st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}") #on affihce le resultat
