
import streamlit as st
import pandas as pd
import sqlite3
from core.optimizer import PackingOptimizer
from core.visualizer import visualize_packing

DB_PATH = "packing_app.db"

def load_boxes():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM boxes", conn)
    return df

def dooskeuze_tab():
    st.title("📐 Productinvoer & Doosanalyse")

    with st.form("product_form"):
        col1, col2 = st.columns(2)
        with col1:
            ref = st.text_input("Productreferentie", "PROD001")
            l = st.number_input("Lengte (mm)", min_value=1, value=100)
            b = st.number_input("Breedte (mm)", min_value=1, value=60)
            h = st.number_input("Hoogte (mm)", min_value=1, value=40)

        with col2:
            margin_x = st.number_input("Marge lengte (mm)", value=0)
            margin_y = st.number_input("Marge breedte (mm)", value=0)
            margin_z = st.number_input("Marge hoogte (mm)", value=0)
            wall = st.number_input("Wanddikte (mm)", value=3)

        submitted = st.form_submit_button("Genereer oplossingen")

    if submitted:
        boxes_df = load_boxes()
        all_results = []
        for _, row in boxes_df.iterrows():
            optimizer = PackingOptimizer(
                product_dim=(l, b, h),
                box_dim=(row.inner_length, row.inner_width, row.inner_height),
                margin=(margin_x, margin_y, margin_z),
                wall=wall,
                product_ref=ref,
                box_id=row.ref
            )
            results = optimizer.run()
            for r in results:
                r["box_ref"] = row.ref
                r["box_inner"] = f'{row.inner_length}x{row.inner_width}x{row.inner_height}'
            all_results.extend(results)

        if all_results:
            df = pd.DataFrame(all_results)
            df["pallet_height"] = df["layers"] * (h + 2 * wall)
            df["volume_efficiency"] = df["efficiency"]

            st.markdown("### 📊 Resultaten")
            selected = st.radio("Selecteer een oplossing voor visualisatie:", df.index, horizontal=True)
            favorites = st.multiselect("✅ Kies favorieten", df.index, default=[])

            st.dataframe(df)

            if selected is not None:
                solution = df.loc[selected]
                fig = visualize_packing(
                    box_dim=tuple(map(float, solution["box_inner"].split("x"))),
                    product_dim=tuple(map(float, solution["rotation"].split("x"))),
                    rows=int(solution["rows"]),
                    cols=int(solution["columns"]),
                    layers=int(solution["layers"]),
                    margin=(margin_x, margin_y, margin_z),
                    wall=wall
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Geen oplossingen gevonden voor dit product en deze dozen.")
