"""
import os
from models.init_db import init_db
init_db()
os.makedirs("data", exist_ok=True)
==================================================================================
Tab 3 – Palletisatie
==================================================================================
Simuleert het stapelen van omdozen op een europallet, waarbij de oriëntatie van
de doos wordt geoptimaliseerd voor maximale benutting. 3D-visualisatie inbegrepen.
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
import itertools

DB_PATH = "data/dozen_db.sqlite"

def load_saved_solutions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM saved_solutions", conn)
    conn.close()
    return df

def visualize_pallet(config, pallet_dim=(1200, 800, 1600)):
    fig = go.Figure()
    color_iter = itertools.cycle(px.colors.qualitative.Set3)
    l, w, h = config["orientation"]

    for z in range(config["layers"]):
        for y in range(config["units_per_col"]):
            for x in range(config["units_per_row"]):
                cx, cy, cz = x * l, y * w, z * h
                fig.add_trace(go.Mesh3d(
                    x=[cx, cx+l, cx+l, cx, cx, cx+l, cx+l, cx],
                    y=[cy, cy, cy+w, cy+w, cy, cy, cy+w, cy+w],
                    z=[cz, cz, cz, cz, cz+h, cz+h, cz+h, cz+h],
                    color=next(color_iter),
                    opacity=1.0
                ))

    pallet_L, pallet_W, pallet_H = pallet_dim
    fig.add_trace(go.Mesh3d(
        x=[0, pallet_L, pallet_L, 0, 0, pallet_L, pallet_L, 0],
        y=[0, 0, pallet_W, pallet_W, 0, 0, pallet_W, pallet_W],
        z=[0, 0, 0, 0, 144, 144, 144, 144],
        color='brown',
        opacity=0.4,
        name='Pallet'
    ))

    fig.update_layout(scene=dict(
        xaxis_title="Lengte",
        yaxis_title="Breedte",
        zaxis_title="Hoogte"
    ))
    st.plotly_chart(fig, use_container_width=True)


def safe_parse_dims(dim_str):
    try:
        if not isinstance(dim_str, str):
            return (0.0, 0.0, 0.0)
        parts = str(dim_str).split("x")
        if len(parts) != 3:
            return (0.0, 0.0, 0.0)
        return tuple(map(float, parts))
    except Exception:
        return (0.0, 0.0, 0.0)
def tab_palletisatie():
    st.subheader("🧱 Palletisatie Visualisatie")

    df = load_saved_solutions()
    if df.empty:
        st.info("Geen opgeslagen oplossingen.")
        return

    selected = st.radio("Selecteer oplossing voor stapeling", options=df.index,
                        format_func=lambda i: f"{df.loc[i, 'product_ref']} - doos {df.loc[i, 'box_id']}")
    row = df.loc[selected]

    box_L, box_B, box_H = safe_parse_dims(row.get("box_dim", "0x0x0"))
    box_rotations = set(itertools.permutations([box_L, box_B, box_H]))

    best_config = None
    max_units = 0
    for rot in box_rotations:
        l, w, h = rot
        units_x = int(1200 // l)
        units_y = int(800 // w)
        layers = int(1600 // h)
        total = units_x * units_y * layers
        if total > max_units:
            max_units = total
            best_config = {
                "orientation": rot,
                "units_per_row": units_x,
                "units_per_col": units_y,
                "layers": layers,
                "total_units": total
            }

    if best_config:
        st.markdown(f"**Beste configuratie**: {best_config['total_units']} dozen")
        visualize_pallet(best_config)
