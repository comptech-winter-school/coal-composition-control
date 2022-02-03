from src.app.streamlit_app import streamlit_app
from scripts.download import load_weights, load_data


load_data()
load_weights()
streamlit_app()
