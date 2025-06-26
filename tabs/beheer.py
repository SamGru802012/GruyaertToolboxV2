
import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "packing_app.db"

def load_boxes():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM boxes", conn)
    return df

def save_boxes(df):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM boxes")
        df.to_sql("boxes", conn, if_exists="append", index=False)

def beheer_tab():
    st.title("📦 Omdozenbeheer")

    st.markdown("Voeg nieuwe dozen toe, pas afmetingen aan of verwijder dozen uit stock.")

    df = load_boxes()

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="doosbeheer",
        column_config={
            "ref": st.column_config.TextColumn("Referentie"),
            "inner_length": st.column_config.NumberColumn("Lengte (mm)"),
            "inner_width": st.column_config.NumberColumn("Breedte (mm)"),
            "inner_height": st.column_config.NumberColumn("Hoogte (mm)"),
            "wall_thickness": st.column_config.NumberColumn("Wanddikte (mm)")
        }
    )

    if st.button("💾 Wijzigingen opslaan"):
        save_boxes(edited_df)
        st.success("Dozen succesvol opgeslagen in database.")
