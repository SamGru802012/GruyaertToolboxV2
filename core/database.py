
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "dozen_db.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS boxes (
            id TEXT PRIMARY KEY,
            inner_length REAL,
            inner_width REAL,
            inner_height REAL,
            wall_thickness REAL DEFAULT 3,
            stock INTEGER,
            description TEXT,
            extra_info TEXT
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_ref TEXT,
            product_rotation TEXT,
            box_id TEXT,
            box_dim TEXT,
            rows INTEGER,
            columns INTEGER,
            layers INTEGER,
            total_units INTEGER,
            pallet_height REAL,
            efficiency REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()

def fetch_solutions():
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM saved_solutions", conn)

def save_solutions(df: pd.DataFrame):
    expected_cols = {
        "product_ref", "product_rotation", "box_id", "box_dim",
        "rows", "columns", "layers", "total_units", "pallet_height", "efficiency"
    }
    if not expected_cols.issubset(df.columns):
        raise ValueError("Oplossingsdata mist vereiste kolommen.")
    with get_connection() as conn:
        df[expected_cols].to_sql("saved_solutions", conn, if_exists="append", index=False)
        conn.commit()
