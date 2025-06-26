import streamlit as st
from data_manager import init_database, get_all_boxes
from optimizer import simulate_product_in_boxes
import pandas as pd

def main_ui():
    st.title("📦 Pack Optimizer")
    tab1, tab2, tab3 = st.tabs(["Product Invoer & Simulatie", "Favorieten & Export", "Palletisatie"])

    with tab1:
        st.subheader("1️⃣ Voer een product in")
        with st.form("product_form"):
            col1, col2, col3 = st.columns(3)
            length = col1.number_input("Lengte (mm)", min_value=1.0)
            width = col2.number_input("Breedte (mm)", min_value=1.0)
            height = col3.number_input("Hoogte (mm)", min_value=1.0)

            col4, col5, col6 = st.columns(3)
            margin_l = col4.number_input("Marge lengte (mm)", min_value=0.0, value=0.0)
            margin_w = col5.number_input("Marge breedte (mm)", min_value=0.0, value=0.0)
            margin_h = col6.number_input("Marge hoogte (mm)", min_value=0.0, value=0.0)

            thickness = st.number_input("Dikte van omverpakking (mm)", min_value=0.0, value=3.0)

            submitted = st.form_submit_button("Simuleer")

        if submitted:
            product = {"length": length, "width": width, "height": height}
            margins = {
                "margin_length": margin_l,
                "margin_width": margin_w,
                "margin_height": margin_h
            }

            boxes_df = get_all_boxes()
            boxes = boxes_df.to_dict(orient="records")
            results = simulate_product_in_boxes(product, margins, boxes)

            if results:
                st.success(f"Gevonden {len(results)} mogelijke plaatsingen in omdozen.")
                result_df = pd.DataFrame([{
                    "Omdoos ID": r["box_id"],
                    "Rotatie (LxBxH)": "×".join(map(str, r["rotation"])),
                    "Rijen × Kolommen × Lagen": "×".join(map(str, r["fit"])),
                    "Totaal aantal producten": r["total_products"]
                } for r in results])
                st.dataframe(result_df)
            else:
                st.warning("Geen enkele geldige plaatsing gevonden voor dit product met deze marges.")

    with tab2:
        st.subheader("2️⃣ Favoriete oplossingen")
        st.info("Nog geen favorieten geselecteerd.")

    with tab3:
        st.subheader("3️⃣ Palletisatie Visualisatie")
        st.info("Selecteer eerst een oplossing.")

    st.sidebar.subheader("📂 Omdozen Database")
    if st.sidebar.button("Toon omdozen"):
        df = get_all_boxes()
        st.sidebar.dataframe(df)