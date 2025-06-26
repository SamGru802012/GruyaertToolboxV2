"""
==================================================================================
Tab 1 – Dooskeuze (geoptimaliseerd)
==================================================================================
Berekent en toont verpakkingsoplossingen, inclusief checkboxes voor selectie en
opslag. Verbetert gebruikerservaring met knoppen, meldingen en validatie.
"""

import streamlit as st
import pandas as pd
import sqlite3
from core.optimizer import calculate_fits
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "dozen_db.sqlite")

def render():
    st.header("🔍 Dooskeuze & Verpakkingsoptimalisatie")

    # Invoer
    col1, col2 = st.columns(2)
    with col1:
        product_ref = st.text_input("Productreferentie", value="PRD001")
        l = st.number_input("Lengte (mm)", min_value=1.0, value=100.0)
        b = st.number_input("Breedte (mm)", min_value=1.0, value=80.0)
        h = st.number_input("Hoogte (mm)", min_value=1.0, value=60.0)
    with col2:
        margin_l = st.number_input("Marge lengte (mm)", value=2.0)
        margin_b = st.number_input("Marge breedte (mm)", value=2.0)
        margin_h = st.number_input("Marge hoogte (mm)", value=2.0)

    if st.button("🔄 Bereken oplossingen"):
        # Dozen ophalen uit DB
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql("SELECT * FROM boxes", conn)
            conn.close()
        except Exception as e:
            st.error(f"Fout bij laden van dozen: {e}")
            return

        if df.empty:
            st.warning("Geen omverpakkingen gevonden in database.")
            return

        resultaten = []

        for _, row in df.iterrows():
            box_id = row["id"]
            dims = (row["inner_length"], row["inner_width"], row["inner_height"])
            wall = row.get("wall_thickness", 3)
            result = calculate_fits((l, b, h), dims, (margin_l, margin_b, margin_h), wall)

            for conf in result:
                resultaten.append({
                    "product_ref": product_ref,
                    "box_id": box_id,
                    "box_dim": f"{dims[0]}x{dims[1]}x{dims[2]}",
                    "product_rotation": conf["rotation"],
                    "rows": conf["rows"],
                    "columns": conf["columns"],
                    "layers": conf["layers"],
                    "total_units": conf["total"],
                    "pallet_height": round(conf["layers"] * (h + margin_h), 2),
                    "efficiency": conf["efficiency"],
                    "✔️ selecteer": False
                })

        if not resultaten:
            st.warning("Geen geschikte omdozen gevonden. Controleer marges of doosafmetingen.")
            return

        result_df = pd.DataFrame(resultaten)
        result_df["✔️ selecteer"] = result_df["✔️ selecteer"].astype(bool)

        with st.form("opslagformulier"):
            st.markdown("### ✅ Selecteer oplossingen om op te slaan")
            edited = st.data_editor(result_df, use_container_width=True, num_rows="dynamic")
            submitted = st.form_submit_button("💾 Bevestig selectie")

        if submitted:
            selectie = edited[edited["✔️ selecteer"] == True].drop(columns=["✔️ selecteer"])
            if selectie.empty:
                st.warning("Geen rijen geselecteerd.")
            else:
                st.session_state["laatste_resultaten"] = selectie
                st.success(f"{len(selectie)} oplossing(en) klaar om op te slaan in tab 2.")
    else:
        st.info("Voer productgegevens in en klik op '🔄 Bereken oplossingen' om te starten.")
