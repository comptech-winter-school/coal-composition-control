from src.app.streamlit_app import streamlit_app
from scripts.download import get_data, get_weights


get_data()
get_weights()
streamlit_app()
