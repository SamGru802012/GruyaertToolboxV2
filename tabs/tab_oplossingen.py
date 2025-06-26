"""
import os
os.makedirs("data", exist_ok=True)
==================================================================================
Tab 2 – Gekozen Oplossingen
==================================================================================
Toont eerder opgeslagen verpakkingsoplossingen met mogelijkheid tot visualisatie
en export naar CSV. Eén oplossing kan geselecteerd worden voor 3D-weergave.
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
import itertools

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "dozen_db.sqlite")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def load_solutions():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM saved_solutions", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()
def visualize_solution(row):
    if L*B*H == 0 or pl*pw*ph == 0:
        st.warning("Ongeldige afmetingen voor visualisatie.")
        return
    if L*B*H == 0 or pl*pw*ph == 0:
        return
    L, B, H = safe_parse_dims(row.get("box_dim", "0x0x0"))
    pl, pw, ph = safe_parse_dims(row.get("product_rotation", "0x0x0"))
    rows, cols, layers = row["rows"], row["columns"], row["layers"]

    fig = go.Figure()
    color_iter = itertools.cycle(px.colors.qualitative.Alphabet)

    for z in range(layers):
        for y in range(cols):
            for x in range(rows):
                cx, cy, cz = x * pl, y * pw, z * ph
                fig.add_trace(go.Mesh3d(
                    x=[cx, cx+pl, cx+pl, cx, cx, cx+pl, cx+pl, cx],
                    y=[cy, cy, cy+pw, cy+pw, cy, cy, cy+pw, cy+pw],
                    z=[cz, cz, cz, cz, cz+ph, cz+ph, cz+ph, cz+ph],
                    color=next(color_iter),
                    opacity=1.0,
                    name=f"Item {x}-{y}-{z}"
                ))

    # Transparante doos
    fig.add_trace(go.Mesh3d(
        x=[0, L, L, 0, 0, L, L, 0],
        y=[0, 0, B, B, 0, 0, B, B],
        z=[0, 0, 0, 0, H, H, H, H],
        opacity=0.1,
        color='gray',
        name='Omdoos'
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
def tab_oplossingen():
    st.subheader("📋 Opgeslagen oplossingen")

    df = load_solutions()
    if df.empty:
        st.info("Nog geen oplossingen opgeslagen.")
        return

    st.dataframe(df.drop(columns=["id"]), use_container_width=True)

    selected = st.radio("Selecteer een oplossing voor visualisatie",
                        options=df.index,
                        format_func=lambda i: f"{df.loc[i, 'product_ref']} - doos {df.loc[i, 'box_id']}")

    row = df.loc[selected]
    visualize_solution(row)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📤 Download als CSV", data=csv, file_name="oplossingen.csv", mime="text/csv")
