"""
==================================================================================
Tab 4 – Beheer van omverpakkingen (CRUD)
==================================================================================
Laat toe om dozen toe te voegen, te bewerken of te verwijderen in de database.
"""

import streamlit as st
import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "dozen_db.sqlite")

def render():
    st.header("🛠️ Beheer van Omverpakkingen")

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM boxes", conn)
    except Exception as e:
        st.error(f"Fout bij laden van dozen: {e}")
        return

    st.subheader("📋 Bestaande dozen")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    st.subheader("💾 Opslaan wijzigingen")
    if st.button("Opslaan"):
        try:
            conn = sqlite3.connect(DB_PATH)
            edited_df.to_sql("boxes", conn, if_exists="replace", index=False)
            conn.commit()
            conn.close()
            st.success("Wijzigingen succesvol opgeslagen.")
        except Exception as e:
            st.error(f"Fout bij opslaan: {e}")
