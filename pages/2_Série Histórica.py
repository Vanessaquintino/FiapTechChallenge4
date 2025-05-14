import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuração do Streamlit (deve ser o primeiro comando)
st.set_page_config(page_title="Série Histórica", page_icon="📊", layout="wide")

st.title('Série Histórica 📊')
st.markdown('''
    Para esta análise, temos um recorte de tempo iniciado em janeiro de 2020 até a data mais recente de atualização no ano de 2025. Os valores são diários.
    O gráfico nos mostra as oscilações significativas ocorridas nos valores ao longo desses 5 anos. Podemos observar dois grandes picos: um pico de baixa expressivo ocorrido no ano de 2020, onde tivemos o menor valor registrado nesses 5 anos, atingindo o valor mínimo de 9.12 (USD), e um pico de alta acentuado em 2022, alcançando o maior valor de 133.18 (USD).
''')

# Carregar a chave da API de uma variável de ambiente
api_key = os.getenv("EIA_API_KEY", "tqFtSvZ18xfhYj1qHrzgL5MEtIxLWXp8qWF15oew")
url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
params = {
    "api_key": api_key,
    "frequency": "annual",
    "data[0]": "value",
    "facets[product][]": "EPCBRENT",
    "start": "2020",
    "end": "2025",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": "0",
    "length": "5000"
}

# Fazer a requisição à API
try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
    data_json = response.json()

    # Verificar se os dados esperados estão na resposta
    if 'response' in data_json and 'data' in data_json['response']:
        df = pd.DataFrame(data_json['response']['data'])

        # Adicionar um mês padrão "01" para valores que estão apenas no formato de ano
        df['period'] = df['period'].apply(lambda x: f"{x}-01" if len(x) == 4 else x)

        # Processar o DataFrame
        df['period'] = pd.to_datetime(df['period'], format='%Y-%m', errors='coerce')  # Converter para datetime
        df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Converter 'value' para numérico
        df.dropna(subset=['period', 'value'], inplace=True)  # Remover linhas com valores inválidos
        df.set_index('period', inplace=True)  # Definir a coluna 'period' como índice
        df.sort_index(ascending=True, inplace=True)  # Ordenar cronologicamente

        # Exibir os dados no Streamlit
        st.dataframe(df)

        # Criar o gráfico interativo com Plotly Graph Objects
        fig = go.Figure()

        # Adicionar a linha com marcadores
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['value'],
            mode='lines+markers',  # Adiciona marcadores aos pontos
            name='Valor',
            line=dict(color='red', width=2)  # Cor e espessura da linha
        ))

        # Atualizar layout do gráfico
        fig.update_layout(
            title={
                'text': 'Gráfico Interativo de Valores',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': 'darkblue'}
            },
            xaxis_title='Período',
            yaxis_title='Valor (USD)',
            yaxis=dict(
                range=[0, df['value'].max() * 1.1],
                gridcolor='lightgray',
                zerolinecolor='gray'
            ),
            xaxis=dict(
                gridcolor='lightgray',
                zerolinecolor='gray'
            ),
            template='plotly_white',
            height=500,
            width=1000,
            legend=dict(
                title='Legenda',
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            ),
            plot_bgcolor='whitesmoke',
            paper_bgcolor='lightyellow'
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Erro: Dados esperados não encontrados na resposta da API.")
except requests.exceptions.RequestException as e:
    st.error(f"Erro ao acessar a API: {e}")
except ValueError as e:
    st.error(f"Erro ao processar os dados: {e}")