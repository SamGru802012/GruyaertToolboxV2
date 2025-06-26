
import streamlit as st
import pandas as pd
from core.database import fetch_solutions, save_solutions

def render_opgeslagen():
    st.header("💾 Opgeslagen Oplossingen")

    try:
        df = fetch_solutions()
        if df.empty:
            st.info("Er zijn nog geen oplossingen opgeslagen.")
        else:
            st.subheader("📘 Bestaande oplossingen")
            st.dataframe(df, use_container_width=True)

            st.download_button(
                label="📤 Exporteer als CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="oplossingen.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Fout bij laden van oplossingen: {e}")

    st.markdown("---")
    st.subheader("💡 Sla nieuwe oplossingen op")

    session_df = st.session_state.get("laatste_resultaten")
    if session_df is None or session_df.empty:
        st.info("Geen simulatieresultaten beschikbaar.")
        return

    session_df = session_df.copy()
    session_df["✔️ Selecteer"] = False
    edited = st.data_editor(session_df, use_container_width=True, num_rows="dynamic", key="edit_save")

    if st.button("🗃️ Bewaar geselecteerde rijen"):
        selectie = edited[edited["✔️ Selecteer"] == True].drop(columns=["✔️ Selecteer"])
        if selectie.empty:
            st.warning("Geen rijen geselecteerd.")
        else:
            try:
                save_solutions(selectie)
                st.success(f"{len(selectie)} oplossing(en) opgeslagen.")
            except Exception as e:
                st.error(f"Opslagfout: {e}")
