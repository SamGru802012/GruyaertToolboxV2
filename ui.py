import streamlit as st
from data_manager import init_database, get_all_boxes
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

            col4, col5 = st.columns(2)
            margin = col4.number_input("Marges in doos (mm)", min_value=0.0, value=0.0)
            thickness = col5.number_input("Dikte van omverpakking (mm)", min_value=0.0, value=3.0)

            submitted = st.form_submit_button("Simuleer")

        if submitted:
            st.info("Simulatie volgt later...")
            st.write(f"Productafmetingen: {length}×{width}×{height} mm")

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