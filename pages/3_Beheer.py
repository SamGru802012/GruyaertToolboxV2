
import streamlit as st
import pandas as pd
import sqlite3
from core.database import get_connection

def fetch_boxes():
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM boxes", conn)

def save_box(data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO boxes (id, inner_length, inner_width, inner_height, stock, description, extra_info)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"], data["inner_length"], data["inner_width"], data["inner_height"],
            data["stock"], data["description"], data["extra_info"]
        ))
        conn.commit()

def render_beheer():
    st.header("🧰 Beheer van Dozen")

    st.subheader("📦 Nieuwe of bestaande doos toevoegen")
    with st.form("box_form"):
        id = st.text_input("Doos-ID")
        length = st.number_input("Lengte (mm)", min_value=10.0)
        width = st.number_input("Breedte (mm)", min_value=10.0)
        height = st.number_input("Hoogte (mm)", min_value=10.0)
        stock = st.number_input("Voorraad", min_value=0, step=1)
        desc = st.text_input("Beschrijving")
        extra = st.text_area("Extra info")

        submitted = st.form_submit_button("💾 Bewaar doos")
        if submitted:
            data = {
                "id": id,
                "inner_length": length,
                "inner_width": width,
                "inner_height": height,
                "stock": stock,
                "description": desc,
                "extra_info": extra
            }
            try:
                save_box(data)
                st.success(f"Doos '{id}' opgeslagen.")
            except Exception as e:
                st.error(f"Fout bij opslaan: {e}")

    st.markdown("---")
    st.subheader("📋 Overzicht van dozen in database")
    df = fetch_boxes()
    if df.empty:
        st.info("Geen dozen in database.")
    else:
        st.dataframe(df, use_container_width=True)
