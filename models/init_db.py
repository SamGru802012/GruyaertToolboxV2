import sqlite3
import os

DB_PATH = "data/dozen_db.sqlite"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Boxes tabel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS boxes (
        id TEXT PRIMARY KEY,
        inner_length REAL,
        inner_width REAL,
        inner_height REAL,
        wall_thickness REAL,
        stock INTEGER,
        description TEXT,
        extra_info TEXT
    )
    """)
    # Oplossingen tabel
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
        efficiency REAL
    )
    """)
    conn.commit()
    conn.close()
