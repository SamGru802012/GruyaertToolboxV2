# streamlit_app.py
import streamlit as st
from utils.data import load_boxes, save_boxes
from ui.tabs import tab_input, tab_selected, tab_palletizing, tab_manage

# Set page config
st.set_page_config(
    page_title="Optimale Verpakkingstool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initiatie (voor score sliders en selectie)
if 'score_weights' not in st.session_state:
    st.session_state.score_weights = {
        'fill': 40,
        'pallet': 30,
        'units': 15,
        'stock': 10,
        'rotation': 5
    }

if 'selected_solutions' not in st.session_state:
    st.session_state.selected_solutions = []

if 'visual_solution' not in st.session_state:
    st.session_state.visual_solution = None

if 'boxes_json' not in st.session_state:
    st.session_state.boxes_json = None

# Load data
boxes_df = load_boxes()

# Tabs
TAB_1, TAB_2, TAB_3, TAB_4 = st.tabs([
    "🔍 Invoer & Oplossingen",
    "☁️ Gekozen Verpakkingen",
    "🏋️ Palletisatie",
    "📂 Omdoosbeheer"
])

with TAB_1:
    tab_input(boxes_df)

with TAB_2:
    tab_selected()

with TAB_3:
    tab_palletizing()

with TAB_4:
    updated_df = tab_manage(boxes_df)
    if updated_df is not None:
        save_boxes(updated_df)
