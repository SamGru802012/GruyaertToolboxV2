"""
==================================================================================
Tab 4 – CRUD voor omverpakkingen
==================================================================================
Laat toe dozen (omverpakkingen) te beheren: toevoegen, bewerken, verwijderen,
met persistente opslag in een SQLite-database. Exporteren naar CSV mogelijk.
"""

import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "data/dozen_db.sqlite"

def load_boxes():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM boxes", conn)
    conn.close()
    return df

def save_boxes(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("boxes", conn, if_exists="replace", index=False)
    conn.close()

def tab_crud():
    st.subheader("📦 Beheer Omverpakkingen")

    df = load_boxes()
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="crud_table"
    )

    if st.button("💾 Wijzigingen opslaan"):
        save_boxes(edited_df)
        st.success("Gegevens opgeslagen in database.")

    csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button("📤 Exporteer naar CSV", data=csv, file_name="dozen_export.csv", mime="text/csv")

    st.markdown("⚠️ Verwijderen gebeurt via de editor: rij verwijderen en opslaan.")
