import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "omverpakkingen.db"

def init_database():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database niet gevonden. Zorg dat 'omverpakkingen.db' in de projectfolder staat.")

def get_all_boxes():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM boxes", conn)
    conn.close()
    return df