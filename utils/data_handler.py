
import json
import pandas as pd

DATA_FILE = "data/omdozen.json"

def load_dozen():
    try:
        with open(DATA_FILE, "r") as f:
            return pd.DataFrame(json.load(f))
    except:
        return pd.DataFrame()

def add_doos(ref, l, b, h, d, s, o):
    df = load_dozen()
    nieuw = {"ref": ref, "dim": [l, b, h], "dikte": d, "stock": s, "omschrijving": o}
    df = df._append(nieuw, ignore_index=True)
    with open(DATA_FILE, "w") as f:
        json.dump(df.to_dict(orient="records"), f)
