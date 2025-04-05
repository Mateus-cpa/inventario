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
    df_linhas_com_resultado = df[df['num tombamento'].isin(id) | df['tombo_antigo'].isin(id) | df['serie_total'].isin(id)]
    
    if not df_linhas_com_resultado.empty:
        return df_linhas_com_resultado

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
        data_inventario = st.date_input("Data do Inventário", dt.date.today()) #talvez não precise por causa do st.session_state('horario_inventário')
        acompanhante = st.text_input("Acompanhante")

    df_resultados_busca = pd.DataFrame(columns=['num tombamento', 'inventariado', 'horario_inventário', 'local_inventario'])
    st.subheader("Inserir Dados do Patrimônio")
    col1, col2 = st.columns([0.4,0.6])
    id = col1.text_input("Id. do Patrimônio (Nº Patrimônio, Tombo Antigo ou Nº Serial)")
    
    #id = '2010060766' #TIC
    #id = '2010041474' #outro
    # Buscar materiais sem patrimônio não inventariado por suas características
    caracteristicas = col2.text_input("Buscar por características")
    
    if id:
        #df_resultados_busca = encontrar_linha_por_id(df, id)
        try:
            df_resultados_busca = df.loc[int(id)].copy()
        except KeyError:
            df_resultados_busca = df.loc[df['tombo_antigo'] == id].copy()
        except ValueError:
            df_resultados_busca = df.loc[df['serie_total'] == id].copy()
        if len(df_resultados_busca) == 1:
            st.subheader("Patrimônio Encontrado")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**Nº Patrimônio:** {df_resultados_busca['num tombamento'].values[0]}")
                st.write(f"**Tombo Antigo:** {df_resultados_busca['tombo_antigo'].values[0]}")
                st.write(f"**Nº Serial:** {df_resultados_busca['serie_total'].values[0]}")
            with col2:
                st.write(f"**Denominação:** {df_resultados_busca['denominacao'].values[0]}")
                st.write(f"**Localidade atual:** {df_resultados_busca['localidade'].values[0]}")
                st.write(f"**Acautelado para:** {df_resultados_busca['acautelado para'].values[0]}")
            with col3:
                st.write(f"**Marca:** {df_resultados_busca['marca_total'].values[0]}")
                st.write(f"**Modelo:** {df_resultados_busca['modelo_total'].values[0]}")
                st.write(f"**Último levantamento:** {df_resultados_busca['ultimo levantamento'].values[0]}")
            with col4:
                st.write(f"**Status:** :red[{df_resultados_busca['status'].values[0]}]")
                st.write(f"**Descrição:** {df_resultados_busca['especificacoes'].values[0]}")
            
        elif len(df_resultados_busca) > 1: #exibir dataframe com checkboxs para selecionar o patrimônio desejado
            st.subheader("Mais de um patrimônio encontrado")
            st.write("Selecione o patrimônio desejado:")
            # CONTINUAR LÓGICA DE SELECIONAR POR CHECKBOX DAQUI
            for index, row in df_resultados_busca.iterrows(): #10 colunas
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

    
    
    # -- Seção Bens inventariados --
    st.subheader(f"{len(df_resultados_busca)} Bens Levantados em {st.session_state['localidade_selecionada']}")
    if df_inventario.empty:
        st.write('Nenhum bem foi adicionado ao inventário ainda.')
    else:
        st.dataframe(df_inventario[df_inventario.inventariado.notna()], use_container_width=True)
    
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