import streamlit as st
import pandas as pd
from optimizer import simulate_packings
from data_manager import get_all_boxes
from math import prod
import plotly.graph_objects as go

def main_ui():
    st.set_page_config(page_title="Pack Optimizer", layout="wide")
    st.title("📦 Pack Optimizer")

    tab1, tab2, tab3 = st.tabs(["1️⃣ Simulatie", "2️⃣ Placeholder", "3️⃣ Placeholder"])

    with tab1:
        st.subheader("📏 Productgegevens")
        with st.form("product_form"):
            product_ref = st.text_input("Product Referentie", "")
            l = st.number_input("Lengte (mm)", min_value=1)
            b = st.number_input("Breedte (mm)", min_value=1)
            h = st.number_input("Hoogte (mm)", min_value=1)

            st.subheader("📐 Marges (ruimte tussen product en doos)")
            margin_l = st.number_input("Marge Lengte (mm)", min_value=0, value=0)
            margin_b = st.number_input("Marge Breedte (mm)", min_value=0, value=0)
            margin_h = st.number_input("Marge Hoogte (mm)", min_value=0, value=0)

            st.subheader("🔢 Beperkingen op layout (optioneel)")
            max_r = st.number_input("Max Rijen", min_value=0, value=0)
            max_k = st.number_input("Max Kolommen", min_value=0, value=0)
            max_lay = st.number_input("Max Lagen", min_value=0, value=0)

            submitted = st.form_submit_button("🚀 Start Simulatie")

        if submitted:
            product_dims = (l + margin_l, b + margin_b, h + margin_h)
            boxes = get_all_boxes()
            results = simulate_packings(product_dims, boxes, max_r, max_k, max_lay)

            if not results:
                st.warning("Geen geldige combinaties gevonden.")
                return

            df = pd.DataFrame([{
                "OmverpakkingID": r["box_id"],
                "Binnenafm. (LxBxH)": "×".join(map(str, r["box_inner"])),
                "Rijen": r["fit"][0],
                "Kolommen": r["fit"][1],
                "Lagen": r["fit"][2],
                "Totaal stuks": r["total_products"],
                "Pallethoogte (mm)": int(r["product_dims"][2] * r["fit"][2]),
                "Volume-efficiëntie (%)": round((prod(r["product_dims"]) * r["total_products"]) / (prod(r["box_inner"]) + 1e-6) * 100, 1),
                "box_inner": r["box_inner"],
                "product_dims": r["product_dims"]
            } for r in results]).sort_values("Volume-efficiëntie (%)", ascending=False).reset_index(drop=True)

            st.dataframe(df.drop(columns=["box_inner", "product_dims"]))
            selected_idx = st.radio("📊 Selecteer een oplossing voor visualisatie", df.index.tolist())
            r = df.loc[selected_idx]

            # Plotly visualisatie
            L, B, H = r["product_dims"]
            rows, cols, layers = r["Rijen"], r["Kolommen"], r["Lagen"]
            box_L, box_B, box_H = r["box_inner"]

            fig = go.Figure()
            for z in range(layers):
                for y in range(cols):
                    for x in range(rows):
                        fig.add_trace(go.Mesh3d(
                            x=[x*L, x*L+L, x*L+L, x*L, x*L, x*L+L, x*L+L, x*L],
                            y=[y*B, y*B, y*B+B, y*B+B, y*B, y*B, y*B+B, y*B+B],
                            z=[z*H, z*H, z*H, z*H, z*H+H, z*H+H, z*H+H, z*H+H],
                            opacity=0.85,
                            color='skyblue',
                            showscale=False
                        ))
            fig.add_trace(go.Mesh3d(
                x=[0, box_L, box_L, 0, 0, box_L, box_L, 0],
                y=[0, 0, box_B, box_B, 0, 0, box_B, box_B],
                z=[0, 0, 0, 0, box_H, box_H, box_H, box_H],
                opacity=0.1,
                color='gray',
                showscale=False
            ))
            fig.update_layout(scene=dict(aspectmode='data'), title='3D Visualisatie')
            st.plotly_chart(fig, use_container_width=True)