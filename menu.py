import streamlit as st
import pandas as pd


def ler_base_processada(caminho):
    # Simulação de leitura de base processada
    df = pd.read_csv(caminho, index_col = 'num tombamento').iloc[:, 1:]
    
    if 'num tombamento.1' in df.columns:
        df['num tombamento'] = df['num tombamento.1']
    else:
        df['num tombamento'] = df.index
    
    #num tombamento como object
    #df['num tombamento'] = df['num tombamento'].astype(object)
    df['tombo_antigo'] = df['tombo_antigo'].astype(object)

    return df

def menu_principal():
    st.title('Menu principal')
    
    """if 'autenticado' not in st.session_state or not st.session_state['autenticado']:
        tela_credenciais()
    else:
        tela_input_dados()"""
    # Para fins de teste, vamos chamar a tela de input de dados diretamente
    CAMINHO_PROCESSADO = 'data_bronze\lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_PROCESSADO)
    st.write(df.columns)
    st.write(df.index)
    
    col1, col2 = st.columns(2)
    credenciamento = col1.button('Credenciamento')
    if credenciamento:
        st.switch_page('pages/credenciamento.py')
    status_base = col2.button('Status da Base de dados')
    if status_base:
        st.switch_page('pages/status_base.py')
    pass

if __name__ == '__main__':
    menu_principal()