import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
import uuid
import os

EXPORT_PATH = "data/exports"

def draw_box(ax, x0, y0, z0, dx, dy, dz, color, name=""):
    """Voegt een transparante box toe aan de plot"""
    x = [x0, x0+dx, x0+dx, x0, x0, x0+dx, x0+dx, x0]
    y = [y0, y0, y0+dy, y0+dy, y0, y0, y0+dy, y0+dy]
    z = [z0, z0, z0, z0, z0+dz, z0+dz, z0+dz, z0+dz]

    i = [0, 0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 7]
    j = [1, 2, 3, 5, 6, 6, 7, 7, 5, 6, 7, 4]
    k = [2, 3, 0, 6, 7, 3, 0, 4, 6, 7, 4, 5]

    ax.add_trace(go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        opacity=0.3,
        color=color,
        name=name,
        showscale=False
    ))

def render_3d_visualisatie(selection):
    """Render de 3D-stack van producten in de doos"""
    dims = [float(x) for x in selection["Binnenafmetingen"].split("x")]
    l, b, h = dims
    rijen = selection["Rijen"]
    kolommen = selection["Kolommen"]
    lagen = selection["Lagen"]

    fig = go.Figure()

    # Transparante doos
    draw_box(fig, 0, 0, 0, l, b, h, "lightgray", "Doos")

    # Productblokken per laag
    kleuren = ["red", "green", "blue", "orange", "purple", "cyan"]
    for z in range(lagen):
        for y in range(kolommen):
            for x in range(rijen):
                px = l / rijen * x
                py = b / kolommen * y
                pz = h / lagen * z
                dx = l / rijen
                dy = b / kolommen
                dz = h / lagen
                kleur = kleuren[z % len(kleuren)]
                draw_box(fig, px, py, pz, dx, dy, dz, kleur, f"Product {z+1}")

    fig.update_layout(
        scene=dict(
            xaxis_title="L",
            yaxis_title="B",
            zaxis_title="H",
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        title="3D Visualisatie van Doosinhoud"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Snapshot download
    if st.button("📸 Snapshot downloaden als PNG"):
        snapshot_name = f"snapshot_{uuid.uuid4().hex[:8]}.png"
        snapshot_path = os.path.join(EXPORT_PATH, snapshot_name)
        pio.write_image(fig, snapshot_path, format="png", scale=2, width=800, height=600)
        with open(snapshot_path, "rb") as f:
            st.download_button("Download PNG", f, file_name=snapshot_name, mime="image/png")

def render_pallet_tab():
    st.markdown("### 🧱 Palletisatie Simulatie")

    if "solutions" not in st.session_state or st.session_state.solutions.empty:
        st.warning("Geen berekende oplossingen beschikbaar.")
        return

    df = st.session_state.solutions
    favorieten = df[df["Favoriet"] == True]
    if favorieten.empty:
        st.info("Geen favorieten gemarkeerd voor stapeling.")
        return

    selectie = st.selectbox("Selecteer een oplossing voor palletisatie", favorieten.index)
    record = favorieten.loc[selectie]

    pallet_l = st.number_input("Pallet lengte (mm)", value=1200.0)
    pallet_b = st.number_input("Pallet breedte (mm)", value=800.0)
    pallet_h = st.number_input("Maximale pallet hoogte (mm)", value=1500.0)
    tolerantie = st.number_input("Hoogtetolerantie (mm)", value=10.0)

    doos_afm = [float(x) for x in record["Binnenafmetingen"].split("x")]
    doos_l, doos_b, doos_h = doos_afm
    pallet_basis_hoogte = 144

    max_x = int(pallet_l // doos_l)
    max_y = int(pallet_b // doos_b)
    max_layers = int((pallet_h - pallet_basis_hoogte + tolerantie) // doos_h)
    totaal_dozen = max_x * max_y * max_layers
    pallet_hoogte = pallet_basis_hoogte + max_layers * doos_h

    st.success(f"Totaal {totaal_dozen} dozen op de pallet ({max_x} x {max_y} x {max_layers})")
    if pallet_hoogte > pallet_h + tolerantie:
        st.warning(f"Overschrijding van max hoogte: {pallet_hoogte} mm > {pallet_h + tolerantie} mm")

    # 3D render pallet
    fig = go.Figure()
    from modules.visualizer import draw_box
    kleuren = ["red", "green", "blue", "orange"]

    for z in range(max_layers):
        for y in range(max_y):
            for x in range(max_x):
                dx = doos_l
                dy = doos_b
                dz = doos_h
                px = x * dx
                py = y * dy
                pz = pallet_basis_hoogte + z * dz
                kleur = kleuren[z % len(kleuren)]
                draw_box(fig, px, py, pz, dx, dy, dz, kleur)

    draw_box(fig, 0, 0, 0, pallet_l, pallet_b, pallet_basis_hoogte, "gray", "Pallet")
    fig.update_layout(
        scene=dict(
            xaxis_title="L",
            yaxis_title="B",
            zaxis_title="H",
            aspectmode="data"
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        title="Palletisatie Visualisatie"
    )
    st.plotly_chart(fig, use_container_width=True)

    if st.button("📸 Download pallet snapshot"):
        from plotly.io import write_image
        snapshot_name = f"pallet_{uuid.uuid4().hex[:8]}.png"
        snapshot_path = os.path.join(EXPORT_PATH, snapshot_name)
        write_image(fig, snapshot_path, format="png", width=800, height=600)
        with open(snapshot_path, "rb") as f:
            st.download_button("Download PNG", f, file_name=snapshot_name, mime="image/png")

    if st.button("↩ Undo laatste actie"):
        from modules.utils import undo_last_action
        undo_last_action()
