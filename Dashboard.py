import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração do Streamlit
st.set_page_config(page_title="Página Inicial", page_icon=":oil_drum:", layout="wide")
st.title('Análise de variação dos preços dos barris de petróleo :oil_drum:')
st.markdown('''
    Este dashboard tem como objetivo apresentar a variação dos preços dos barris de petróleo ao longo do tempo.
    Os dados foram obtidos através da API da EIA (U.S. Energy Information Administration).
''')


# Chamando a API da EIA para obter os dados de preços dos barris de petróleo
url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
api_key = "tqFtSvZ18xfhYj1qHrzgL5MEtIxLWXp8qWF15oew"
params = {
    "api_key": api_key,
    "frequency": "monthly",
    "data[0]": "value",
    "facets[product][]": "EPCBRENT",
    "start": "2020-01-01",
    "end": "2025-02-01",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": "0",
    "length": "5000"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data_json = response.json()
    if 'response' in data_json and 'data' in data_json['response']:
        df = pd.DataFrame(data_json['response']['data'])
        
        # Processando o DataFrame
        df['period'] = pd.to_datetime(df['period'], format='%Y-%m')  # Converter para datetime
        df.set_index('period', inplace=True)  # Definir a coluna 'period' como índice
        df.index = df.index.strftime('%Y-%m')  # Remover a contagem de horas no índice
        df.sort_index(ascending=True, inplace=True)  # Ordenar cronologicamente
        
        # Exibindo os dados no Streamlit
        st.dataframe(df)
    else:
        st.error("Erro: Dados esperados não encontrados na resposta da API.")
else:
    st.error(f"Erro ao acessar a API: {response.status_code}")
    st.text(response.text)

