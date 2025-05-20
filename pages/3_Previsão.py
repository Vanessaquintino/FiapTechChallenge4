import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
import requests
import xgboost as xgb
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Previsão", page_icon="📈")

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

# Remover a linha: df = df_filtrado.toPandas()
df = df_filtrado.copy()  # Apenas copia o DataFrame pandas

# Ajustar o nome da coluna para 'preco' e 'period' para 'data'
df = df.rename(columns={'period': 'data', 'value': 'preco'})

# Primeiro, defina a coluna 'data' como índice
df = df.set_index('data')

# Em seguida, converta o índice para o tipo DatetimeIndex (caso ainda não seja)
df.index = pd.to_datetime(df.index)

# Finalmente, ordene o DataFrame pelo índice (que agora são as datas)
df = df.sort_index()

# Criar variáveis de lags
def create_lags(df, n_lags):
    df_lags = df.copy()
    for lag in range(1, n_lags+1):
        df_lags[f'lag_{lag}'] = df_lags['preco'].shift(lag)
    return df_lags.dropna()  # Remover valores nulos gerados pelos lags

# Criar lags (necessário para XGBoost com lags)
df_lags = create_lags(df, n_lags=5)

df = df.dropna()

# Separar treino e teste
train_size = int(len(df_lags) * 0.8)
train = df_lags[:train_size]
test = df_lags[train_size:]

# Definir as variáveis independentes (X) e dependentes (y)
X_train = train.drop(columns=['preco'])
y_train = train['preco']
X_test = test.drop(columns=['preco'])
y_test = test['preco']

# Converter para DMatrix, formato que o XGBoost entende
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Definir os parâmetros do modelo
params = {
    'objective': 'reg:squarederror',  # Regressão
    'max_depth': 5,  # Profundidade das árvores
    'eta': 0.1,  # Taxa de aprendizado
    'eval_metric': 'rmse'  # Usando RMSE para avaliação
}

# Treinar o modelo
num_round = 100  # Número de iterações
model_xgb = xgb.train(params, dtrain, num_round)

# Fazer previsões
forecast_xgb = model_xgb.predict(dtest)

# Plotar os resultados
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(train.index, y_train, label='Treinamento', color='blue')
ax.plot(test.index, y_test, label='Teste Real', color='green')
ax.plot(test.index, forecast_xgb, label='Previsão XGBoost', color='red')
ax.set_title("Previsão XGBoost - Dados de Petróleo")
ax.set_xlabel("Data")
ax.set_ylabel("Valor do Petróleo")
ax.legend()
st.pyplot(fig)

# Obter a última data do DataFrame original
last_date = df.index[-1]

# Gerar as datas dos próximos 90 dias
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=90)

# Criar um DataFrame para as previsões futuras
df_forecast = pd.DataFrame(index=future_dates)

# Definir as variáveis independentes (X) e dependentes (y) para treino
X_train = train.drop(columns=['preco'])
y_train = train['preco']

# Definir as variáveis independentes (X) para teste (usaremos para avaliar, não para treinar novamente)
X_test = test.drop(columns=['preco'])
y_test = test['preco']

# Inicializar e treinar o modelo XGBoost
model_xgb_lag = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=150, seed=123)
model_xgb_lag.fit(X_train, y_train)

# Previsões no conjunto de teste (para avaliação, se desejar)
forecast_xgb_test = model_xgb_lag.predict(X_test)

# --- Previsão para os próximos 90 dias usando a lógica de lags ---
# Obter os últimos 5 valores reais do DataFrame original para iniciar a previsão
last_known_values = df['preco'].tail(5).values

# Obter a última data do DataFrame original
last_date = df.index[-1]

# Gerar as datas dos próximos 90 dias
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=90)

# Criar um DataFrame para as previsões futuras
df_forecast = pd.DataFrame(index=future_dates)

# Lista para armazenar as previsões futuras
forecast_future = []

# Preencher os lags e fazer as previsões para as datas futuras
for i in range(len(df_forecast)):
    # Criar o array de lags para a previsão atual
    current_lags = last_known_values.reshape(1, -1)

    # Fazer a previsão
    future_price = model_xgb_lag.predict(current_lags)[0]
    forecast_future.append(future_price)

    # Atualizar os últimos valores conhecidos para a próxima iteração
    last_known_values = np.roll(last_known_values, -1)
    last_known_values[-1] = future_price

# Adicionar a coluna de previsão ao DataFrame de previsão
df_forecast['preco_previsto'] = forecast_future

# --- Plotar os resultados ---
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(train.index, y_train, label='Treinamento', color='blue')
ax.plot(test.index, y_test, label='Teste Real', color='green')
ax.plot(test.index, forecast_xgb_test, label='Previsão XGBoost (Teste)', color='red')
ax.plot(df_forecast.index, df_forecast['preco_previsto'], label='Previsão XGBoost (90 dias)', color='orange')
ax.set_title("Previsão do Preço do Petróleo Brent - XGBoost com Lags (Exemplo)")
ax.set_xlabel("Data")
ax.set_ylabel("Valor do Petróleo")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)