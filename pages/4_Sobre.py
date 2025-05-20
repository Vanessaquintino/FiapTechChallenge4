import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # Adicione esta linha
import os

# Página de sobre
st.title('Sobre 💼')
# st.markdown('''
#         Explore insights sobre a variação dos preços dos barris de petróleo ao longo do tempo.
#         Os dados foram obtidos através da API da EIA (U.S. Energy Information Administration).
#     ''')