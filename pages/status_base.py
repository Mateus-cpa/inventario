import streamlit as st
import pandas as pd
from menu import ler_base_processada
import os
import altair as alt

def pagina_principal(df):
    """Configura as propriedades da página no Streamlit."""
    st.set_page_config(
        page_title='Status da Base Processada',
        page_icon='📊',
        layout='wide'
    )
    
    st.title('Status da Base Processada')

    """Aplica filtro por status no DataFrame."""
    col1,col2 = st.columns(2)
    filtro_ativos = col1.button('Bens ativos')
    if filtro_ativos:
        df = df[df['status'].isin(['EFETIVADO','ACAUTELADO','BEM NÃO LOCALIZADO'])]
    filtro_status = col2.multiselect('Filtrar por status: ', df['status'].unique())
    if filtro_status:
        df = df[df['status'].isin(filtro_status)]

    """Exibe os KPIs de quantidade de linhas e colunas."""
    col1, col2 = st.columns(2)
    col1.metric('Qtd. de Linhas', df.shape[0])
    col2.metric('Qtd. de Colunas', df.shape[1])


    """Exibe o DataFrame e informações sobre os tipos de dados."""
    st.dataframe(df.sample(10))
    
    #retornar a proporção de valores nulos na coluna
    st.subheader('Colunas vazias')
    df_null = df.isnull().sum()/len(df)*100
    df_null = df_null[df_null > 0]
    df_null = df_null.sort_values(ascending=False)
    st.bar_chart(data=df_null)

    st.subheader('Filtrar colunas')
    coluna = st.selectbox('Selecione a coluna', df.columns)
    col1,col2,col3 = st.columns(3)
    col1.subheader(f'**Tipo de dado:** {df[coluna].dtype}')
    try:
        col1.metric('% de valores nulos', round(df_null[coluna],2))
    except KeyError:
        col1.metric('% de valores nulos', 0.00)
    
    if (df[coluna].dtype == 'int64' or df[coluna].dtype == 'float64'):
        col3.metric('Mínimo', round(df[coluna].min(),2))
        col2.metric('Mediana', round(df[coluna].median(),2))
        col2.metric('Média', round(df[coluna].mean(),2))
        col3.metric('Máximo', round(df[coluna].max(),2))

    st.divider()    
    #compara tamanho em MB de planilha data e data_bronze
    st.subheader('Comparativo de tamanhos em MB')
    tamanho_inicial_mb = os.path.getsize('data/lista_bens.xlsx') / (1024 * 1024)
    tamanho_final_mb = os.path.getsize('data_bronze/lista_bens-processado.csv') / (1024 * 1024)
    col1, col2, col3 = st.columns(3)
    col1.metric('Inicial', round(tamanho_inicial_mb,2))
    col2.metric('Final', round(tamanho_final_mb,2))
    col3.metric('Redução (%)', round((tamanho_inicial_mb - tamanho_final_mb)/tamanho_inicial_mb,2))
    
    st.divider()
    #gráfico quantidade por status
    st.subheader('Quantidade de bens por status')
    df_status = df['status'].value_counts()
    st.bar_chart(data=df_status, use_container_width=True)
    
    st.subheader('Quantidade de bens por status ativos'    )
    df_ativos = df[df['status'].isin(['EFETIVADO','ACAUTELADO','BEM NÃO LOCALIZADO'])]
    df_ativos = df_ativos['status'].value_counts()
    st.bar_chart(data=df_ativos, use_container_width=True)

    #proporção de bens acautelados por validação de assinatura
    st.subheader('Proporção de bens acautelados por validação de assinatura')
    df_acautelados = df[df['status'] == 'ACAUTELADO']
    df_acautelados = df_acautelados['validado eletron'].value_counts()
    st.bar_chart(data=df_acautelados, use_container_width=True)

    #boxplot de valor_atual_tratado por sigla
    st.subheader('Boxplot de valor atual tratado por grupo de material')
    df_boxplot = df[['grupo de material','valor_atual_tratado']].dropna()
    df_boxplot['valor_atual_tratado'] = df_boxplot['valor_atual_tratado'].astype(float)
    grafico_boxplot = alt.Chart(df_boxplot).mark_boxplot().encode(
        y=alt.Y('grupo de material', sort='-x'),
        x='valor_atual_tratado',
        #tooltip=None
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(grafico_boxplot, use_container_width=True)
if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze\lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)