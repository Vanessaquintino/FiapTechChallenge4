import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração do Streamlit
st.set_page_config(page_title="Página Inicial", page_icon=":oil_drum:", layout="wide")
st.title('Análise de variação dos preços dos barris de petróleo :oil_drum:')
st.markdown('''
    Esse projeto tem como objetivo apresentar a variação dos preços dos barris de petróleo ao longo do tempo.
    Os dados foram obtidos através da API da EIA (U.S. Energy Information Administration).
''')


# Texto adicional da página
st.title('Introdução 📖')
st.markdown('''
Para o desenvolvimento desse trabalho vamos partir das seguintes premissas:

1. Coleta de Dados via API As informações sobre o preço do petróleo foram obtidas por meio de uma API pública de dados econômicos, como a da EIA (U.S. Energy Information Administration) ou Quandl, que fornecem séries temporais atualizadas sobre commodities energéticas.

Os dados coletados incluíram: data da cotação, valor do barril em USD.

A coleta foi feita com requisições programadas via Python (ex: requests, pandas.read_json) e armazenada de forma bruta no Databricks para tratamento posterior.

Após ingestão, os dados foram convertidos para tipos adequados (Date, Float) e persistidos como uma tabela Delta no Databricks, garantindo performance e versionamento.

2. Uso do Databricks O Databricks foi utilizado como a principal plataforma de desenvolvimento, análise e modelagem:
Armazenamento dos dados em Delta Lake, com versionamento seguro.

Utilização de PySpark para transformação dos dados e criação de tabelas confiáveis.

Exploração e visualização interativa dos dados com Plotly e comandos display() do Databricks.

3. Dashboard Interativo Um dashboard interativo foi criado com uso de Plotly (e/ou Databricks SQL dashboards), contendo visualizações de:

Evolução histórica do preço do petróleo.

Variações mensais e sazonais.

Essas visualizações estarão organizadas para guiar o usuário por um storytelling analítico, mostrando como fatores externos impactam o preço do petróleo.

4. Criação e um modelo de previsão dos preços para os próximos 90 dias.

5. Documentação do plano para fazer o deploy em produção do modelo com melhor performance de previsão.

6. Compartilhamento de um MVP do modelo em produção utilizando o Streamlit.

7. Apresentação do trabalho por meio de um vídeo.
''')
