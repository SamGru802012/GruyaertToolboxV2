
import streamlit as st

def push_undo(action_type, payload):
    if "undo_stack" not in st.session_state:
        st.session_state.undo_stack = []
    st.session_state.undo_stack.append((action_type, payload))

def pop_undo():
    if "undo_stack" in st.session_state and st.session_state.undo_stack:
        return st.session_state.undo_stack.pop()
    return None

def clear_undo():
    st.session_state.undo_stack = []

def format_dimensions(l, b, h):
    return f"{int(l)}×{int(b)}×{int(h)} mm"
