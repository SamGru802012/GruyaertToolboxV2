
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
    st.title("📦 Verpakkingsoptimalisatie")

    st.markdown("Voer hieronder de afmetingen van het product in en selecteer marges en wanddikte:")

    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            ref = st.text_input("Productreferentie", "PROD001")
            l = st.number_input("Lengte product (mm)", min_value=1, value=100)
            b = st.number_input("Breedte product (mm)", min_value=1, value=60)
            h = st.number_input("Hoogte product (mm)", min_value=1, value=40)
        with col2:
            margin_x = st.number_input("Marge lengte (mm)", value=0)
            margin_y = st.number_input("Marge breedte (mm)", value=0)
            margin_z = st.number_input("Marge hoogte (mm)", value=0)
            wall = st.number_input("Wanddikte doos (mm)", value=3)

        submitted = st.form_submit_button("Genereer verpakkingsopties")

    if submitted:
        boxes_df = load_boxes()
        if boxes_df.empty:
            st.error("⚠️ Geen omdozen gevonden in de database.")
            return

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

        if not all_results:
            st.warning("❌ Geen geldige verpakkingsopties gevonden voor de ingegeven parameters.")
            return

        df = pd.DataFrame(all_results)
        df["pallet_height"] = df["layers"] * (h + 2 * wall)
        df["volume_efficiency"] = df["efficiency"]

        st.markdown("### 📊 Overzicht van mogelijke configuraties")
        st.dataframe(df, use_container_width=True)

        indices = df.index.tolist()
        selected = st.radio("🔘 Selecteer een oplossing voor 3D visualisatie", indices, horizontal=True)
        favorites = st.multiselect("⭐ Selecteer favoriete oplossingen", indices, default=[])

        if selected is not None:
            solution = df.loc[selected]
            st.markdown(f"**Visualisatie voor doos:** `{solution['box_ref']}` met rotatie `{solution['rotation']}`")
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
