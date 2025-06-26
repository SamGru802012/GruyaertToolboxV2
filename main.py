
import streamlit as st
from utils import optimizer, palletizer, visualizer, data_handler
from utils.models import ProductInput
import json

st.set_page_config(page_title="Verpakkingsoptimalisatie", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["📦 Invoer & Voorstellen", "⭐ Gekozen Oplossingen", "🧱 Palletisatie", "📂 Omdoosbeheer"])

with tab1:
    st.header("📦 Invoer & Verpakkingsvoorstellen")
    product_l = st.number_input("Product Lengte (mm)", min_value=1)
    product_b = st.number_input("Product Breedte (mm)", min_value=1)
    product_h = st.number_input("Product Hoogte (mm)", min_value=1)
    gewicht = st.number_input("Gewicht (g)", min_value=0)
    marge_l = st.number_input("Marge Lengte (mm)", value=0)
    marge_b = st.number_input("Marge Breedte (mm)", value=0)
    marge_h = st.number_input("Marge Hoogte (mm)", value=0)
    dikte = st.number_input("Dikte omverpakking (mm)", value=3)
    pallet_l = st.number_input("Pallet Lengte (mm)", value=1200)
    pallet_b = st.number_input("Pallet Breedte (mm)", value=800)
    pallet_h = st.number_input("Max Pallethoogte (mm)", value=1440)

    if st.button("Genereer voorstellen"):
        product = ProductInput(product_l, product_b, product_h, gewicht, [marge_l, marge_b, marge_h])
        voorstellen = optimizer.genereer_voorstellen(product, dikte)
        st.session_state["voorstellen"] = voorstellen
        for i, voorstel in enumerate(voorstellen):
            with st.expander(f"Rotatie {i+1} - Score: {voorstel.score:.2f}"):
                st.plotly_chart(visualizer.teken_doos(product, voorstel))
                st.checkbox("Favoriet", key=f"fav_{i}")
                st.radio("Selecteer voor visualisatie", [f"Rotatie {i+1}"], key=f"vis_{i}")

with tab2:
    st.header("⭐ Gekozen oplossingen")
    if "voorstellen" in st.session_state:
        for i, voorstel in enumerate(st.session_state["voorstellen"]):
            if st.session_state.get(f"fav_{i}"):
                st.subheader(f"Favoriet: Rotatie {i+1}")
                st.plotly_chart(visualizer.teken_doos(None, voorstel))
        if st.button("Exporteer naar CSV"):
            st.success("CSV geëxporteerd")
        if st.button("Exporteer naar PDF"):
            st.success("PDF geëxporteerd")

with tab3:
    st.header("🧱 Palletisatie")
    if "voorstellen" in st.session_state:
        gekozen = next((v for i, v in enumerate(st.session_state["voorstellen"]) if st.session_state.get(f"vis_{i}") == f"Rotatie {i+1}"), None)
        if gekozen:
            fig = palletizer.palletiseer(gekozen)
            st.plotly_chart(fig)

with tab4:
    st.header("📂 Omdoosbeheer")
    dozen = data_handler.load_dozen()
    st.dataframe(dozen)
    with st.expander("➕ Nieuwe doos toevoegen"):
        new_ref = st.text_input("Referentie")
        new_l = st.number_input("Lengte (mm)", key="nl")
        new_b = st.number_input("Breedte (mm)", key="nb")
        new_h = st.number_input("Hoogte (mm)", key="nh")
        new_d = st.number_input("Dikte (mm)", key="nd", value=3)
        new_s = st.number_input("Stock", key="ns", value=0)
        new_o = st.text_input("Omschrijving")
        if st.button("Voeg toe"):
            data_handler.add_doos(new_ref, new_l, new_b, new_h, new_d, new_s, new_o)
            st.success("Doos toegevoegd")
