import streamlit as st
import pandas as pd
from levantamento import ler_base_processada

def pagina_principal(df):
    st.title('Status da Base Processada')

    # Filtro por status
    filtro_status = st.multiselect('Filtrar por colunas: ',df['status'].unique())
    df = df[df['status'].isin(filtro_status)]

    #KPIs
    col1, col2 = st.columns(2)
    col1.metric('Qtd. de Linhas', df.shape[0])
    col2.metric('Qtd. de Colunas', df.shape[1])

    #dataframe
    st.dataframe(df)

    #mostrar dtype de cada coluna
    st.write('Filtrar colunas')
    coluna = st.selectbox('Selecione a coluna', df.columns)
    st.write(f'Tipo de dado da coluna {coluna}: {df[coluna].dtype}')

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)