import streamlit as st
import pandas as pd
import datetime as dt
from menu import ler_base_processada

#Funções auxiliares
def obter_localidades():
    localidades = pd.read_csv("data_bronze/localidades.csv").values.tolist()
    return localidades

def encontrar_indice_por_id(df: pd.DataFrame, id_busca: str) -> int | None:
    """
    Busca um ID em diferentes colunas de um DataFrame e retorna o índice da linha correspondente.

    A busca é realizada nas colunas 'num tombamento' (testando como string e inteiro),
    'tombo_antigo' e 'serie_total'.

    Args:
        df: O DataFrame pandas onde a busca será realizada.
        id_busca: A string ID a ser procurada.

    Returns:
        O índice da linha onde o ID foi encontrado. Retorna None se o ID não for encontrado.
    """
    # retorna lista de index com todos resultados que tenham id procurando em 'num tombamento', 'tombo_antigo' e 'serie_total'
    try:
        df_resultados_busca = df[df['num tombamento'].astype(str) == str(id_busca)]
    except KeyError:
        df_resultados_busca = df[df['tombo_antigo'].astype(str) == str(id_busca)]
    except ValueError:
        df_resultados_busca = df[df['serie_total'].astype(str) == str(id_busca)]
    index_resultados = df_resultados_busca.index.tolist()
    if len(index_resultados) == 1:
        st.session_state['inventario'].append(df_resultados_busca['num tombamento'].values[0])
    if len(index_resultados) > 0:
        return index_resultados
    else:
        st.warning("Patrimônio não encontrado.")

    return None

def exibir_detalhes_patrimonio(df, resultados_busca):
    """
    Exibe os detalhes do patrimônio encontrado no DataFrame.

    Args:
        df: O DataFrame pandas onde a busca será realizada.
        id_busca: O ID do patrimônio a ser buscado.
    """
    if len(resultados_busca) == 1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**Nº Patrimônio:** {df.loc[resultados_busca,'num tombamento'].values[0]}")
            if pd.notna(df.loc[resultados_busca,'tombo_antigo'].values[0]):
                st.write(f"**Tombo Antigo:** {df.loc[resultados_busca,'tombo_antigo'].values[0]}")
            st.write(f"**Nº Serial:** {df.loc[resultados_busca,'serie_total'].values[0]}")
        with col2:
            st.write(f"**Denominação:** {df.loc[resultados_busca,'denominacao'].values[0]}")
            st.write(f"**Localidade atual:** {df.loc[resultados_busca,'localidade'].values[0]}")
            if df.loc[resultados_busca,'status'].values[0] == 'ACAUTELADO':
                st.write(f"**Acautelado para:** {df.loc[resultados_busca,'acautelado para'].values[0]}")
        with col3:
            st.write(f"**Marca:** {df.loc[resultados_busca,'marca_total'].values[0]}")
            if pd.notna(df.loc[resultados_busca,'modelo_total'].values[0]):
                st.write(f"**Modelo:** {df.loc[resultados_busca,'modelo_total'].values[0]}")
            if df.loc[resultados_busca,'ano do levantamento'].values[0] == dt.date.today().year:
                st.write(f"**Levantamento:** :red[{df.loc[resultados_busca,'ultimo levantamento'].values[0]}]")
            else:
                st.write(f"**Levantamento:** :green[{df.loc[resultados_busca,'ultimo levantamento'].values[0]}]")
        with col4:
            if df.loc[resultados_busca,'status'].values[0] == 'ALIENADO':
                st.write(f"**Status:** :red[ALIENADO]")
            else:
                st.write(f"**Status:** :green[{df.loc[resultados_busca,'status'].values[0]}]")
            st.write(f"**Descrição:** {df.loc[resultados_busca,'especificacoes'].values[0]}")
        
    elif len(resultados_busca) > 1: #exibir dataframe com checkboxs para selecionar o patrimônio desejado
        st.subheader("Mais de um patrimônio encontrado")
        st.write("Selecione o patrimônio desejado:")
        # CONTINUAR LÓGICA DE SELECIONAR POR CHECKBOX DAQUI
        for index, row in df.loc[[resultados_busca]].iterrows():
            col_check, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns(11)
            with col_check: #adicionar um checkbox para cada linha encontrada
                if st.checkbox(f"{row['num tombamento']}", key=f"check_{index}"):
                    st.session_state['patrimonio_selecionado'] = row['num tombamento']
                col2.write(f"**Descrição:** {row['denominacao']}")
            
                col3.write(f"**Nº Patrimônio:** {row['num tombamento']}")
                col4.write(f"**Tombo Antigo:** {row['tombo_antigo']}")
                col5.write(f"**Nº Serial:** {row['serie_total']}")
                col6.write(f"**Localidade atual:** {row['localidade']}")
                col7.write(f"**Marca:** {row['marca_total']}")
                col8.write(f"**Modelo:** {row['modelo_total']}")
                col9.write(f"**Último levantamento:** {row['ultimo levantamento']}")
                col10.write(f"**Status:** {row['status']}")
                col11.write(f"**Descrição:** {row['especificacoes']}")
                st.divider()
        st.dataframe(df_resultados_busca[['num tombamento', 'tombo_antigo', 'serie_total', 
                                            'denominacao', 'localidade', 'acautelado para', 
                                            'marca_total', 'modelo_total', 'ultimo levantamento', 
                                            'status', 'especificacoes']], use_container_width=True, hide_index=True)
    else:
        st.write("Patrimônio não encontrado.")

def buscar_patrimonios_nao_inventariados(ano, localidade, caracteristicas=None):
    # Simulação de busca no banco de dados
    
    df = df[df['localidade'] == localidade]
    df = df[df['ultimo levantamento'] < dt.date.today().year]
    if caracteristicas:
        df = df[df['Descrição'].str.contains(caracteristicas, case=False)]
    return df

def adicionar_ao_inventario(item):
    st.session_state['inventario'].append(item)
    if 'patrimonios_nao_inventariados' in st.session_state:
        st.session_state['patrimonios_nao_inventariados'] = st.session_state['patrimonios_nao_inventariados'][
            ~st.session_state['patrimonios_nao_inventariados']['Descrição'].isin([item['Descrição']])
        ]


# --- Tela de Input de Dados ---
def tela_input_dados(df):
    colunas_de_interesse = ['denominacao', 'marca_total', 'modelo_total', 'serie_total', 'status', 'localidade','acautelado para', 'tombo_antigo', 'ultimo levantamento', 'especificacoes','num tombamento']
    st.title("Levantamento Patrimonial")
    if 'localidade_selecionada' not in st.session_state:
        st.session_state['localidade_selecionada'] = None
    if 'inventario' not in st.session_state:
        st.session_state['inventario'] = []
    df_inventario = pd.DataFrame(columns=['num tombamento', 'inventariado', 'horario_inventário', 'local_inventario'])
    df_inventario['num tombamento'] = df['num tombamento']
    col1, col2 = st.columns(2)
    with col1:
        localidades = obter_localidades()
        localidade_escolhida = st.selectbox("Localidade", localidades, key="localidade_escolha")
        if localidade_escolhida == "Nova Localidade":
            nova_localidade = st.text_input("Nova Localidade", key="nova_localidade")
            if nova_localidade:
                st.session_state['localidade_selecionada'] = nova_localidade
            else:
                st.session_state['localidade_selecionada'] = None
        else:
            st.session_state['localidade_selecionada'] = localidade_escolhida

    with col2:
        #data_inventario = st.date_input("Data do Inventário", dt.date.today()) #talvez não precise por causa do st.session_state('horario_inventário')
        acompanhante = st.text_input("Acompanhante")

    df_resultados_busca = pd.DataFrame(columns=['num tombamento', 'inventariado', 'horario_inventário', 'local_inventario'])
    
    # busca de material
    st.subheader("Inserir Dados do Patrimônio")
    
    col1, col2, col3 = st.columns([0.4,0.3,0.3])
    id = col1.text_input("Id. do Patrimônio (Nº Patrimônio, Tombo Antigo ou Nº Serial)")
    #id = '2010060766' #TIC
    #id = '2010041474' #outro
    botao_detentor = col2.button("Buscar Detentor")
    if botao_detentor:
        detentor = st.multiselect('Selecione o detentor', df['acautelado para'].unique(), key="detentor")
        df_resultados_busca = df_resultados_busca[df['acautelado para'] == detentor]
    botao_caracteristicas = col3.button("Buscar Características")
    if botao_caracteristicas: # Buscar materiais sem patrimônio não inventariado por suas características    
        df_caracteristicas = pd.read_csv('data_bronze/caracteristicas.csv')
        caracteristicas = st.multiselect("Buscar por características",df_caracteristicas)
    
    resultados_busca = encontrar_indice_por_id(df, id)
    st.write(resultados_busca)
    
    #Exibir resultados de busca
    st.subheader("Resultados da Busca")
    if resultados_busca != None:
        exibir_detalhes_patrimonio(df, resultados_busca)
    
    st.divider()
    
    if botao_caracteristicas:
        if st.session_state['localidade_selecionada']:
            ano_atual = dt.date.today().year
            patrimonios_nao_inventariados = buscar_patrimonios_nao_inventariados(
                ano_atual, st.session_state['localidade_selecionada'], caracteristicas
            )
            if not patrimonios_nao_inventariados.empty:
                st.subheader("Patrimônios Não Inventariados")
                for index, row in patrimonios_nao_inventariados.iterrows():
                    col_check, col_info = st.columns([0.1, 0.9])
                    with col_check:
                        if st.checkbox(f"Adicionar", key=f"add_{index}"):
                            item_para_adicionar = {
                                'Descrição': row['Descrição'],
                                'Local': row['Local'],
                                'Unidade': row['Unidade'],
                                'Ultimo_Inventario': row['Ultimo_Inventario'],
                                'Numero_Serie': row['Numero_Serie'],
                                'Tipo': row['Tipo']
                            }
                            adicionar_ao_inventario(item_para_adicionar)
                    with col_info:
                        st.write(f"**Descrição:** {row['Descrição']}")
                        st.write(f"**Local:** {row['Local']}")
                        st.write(f"**Unidade:** {row['Unidade']}")
                        st.write(f"**Último Inventário:** {row['Ultimo_Inventario']}")
            else:
                st.info("Nenhum patrimônio não inventariado encontrado com as características fornecidas.")
        else:
            st.warning("Selecione ou insira uma localidade primeiro.")

    
    
    # -- Seção Bens inventariados --
    st.subheader(f"{len(st.session_state['inventario'])} Bens Levantados em {st.session_state['localidade_selecionada']}")
    if df_inventario.empty:
        st.write('Nenhum bem foi adicionado ao inventário ainda.')
    else:
        st.data_editor(df[colunas_de_interesse].loc[st.session_state['inventario']], use_container_width=True)
    st.divider()
    
    # -- Seção bens a inventariar --
    df_localidade = df[df['localidade'].isin(list(localidade_escolhida))]
    #excluir os bens que já foram inventariados
    df_localidade = df_localidade[df_localidade['num tombamento'].isin(st.session_state['inventario']) == False]
    st.subheader(f"{df_localidade.shape[0]} Bens a inventariar em {st.session_state['localidade_selecionada']}")    
    st.dataframe(df_localidade[colunas_de_interesse], use_container_width=True)

    st.divider()

    if st.button("Concluir Levantamento"):
        st.success("Levantamento concluído!")
            # Adicionar lógica para salvar os dados do inventário no banco de dados
        
    

if __name__ == "__main__":
    CAMINHO_ARQ_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
    df= ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    tela_input_dados(df)
    # A autenticação deve ser implementada antes de chamar a função de input de dados