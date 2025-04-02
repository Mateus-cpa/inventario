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

    """Exibe os KPIs de quantidade de linhas e colunas."""
    col1, col2 = st.columns(2)
    col1.metric('Qtd. de Linhas', df.shape[0])
    col2.metric('Qtd. de Colunas', df.shape[1])

    """Aplica filtro por status no DataFrame."""
    filtro_status = st.multiselect('Filtrar por status: ', df['status'].unique())
    if filtro_status:
        df = df[df['status'].isin(filtro_status)]


    """Exibe o DataFrame e informações sobre os tipos de dados."""
    st.dataframe(df)
    st.subheader('Filtrar colunas')
    coluna = st.selectbox('Selecione a coluna', df.columns)
    st.write(f'Tipo de dado da coluna {coluna}: {df[coluna].dtype}')


    

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)