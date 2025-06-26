# utils/data.py
import pandas as pd
import os
import json

JSON_PATH = "utils/boxes.json"
CSV_PATH = "omverpakkingen_geconverteerd.csv"
EXPORT_CSV = "boxes_export.csv"

def load_boxes():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    elif os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        return pd.DataFrame(columns=["Referentie", "Lengte", "Breedte", "Hoogte", "Dikte", "Stock", "Omschrijving", "Extra info"])

def save_boxes(df):
    with open(JSON_PATH, 'w') as f:
        json.dump(df.to_dict(orient='records'), f, indent=2)
    df.to_csv(EXPORT_CSV, index=False)
