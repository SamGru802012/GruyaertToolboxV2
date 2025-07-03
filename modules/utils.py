import streamlit as st

def initialize_session():
    if 'undo_stack' not in st.session_state:
        st.session_state.undo_stack = []
    if 'selected_solution' not in st.session_state:
        st.session_state.selected_solution = None
