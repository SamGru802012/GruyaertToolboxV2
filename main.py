"""
Pack Optimizer App - Streamlit

Beschrijving:
Deze applicatie optimaliseert verpakkingen door te berekenen hoe een product (in 6 mogelijke oriëntaties)
in verschillende omdozen past. De gebruiker kan marges, dooslimieten en productdimensies instellen.
De simulaties tonen hoeveel producten per doos mogelijk zijn op basis van opgegeven limieten.

Belangrijke Functionaliteiten:
- Rotatie-simulatie: 6 rotaties van elk product worden getest in elke doos
- Marges: gebruikers kunnen afzonderlijk marges per richting instellen (L/B/H)
- Limieten: optionele beperking op max. rijen, kolommen en lagen per doos
- Database: dozen worden geladen vanuit een lokale SQLite database
- UI: Streamlit-applicatie met tabbladen en intuïtieve invoer

Samenwerking:
Deze code is geschreven voor iteratieve samenwerking met de GPT "Python & Streamlit Expert".
Bij het opstarten van een nieuwe sessie, kan deze uitleg als context dienen om direct verder te bouwen
op de bestaande architectuur zonder herhaling van vereisten.
"""

import streamlit as st
from ui import main_ui

# Configureer de Streamlit pagina
st.set_page_config(page_title="Pack Optimizer", layout="wide")

# Start de hoofdinterface
main_ui()