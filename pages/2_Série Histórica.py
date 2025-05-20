import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

st.title("Série Histórica 📈")
st.markdown('''
        Para esta análise, temos um recorte de tempo iniciado em janeiro de 2020 até a data mais recente de atualização no ano de 2025. Os valores são diários.
        O gráfico nos mostra as oscilações significativas ocorridas nos valores ao longo desses 5 anos. Podemos observar dois grandes picos: um pico de baixa expressivo ocorrido no ano de 2020, onde tivemos o menor valor registrado nesses 5 anos, atingindo o valor mínimo de 9.12 (USD), e um pico de alta acentuado em 2022, alcançando o maior valor de 133.18 (USD).
    ''')


# Obtém a chave da API do ambiente (ou usa uma padrão)
api_key = os.getenv("EIA_API_KEY", "tqFtSvZ18xfhYj1qHrzgL5MEtIxLWXp8qWF15oew")

# Pega a data de ontem (D-1)
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# URL e parâmetros para consulta dos dados do petróleo Brent na API da EIA
url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
params = {
    "api_key": api_key,
    "frequency": "daily",
    "data[0]": "value",
    "facets[product][]": "EPCBRENT",
    "start": "2020-01-01",
    "end": end_date,
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": "0",
     "length": "5000"
}

# Faz a requisição
response = requests.get(url, params=params)

# Verifica resposta
if response.status_code == 200:
    data_json = response.json()
    df = pd.DataFrame(data_json['response']['data'])
else:
    print("Erro ao acessar a API:", response.status_code)
    print(response.text)

df_filtrado = df[['period', 'value']]
df_filtrado.head()

# Remove símbolos não numéricos (exceto vírgula e ponto)
df_filtrado['value'] = df_filtrado['value'].str.replace(r'[^\d,.-]', '', regex=True)

# Se vírgula é decimal e ponto é separador de milhar
df_filtrado['value'] = df_filtrado['value'].str.replace(',', '.', regex=False)

# Converte para float
df_filtrado['value'] = pd.to_numeric(df_filtrado['value'], errors='coerce')

df_filtrado.head()

df_filtrado.info()

# Converter e organizar o DataFrame corretamente
df_selecionado = df_filtrado.copy() # Create a copy of df_filtrado and assign it to df_selecionado
df_selecionado.index = pd.to_datetime(df_filtrado['period'], format='%Y-%m-%d')
df_selecionado.drop(columns=['period'], inplace=True)
df_selecionado.sort_index(ascending=True, inplace=True)  # Ordem cronológica correta

# Converter e organizar o DataFrame corretamente
df.index = pd.to_datetime(df['period'], format='%Y-%m-%d')
df.drop(columns=['period'], inplace=True)
df.sort_index(ascending=True, inplace=True)  # Ordem cronológica correta


# Converter a coluna 'value' para tipo numérico, tratando erros
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Remover linhas com valores NaN
df = df.dropna()

# Criar o gráfico interativo
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['value'],
    mode='lines',
    name='value'
))

# Atualizar layout
fig.update_layout(
    title={'text': 'Gráfico Interativo de Valores', 'x': 0.35},
    xaxis_title='Periodo',
    yaxis_title='Valor (USD)',
    yaxis=dict(range=[0, df['value'].max() * 1.1]),
    template='plotly_white',
    height=500,
    width=1000
)

# Mostrar o gráfico
st.plotly_chart(fig, use_container_width=True)