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
Pack Optimizer App - Data Manager

Deze module beheert het laden van dozeninformatie vanuit een lokale SQLite database.
Sinds update juni 2025 gaan we ervan uit dat de afmetingen in de database de **netto binnenafmetingen** zijn.
De wanddikte wordt enkel als metadata opgeslagen (geen berekening meer nodig).

Database-structuur:
- id: unieke referentie van de doos
- length, width, height: netto binnenafmetingen in mm
- thickness: wanddikte (optioneel, voor visuele doeleinden)
- stock: aantal stuks beschikbaar
- description, extra: metadata
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "omverpakkingen.db"

def get_all_boxes():
    "Haalt alle omdozen op uit de SQLite database als pandas DataFrame."
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM boxes", conn)
    conn.close()
    return df