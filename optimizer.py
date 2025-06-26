"""
Pack Optimizer App - Streamlit

Beschrijving:
Deze applicatie optimaliseert verpakkingen door te berekenen hoe een product (in 6 mogelijke oriëntaties)
in verschillende omdozen past. De gebruiker kan marges, dooslimieten en productdimensies instellen.
De simulaties tonen hoeveel producten per doos mogelijk zijn op basis van opgegeven limieten.

Functionaliteiten ✅
--------------------
- ✅ 6 productrotaties per simulatie
- ✅ Per-richting marges (L/B/H)
- ✅ Limieten op rijen / kolommen / lagen
- ✅ SQLite database met binnenafmetingen (geen buitenafmetingen)
- ✅ CSV import verwerkt als netto binnenmaten
- ✅ Resultatentabel in Gruyaert-kolomstructuur
- ✅ Pallethoogte berekend (per oplossing)
- ✅ Product Referentie als input

Nog te implementeren 🟡
------------------------
- ⬜ CRUD voor dozenbeheer in de app
- ⬜ Export naar CSV/PDF van oplossingen
- ⬜ Plotly 3D visualisatie van product in doos
- ⬜ Palletisatie visualisatie (dozen op pallet)
- ⬜ Favorietenbeheer: selecteren + bewaren

Deze commentaar fungeert als context voor verdere ontwikkeling in samenwerking met GPT "Python & Streamlit Expert".
"""

"""
Pack Optimizer App - Streamlit

Beschrijving:
Deze applicatie optimaliseert verpakkingen door te berekenen hoe een product (in 6 mogelijke oriëntaties)
in verschillende omdozen past. De gebruiker kan marges, dooslimieten en productdimensies instellen.
De simulaties tonen hoeveel producten per doos mogelijk zijn op basis van opgegeven limieten.

Belangrijke Functionaliteiten:
- ✅ Rotatie-simulatie: 6 rotaties van elk product worden getest in elke doos
- ✅ Marges: gebruikers kunnen afzonderlijk marges per richting instellen (L/B/H)
- ✅ Limieten: optionele beperking op max. rijen, kolommen en lagen per doos
- ✅ Resultatenweergave: volgens opgegeven voorbeeldkolommen (incl. volume-efficiëntie)
- ✅ Binnenafmetingen: CSV bevat enkel netto binnenmaten; wanddikte is enkel metadata
- ✅ Dozen in SQLite-database, geladen bij opstart
- ❌ CRUD-beheer van dozen in UI
- ❌ Export naar CSV en PDF van geselecteerde resultaten
- ❌ Visualisatie van producten in dozen (Plotly)
- ❌ Palletisatie van dozen en visualisatie per laag
- ❌ Favorietenbeheer (selecteren, bewaren per sessie)

Samenwerking:
Deze code is geschreven voor iteratieve samenwerking met de GPT "Python & Streamlit Expert".
Bij het opstarten van een nieuwe sessie, kan deze uitleg als context dienen om direct verder te bouwen
op de bestaande architectuur zonder herhaling van vereisten.
"""

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

from itertools import permutations
import math

# Genereert 6 unieke rotaties van een product (L, B, H)
def generate_rotations(dimensions):
    return list(set(permutations(dimensions)))

# Berekent het aantal producten dat past in een doos per rotatie met limieten
def calculate_fit(inner_dims, product_dims, limits):
    return tuple(min(math.floor(i / p), lim) for i, p, lim in zip(inner_dims, product_dims, limits))

# Hoofdfunctie: simuleer alle geldige plaatsingen van een product in elke doos
def simulate_product_in_boxes(product, margins, boxes, limits):
    results = []
    product_dims = (product["length"], product["width"], product["height"])
    rotations = generate_rotations(product_dims)

    for box in boxes:
        # Corrigeer binnenmaten op basis van marges
        inner = (
            box["inner_length"] - margins["margin_length"],
            box["inner_width"] - margins["margin_width"],
            box["inner_height"] - margins["margin_height"],
        )

        for rotation in rotations:
            lims = (limits["max_rows"], limits["max_cols"], limits["max_layers"])
            fit = calculate_fit(inner, rotation, lims)
            total = fit[0] * fit[1] * fit[2]
            if total > 0:
                results.append({
                    "box_id": box["id"],
                    "rotation": rotation,
                    "fit": fit,
                    "total_products": total,
                    "box_inner": inner,
                    "product_dims": rotation
                })

    results.sort(key=lambda r: r["total_products"], reverse=True)
    return results