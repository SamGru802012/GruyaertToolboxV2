"""
==================================================================================
Verpakkingsoptimalisatie App – hoofdentry
==================================================================================
Streamlit applicatie om optimale productverpakking en palletisatie te simuleren.
"""

import streamlit as st
from models.init_db import init_db
from tabs import dooskeuze, oplossingen, palletisatie, beheer

init_db()
st.set_page_config(layout="wide", page_title="Verpakkingsoptimalisatie")

tab = st.sidebar.radio("📋 Menu", ["Dooskeuze", "Opgeslagen Oplossingen", "Palletisatie", "Beheer"])

if tab == "Dooskeuze":
    dooskeuze.render()
elif tab == "Opgeslagen Oplossingen":
    oplossingen.render()
elif tab == "Palletisatie":
    palletisatie.render()
elif tab == "Beheer":
    beheer.render()
