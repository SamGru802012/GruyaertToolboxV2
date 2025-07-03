import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import itertools
import uuid
from modules.utils import add_to_undo_stack
from modules.visualizer import render_3d_visualisatie

DB_PATH = "data/boxes.sqlite"

def generate_rotations(dimensions):
    return list(set(itertools.permutations(dimensions)))

def calculate_fit(box, product, margins, limits):
    binnen_l, binnen_b, binnen_h = box["binnen_l"], box["binnen_b"], box["binnen_h"]
    product_l, product_b, product_h = product
    margin_l, margin_b, margin_h = margins

    netto_l = binnen_l - margin_l
    netto_b = binnen_b - margin_b
    netto_h = binnen_h - margin_h

    if netto_l < 0 or netto_b < 0 or netto_h < 0:
        return None

    rijen = int(netto_l // product_l)
    kolommen = int(netto_b // product_b)
    lagen = int(netto_h // product_h)

    if limits:
        max_r, max_k, max_l = limits
        rijen = min(rijen, max_r)
        kolommen = min(kolommen, max_k)
        lagen = min(lagen, max_l)

    totaal = rijen * kolommen * lagen
    doos_volume = binnen_l * binnen_b * binnen_h
    product_volume = product_l * product_b * product_h
    volume_eff = 0
    if doos_volume > 0:
        volume_eff = round((totaal * product_volume) / doos_volume * 100, 2)

    if totaal > 0:
        return {
            "rijen": rijen,
            "kolommen": kolommen,
            "lagen": lagen,
            "totaal_stuks": totaal,
            "volume_eff": volume_eff
        }
    return None

def render_optimization_tab():
    with st.form("optimalisatie_form"):
        st.markdown("### 📦 Verpakkingsoptimalisatie")

        product_ref = st.text_input("Productreferentie", help="Unieke naam of referentie van het product")
        col1, col2, col3 = st.columns(3)
        with col1:
            l = st.number_input("Lengte (mm)", min_value=1.0, help="Productlengte in mm")
        with col2:
            b = st.number_input("Breedte (mm)", min_value=1.0, help="Productbreedte in mm")
        with col3:
            h = st.number_input("Hoogte (mm)", min_value=1.0, help="Producthoogte in mm")

        wanddikte = st.number_input("Wanddikte omverpakking (mm)", min_value=0.0, value=3.0, help="Wanddikte van de doos in mm")

        st.markdown("**Marges binnen de doos (mm)**")
        m1, m2, m3 = st.columns(3)
        margin_l = m1.number_input("Marge Lengte", min_value=0.0, value=0.0)
        margin_b = m2.number_input("Marge Breedte", min_value=0.0, value=0.0)
        margin_h = m3.number_input("Marge Hoogte", min_value=0.0, value=0.0)

        st.markdown("**Limieten per richting (optioneel)**")
        l1, l2, l3 = st.columns(3)
        max_rijen = l1.number_input("Max rijen (lengte-as)", min_value=1, value=999)
        max_kolommen = l2.number_input("Max kolommen (breedte-as)", min_value=1, value=999)
        max_lagen = l3.number_input("Max lagen (hoogte-as)", min_value=1, value=999)

        submitted = st.form_submit_button("Bereken optimale verpakkingen")

    if submitted:
        st.session_state.solutions = []
        conn = sqlite3.connect(DB_PATH)
        boxes = pd.read_sql("SELECT * FROM boxes", conn)
        conn.close()

        product_dims = [l, b, h]
        margins = [margin_l, margin_b, margin_h]
        limits = (max_rijen, max_kolommen, max_lagen)

        results = []
        for _, box in boxes.iterrows():
            box_id = box["id"]
            box_dims = (box["binnen_l"], box["binnen_b"], box["binnen_h"])
            box_rotaties = generate_rotations(box_dims)
            product_rotaties = generate_rotations(product_dims)

            for p_rot in product_rotaties:
                for b_rot in box_rotaties:
                    fit = calculate_fit(
                        {"binnen_l": b_rot[0], "binnen_b": b_rot[1], "binnen_h": b_rot[2]},
                        p_rot, margins, limits
                    )
                    if fit:
                        results.append({
                            "Inhoud": product_ref,
                            "OmverpakkingID": box_id,
                            "Binnenafmetingen": f"{b_rot[0]}x{b_rot[1]}x{b_rot[2]}",
                            "Rijen": fit["rijen"],
                            "Kolommen": fit["kolommen"],
                            "Lagen": fit["lagen"],
                            "Totaal stuks": fit["totaal_stuks"],
                            "Pallethoogte (mm)": f"{fit['lagen'] * b_rot[2] + 144:.0f}",
                            "Volume-efficiëntie": f"{fit['volume_eff']}%",
                            "Favoriet": False,
                            "Visualisatie": False
                        })

        if results:
            st.success(f"{len(results)} oplossingen gevonden.")
            df = pd.DataFrame(results)
            st.session_state.solutions = df
            add_to_undo_stack(df)
        else:
            st.warning("Geen geldige verpakkingsoplossingen gevonden.")

    if "solutions" in st.session_state and len(st.session_state.solutions) > 0:
        df = st.session_state.solutions.copy()
        selected = st.radio("Selecteer een oplossing voor actie", df.index, horizontal=True)
        actie_col1, actie_col2, actie_col3 = st.columns(3)
        with actie_col1:
            if st.button("✅ Markeer als favoriet"):
                st.session_state.solutions.at[selected, "Favoriet"] = True
                add_to_undo_stack(st.session_state.solutions)
        with actie_col2:
            if st.button("📊 Toon visualisatie"):
                selection = df.loc[selected]
                render_3d_visualisatie(selection)
        with actie_col3:
            if st.button("↩ Undo laatste actie"):
                from modules.utils import undo_last_action
                undo_last_action()
        st.dataframe(st.session_state.solutions)
