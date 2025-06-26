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
                    "Omdoos ID": r["box_id"],
                    "Rotatie (LxBxH)": "×".join(map(str, r["rotation"])),
                    "Rijen × Kolommen × Lagen": "×".join(map(str, r["fit"])),
                    "Totaal aantal producten": r["total_products"]
                } for r in results])
                st.dataframe(result_df)
            else:
                st.warning("Geen enkele geldige plaatsing gevonden voor dit product met deze marges en limieten.")

    with tab2:
        st.subheader("2️⃣ Favoriete oplossingen")
        st.info("Nog geen favorieten geselecteerd.")

    with tab3:
        st.subheader("3️⃣ Palletisatie Visualisatie")
        st.info("Selecteer eerst een oplossing.")

    # Sidebar toont extra tools zoals database
    st.sidebar.subheader("📂 Omdozen Database")
    if st.sidebar.button("Toon omdozen"):
        df = get_all_boxes()
        st.sidebar.dataframe(df)