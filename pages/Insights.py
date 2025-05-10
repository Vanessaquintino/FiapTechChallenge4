import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# Função para buscar e processar dados da API
def fetch_and_process_data(api_key, start_date, end_date):
    url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
    params = {
        "api_key": api_key,
        "frequency": "monthly",
        "data[0]": "value",
        "facets[product][]": "EPCBRENT",
        "start": start_date,
        "end": end_date,
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": "0",
        "length": "5000"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
        data_json = response.json()

        if 'response' in data_json and 'data' in data_json['response']:
            df = pd.DataFrame(data_json['response']['data'])
            df['period'] = pd.to_datetime(df['period'], format='%Y-%m')  # Converter para datetime
            df.set_index('period', inplace=True)  # Definir a coluna 'period' como índice
            df.sort_index(ascending=True, inplace=True)  # Ordenar cronologicamente
            return df
        else:
            st.error("Erro: Dados esperados não encontrados na resposta da API.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
        return None

# Função para criar e exibir o gráfico
def plot_data(df, title):
    if 'value' in df.columns:
        fig = px.line(df, x=df.index, y='value', 
                      title=title,
                      labels={'x': 'Data', 'value': 'Preço (USD)'})
        fig.update_layout(xaxis_title='Data', yaxis_title='Preço (USD)')
        st.plotly_chart(fig)
    else:
        st.warning("A coluna 'value' não foi encontrada no DataFrame.")

# Página de Insights
st.title('Insights :bulb:')
st.markdown('''
        Explore insights sobre a variação dos preços dos barris de petróleo ao longo do tempo.
        Os dados foram obtidos através da API da EIA (U.S. Energy Information Administration).
    ''')

# Obter chave da API de uma variável de ambiente
api_key = os.getenv("EIA_API_KEY", "tqFtSvZ18xfhYj1qHrzgL5MEtIxLWXp8qWF15oew")  # Substituir por sua variável de ambiente

# Criar abas para cada ano
tabs = {
    'Ano de 2020': ('2020-01-01', '2020-12-31'),
    'Ano de 2021': ('2021-01-01', '2021-12-31'),
    'Ano de 2022': ('2022-01-01', '2022-12-31'),
    'Ano de 2023': ('2023-01-01', '2023-12-31'),
    'Ano de 2024': ('2024-01-01', '2024-12-31'),
    'Ano de 2025': ('2025-01-01', '2025-12-31')
}

# Dicionário com textos específicos para cada aba
tab_texts = {
    'Ano de 2020': '''
    Podemos observar no gráfico e nos valores de variação o comportamento dos valores do Petroleo brent no ano de 2020, os valores de variação demonstram a alta volatilidade no mercado de petróleo, fortemente ligada à influência da pandemia do COVID-19.

1. Com o avanço da pandemia e a adoção de medidas de restrição (lockdowns, fechamento de fronteiras, queda do transporte aéreo e terrestre), a demanda global por petróleo despencou drasticamente. Isso pressionou os preços para níveis históricos, levando o petróleo a mínimos de décadas — em alguns casos, contratos futuros chegaram a ficar negativos (como no caso do WTI em abril de 2020).

2. Excesso de oferta e armazenamento esgotado a produção seguiu alta por um tempo, gerando um excesso de oferta. Como os estoques mundiais de petróleo estavam quase no limite, os preços colapsaram ainda mais.

3. A partir do segundo semestre houve uma recuperação parcial, com acordos de corte de produção pela OPEP+ e esperanças de recuperação econômica (vacinas em desenvolvimento, retomada da atividade), os preços começaram a se recuperar, atingindo valores significativamente mais altos até o fim do ano.
    ''',
    'Ano de 2021': '''
    O gráfico de linha mostra a evolução diária do valor do petróleo Brent ao longo de 2021. 
    Podemos observar uma clara tendência de alta ao longo do ano, com algumas flutuações.

1. Recuperação da Demanda Global: Após o choque da demanda em 2020 devido à pandemia, 2021 viu uma recuperação gradual da atividade econômica global à medida que as vacinas eram distribuídas e as restrições eram relaxadas.

2. Restrições de Oferta pela OPEP+: Houve cortes de produção significativos em 2020 para sustentar os preços e, em 2021, houve o aumento da produção de forma gradual e controlada.

3. Redução dos Estoques: A redução dos estoques de petróleo em países consumidores importantes, como os Estados Unidos, também exerceu pressão altista sobre os preços.
    ''',
     'Ano de 2022': '''
2022 foi um ano de grande turbulência para o mercado de petróleo, dominado pelas consequências da guerra na Ucrânia e pelas respostas globais a esse evento. A forte alta inicial e a subsequente volatilidade, seguida por uma tendência de baixa no final do ano, refletem a complexa interação desses fatores geopolíticos e econômicos. A variação absoluta de $57.16 e a variação percentual de 75.19% são significativamente maiores do que as observadas em 2021, evidenciando a maior volatilidade.

1. Guerra na Ucrânia e sanções à Rússia: A invasão da Ucrânia pela Rússia em fevereiro de 2022 gerou uma crise geopolítica que afetou diretamente os mercados de energia. Com a Rússia sendo um dos maiores produtores e exportadores de petróleo do mundo, as sanções impostas por países ocidentais reduziram a oferta global da commodity. Além disso, a possibilidade de a Rússia cortar ou reduzir sua produção em retaliação aumentou a incerteza no mercado, elevando os preços para mais de US$ 120 por barril .

2. Decisão da OPEC+ de reduzir a produção: Em outubro de 2022, a OPEC+ (Organização dos Países Exportadores de Petróleo e aliados) anunciou um corte na produção de 2 milhões de barris por dia, o maior desde 2020. Essa redução visava equilibrar os preços após uma queda para menos de US$ 90 em agosto, mas também teve o efeito de elevar os preços novamente, já que a oferta global foi restringida .

3. Recuperação econômica pós-pandemia: Com o avanço das campanhas de vacinação e a flexibilização das restrições relacionadas à COVID-19, a demanda por petróleo aumentou significativamente em 2022. A retomada da atividade econômica global, especialmente na China e nos Estados Unidos, impulsionou o consumo de energia, pressionando os preços para cima.

4. Estoques baixos e investimentos insuficientes: Durante a pandemia, muitos países reduziram investimentos em energia e combustíveis fósseis, priorizando transições para fontes renováveis. Essa falta de investimento resultou em uma oferta mais apertada de petróleo, agravando a escassez quando a demanda começou a crescer novamente. Além disso, os estoques globais de petróleo estavam baixos, o que limitou a capacidade de resposta a choques de oferta .
    ''',
    'Ano de 2023': '''
Podemos observar que em 2023 houve uma volatividade consideravél dos valores, havendo picos de alta e baixa. Esse movimento é bastante influenciado por:

1. Guerra na Ucrânia: A invasão russa da Ucrânia, que se intensificou em 2022 e continuou em 2023, gerou grande incerteza no mercado de energia. As sanções impostas à Rússia, um dos maiores produtores de petróleo e gás, impactaram a oferta global e elevaram os preços, especialmente no início de 2023. Temores de interrupções no fornecimento e a busca por alternativas energéticas por parte de alguns países contribuíram para essa pressão.

2. Tensões no Oriente Médio: A instabilidade persistente em algumas regiões produtoras do Oriente Médio sempre representa um risco para o fornecimento de petróleo. Embora não tenha havido conflitos de grande escala que impactassem diretamente a produção em 2023, as tensões geopolíticas na região mantiveram um certo nível de preocupação no mercado.

3. Inflação e Taxas de Juros: A alta inflação global e as subsequentes elevações nas taxas de juros por parte de bancos centrais em todo o mundo também afetaram o mercado de petróleo. Taxas de juros mais altas podem desacelerar a atividade econômica e reduzir a demanda por energia. Além disso, a inflação em si pode impactar os custos de produção e transporte do petróleo.

4. Força do Dólar Americano: Como o petróleo é geralmente negociado em dólares americanos, a força da moeda americana pode influenciar os preços para compradores em outras moedas. Um dólar mais forte pode tornar o petróleo mais caro para esses compradores, potencialmente diminuindo a demanda.
     ''',
    'Ano de 2024': '''
Mesmo com uma variação menor que os anos anteriores o gráfico nos mostra que 2024 também apresenta volatividade nos valores com dois picos de lata consideraiveis um em março e outro em julho, além de uma queda consecutiva a partir de setembro. Os preços do petróleo apresentaram um recuo em 2024, marcando o segundo ano consecutivo de queda, à medida que a recuperação da demanda pós-pandemia perdeu fôlego, a economia da China enfrentou dificuldades e os Estados Unidos e outros produtores não pertencentes à Organização dos Países Exportadores de Petróleo (Opep) aumentaram a produção de petróleo em um mercado global bem abastecido.

A continuação da Guerra de Russia e Ucrania continua influênciando no mercado e continua trazendo incertezas.
     ''',
}


# Criar abas para cada ano
tab_objects = st.tabs(list(tabs.keys()))

for tab, (start_date, end_date), tab_name in zip(tab_objects, tabs.values(), tabs.keys()):
    with tab:
        # Buscar e processar os dados
        df = fetch_and_process_data(api_key, start_date, end_date)
        if df is not None:
            # Exibir o gráfico
            plot_data(df, f'Variação dos Preços dos Barris de Petróleo em {start_date[:4]}')
        
        # Exibir o texto específico da aba
        if tab_name in tab_texts:
            st.markdown(tab_texts[tab_name])