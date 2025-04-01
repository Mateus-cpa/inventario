import streamlit as st
import pandas as pd
import datetime as dt

# --- Simulação de Dados e Funções ---
# Substitua por sua lógica real de conexão com o banco de dados

def obter_localidades():
    localidades = pd.read_csv("data_bronze/localidades.csv").values.tolist()
    return localidades

def buscar_patrimonios_nao_inventariados(ano, localidade, caracteristicas=None):
    # Simulação de busca no banco de dados
    
    df = pd.read_csv('data_bronze/lista_bens-processado.csv')
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

"""def obter_dados_inventario_atual():
    if 'inventario' in st.session_state:
        return pd.DataFrame(st.session_state['inventario'])
    return pd.DataFrame()
"""
# --- Tela de Input de Dados ---
def tela_input_dados():
    st.title("Levantamento Patrimonial")

    if 'localidade_selecionada' not in st.session_state:
        st.session_state['localidade_selecionada'] = None
    if 'inventario' not in st.session_state:
        st.session_state['inventario'] = []
    df = pd.read_csv('data_bronze/lista_bens-processado.csv')
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
    id = st.text_input("Identificação do Patrimônio (Nº Patrimônio, Tombo Antigo ou Nº Serial)")   
    if id:
        #procurar id nas colunas 'num patrimonio', 'tombo_antigo', 'serie_total' do dataframe df e exibir a linha correspondente
        # Se o id for encontrado, exibir as informações do patrimônio
        id_linha = df[(df['num patrimonio'] == id) | (df['tombo_antigo'] == id) | (df['serie_total'] == id)]            
        if id_linha.empty:
            st.warning(f"Identificação {id} não encontrada, verifique a etiqueta ou se o material é de outra UG.")
            adicionar_de_outra_ug = st.button("Adicionar de Outra UG")
            if adicionar_de_outra_ug:
                # Inserir linha ao df com o numero de patrimonio no indice e as colunas 'inventariado', 'horario_inventário', 'local_inventario' preenchidas
                df.loc[id] = {
                    'num patrimonio': id,
                    'denominacao': 'Material de outra UG',
                    'tombo_antigo': None,
                    'serie_total': None,
                    'localidade': st.session_state['localidade_selecionada'],
                    'status': None,
                    'marca_total': None,
                    'modelo_total': None,
                    'ultimo levantamento': data_inventario,
                    'especificacoes': None,
                    'inventariado': 'sim',
                    'horario_inventário': dt.datetime.now(),
                    'local_inventario': st.session_state['localidade_selecionada']}

                st.success(f"Patrimônio {id} adicionado de outra UG.")
        elif len(id_linha) == 1:
            st.subheader("Patrimônio Encontrado")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**Nº Patrimônio:** {id_linha['num patrimonio'].values[0]}")
                st.write(f"**Tombo Antigo:** {id_linha['tombo_antigo'].values[0]}")
                st.write(f"**Nº Serial:** {id_linha['serie_total'].values[0]}")
            with col2:
                st.write(f"**Denominação:** {id_linha['denominacao'].values[0]}")
                st.write(f"**Localidade atual:** {id_linha['localidade'].values[0]}")
                st.write(f"**Acautelado para:** {id_linha['acautelado para'].values[0]}")
            with col3:
                st.write(f"**Marca:** {id_linha['marca_total'].values[0]}")
                st.write(f"**Modelo:** {id_linha['modelo_total'].values[0]}")
                st.write(f"**Último levantamento:** {id_linha['ultimo levantamento'].values[0]}")
            with col4:
                st.write(f"**Status:** {id_linha['status'].values[0]}")
                st.write(f"**Descrição:** {id_linha['especificacoes'].values[0]}")
        elif len(id_linha) > 1:
            st.write('**Mais de um patrimônio encontrado:** Escolha uma das opções abaixo:')
            for index, row in id_linha.iterrows():
                #adicionar um checkbox para cada linha encontrada
                col_check, col_info = st.columns([0.1, 0.9])
                with col_check:
                    if st.checkbox(f"Selecionar {row['num patrimonio']}", key=f"check_{index}"):
                        st.session_state['patrimonio_selecionado'] = row['num patrimonio']
                with col_info:
                    st.write(f"**Descrição:** {row['denominacao']}")
                    st.write(f"**Nº Patrimônio:** {row['num patrimonio']}")
                    st.write(f"**Tombo Antigo:** {row['tombo_antigo']}")
                    st.write(f"**Nº Serial:** {row['serie_total']}")
                    st.write(f"**Localidade atual:** {row['localidade']}")
                    st.write(f"**Marca:** {row['marca_total']}")
                    st.write(f"**Modelo:** {row['modelo_total']}")
                    st.write(f"**Último levantamento:** {row['ultimo levantamento']}")
                    st.write(f"**Status:** {row['status']}")
                    st.write(f"**Descrição:** {row['especificacoes']}")
            # se for marcado o checkbox, adicionar à lista de inventário
                
        # adicionar à coluna 'inventariado' = 'sim' no banco de dados
        df.loc[id, 'inventariado'] = 'sim'
        # adicionar à coluna 'horario_inventário' = datetime no banco de dados
        df.loc[id, 'horario_inventário'] = dt.datetime.now()
        # adicionar à coluna 'local_inventario' = localidade no banco de dados
        df.loc[id, 'local_inventario'] = st.session_state['localidade_selecionada']
        # Se encontrado, exibir informações e botão para adicionar ao inventário
        pass
    
    # Buscar materiais sem patrimônio nãop inventariado spor suas características
    caracteristicas = st.text_input("Buscar por características")
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
    if material_selecionado:
        st.subheader("Leitura de Serial (se necessário)")
        for index, row in df_inventario.iterrows():
            if row['Tipo'] == 'TIC' and pd.isna(row['Numero_Serie']):
                st.write(f"**{row['Descrição']} (TIC sem Serial)**")
                novo_serial = st.text_input(f"Ler Serial para {row['Descrição']}", key=f"serial_{index}")
                if novo_serial:
                    st.write(f"Serial lido: {novo_serial}")
                    # Adicionar lógica para atualizar o número de série no inventário
                    # ou no banco de dados, se já estiver sendo persistido
                    pass

    st.subheader("Bens Levantados")
    df_inventario = df[df['local_inventario'] == st.session_state['localidade_selecionada']]
    df_inventario = df_inventario[['num patrimonio', 'denominacao', 'tombo_antigo', 'serie_total', 'localidade', 'status', 'marca_total', 'modelo_total', 'ultimo levantamento', 'especificacoes']]
    if not df_inventario.empty:
        st.dataframe(df_inventario)
        st.subheader("Imprimir/Substituir Etiqueta")
        for index, row in df_inventario.iterrows():
            st.write(f"**{row['Descrição']}**")
            col_print = st.checkbox("Emitir Etiqueta", value=True, key=f"print_{index}")
            if col_print:
                st.write("Opções de impressão/substituição...") # Adicione a lógica de impressão aqui
    else:
        st.info("Nenhum bem foi adicionado ao inventário ainda.")
    
    st.subheader("Adicionar Bens Acautelados")
    adicionar_acautelados = st.radio("Adicionar bens acautelados", ["Sim", "Não"], key="acautelados")
    if adicionar_acautelados == "Não":
        if st.button("Concluir Levantamento"):
            st.success("Levantamento concluído!")
            # Adicionar lógica para salvar os dados do inventário no banco de dados
    else:
        st.warning("Marque 'Não' para adicionar bens acautelados e habilitar a conclusão.")

    # Listar bens a inventariar
    st.subheader("Bens a Inventariar")
    df_localidade = df[df['localidade'] == st.session_state['localidade_selecionada']]
    df_localidade = df_localidade[df_localidade['inventariado'] == 'não']
    df_localidade = df_localidade[['num patrimonio', 'denominacao', 'tombo_antigo', 'serie_total', 'localidade', 'status', 'marca_total', 'modelo_total', 'ultimo levantamento', 'especificacoes']]
    st.dataframe(df_localidade)

    

if __name__ == "__main__":
    
    """if 'autenticado' not in st.session_state or not st.session_state['autenticado']:
        tela_credenciais()
    else:
        tela_input_dados()"""
    # Para fins de teste, vamos chamar a tela de input de dados diretamente
    tela_input_dados()
    # A autenticação deve ser implementada antes de chamar a função de input de dados