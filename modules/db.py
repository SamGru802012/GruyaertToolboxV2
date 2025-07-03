
import sqlite3
import pandas as pd

DB_PATH = "data/boxes.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boxes (
            id TEXT PRIMARY KEY,
            binnen_l REAL,
            binnen_b REAL,
            binnen_h REAL,
            wanddikte REAL,
            stock INTEGER,
            omschrijving TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_ref TEXT,
            product_afm TEXT,
            doos_id TEXT,
            doos_rotatie TEXT,
            product_rotatie TEXT,
            rijen INTEGER,
            kolommen INTEGER,
            lagen INTEGER,
            totaal_stuks INTEGER,
            volume_eff REAL,
            geselecteerd BOOLEAN DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

def fetch_boxes():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM boxes", conn)
    conn.close()
    return df

def insert_solution(solution_dict):
    conn = get_connection()
    cursor = conn.cursor()
    columns = ', '.join(solution_dict.keys())
    placeholders = ', '.join(['?'] * len(solution_dict))
    sql = f"INSERT INTO solutions ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(solution_dict.values()))
    conn.commit()
    conn.close()

def fetch_solutions():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM solutions", conn)
    conn.close()
    return df

def update_solution_selection(solution_id, selected):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE solutions SET geselecteerd = ? WHERE id = ?", (selected, solution_id))
    conn.commit()
    conn.close()
