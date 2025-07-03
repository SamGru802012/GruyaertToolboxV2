import streamlit as st
import copy

def initialize_session():
    if 'undo_stack' not in st.session_state:
        st.session_state.undo_stack = []
    if 'solutions' not in st.session_state:
        st.session_state.solutions = None

def add_to_undo_stack(state_snapshot):
    snapshot = copy.deepcopy(state_snapshot)
    st.session_state.undo_stack.append(snapshot)

def undo_last_action():
    if st.session_state.undo_stack:
        previous = st.session_state.undo_stack.pop()
        st.session_state.solutions = previous
