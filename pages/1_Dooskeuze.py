
import streamlit as st
import pandas as pd
from core.database import get_connection
from core.visualizer import draw_box

def load_boxes():
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM boxes", conn)

def simulate_solution(box):
    # Simuleer dummy oplossing voor demo
    return pd.DataFrame([{
        "product_ref": "DEMO123",
        "product_rotation": "90°",
        "box_id": box["id"],
        "box_dim": f"{box['inner_length']}x{box['inner_width']}x{box['inner_height']}",
        "rows": 2,
        "columns": 2,
        "layers": 3,
        "total_units": 12,
        "pallet_height": box["inner_height"] * 3,
        "efficiency": 78.5
    }])

def render_dooskeuze():
    st.header("📦 Dooskeuze & Simulatie")
    boxes = load_boxes()

    if boxes.empty:
        st.warning("Geen dozen beschikbaar in de database.")
        return

    box_selected = st.selectbox("Kies een doos", boxes["id"].tolist())
    box = boxes[boxes["id"] == box_selected].iloc[0]

    st.markdown(f"**Afmetingen (binnen):** {box['inner_length']} x {box['inner_width']} x {box['inner_height']} mm")

    fig = draw_box(box["inner_length"], box["inner_width"], box["inner_height"])
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🔍 Simuleer oplossing"):
        results = simulate_solution(box)
        st.session_state["laatste_resultaten"] = results
        st.success("Simulatie voltooid. Ga naar 'Opgeslagen' om op te slaan.")
        st.dataframe(results, use_container_width=True)
