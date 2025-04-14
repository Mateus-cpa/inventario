import streamlit as st
import pandas as pd
from menu import ler_base_processada
import os

def pagina_principal(df):
    """Configura as propriedades da página no Streamlit."""
    st.set_page_config(
        page_title='Status da Base Processada',
        page_icon='📊',
        layout='wide'
    )

# gráfico quantidade por status

# gráfico levantamnto geral em relação ao estimado

# grafico levantamento relativo de cada unidade
        
    

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze\lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)