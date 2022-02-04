import streamlit as st

from scripts.download import load_data, load_weights
from src.app.streamlit_app import streamlit_app

if 'downloaded' not in st.session_state:
    st.session_state['downloaded'] = False
    print('downloaded in state')

if st.session_state.get('downloaded', False):
    load_data()
    load_weights()
    st.session_state['downloaded'] = True

# main app
streamlit_app()
