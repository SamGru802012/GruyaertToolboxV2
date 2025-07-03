
import streamlit as st
import pandas as pd
import json
from modules import algorithm, db, visualizer, utils
import plotly.io as pio

st.set_page_config(page_title="Verpakkingsoptimalisatie", layout="wide")
db.init_db()

# Init session_state
if "solutions" not in st.session_state:
    st.session_state["solutions"] = []

if "selected_solution" not in st.session_state:
    st.session_state["selected_solution"] = None

if "undo_stack" not in st.session_state:
    st.session_state["undo_stack"] = []

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Verpakkingsoptimalisatie",
    "⭐ Geselecteerde oplossingen",
    "📦 Palletisatie",
    "🗃️ Dozenbeheer"
])

with tab1:
    st.header("🔍 Verpakkingsoptimalisatie")

    with st.form("product_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_ref = st.text_input("Productreferentie", help="Unieke naam of code voor het product")
            product_l = st.number_input("Lengte (mm)", min_value=1, step=1)
            product_b = st.number_input("Breedte (mm)", min_value=1, step=1)
            product_h = st.number_input("Hoogte (mm)", min_value=1, step=1)
        with col2:
            marge_l = st.number_input("Marge lengte (mm)", min_value=0, value=0)
            marge_b = st.number_input("Marge breedte (mm)", min_value=0, value=0)
            marge_h = st.number_input("Marge hoogte (mm)", min_value=0, value=0)
            max_rijen = st.number_input("Max rijen (langs lengte-as)", min_value=0, value=0)
            max_kolommen = st.number_input("Max kolommen (langs breedte-as)", min_value=0, value=0)
            max_lagen = st.number_input("Max lagen (gestapeld in hoogte)", min_value=0, value=0)

        submitted = st.form_submit_button("➕ Bereken optimalisaties")

    if submitted:
        product_afm = [product_l, product_b, product_h]
        marges = [marge_l, marge_b, marge_h]
        limieten = [max_rijen, max_kolommen, max_lagen]
        doos_df = db.fetch_boxes()

        if doos_df.empty:
            st.error("❌ Geen dozen beschikbaar in de database.")
        else:
            resultaten = algorithm.optimize_packaging(product_afm, marges, doos_df, limieten)
            for r in resultaten:
                r["product_ref"] = product_ref
            st.session_state["solutions"] = resultaten
            st.success(f"{len(resultaten)} oplossingen berekend.")

    if st.session_state["solutions"]:
        df = pd.DataFrame(st.session_state["solutions"])
        df["Binnenafm."] = df.apply(lambda x: utils.format_dimensions(x["binnen_l"], x["binnen_b"], x["binnen_h"]), axis=1)
        df_display = df[["product_ref", "doos_id", "Binnenafm.", "rijen", "kolommen", "lagen", "totaal_stuks", "volume_eff"]]

        selected_idx = st.selectbox("Selecteer een oplossing om te visualiseren", df_display.index)
        st.dataframe(df_display.sort_values("volume_eff", ascending=False), use_container_width=True)

        if st.button("📊 Visualiseer geselecteerde oplossing"):
            selected = st.session_state["solutions"][selected_idx]
            st.session_state["selected_solution"] = selected
            fig = visualizer.visualize_box(
                [selected["binnen_l"], selected["binnen_b"], selected["binnen_h"]],
                eval(selected["product_rotatie"]),
                selected["rijen"], selected["kolommen"], selected["lagen"]
            )
            st.plotly_chart(fig, use_container_width=True)
            if st.download_button("📸 Download snapshot (PNG)", pio.to_image(fig, format="png"), file_name="visualisatie.png"):
                st.toast("Snapshot geëxporteerd ✅")

        if st.button("✅ Bewaar als favoriet"):
            selected = st.session_state["solutions"][selected_idx]
            db.insert_solution(selected)
            utils.push_undo("save", selected)
            st.success("Oplossing bewaard als favoriet")

with tab2:
    st.header("⭐ Geselecteerde oplossingen")
    favs = db.fetch_solutions()
    if not favs.empty:
        st.dataframe(favs, use_container_width=True)
    else:
        st.info("Nog geen favorieten opgeslagen.")

with tab3:
    st.header("📦 Palletisatie")
    st.info("Deze functie wordt verder uitgewerkt.")

with tab4:
    st.header("🗃️ Dozenbeheer")
    doos_data = db.fetch_boxes()
    if doos_data.empty:
        st.warning("Geen dozen gevonden in de database.")
    else:
        edited = st.data_editor(doos_data, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Opslaan wijzigingen"):
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM boxes")
            for _, row in edited.iterrows():
                cursor.execute("""
                    INSERT INTO boxes (id, binnen_l, binnen_b, binnen_h, wanddikte, stock, omschrijving)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row["id"]),
                    row["binnen_l"],
                    row["binnen_b"],
                    row["binnen_h"],
                    row["wanddikte"],
                    row["stock"],
                    row["omschrijving"]
                ))
            conn.commit()
            conn.close()
            st.success("Dozen succesvol opgeslagen.")
