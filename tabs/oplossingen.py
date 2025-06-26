"""
==================================================================================
Tab 2 – Opgeslagen Oplossingen
==================================================================================
Toont opgeslagen configuraties met visualisatieoptie en export naar CSV.
"""

import streamlit as st
import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "dozen_db.sqlite")

def render():
    st.header("💾 Opgeslagen Oplossingen")

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM saved_solutions", conn)
        conn.close()
    except Exception as e:
        st.error(f"Fout bij laden van oplossingen: {e}")
        return

    if df.empty:
        st.info("Nog geen oplossingen opgeslagen.")
        return

    selected_index = st.radio("Selecteer een oplossing voor export of visualisatie:", df.index)

    st.dataframe(df)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Exporteer naar CSV"):
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False).encode(),
                file_name="oplossingen.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("🗃 Bewaar laatste resultaten (sessie)"):
            session_df = st.session_state.get("laatste_resultaten")
            if session_df is not None:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    session_df.to_sql("saved_solutions", conn, if_exists="append", index=False)
                    conn.commit()
                    conn.close()
                    st.success("Resultaten opgeslagen.")
                except Exception as e:
                    st.error(f"Opslagfout: {e}")
            else:
                st.warning("Geen sessieresultaten beschikbaar om op te slaan.")
