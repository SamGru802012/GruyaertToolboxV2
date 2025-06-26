"""
==================================================================================
Tab 2 – Opgeslagen Oplossingen
==================================================================================
Toont opgeslagen configuraties met visualisatieoptie en export naar CSV.
Laat ook toe om recente resultaten op te slaan (met selectie via checkbox).
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
    else:
        st.subheader("📘 Bestaande opgeslagen oplossingen")
        selected_idx = st.radio("Selecteer oplossing voor inspectie/export:", df.index, horizontal=True)
        st.dataframe(df)

        st.download_button(
            label="📤 Exporteer alle oplossingen (CSV)",
            data=df.to_csv(index=False).encode(),
            file_name="oplossingen.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.subheader("💡 Nieuwe oplossingen bewaren uit tabblad 1")

    session_df = st.session_state.get("laatste_resultaten")
    if session_df is None or session_df.empty:
        st.info("Geen nieuwe resultaten beschikbaar in de sessie.")
        return

    session_df["selecteer"] = False
    edited = st.data_editor(session_df, num_rows="dynamic", use_container_width=True, key="selecteer_opslag")

    if st.button("🗃️ Bewaar geselecteerde oplossingen"):
        selectie = edited[edited["selecteer"] == True].drop(columns=["selecteer"])
        if selectie.empty:
            st.warning("Geen rijen geselecteerd om op te slaan.")
        else:
            try:
                conn = sqlite3.connect(DB_PATH)
                selectie.to_sql("saved_solutions", conn, if_exists="append", index=False)
                conn.commit()
                conn.close()
                st.success(f"{len(selectie)} oplossing(en) succesvol opgeslagen.")
            except Exception as e:
                st.error(f"Opslagfout: {e}")
