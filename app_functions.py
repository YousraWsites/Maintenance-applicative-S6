"""Logique métier du convertisseur de devises, isolée de l'interface Streamlit.

Extraite de app.py (maintenance perfective) pour permettre des tests
unitaires sans dépendre de Streamlit.
"""


def convert(amount, from_currency, to_currency, rates):
    """Convertit `amount` de `from_currency` vers `to_currency` selon `rates`.

    Lève ValueError si le montant est invalide ou si les deux devises sont
    identiques, conformément aux règles posées par la maintenance corrective.
    """
    if amount <= 0:
        raise ValueError("Le montant doit être supérieur à zéro.")
    if from_currency == to_currency:
        raise ValueError("Les deux devises ne peuvent pas être identiques.")
    return amount * rates[to_currency] / rates[from_currency]


def build_currency_list(rates, extra_currencies=None):
    """Construit la liste des devises proposées : celles de `rates`, plus
    celles de `extra_currencies` si elles existent dans `rates` et ne sont
    pas déjà présentes (évite les doublons dans le selectbox).
    """
    currencies = list(rates.keys())
    for devise in extra_currencies or []:
        if devise in rates and devise not in currencies:
            currencies.append(devise)
    return currencies
