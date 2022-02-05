import streamlit as st

from scripts.download import load_data, load_weights
from src.app.streamlit_app import streamlit_app


if 'downloaded' not in st.session_state:
    load_data()
    load_weights()
    st.session_state['downloaded'] = True

# main app
streamlit_app()
