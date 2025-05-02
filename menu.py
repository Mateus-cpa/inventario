import streamlit as st # type: ignore
import pandas as pd # type: ignore


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
    
    if not st.user.is_logged_in:
        st.login("microsoft")
    else:
        st.switch_page('pages/levantamento.py')
        # Para fins de teste, vamos chamar a tela de input de dados diretamente
        #CAMINHO_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
        #df = ler_base_processada(CAMINHO_PROCESSADO)
    
    
    pass

if __name__ == '__main__':
    menu_principal()