import streamlit as st
import pandas as pd
from menu import ler_base_processada

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
    df_null = df_null.sort_values(ascending=False)
    st.bar_chart(data=df_null)

    st.subheader('Filtrar colunas')
    coluna = st.selectbox('Selecione a coluna', df.columns)
    col1,col2,col3 = st.columns(3)
    col1.subheader(f'**Tipo de dado:** {df[coluna].dtype}')
    col2.metric('% de valores nulos', round(df_null[coluna],2))
    col3.metric('Aguarda',len(df))
    if df[coluna].dtype == 'int64':
        col1.metric('Mínimo', round(df[coluna].min()))
        col2.metric('Mediana', round(df[coluna].median()))
        col2.metric('Média', round(df[coluna].mean()))
        col3.metric('Máximo', round(df[coluna].max()))
    #grafico para distribuição pela coluna selecionada de df
    
    

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)