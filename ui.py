"""
Pack Optimizer App - Streamlit

Beschrijving:
Deze applicatie optimaliseert verpakkingen door te berekenen hoe een product (in 6 mogelijke oriëntaties)
in verschillende omdozen past. De gebruiker kan marges, dooslimieten en productdimensies instellen.
De simulaties tonen hoeveel producten per doos mogelijk zijn op basis van opgegeven limieten.

Belangrijke Functionaliteiten:
- Rotatie-simulatie: 6 rotaties van elk product worden getest in elke doos
- Marges: gebruikers kunnen afzonderlijk marges per richting instellen (L/B/H)
- Limieten: optionele beperking op max. rijen, kolommen en lagen per doos
- Database: dozen worden geladen vanuit een lokale SQLite database
- UI: Streamlit-applicatie met tabbladen en intuïtieve invoer

Samenwerking:
Deze code is geschreven voor iteratieve samenwerking met de GPT "Python & Streamlit Expert".
Bij het opstarten van een nieuwe sessie, kan deze uitleg als context dienen om direct verder te bouwen
op de bestaande architectuur zonder herhaling van vereisten.
"""

import streamlit as st
from data_manager import init_database, get_all_boxes
from optimizer import simulate_product_in_boxes
import pandas as pd
from math import prod

# Hoofdinterface voor de app
def main_ui():
    st.title("📦 Pack Optimizer")

    # Tabs voor navigatie door de app
    tab1, tab2, tab3 = st.tabs([
        "Product Invoer & Simulatie",
        "Favorieten & Export",
        "Palletisatie"
    ])

    with tab1:
        st.subheader("1️⃣ Voer een product in")

        # Formulier voor producteigenschappen + simulatie
        with st.form("product_form"):
            product_ref = st.text_input("Product Referentie", "")
            # Afmetingen van het product
            col1, col2, col3 = st.columns(3)
            length = col1.number_input("Lengte (mm)", min_value=1.0)
            width = col2.number_input("Breedte (mm)", min_value=1.0)
            height = col3.number_input("Hoogte (mm)", min_value=1.0)

            # Marges in de doos
            col4, col5, col6 = st.columns(3)
            margin_l = col4.number_input("Marge lengte (mm)", min_value=0.0, value=0.0)
            margin_w = col5.number_input("Marge breedte (mm)", min_value=0.0, value=0.0)
            margin_h = col6.number_input("Marge hoogte (mm)", min_value=0.0, value=0.0)

            # Wanddikte (nog niet actief gebruikt)
            thickness = st.number_input("Dikte van omverpakking (mm)", min_value=0.0, value=3.0)

            # Beperkingen op rijen/kolommen/lagen
            st.markdown("### Limieten (optioneel)")
            col7, col8, col9 = st.columns(3)
            lim_rows = col7.number_input("Max. aantal rijen (langs lengte)", min_value=1, value=100)
            lim_cols = col8.number_input("Max. aantal kolommen (langs breedte)", min_value=1, value=100)
            lim_layers = col9.number_input("Max. aantal lagen (hoogte)", min_value=1, value=100)

            submitted = st.form_submit_button("Simuleer")

        if submitted:
            # Gebruikersinput verzamelen
            product = {"length": length, "width": width, "height": height}
            margins = {
                "margin_length": margin_l,
                "margin_width": margin_w,
                "margin_height": margin_h
            }
            limits = {
                "max_rows": lim_rows,
                "max_cols": lim_cols,
                "max_layers": lim_layers
            }

            # Laad omdozen uit de database
            boxes_df = get_all_boxes()
            boxes = boxes_df.to_dict(orient="records")

            # Simuleer alle rotaties en beperkingen
            results = simulate_product_in_boxes(product, margins, boxes, limits)

            if results:
                st.success(f"Gevonden {len(results)} mogelijke plaatsingen in omdozen.")
                result_df = pd.DataFrame([{
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

                # Selecteer oplossing voor visualisatie
                selected_idx = st.radio('📊 Selecteer een oplossing om te visualiseren', result_df.index.tolist())
                selected_row = result_df.loc[selected_idx]

                # Visualisatie in Plotly
                import plotly.graph_objects as go

                box_l, box_w, box_h = selected_row['box_inner']
                prod_l, prod_w, prod_h = selected_row['product_dims']
                rows, cols, layers = selected_row['Rijen'], selected_row['Kolommen'], selected_row['Lagen']

                fig = go.Figure()

                # Voeg alle producten toe als blokken
                for z in range(layers):
                    for y in range(cols):
                        for x in range(rows):
                            fig.add_trace(go.Mesh3d(
                                x=[x*prod_l, x*prod_l + prod_l, x*prod_l + prod_l, x*prod_l, x*prod_l, x*prod_l + prod_l, x*prod_l + prod_l, x*prod_l],
                                y=[y*prod_w, y*prod_w, y*prod_w + prod_w, y*prod_w + prod_w, y*prod_w, y*prod_w, y*prod_w + prod_w, y*prod_w + prod_w],
                                z=[z*prod_h, z*prod_h, z*prod_h, z*prod_h, z*prod_h + prod_h, z*prod_h + prod_h, z*prod_h + prod_h, z*prod_h + prod_h],
                                opacity=0.85,
                                color='skyblue',
                                showscale=False
                            ))

                # Omdoos als transparant wireframe
                fig.add_trace(go.Mesh3d(
                    x=[0, box_l, box_l, 0, 0, box_l, box_l, 0],
                    y=[0, 0, box_w, box_w, 0, 0, box_w, box_w],
                    z=[0, 0, 0, 0, box_h, box_h, box_h, box_h],
                    opacity=0.1,
                    color='gray',
                    showscale=False
                ))

                fig.update_layout(scene=dict(
                    xaxis_title='L',
                    yaxis_title='B',
                    zaxis_title='H',
                    aspectmode='data'),
                    title='3D Visualisatie van Producten in Omdoos')

                st.plotly_chart(fig, use_container_width=True)

                # Checkbox per rij via expander
                st.markdown("### ✅ Selecteer favorieten")
                selections = []
                for i, row in result_df.iterrows():
                    with st.expander(f"{row['OmverpakkingID']} — {row['Totaal stuks']} stuks"):
                        st.write(row.drop(["box_inner", "product_dims"]))
                        if st.checkbox("Toevoegen aan favorieten", key=f"fav_{i}"):
                            selections.append(row.to_dict())


                if st.button("➕ Voeg geselecteerde favorieten toe"):
                    st.success(f"{len(selections)} favoriet(en) toegevoegd.")


                if st.button("➕ Voeg geselecteerde favorieten toe"):
                    selected = edited_df[edited_df["Favoriet"] == True].drop(columns=["Favoriet"])
                    st.success(f"{len(selected)} favoriet(en) toegevoegd.")

                # Checkbox selectie van favorieten
                selected_indices = st.multiselect(
                    '✅ Selecteer oplossingen om op te slaan als favoriet',
                    options=result_df.index.tolist(),
                    format_func=lambda i: f"{result_df.loc[i, 'OmverpakkingID']} - {result_df.loc[i, 'Totaal stuks']} stuks"
                )
                if st.button('➕ Opslaan als favoriet'):
                    for i in selected_indices:
                    st.success(f"{len(selected_indices)} oplossing(en) toegevoegd aan favorieten.")
            else:
                st.warning("Geen enkele geldige plaatsing gevonden voor dit product met deze marges en limieten.")

    with tab3:
        st.subheader("3️⃣ Palletisatie Visualisatie")
        st.info("Selecteer eerst een oplossing.")

    # Sidebar toont extra tools zoals database
    st.sidebar.subheader("📂 Omdozen Database")
    if st.sidebar.button("Toon omdozen"):
        df = get_all_boxes()
        st.sidebar.dataframe(df)