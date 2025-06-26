import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'dozen_db.sqlite')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()
