import streamlit as st
import pandas as pd
import datetime as dt
from menu import ler_base_processada

#Funções auxiliares
def obter_localidades():
    localidades = pd.read_csv("data_bronze/localidades.csv").values.tolist()
    return localidades


def encontrar_linha_por_id(df, id):
    """
    Retorna um DataFrame contendo a linha onde o id corresponde a um valor em 
    'num tombamento', 'tombo_antigo' ou 'serie_total'.
    """
    
    # Verifica se o id é um índice do DataFrame
    if id in df.index:
        return df.loc[[id]] 

    # Verifica se o id existe em qualquer uma das colunas especificadas
    mascara = (df['num tombamento'] == id) | (df['tombo_antigo'] == id) | (df['serie_total'] == id)
    
    # Retorna o DataFrame com a linha correspondente, se encontrada
    if mascara.any():
        return df[mascara]
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se o id não for encontrado


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
    st.title("Levantamento Patrimonial")

    if 'localidade_selecionada' not in st.session_state:
        st.session_state['localidade_selecionada'] = None
    if 'inventario' not in st.session_state:
        st.session_state['inventario'] = []
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
        data_inventario = st.date_input("Data do Inventário", dt.date.today())
        acompanhante = st.text_input("Acompanhante")

    st.subheader("Inserir Dados do Patrimônio")
    col1, col2 = st.columns([0.4,0.6])
    id = col1.text_input("Identificação do Patrimônio (Nº Patrimônio, Tombo Antigo ou Nº Serial)")
    #id = '2010060766' #TIC
    #id = '2010041474' #outro
    df_inventario = pd.DataFrame()

    if id:
        df_inventario = encontrar_linha_por_id(df, id)

        if not df_inventario.empty:
            st.subheader("Patrimônio Encontrado")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**Nº Patrimônio:** {df_inventario['num tombamento'].values[0]}")
                st.write(f"**Tombo Antigo:** {df_inventario['tombo_antigo'].values[0]}")
                st.write(f"**Nº Serial:** {df_inventario['serie_total'].values[0]}")
            with col2:
                st.write(f"**Denominação:** {df_inventario['denominacao'].values[0]}")
                st.write(f"**Localidade atual:** {df_inventario['localidade'].values[0]}")
                st.write(f"**Acautelado para:** {df_inventario['acautelado para'].values[0]}")
            with col3:
                st.write(f"**Marca:** {df_inventario['marca_total'].values[0]}")
                st.write(f"**Modelo:** {df_inventario['modelo_total'].values[0]}")
                st.write(f"**Último levantamento:** {df_inventario['ultimo levantamento'].values[0]}")
            with col4:
                st.write(f"**Status:** {df_inventario['status'].values[0]}")
                st.write(f"**Descrição:** {df_inventario['especificacoes'].values[0]}")
        else:
            st.write("Patrimônio não encontrado.")
    # caso retornem mais de um patrimônio, exibir as opções
    """elif len(df[[id]]) > 1:
        st.write('**Mais de um patrimônio encontrado:** Escolha uma das opções abaixo:')
        for index, row in id_linha.iterrows():
            #adicionar um checkbox para cada linha encontrada
            col_check, col_info = st.columns([0.1, 0.9])
            with col_check:
                if st.checkbox(f"Selecionar {row['num tombamento']}", key=f"check_{index}"):
                    st.session_state['patrimonio_selecionado'] = row['num tombamento']
            with col_info:
                st.write(f"**Descrição:** {row['denominacao']}")
                st.write(f"**Nº Patrimônio:** {row['num tombamento']}")
                st.write(f"**Tombo Antigo:** {row['tombo_antigo']}")
                st.write(f"**Nº Serial:** {row['serie_total']}")
                st.write(f"**Localidade atual:** {row['localidade']}")
                st.write(f"**Marca:** {row['marca_total']}")
                st.write(f"**Modelo:** {row['modelo_total']}")
                st.write(f"**Último levantamento:** {row['ultimo levantamento']}")
                st.write(f"**Status:** {row['status']}")
                st.write(f"**Descrição:** {row['especificacoes']}")"""
        # se for marcado o checkbox, adicionar à lista de inventário
                
    # adicionar à coluna 'inventariado' = 'sim' no banco de dados
    df_inventario.loc[id, 'inventariado'] = 'sim'
    # adicionar à coluna 'horario_inventário' = datetime no banco de dados
    df_inventario.loc[id, 'horario_inventário'] = dt.datetime.now()
    # adicionar à coluna 'local_inventario' = localidade no banco de dados
    df_inventario.loc[id, 'local_inventario'] = st.session_state['localidade_selecionada']
    # Se encontrado, exibir informações e botão para adicionar ao inventário
    
    
    # Buscar materiais sem patrimônio não inventariado por suas características
    caracteristicas = col2.text_input("Buscar por características")
    if caracteristicas:
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

    # Campo para leitura de serial se for TIC e não tiver serial
    if (id and 
        id_linha['grupo de material'] == 'MATERIAL DE TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO - TIC' and 
        id_linha['serie_total'] == 'Sem serial cadastrado'):
        st.subheader("Leitura de Serial (se necessário)")
        st.write(f"**{id_linha['denominacao']} (TIC sem Serial)**")
        novo_serial = st.text_input(f"Ler Serial para {id_linha['denominacao']}", key=f"cadastra_serial")
        if novo_serial:
            st.write(f"Serial lido: {novo_serial}")
            # Adicionar lógica para atualizar o número de série no inventário
            # ou no banco de dados, se já estiver sendo persistido
            pass
    
    # -- Seção Bens inventariados --
    st.subheader(f"Bens Levantados em {st.session_state['localidade_selecionada']}")
    if len(df_inventario) == 0:
        st.write('Nenhum bem foi adicionado ao inventário ainda.')
    else:
        st.dataframe(df_inventario)
    
    #Seção Bens acautelados
    st.subheader("Adicionar Bens Acautelados")
    adicionar_acautelados = st.radio("Adicionar bens acautelados", ["Sim", "Não"], key="acautelados")
    if adicionar_acautelados == "Não":
        if st.button("Concluir Levantamento"):
            st.success("Levantamento concluído!")
            # Adicionar lógica para salvar os dados do inventário no banco de dados
    else:
        st.warning("Marque 'Não' para finalizar inventário e habilitar a conclusão.")

    # Listar bens a inventariar
    df_localidade = df[df['localidade'].isin(list(localidade_escolhida))]
    #df_localidade = df[df['localidade'] == st.session_state['localidade_selecionada']]
    #df_localidade = df_localidade[df_localidade['inventariado'] == None]
    df_localidade = df_localidade[['denominacao', 'marca_total', 'modelo_total', 'serie_total', 'status','acautelado para', 'tombo_antigo', 'ultimo levantamento', 'especificacoes','num tombamento', 'localidade']]
    st.subheader(f"{df_localidade.shape[0]} Bens a inventariar em {st.session_state['localidade_selecionada']}")    
    st.dataframe(df_localidade)

    

if __name__ == "__main__":
    CAMINHO_ARQ_PROCESSADO = 'data_bronze/lista_bens-processado.csv'
    df= ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    tela_input_dados(df)
    # A autenticação deve ser implementada antes de chamar a função de input de dados