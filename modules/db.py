import streamlit as st
import pandas as pd
from modules.visualizer import render_3d_visualisatie
from modules.utils import add_to_undo_stack, undo_last_action
import uuid
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

EXPORT_PATH = "data/exports"

def render_favorites_tab():
    st.markdown("### ⭐ Geselecteerde oplossingen")
    df = st.session_state.get("solutions", pd.DataFrame())
    favorites = df[df["Favoriet"] == True].copy()

    if favorites.empty:
        st.info("Geen favorieten gemarkeerd.")
        return

    # Zoek- en filtervelden
    zoek = st.text_input("🔍 Zoek op productreferentie")
    if zoek:
        favorites = favorites[favorites["Inhoud"].str.contains(zoek, case=False)]

    # Sortering op volume-efficiëntie
    favorites = favorites.sort_values(by="Volume-efficiëntie", ascending=False)

    # Tabel tonen
    selected = st.radio("Selecteer een favoriet voor actie", favorites.index, horizontal=True)
    st.dataframe(favorites)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Visualiseer selectie"):
            render_3d_visualisatie(favorites.loc[selected])
    with col2:
        if st.button("📄 Exporteer als CSV"):
            csv_file = favorites.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv_file, file_name="favorieten.csv", mime="text/csv")
    with col3:
        if st.button("🗑 Verwijder selectie"):
            df.at[selected, "Favoriet"] = False
            st.session_state.solutions = df
            add_to_undo_stack(df)
            st.success("Favoriet verwijderd.")

    st.markdown("### 📑 Exporteer als PDF inclusief visualisatie")
    if st.button("Genereer PDF"):
        record = favorites.loc[selected]
        fig_name = f"pdfsnap_{uuid.uuid4().hex[:8]}.png"
        fig_path = os.path.join(EXPORT_PATH, fig_name)

        from modules.visualizer import render_3d_visualisatie
        import plotly.io as pio
        import plotly.graph_objects as go

        # Herbouw visualisatie voor snapshot
        dims = [float(x) for x in record["Binnenafmetingen"].split("x")]
        l, b, h = dims
        rijen = record["Rijen"]
        kolommen = record["Kolommen"]
        lagen = record["Lagen"]

        fig = go.Figure()
        from modules.visualizer import draw_box
        draw_box(fig, 0, 0, 0, l, b, h, "lightgray", "Doos")
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
        pio.write_image(fig, fig_path, format="png", width=800, height=600)

        # PDF genereren
        pdf_name = f"favoriet_{uuid.uuid4().hex[:8]}.pdf"
        pdf_path = os.path.join(EXPORT_PATH, pdf_name)
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.drawString(50, 800, f"Favoriet Oplossing - {record['Inhoud']}")
        c.drawString(50, 780, f"Omverpakking ID: {record['OmverpakkingID']}")
        c.drawString(50, 760, f"Afmetingen: {record['Binnenafmetingen']}")
        c.drawString(50, 740, f"Stuks: {record['Totaal stuks']} | Volume-efficiëntie: {record['Volume-efficiëntie']}")
        c.drawImage(ImageReader(fig_path), 50, 400, width=500, height=350)
        c.showPage()
        c.save()

        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=pdf_name, mime="application/pdf")

    st.markdown("### ↩ Undo laatste verwijdering")
    if st.button("Undo"):
        undo_last_action()
