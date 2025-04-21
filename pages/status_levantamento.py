import streamlit as st
import pandas as pd
from menu import ler_base_processada
import os
import datetime as dt
import altair as alt


def pagina_principal(df):
    """Configura as propriedades da página no Streamlit."""
    st.set_page_config(
        page_title='Status da Base Processada',
        page_icon='📊',
        layout='wide'
    )

    #variaveis
    df_ativos = df[df['status'].isin(['EFETIVADO','ACAUTELADO','BEM NÃO LOCALIZADO'])]
    
    # gráfico levantamento geral em relação ao estimado
    st.title('Status da Base Processada')

    col1,col2 = st.columns(2)
    filtro_todos_bens = col1.button('Incluir inativos')
    if filtro_todos_bens:
        df_ativos = df.copy()
    filtro_unidade = col2.multiselect('Filtrar por Unidade: ', df_ativos['sigla'].unique())
    if filtro_unidade:
        df_ativos = df_ativos[df_ativos['sigla'].isin(filtro_unidade)]
    #else:
        #mostrar gráfico de levantamento geral em relação ao estimado
        #ler histórico de levantamentos em data_silver
        # criar reta de estimativa de levantamento por dia sendo 312 por dia a partir de 14/04/2025

    #variável
    qtde_bens_inventariados = df_ativos[df_ativos['ano do levantamento'] == dt.date.today().year].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric('Qtd. de Bens', df_ativos.shape[0])
    #bens inventariados no ano atual
    col2.metric('Qtd. de Bens Inventariados', qtde_bens_inventariados)
    col3.metric('Percentual de Bens Inventariados', f'{round(df_ativos[df_ativos['ano do levantamento'] == dt.date.today().year].shape[0]/df_ativos.shape[0]*100,2)} %')
    
    #dataframe de quantidade levantado por ano de levantamento
    st.subheader('Quantidade levantada por ano')
    df_lev = df_ativos.groupby('ano do levantamento').size().reset_index(name='quantidade')
    df_lev['ano do levantamento'] = df_lev['ano do levantamento'].astype(str)
    df_lev = df_lev.sort_values(by='ano do levantamento')
    #gráfico de barras com os anos de levantamento
    chart = alt.Chart(df_lev).mark_bar().encode(
        x=alt.X('ano do levantamento', title='Ano do Levantamento'),
        y=alt.Y('quantidade', title='Quantidade de Bens'),
        color=alt.Color('ano do levantamento', legend=None),
        tooltip=['ano do levantamento', 'quantidade']
    ).properties(
        width=600,
        height=400
    )
    # Adicionar rótulos com os valores
    text = alt.Chart(df_lev).mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('ano do levantamento'),
        y=alt.Y('quantidade'),
        text=alt.Text('quantidade:Q')  # Exibe os valores
    )
    # Combinar o gráfico de barras com os rótulos
    chart_with_text = (chart + text).configure_view(
        fill='white')
    st.altair_chart(chart_with_text, use_container_width=True)
    """Legenda: Último levantamento em 2010 significa que nunca foi inventariado"""
        
    #criar botão de salvar gráfico como imagem em graficos_levantamento com a data atual
    botao_salvar_imagem = st.button('Salvar gráfico como imagem')
    if botao_salvar_imagem:
        chart.save(f'graficos_levantamento/grafico_levantamento_{dt.date.today()}.png')
    st.divider()
   
    # grafico levantamento relativo de cada unidade
    st.header('Levantamento relativo de cada unidade')
    #pegar os dados de data_silver e concatenar em um dataframe
    df_levantamento_historico = pd.DataFrame()
    for arq in os.listdir('data_silver'):
        if arq.endswith('.json'):
            df_levantamento_parcial = pd.read_json(os.path.join('data_silver', arq)).T
            
            #adicionar coluna de data de levantamento pelo nome do arquivo
            df_levantamento_parcial['data_levantamento'] = arq.split('_')[2].split('.')[0]
            #converter para datetime
            df_levantamento_parcial['data_levantamento'] = pd.to_datetime(df_levantamento_parcial['data_levantamento'], format='%Y-%m-%d')
            #indexar com data, mas somente yyyy-mm-dd
            df_levantamento_parcial['data_levantamento'] = df_levantamento_parcial['data_levantamento'].dt.date
            df_levantamento_parcial['unidade'] = df_levantamento_parcial.index
            
            #transformar data_levantamento em índice
            df_levantamento_parcial.set_index('data_levantamento', drop=True, inplace=True)
            #df_levantamento_parcial = df_levantamento_parcial['perc_levantado']
            df_levantamento_historico = pd.concat([df_levantamento_historico, df_levantamento_parcial])
    
    #criar gráfico de linha do tempo onde cada unidade é uma linha e o valor é perc_levantado
    st.subheader('Gráfico de Linha do Tempo por Unidade')

        # Resetar o índice para garantir que as colunas necessárias estejam disponíveis
    df_levantamento_historico_reset = df_levantamento_historico.reset_index()

    # Criar o gráfico com Altair
    line_chart = alt.Chart(df_levantamento_historico_reset).mark_line().encode(
        x=alt.X('data_levantamento:T', title='Data do Levantamento'),
        y=alt.Y('perc_levantado:Q', title='Percentual Levantado', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('unidade:N', title='Unidade'),
        tooltip=['data_levantamento', 'unidade', 'perc_levantado']
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        grid=True
    )   
    # Exibir o gráfico no Streamlit
    st.altair_chart(line_chart, use_container_width=True)
    

    st.subheader('Maiores percentuais Levantados')
    # criar rank de unidades com maior percentual levantado na última data de levantamento
    #pegar a última data de levantamento
    ultima_data_levantamento = df_levantamento_historico.index[-1]
    #filtrar o dataframe pela última data de levantamento
    df_ultimo_levantamento = df_levantamento_historico[df_levantamento_historico.index == ultima_data_levantamento]
    #ordenar pelo percentual levantado
    df_ultimo_levantamento = df_ultimo_levantamento.sort_values(by='perc_levantado', ascending=False)
    #pegar as 10 primeiras unidades
    df_ultimo_levantamento = df_ultimo_levantamento.head(10)
    #criar gráfico de barras com as unidades e o percentual levantado
    chart = alt.Chart(df_ultimo_levantamento).mark_bar().encode(
        x=alt.X('unidade:N', title='Unidade'),
        y=alt.Y('perc_levantado:Q', title='Percentual Levantado', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('unidade:N', legend=None),
        tooltip=['unidade', 'perc_levantado']
    ).properties(
        width=600,
        height=400
    )
    # Adicionar rótulos com os valores
    text = alt.Chart(df_ultimo_levantamento).mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('unidade:N'),
        y=alt.Y('perc_levantado:Q'),
        text=alt.Text('perc_levantado:Q')  # Exibe os valores
    )
    # Combinar o gráfico de barras com os rótulos
    chart_with_text = (chart + text).configure_view(
        fill='white')
    st.altair_chart(chart_with_text, use_container_width=True)
    
    # Menores percentuais Levantados
    st.subheader('Menores percentuais Levantados')
    # criar rank de unidades com menor percentual levantado na última data de levantamento
    df_ultimo_levantamento = df_levantamento_historico.sort_values(by='perc_levantado', ascending=True)
    #pegar as 10 primeiras unidades
    df_ultimo_levantamento = df_ultimo_levantamento.head(10)
    #criar gráfico de barras com as unidades e o percentual levantado
    chart = alt.Chart(df_ultimo_levantamento).mark_bar().encode(
        x=alt.X('unidade:N', title='Unidade'),
        y=alt.Y('perc_levantado:Q', title='Percentual Levantado', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('unidade:N', legend=None),
        tooltip=['unidade', 'perc_levantado']
    ).properties(
        width=600,
        height=400
    )
    # Adicionar rótulos com os valores
    text = alt.Chart(df_ultimo_levantamento).mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('unidade:N'),
        y=alt.Y('perc_levantado:Q'),
        text=alt.Text('perc_levantado:Q')  # Exibe os valores
    )
    # Combinar o gráfico de barras com os rótulos
    chart_with_text = (chart + text).configure_view(
        fill='white')
    st.altair_chart(chart_with_text, use_container_width=True)

    

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze\lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)