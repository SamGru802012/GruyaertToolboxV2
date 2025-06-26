"""
==================================================================================
Streamlit Verpakkingsoptimalisatie App
==================================================================================

Beschrijving:
-------------
Deze applicatie helpt bij het optimaliseren van verpakkingen:
- Producten worden in dozen geplaatst met 6 rotatiemogelijkheden.
- Dozen worden vervolgens optimaal gestapeld op een europallet.
- Alles wordt opgeslagen in een SQLite-database met visuele 3D ondersteuning.
- Ondersteuning voor CRUD-operaties op doosdata.
"""

import streamlit as st
from tabs.tab_dooskeuze import tab_dooskeuze
from tabs.tab_oplossingen import tab_oplossingen
from tabs.tab_palletisatie import tab_palletisatie
from tabs.tab_crud import tab_crud

st.set_page_config(layout="wide", page_title="Verpakkingsoptimalisatie")

tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Dooskeuze",
    "2️⃣ Gekozen Oplossingen",
    "3️⃣ Palletisatie",
    "4️⃣ CRUD Omverpakkingen"
])

# Koppel elke tab aan zijn module
with tab1:
    tab_dooskeuze()

with tab2:
    tab_oplossingen()

with tab3:
    tab_palletisatie()

with tab4:
    tab_crud()
