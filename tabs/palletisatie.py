"""
==================================================================================
Tab 3 – Palletisatie
==================================================================================
Toont hoe een geselecteerde doosconfiguratie op een pallet kan worden gestapeld.
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "dozen_db.sqlite")

PALLET_L = 1200
PALLET_B = 800
PALLET_H = 144  # standaard europallet

def render():
    st.header("🧱 Palletisatie")

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM saved_solutions", conn)
        conn.close()
    except Exception as e:
        st.error(f"Fout bij laden van oplossingen: {e}")
        return

    if df.empty:
        st.info("Nog geen oplossingen beschikbaar.")
        return

    selected_index = st.radio("Selecteer een oplossing voor palletisatie:", df.index)
    row = df.loc[selected_index]

    try:
        box_L, box_B, box_H = map(float, row["box_dim"].split("x"))
    except:
        st.error("Kan doosafmetingen niet parsen.")
        return

    try:
        count_L = int(PALLET_L // box_L)
        count_B = int(PALLET_B // box_B)
        max_layers = int((1600 - PALLET_H) // box_H)
        total = count_L * count_B * max_layers
    except:
        st.error("Fout bij stapelberekening.")
        return

    fig = go.Figure()
    colors = ["red", "green", "blue", "orange", "purple", "cyan", "magenta"]

    for layer in range(max_layers):
        for i in range(count_L):
            for j in range(count_B):
                x0 = i * box_L
                y0 = j * box_B
                z0 = layer * box_H
                color = colors[layer % len(colors)]

                fig.add_trace(go.Mesh3d(
                    x=[x0, x0+box_L, x0+box_L, x0, x0, x0+box_L, x0+box_L, x0],
                    y=[y0, y0, y0+box_B, y0+box_B, y0, y0, y0+box_B, y0+box_B],
                    z=[z0, z0, z0, z0, z0+box_H, z0+box_H, z0+box_H, z0+box_H],
                    color=color,
                    opacity=0.5,
                    showscale=False
                ))

    fig.update_layout(
        scene=dict(
            xaxis_title="Lengte (mm)",
            yaxis_title="Breedte (mm)",
            zaxis_title="Hoogte (mm)"
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)
