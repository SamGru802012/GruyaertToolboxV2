import streamlit as st
from modules import algorithm, db, visualizer, utils

# Initialize session state
utils.initialize_session()

# App layout with tabs
st.set_page_config(page_title="Verpakkingsoptimalisatie & Palletisatie", layout="wide")
st.title("📦 Verpakkingsoptimalisatie & Palletisatie App")

# Tab structure
tab1, tab2, tab3 = st.tabs(["🔹 Verpakkingsoptimalisatie", "🔹 Geselecteerde Oplossingen", "🔹 Palletisatie"])

with tab1:
    algorithm.render_optimization_tab()

with tab2:
    db.render_favorites_tab()

with tab3:
    visualizer.render_pallet_tab()
