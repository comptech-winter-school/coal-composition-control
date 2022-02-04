import streamlit as st

from src.app.streamlit_app import streamlit_app
from scripts.download import load_data, load_weights


if 'downloaded' not in st.session_state:
    st.session_state['downloaded'] = 'not downloaded'

if st.session_state['downloaded'] == 'not downloaded':
    load_data()
    load_weights()
    st.session_state['downloaded'] = 'downloaded'

# main app
streamlit_app()
