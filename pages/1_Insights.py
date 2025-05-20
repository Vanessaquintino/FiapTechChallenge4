import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  
import os

st.title('Insights :bulb:')
st.markdown('''
        Explore insights sobre a variação dos preços dos barris de petróleo ao longo do tempo.
        Os dados foram obtidos através da API da EIA (U.S. Energy Information Administration).
    ''')


api_key = os.getenv("EIA_API_KEY", "tqFtSvZ18xfhYj1qHrzgL5MEtIxLWXp8qWF15oew")
start_date = "2020-01-01"
end_date = "2025-05-19"

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
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data_json = response.json()
        df = pd.DataFrame(data_json['response']['data'])
        df = df[['period', 'value']]
        df['value'] = df['value'].str.replace(r'[^\d,.-]', '', regex=True)
        df['value'] = df['value'].str.replace(',', '.', regex=False)
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['period'] = pd.to_datetime(df['period'], errors='coerce')
        df = df.dropna()
        df = df.set_index('period')
        df.sort_index(ascending=True, inplace=True)
        return df
    else:
        st.error(f"Erro ao acessar a API: {response.status_code}")
        return pd.DataFrame()


# Buscar e processar os dados
df = fetch_and_process_data(api_key, start_date, end_date)

# Criar abas para cada ano
tabs = {
    'Ano de 2020': ('2020-01-01', '2020-12-31'),
    'Ano de 2021': ('2021-01-01', '2021-12-31'),
    'Ano de 2022': ('2022-01-01', '2022-12-31'),
    'Ano de 2023': ('2023-01-01', '2023-12-31'),
    'Ano de 2024': ('2024-01-01', '2024-12-31'),
    'Ano de 2025': ('2025-01-01', '2025-12-31'),
    'Correlação com o Dólar': ('09-04-2025', '01-01-2025')
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
       'Ano de 2025': '''
    Tendência de Alta Inicial: O valor começa o ano de 2025 com uma tendência de alta, atingindo o pico em meados de janeiro, próximo a 83.48 (o maior valor registrado).

    Período de Flutuação: Após o pico, observamos um período de relativa estabilidade com algumas oscilações, mantendo-se geralmente acima de 75 até meados de março.

    Queda Acentuada: Uma queda significativa e relativamente rápida começa por volta do final de março, levando o valor ao seu ponto mais baixo em maio, próximo a 61.57 (o menor valor registrado).

    Recuperação Tênue: No final do período apresentado (início de maio), parece haver uma leve tentativa de recuperação, mas ainda em patamares bem inferiores aos observados no início do ano.

    A queda no preço do petróleo Brent em 2025 é resultado de um aumento na oferta por parte da OPEP+, aliado a uma demanda global enfraquecida, criando um desequilíbrio no mercado que pressiona os preços para baixo
       ''',
         'Correlação com o Dólar': '''
    No início do período (próximo a 2025-04-09): O dólar (azul) mostra uma alta considerável, enquanto o Brent (verde) apresenta uma queda.

    Por volta de 2025-04-12 a 2025-04-16: Ambas as linhas mostram uma tendência de alta, embora com magnitudes diferentes.

    De 2025-04-16 até aproximadamente 2025-04-22: O dólar inicia uma queda mais acentuada, enquanto o Brent permanece relativamente alto e depois começa a cair também.

    Do final de abril até o início de maio: Ambas as linhas parecem ter uma tendência de queda, com algumas flutuações.
         ''',
}

# Criar abas para cada ano
tab_names = list(tabs.keys())
tab_objs = st.tabs(tab_names)

for i, tab in enumerate(tab_objs):
    with tab:
        ano_inicio, ano_fim = tabs[tab_names[i]]
        df_ano = fetch_and_process_data(api_key, ano_inicio, ano_fim)

        fig_ano = go.Figure()
        if not df_ano.empty:
            fig_ano.add_trace(go.Scatter(
                x=df_ano.index,
                y=df_ano['value'],
                mode='lines+markers',
                name='value',
                marker=dict(symbol='circle', size=8, color='#1f77b4'),
                line=dict(width=2, color='#1f77b4')
            ))
            fig_ano.update_layout(
                title={'text': f'Valores do Petróleo Brent - {tab_names[i]}', 'x': 0.35},
                xaxis_title='Período',
                yaxis_title='Valor (USD)',
                yaxis=dict(range=[0, df_ano['value'].max() * 1.1]),
                template='plotly_white',
                height=500,
                width=1000
            )
            fig_ano.update_xaxes(tickangle=45)
            st.plotly_chart(fig_ano, use_container_width=True)
        else:
            st.warning("Sem dados para este período.")

        st.markdown(tab_texts[tab_names[i]])

    #incluir a aba de dolar 


        # if tab_names[i] == 'Correlação com o Dólar':
        #     @st.cache_data
        #     def fetch_usd_brl(start_date, end_date):
        #         url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"
        #         resp = requests.get(url)
        #         if resp.status_code == 200:
        #             df_usd = pd.DataFrame(resp.json())
        #             df_usd['data'] = pd.to_datetime(df_usd['data'], dayfirst=True)
        #             df_usd['valor'] = pd.to_numeric(df_usd['valor'], errors='coerce')
        #             df_usd = df_usd.set_index('data')
        #             return df_usd
        #         else:
        #             return pd.DataFrame()

        #     df_brl = fetch_usd_brl("2020-01-01", "2025-05-19")
        #     df_brent = fetch_and_process_data(api_key, "2020-01-01", "2025-05-19")

        #     # Unir os dois dataframes pela data
        #     df_corr = pd.merge(df_brent, df_brl, left_index=True, right_index=True, how='inner', suffixes=('_brent', '_usdbrl'))

        #     if not df_corr.empty:
        #         corr = df_corr['value'].corr(df_corr['valor'])
        #         st.write(f"**Correlação entre Brent e USD/BRL:** `{corr:.2f}`")
        #         fig_corr = go.Figure()
        #         fig_corr.add_trace(go.Scatter(
        #             x=df_corr.index, y=df_corr['value'], name='Brent (USD)', yaxis='y1', line=dict(color='blue')
        #         ))
        #         fig_corr.add_trace(go.Scatter(
        #             x=df_corr.index, y=df_corr['valor'], name='USD/BRL', yaxis='y2', line=dict(color='green')
        #         ))
        #         fig_corr.update_layout(
        #             title="Petróleo Brent vs Dólar (USD/BRL)",
        #             xaxis=dict(title='Data'),
        #             yaxis=dict(title='Brent (USD)', side='left'),
        #              legend=dict(x=0.01, y=0.99),
        #             height=500,
        #             width=1000,
        #             template='plotly_white'
        #         )
        #         st.plotly_chart(fig_corr, use_container_width=True)
        #     else:
        #         st.warning("Não foi possível obter dados para correlação.")

        #     st.markdown(tab_texts[tab_names[i]])
  
