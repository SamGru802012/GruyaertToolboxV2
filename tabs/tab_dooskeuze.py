"""
==================================================================================
Tab 1 – Dooskeuze
==================================================================================
Genereert alle mogelijke verpakkingscombinaties voor een ingegeven product
- Alle 6 productrotaties worden getest op alle beschikbare dozen
- Resultaten worden weergegeven in een tabel
- Eén oplossing kan visueel worden weergegeven in 3D met plotly
"""

import streamlit as st
import pandas as pd
import sqlite3
import itertools
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

DB_PATH = "data/dozen_db.sqlite"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM boxes", conn)
    conn.close()
    return df

def generate_rotations(l, b, h):
    return set(itertools.permutations([l, b, h]))

def tab_dooskeuze():
    st.subheader("🧮 Doosoptimalisatie")

    with st.form("product_form"):
        l = st.number_input("Productlengte (mm)", min_value=1, value=100)
        b = st.number_input("Productbreedte (mm)", min_value=1, value=50)
        h = st.number_input("Producthoogte (mm)", min_value=1, value=40)
        margin_l = st.number_input("Marge Lengte (mm)", value=5)
        margin_b = st.number_input("Marge Breedte (mm)", value=5)
        margin_h = st.number_input("Marge Hoogte (mm)", value=5)
        submitted = st.form_submit_button("Genereer oplossingen")

    if submitted:
        df_boxes = load_data()
        rotations = generate_rotations(l, b, h)
        results = []

        for _, box in df_boxes.iterrows():
            L, B, H = box['inner_length'], box['inner_width'], box['inner_height']
            wall = box['wall_thickness']
            usable_L = L - 2*wall - 2*margin_l
            usable_B = B - 2*wall - 2*margin_b
            usable_H = H - 2*wall - 2*margin_h

            if usable_L <= 0 or usable_B <= 0 or usable_H <= 0:
                continue

            for rot in rotations:
                pl, pw, ph = rot
                rows = int(usable_L // pl)
                cols = int(usable_B // pw)
                layers = int(usable_H // ph)
                total = rows * cols * layers
                if total == 0:
                    continue
                volume = pl * pw * ph * total
                box_volume = usable_L * usable_B * usable_H
                eff = round((volume / box_volume) * 100, 2)
                results.append({
                    "rotation": f"{pl}x{pw}x{ph}",
                    "box_id": box["id"],
                    "box_dim": f"{L}x{B}x{H}",
                    "rows": rows,
                    "cols": cols,
                    "layers": layers,
                    "total": total,
                    "eff": eff,
                    "rot": (pl, pw, ph),
                    "dim": (L, B, H)
                })

        if not results:
            st.warning("Geen combinaties gevonden.")
            return

        df = pd.DataFrame(results).sort_values("eff", ascending=False)
        selected = st.radio("Selecteer voor visualisatie", options=df.index,
                            format_func=lambda i: f"Doos {df.loc[i, 'box_id']} ({df.loc[i, 'total']} stuks)")

        st.dataframe(df.drop(columns=["rot", "dim"]), use_container_width=True)

        row = df.loc[selected]
        plot_box_with_products(row["rot"], row["dim"], row["rows"], row["cols"], row["layers"])

        # Opslaan knop
        if st.button("💾 Opslaan als oplossing"):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO saved_solutions (
                product_ref, product_rotation, box_id, box_dim,
                rows, columns, layers, total_units, pallet_height, efficiency
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "PROD001", row["rotation"], row["box_id"], row["box_dim"],
                row["rows"], row["cols"], row["layers"], row["total"],
                row["layers"] * int(row["dim"][2]) + 144,
                row["eff"]
            ))
            conn.commit()
            conn.close()
            st.success("Oplossing opgeslagen.")

def plot_box_with_products(rot, dim, rows, cols, layers):
    pl, pw, ph = rot
    L, B, H = dim
    fig = go.Figure()
    color_iter = itertools.cycle(px.colors.qualitative.Alphabet)

    for z in range(layers):
        for y in range(cols):
            for x in range(rows):
                cx, cy, cz = x*pl, y*pw, z*ph
                fig.add_trace(go.Mesh3d(
                    x=[cx, cx+pl, cx+pl, cx, cx, cx+pl, cx+pl, cx],
                    y=[cy, cy, cy+pw, cy+pw, cy, cy, cy+pw, cy+pw],
                    z=[cz, cz, cz, cz, cz+ph, cz+ph, cz+ph, cz+ph],
                    color=next(color_iter),
                    opacity=1.0
                ))
    fig.add_trace(go.Mesh3d(
        x=[0, L, L, 0, 0, L, L, 0],
        y=[0, 0, B, B, 0, 0, B, B],
        z=[0, 0, 0, 0, H, H, H, H],
        opacity=0.1,
        color='gray',
        name='Omdoos'
    ))
    fig.update_layout(scene=dict(
        xaxis_title="L",
        yaxis_title="B",
        zaxis_title="H"
    ))
    st.plotly_chart(fig, use_container_width=True)
