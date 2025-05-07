import streamlit as st #type: ignore[import]
import pandas as pd #type: ignore[import]
import datetime as dt
from menu import ler_base_processada
#import gerar_etiqueta as etiq

#Funções auxiliares
def obter_localidades():
    localidades = pd.read_csv("data_bronze/localidades.csv").values.tolist()
    return localidades

def escolhe_dentre_resultados(df, index):
    """
    Exibe uma lista de resultados encontrados e permite ao usuário escolher quais deles.

    Args:
        index: Lista de índices dos resultados encontrados.
    """
    st.write("**Mais de um patrimônio encontrado. Selecione o desejado:** ")
    for index, row in df.iterrows():
        if st.checkbox(f"{row['status']} - {row['num tombamento']} - {row['denominacao']} - {row['marca_total']} - {row['modelo_total']} - {row['serie_total']} - {row['localidade']} - {row['acautelado para']} - {row['ultimo levantamento']}",
                       key=f"select_{index}"):
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
            return indices[0]
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
    Exibe os detalhes do patrimônio encontrado no DataFrame, se 1 resultado, 
    ou uma lista para seleção, se vários resultados.

    Args:
        df: O DataFrame pandas onde a busca será realizada.
        id_busca: O ID do patrimônio a ser buscado.
    """
    df.set_index('num tombamento', inplace=True, drop=False)
    if resultados_busca is None:
        resultados_busca = []
    if isinstance(resultados_busca, int):
        resultados_busca = [resultados_busca]
    if len(resultados_busca) > 0:
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
            
            
        with col3:
            st.write(f"**Marca:** {df.loc[resultados_busca,'marca_total'].values[0]}")
            if pd.notna(df.loc[resultados_busca,'modelo_total'].values[0]):
                st.write(f"**Modelo:** {df.loc[resultados_busca,'modelo_total'].values[0]}")
            if df.loc[resultados_busca,'ano do levantamento'].values[0] == dt.date.today().year:
                st.write(f"**Levantamento:** :red[{df.loc[resultados_busca,'ultimo levantamento'].values[0]}]")
            else:
                st.write(f"**Levantamento:** :green[{df.loc[resultados_busca,'ultimo levantamento'].values[0]}]")
            st.write(f"**Valor:** R$ {round(df.loc[resultados_busca,'valor'].values[0],2)}")
            
                
        with col4:
            if df.loc[resultados_busca,'status'].values[0] == 'ALIENADO':
                st.write(f"**Status:** :red[ALIENADO]")
            else:
                st.write(f"**Status:** :green[{df.loc[resultados_busca,'status'].values[0]}]")
            if df.loc[resultados_busca,'status'].values[0] == 'ACAUTELADO':
                st.write(f"**Acautelado para:** {df.loc[resultados_busca,'acautelado para'].values[0]}")
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
    # -- configurações iniciais --
    colunas_de_interesse = ['denominacao', 'status', 'marca_total', 'modelo_total', 'serie_total', 'localidade','acautelado para', 'tombo_antigo', 'ultimo levantamento', 'valor','especificacoes','num tombamento']
    st.title("Levantamento Patrimonial")
    if 'localidade_selecionada' not in st.session_state:
        st.session_state['localidade_selecionada'] = None
    if 'inventario' not in st.session_state:
        st.session_state['inventario'] = []
    if 'gerar_etiquetas' not in st.session_state:
        st.session_state['gerar_etiquetas'] = []
    
    #verificar se df_inventario será utilizado
    df_inventario = pd.DataFrame(columns=['num_tombamento', 'inventariado', 'horario_inventario', 'local_inventario'])
    df_inventario['num tombamento'] = df.index

    # Informar localidade e acompanhamento inventario
    col1, col2 = st.columns(2)
    with col1:
        localidades = obter_localidades()
        localidade_escolhida = st.selectbox("Localidade", localidades, key="localidade_escolha")
        nova_localidade = col1.button('Nova localidade')
        if nova_localidade:
            nova_localidade = st.text_input("Nova Localidade", key="nova_localidade")
            if nova_localidade:
                st.session_state['localidade_selecionada'] = nova_localidade
            else:
                st.session_state['localidade_selecionada'] = None
        else:
            st.session_state['localidade_selecionada'] = localidade_escolhida
    with col2:
        acompanhamento = st.text_input("Acompanhamento inventário")
    df_resultados_busca = pd.DataFrame(columns=['num tombamento', 'inventariado', 'horario_inventário', 'local_inventario'])
    
    
    # -- Inserção de dados --
    st.subheader("Inserir Dados do Patrimônio")
    busca = st.segmented_control('Buscar por:', ['ID', 'Cautela', 'Características'], key="busca", selection_mode="single", default="ID")
    id, index_cautela, index_caracteristicas = '', [], []
    # -- Campos de entrada --
    if busca == 'ID':
        id = st.text_input("Id. do Patrimônio (Nº Patrimônio, Tombo Antigo ou Nº Serial)")
    if busca == 'Cautela':
       detentor = st.selectbox("Adicionar bens de detentor", df['acautelado para'].unique(), key="detentor")
       index_cautela = df[df['acautelado para'] == detentor].index.tolist()
    if busca == 'Características':
        caracteristicas = st.selectbox("Buscar por características",df['caracteristicas'].unique(), key="caracteristicas", index=0)
        if caracteristicas == '':
            caracteristicas = None
        else:
            caracteristicas = [caracteristicas]
        if caracteristicas:
            index_caracteristicas = df[df['caracteristicas'].str.contains(caracteristicas[0], case=False)].index.tolist()
    else:
        index_caracteristicas = []

    # -- Resultados de busca -- 
    st.subheader("Resultados da Busca")
    resultados_busca = None
    if len(index_cautela) > 0: #retorna resultados por cautela
        resultados_busca = escolhe_dentre_resultados(index = index_cautela, df = df.loc[index_cautela])
        detentor = 'nan'
    elif len(index_caracteristicas) > 0: #retorna resultados por características
        resultados_busca = escolhe_dentre_resultados(index = index_caracteristicas, df = df.loc[index_caracteristicas])
    elif id != '':
        resultados_busca = encontrar_indice_por_id(df=df, id_busca=id)
        exibir_detalhes_patrimonio(df, resultados_busca)
    
    st.divider()
    
    
    
    # -- Seção Bens inventariados --
    st.subheader(f"{len(st.session_state['inventario'])} Bem(ns) Levantado(s) em {st.session_state['localidade_selecionada']}")
    inventario_convertido = [int(valor) for valor in st.session_state['inventario']]
    df.set_index('num tombamento', inplace=True, drop=False)
    df_inventario = df[df.index.isin(inventario_convertido)]
    if df_inventario.empty:
        st.warning('Nenhum bem foi adicionado ao inventário ainda.')
    else:
        df_inventario = df_inventario[colunas_de_interesse]
        df_inventario['gerar_etiquetas'] = False
        df_inventario['excluir'] = False
        # colocar na primeira coluna o checkbox para gerar etiquetas
        cols = df_inventario.columns
        # colocar gerar_etiquetas na primeira coluna
        first_cols = ['gerar_etiquetas', 'excluir'] 
        other_cols = [col for col in cols if (col not in first_cols)]
        cols = first_cols + other_cols
        df_inventario = df_inventario[cols]
        df_etiquetas = st.data_editor(df_inventario, use_container_width=True)
        col1, col2, col3 = st.columns([0.1, 0.17, 0.73])
        if col2.button('Gerar etiquetas'):
            st.session_state['gerar_etiquetas'] = df_etiquetas.loc[df_etiquetas['gerar_etiquetas'] == True].index.tolist()
        if col3.button('Excluir itens'):
            st.session_state['inventario'] = df_etiquetas.loc[df_etiquetas['excluir'] == False].index.tolist()
            
    st.divider()
    
    # -- Verificação de duplicidade --
    if len(st.session_state['inventario']) != len(set(st.session_state['inventario'])):
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
    st.subheader(f"{df_localidade.shape[0]} Bem(ns) a inventariar em {st.session_state['localidade_selecionada']}")    
    st.dataframe(df_localidade[colunas_de_interesse], use_container_width=True)

    st.divider()
    
    # -- Gerar etiquetas --
    if len(st.session_state['gerar_etiquetas']) > 0:
        st.subheader("Etiquetas a gerar:")
        # permitir selecionar vários itens de df_inventario e adicionar na lista st.session_state['etiquetas'] e após botão de imprimir etiquetas
        st.dataframe(df_inventario[df_inventario['gerar_etiquetas'] == True][colunas_de_interesse], use_container_width=True)
        if st.button("Imprimir etiquetas"):
            #etiq.gerar_etiquetas(st.session_state['etiquetas'], st.session_state['localidade_selecionada'][0])
            st.success("Etiquetas impressas com sucesso!")
        st.divider()

    # -- Concluir levantamento --
    if st.button("Concluir Levantamento"):
        st.success("Levantamento concluído!")
        # Transformar st.session_state['inventario'] em txt
        path_destino = f'data_gold/{st.session_state["localidade_selecionada"]}.txt'
        path_destino = path_destino.replace("'", "").replace("[", "").replace("]", "")
        with open(path_destino, 'w') as f:
            for item in st.session_state['inventario']:
                f.write(f"{item}\n")    
        with open(path_destino, 'r') as f:        
            conteudo_arquivo = f.read()    
        st.download_button(
            label="Baixar inventário",
            data=conteudo_arquivo,
            file_name=path_destino.split('/')[-1],
            mime='text/plain',
            #icon=':download:'
        )
        
        
    

if __name__ == "__main__":
    CAMINHO_ARQ_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
    df= ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    tela_input_dados(df)
    # A autenticação deve ser implementada antes de chamar a função de input de dados