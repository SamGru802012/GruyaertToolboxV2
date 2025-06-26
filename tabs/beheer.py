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

    if df.empty:
        st.info("De database bevat nog geen dozen.")
        df = pd.DataFrame(columns=[
            "id", "inner_length", "inner_width", "inner_height",
            "wall_thickness", "stock", "description", "extra_info"
        ])

    st.subheader("📋 Beheer dozen (bewerken, toevoegen, verwijderen)")
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_boxes"
    )

    st.subheader("💾 Acties")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Opslaan wijzigingen in database"):
            try:
                # Validatie voor unieke ID's
                if edited_df["id"].duplicated().any():
                    st.error("Elke doos moet een unieke 'id' hebben.")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    edited_df.to_sql("boxes", conn, if_exists="replace", index=False)
                    conn.commit()
                    conn.close()
                    st.success("Wijzigingen opgeslagen.")
            except Exception as e:
                st.error(f"Fout bij opslaan: {e}")
    with col2:
        if st.button("🔄 Herladen vanuit database"):
            st.experimental_rerun()
