# ui/tabs/tab_input.py
import streamlit as st
from utils.scoring import compute_score
from utils.generator import generate_solutions
from utils.visuals import show_solution_3d

def tab_input(boxes_df):
    st.header("🔍 Invoer van product + configuratie")

    with st.expander(":gear: Invoer parameters", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            l = st.number_input("Lengte product (mm)", min_value=1, value=100)
            margin_l = st.number_input("Marge lengte (mm)", min_value=0, value=5)
            pallet_l = st.number_input("Lengte pallet (mm)", min_value=1, value=1200)
        with col2:
            b = st.number_input("Breedte product (mm)", min_value=1, value=80)
            margin_b = st.number_input("Marge breedte (mm)", min_value=0, value=5)
            pallet_b = st.number_input("Breedte pallet (mm)", min_value=1, value=800)
        with col3:
            h = st.number_input("Hoogte product (mm)", min_value=1, value=60)
            margin_h = st.number_input("Marge hoogte (mm)", min_value=0, value=5)
            pallet_h = st.number_input("Maximale pallethoogte (mm)", min_value=1, value=1600)

        wall = st.number_input("Dikte omverpakking (mm)", min_value=0, value=3)
        weight_per_item = st.number_input("Gewicht per stuk (kg)", min_value=0.0, value=0.5)
        colli_target = st.number_input("Gewenst aantal colli", min_value=1, value=100)
        tolerance = st.slider("Tolerantie op colli (%)", 0, 100, 10)

    with st.expander("🔎 Filters", expanded=False):
        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            min_stock = st.number_input("Minimale stock", min_value=0, value=0, step=10)
        with colf2:
            max_length = st.number_input("Max lengte doos (mm)", min_value=0, value=2000)
            max_width = st.number_input("Max breedte doos (mm)", min_value=0, value=1200)
        with colf3:
            max_height = st.number_input("Max hoogte doos (mm)", min_value=0, value=1200)
            max_weight = st.number_input("Max totaalgewicht doos (kg)", min_value=0.0, value=20.0)

    with st.expander("⚖️ Score-instellingen", expanded=False):
        sw = st.session_state.score_weights
        colw1, colw2 = st.columns(2)
        with colw1:
            sw['fill'] = st.slider("Doosvulling (volume efficiëntie)", 0, 100, sw['fill'])
            sw['pallet'] = st.slider("Pallet efficiëntie", 0, 100, sw['pallet'])
            sw['units'] = st.slider("Efficiëntie per colli", 0, 100, sw['units'])
        with colw2:
            sw['stock'] = st.slider("Voorrangsgewicht bij stock", 0, 100, sw['stock'])
            sw['rotation'] = st.slider("Rotatiecomplexiteit (straf)", 0, 100, sw['rotation'])

        total = sw['fill'] + sw['pallet'] + sw['units'] + sw['stock'] + sw['rotation']
        st.markdown(f"**Totaal: {total}/100 punten**")

    st.divider()
    st.subheader(":card_file_box: Genereer oplossingen")

    if st.button("Bereken oplossingen"):
        solutions = generate_solutions(
            l, b, h, weight_per_item, boxes_df,
            margin_l, margin_b, margin_h, wall,
            pallet_l, pallet_b, pallet_h,
            min_stock, max_length, max_width, max_height, max_weight,
            colli_target, tolerance
        )
        scored = compute_score(solutions, st.session_state.score_weights)
        st.session_state['current_solutions'] = scored

    if 'current_solutions' in st.session_state:
        from utils.table import show_solution_table
        show_solution_table(st.session_state['current_solutions'])

        if st.session_state.visual_solution:
            st.plotly_chart(show_solution_3d(st.session_state.visual_solution), use_container_width=True)
