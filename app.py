
import streamlit as st
from core.database import init_db

st.set_page_config(
    page_title="Verpakkingsoptimalisatie",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

st.sidebar.title("📋 Navigatie")
st.sidebar.info("Gebruik het menu om door de applicatie te navigeren.")

st.title("📦 Verpakkingsoptimalisatie App")
st.markdown("Welkom! Gebruik het menu links om een doos te kiezen, simulaties uit te voeren of bestaande data te beheren.")
