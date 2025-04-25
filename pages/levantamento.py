import streamlit as st
import pandas as pd
import datetime as dt
from menu import ler_base_processada

#Funções auxiliares
def obter_localidades():
    localidades = pd.read_csv("data_bronze/localidades.csv").values.tolist()
    return localidades

def escolhe_dentre_resultados(index, df):
    """
    Exibe uma lista de resultados encontrados e permite ao usuário escolher quais deles.

    Args:
        index: Lista de índices dos resultados encontrados.
    """
    st.subheader("Mais de um patrimônio encontrado. Selecione o desejado:")
    for index, row in df.iterrows():
        if st.checkbox(f"{row['num tombamento']} - {row['denominacao']} - {row['marca_total']} - {row['modelo_total']} - {row['serie_total']} - {row['localidade']}", key=f"select_{index}"):
            st.session_state['inventario'].append(int(row['num tombamento']))
            st.success(f"Patrimônio {row['num tombamento']} adicionado ao inventário.")
            break  # Adiciona apenas um patrimônio por vez

    return index

def encontrar_indice_por_id(df: pd.DataFrame, id_busca: str) -> list[int] | None:
    """
    Busca um ID em diferentes colunas de um DataFrame e retorna o(s) índice(s) da linha correspondente.

    A busca é realizada nas colunas 'num tombamento', 'tombo_antigo' e 'serie_total'.

    Args:
        df: O DataFrame pandas onde a busca será realizada.
        id_busca: A string ID a ser procurada.

    Returns:
        Uma lista de índices onde o ID foi encontrado. Retorna None se o ID não for encontrado.
    """
    try:
        # Busca em todas as colunas relevantes
        df.set_index('num tombamento', inplace=True, drop=False)
        resultados = df[
            (df['num tombamento'].astype(str) == str(id_busca)) |
            (df['tombo_antigo'].astype(str) == str(id_busca)) |
            (df['serie_total'].astype(str) == str(id_busca))
        ]
        
        if resultados.empty:
            st.warning("Patrimônio não encontrado.")
            return None

        # Obtém os índices dos resultados encontrados
        indices = resultados.index.tolist()
        if len(indices) == 1:
                    # Adiciona diretamente ao inventário se houver apenas um resultado
                    st.session_state['inventario'].append(indices[0])
                    st.success(f"Patrimônio {resultados.iloc[0]['num tombamento']} adicionado ao inventário.")
        else:
            escolhe_dentre_resultados(index = indices, df = resultados)

    except KeyError as e:
        st.error(f"Erro ao acessar colunas: {e}")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
        return None

def exibir_detalhes_patrimonio(df, resultados_busca):
    """
    Exibe os detalhes do patrimônio encontrado no DataFrame.

    Args:
        df: O DataFrame pandas onde a busca será realizada.
        id_busca: O ID do patrimônio a ser buscado.
    """
    df.set_index('num tombamento', inplace=True, drop=False)
    if len(resultados_busca) == 1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**Nº Patrimônio:** {df.loc[resultados_busca,'num tombamento'].values[0]}")
            if pd.notna(df.loc[resultados_busca,'tombo_antigo'].values[0]):
                st.write(f"**Tombo Antigo:** {df.loc[resultados_busca,'tombo_antigo'].values[0]}")
            st.write(f"**Nº Serial:** {df.loc[resultados_busca,'serie_total'].values[0]}")
        with col2:
            st.write(f"**Denominação:** {df.loc[resultados_busca,'denominacao'].values[0]}")
            if df.loc[resultados_busca,'localidade'].values[0] == st.session_state['localidade_selecionada'][0]:
                st.write(f"**Divergência de localidade:** :green[{"não"}]")
            else:
                st.write(f"**Divergência de localidade:** :red[{"SIM"}]")
            if df.loc[resultados_busca,'localidade'].values[0] == st.session_state['localidade_selecionada'][0]:
                st.write(f"**Localidade:** :green[{df.loc[resultados_busca,'localidade'].values[0]}]")
            else:
                st.write(f"**Localidade:** :red[{df.loc[resultados_busca,'localidade'].values[0]}]")
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
            st.write(f"**Valor:** {df.loc[resultados_busca,'valor'].values[0]}")
            
                
        with col4:
            if df.loc[resultados_busca,'status'].values[0] == 'ALIENADO':
                st.write(f"**Status:** :red[ALIENADO]")
            else:
                st.write(f"**Status:** :green[{df.loc[resultados_busca,'status'].values[0]}]")
            st.write(f"**Descrição:** {df.loc[resultados_busca,'especificacoes'].values[0]}")
        
    
    else:
        # Se não houver resultados, exibir mensagem
        st.write("Patrimônio não encontrado.")

def buscar_patrimonios_nao_inventariados(ano, localidade, caracteristicas=None):
    # Simulação de busca no banco de dados
    
    df = df[df['localidade'] == localidade]
    df = df[df['ultimo levantamento'] < dt.date.today().year]
    if caracteristicas:
        df = df[df['Descrição'].str.contains(caracteristicas, case=False)]
    return df

def adicionar_ao_inventario(item):
    if item not in st.session_state['inventario']:
        # Adiciona o item ao inventário
        st.session_state['inventario'].append(item)
    else:
        st.warning("Item já adicionado ao inventário.")
    if 'patrimonios_nao_inventariados' in st.session_state:
        st.session_state['patrimonios_nao_inventariados'] = st.session_state['patrimonios_nao_inventariados'][
            ~st.session_state['patrimonios_nao_inventariados']['Descrição'].isin([item['Descrição']])
        ]


# --- Tela de Input de Dados ---
def tela_input_dados(df):
    colunas_de_interesse = ['denominacao', 'status', 'marca_total', 'modelo_total', 'serie_total', 'localidade','acautelado para', 'tombo_antigo', 'ultimo levantamento', 'valor','especificacoes','num tombamento']
    st.title("Levantamento Patrimonial")
    if 'localidade_selecionada' not in st.session_state:
        st.session_state['localidade_selecionada'] = None
    if 'inventario' not in st.session_state:
        st.session_state['inventario'] = []
    df_inventario = pd.DataFrame(columns=['num tombamento', 'inventariado', 'horario_inventário', 'local_inventario'])
    df_inventario['num tombamento'] = df.index
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
        acompanhante = st.text_input("Acompanhante")

    df_resultados_busca = pd.DataFrame(columns=['num tombamento', 'inventariado', 'horario_inventário', 'local_inventario'])
    
    # -- Inserção de dados --
    st.subheader("Inserir Dados do Patrimônio")
    col1, col2, col3 = st.columns([0.4,0.3,0.3])
    #id
    id = col1.text_input("Id. do Patrimônio (Nº Patrimônio, Tombo Antigo ou Nº Serial)")
    #detentor
    detentor = col2.selectbox("Adicionar bens de detentor", df['acautelado para'].unique(), key="detentor")
    cautela = df[df['acautelado para'] == detentor].index.tolist()
        #for i in range(len(id_detentor)):
        #    st.session_state['inventario'].append(id_detentor[i])
    # botão para buscar características
    botao_caracteristicas = col3.button("Buscar Características")
    if botao_caracteristicas: # Buscar materiais sem patrimônio não inventariado por suas características    
        df_caracteristicas = pd.read_csv('data_bronze/caracteristicas.csv')
        caracteristicas = st.multiselect("Buscar por características",df_caracteristicas)

    # -- Resultados de busca --
    resultados_busca = None
    if len(cautela) > 0: #retorna resultados por cautela
        resultados_busca = escolhe_dentre_resultados(index = cautela, df = df.loc[cautela])
    if id != '':
        resultados_busca = encontrar_indice_por_id(df=df, id_busca=id)
    else:
        st.warning('Nenhum resultado encontrado.')
    

    # -- Resultados de busca -- 
    st.write(resultados_busca)
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
    inventario_convertido = [int(valor) for valor in st.session_state['inventario']]
    df.set_index('num tombamento', inplace=True, drop=False)
    df_inventario = df[df.index.isin(inventario_convertido)]
    if df_inventario.empty:
        st.write('Nenhum bem foi adicionado ao inventário ainda.')
    
    else:
        st.data_editor(df_inventario[colunas_de_interesse], use_container_width=True)
    st.divider()
    
    # -- Verificação de duplicidade --
    len(st.session_state['inventario']) != len(set(st.session_state['inventario']))
    st.warning("Existem itens duplicados no inventário. Verifique os IDs.")
    # Exibir os itens duplicados
    duplicados = [item for item in set(st.session_state['inventario']) if st.session_state['inventario'].count(item) > 1]
    st.write("Itens duplicados:", duplicados)
    
    st.divider()
    
    # -- Seção bens a inventariar --
    df_localidade = df[df['localidade'].isin(list(localidade_escolhida))]
    df_localidade.set_index('num tombamento', inplace=True,drop=False)
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