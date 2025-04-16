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
    
    
    st.divider()
    """Exibe o DataFrame e informações sobre os tipos de dados."""
    st.dataframe(df_ativos)

# grafico levantamento relativo de cada unidade
        
    

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze\lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)