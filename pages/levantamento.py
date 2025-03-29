import streamlit as st
import pandas as pd
import datetime

# --- Simulação de Dados e Funções ---
# Substitua por sua lógica real de conexão com o banco de dados

def obter_localidades():
    return ["Prédio Administrativo", "Almoxarifado", "Laboratório A", "Nova Localidade"]

def buscar_patrimonios_nao_inventariados(ano, localidade, caracteristicas=None):
    # Simulação de busca no banco de dados
    data = {
        'Descrição': ['Computador Dell', 'Monitor LG', 'Impressora HP'],
        'Local': ['Prédio Administrativo', 'Laboratório A', 'Almoxarifado'],
        'Unidade': ['Setor TI', 'Laboratório', 'Almoxarifado'],
        'Ultimo_Inventario': [2023, 2023, 2022],
        'Numero_Serie': ['ABC12345', None, 'XYZ78901'],
        'Tipo': ['TIC', 'TIC', 'Não TIC']
    }
    df = pd.DataFrame(data)
    df = df[df['Local'] == localidade]
    df = df[df['Ultimo_Inventario'] < ano]
    if caracteristicas:
        df = df[df['Descrição'].str.contains(caracteristicas, case=False)]
    return df

def adicionar_ao_inventario(item):
    st.session_state['inventario'].append(item)
    if 'patrimonios_nao_inventariados' in st.session_state:
        st.session_state['patrimonios_nao_inventariados'] = st.session_state['patrimonios_nao_inventariados'][
            ~st.session_state['patrimonios_nao_inventariados']['Descrição'].isin([item['Descrição']])
        ]

def obter_dados_inventario_atual():
    if 'inventario' in st.session_state:
        return pd.DataFrame(st.session_state['inventario'])
    return pd.DataFrame()

# --- Tela de Input de Dados ---
def tela_input_dados():
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
        data_inventario = st.date_input("Data do Inventário", datetime.date.today())
        acompanhante = st.text_input("Acompanhante")

    st.subheader("Inserir Dados do Patrimônio")
    opcao_busca = st.radio("Buscar por", ["Número Serial", "Patrimônio Antigo", "Patrimônio Novo", "Características"], key="opcao_busca")

    if opcao_busca == "Número Serial":
        numero_serial = st.text_input("Número Serial")
        if numero_serial:
            st.info(f"Buscar patrimônio com Número Serial: {numero_serial}")
            # Adicionar lógica para buscar por número serial no banco de dados
            # Se encontrado, exibir informações e botão para adicionar ao inventário
            pass
    elif opcao_busca == "Patrimônio Antigo":
        patrimonio_antigo = st.text_input("Patrimônio Antigo")
        if patrimonio_antigo:
            st.info(f"Buscar patrimônio com Patrimônio Antigo: {patrimonio_antigo}")
            # Adicionar lógica para buscar por patrimônio antigo no banco de dados
            # Se encontrado, exibir informações e botão para adicionar ao inventário
            pass
    elif opcao_busca == "Patrimônio Novo":
        patrimonio_novo = st.text_input("Patrimônio Novo")
        if patrimonio_novo:
            st.info(f"Buscar patrimônio com Patrimônio Novo: {patrimonio_novo}")
            # Adicionar lógica para buscar por patrimônio novo no banco de dados
            # Se encontrado, exibir informações e botão para adicionar ao inventário
            pass
    elif opcao_busca == "Características":
        caracteristicas = st.text_input("Características para Filtro")
        if st.button("Buscar Patrimônios"):
            if st.session_state['localidade_selecionada']:
                ano_atual = datetime.date.today().year
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

    st.subheader("Bens Levantados")
    df_inventario = obter_dados_inventario_atual()
    if not df_inventario.empty:
        st.dataframe(df_inventario)
        st.subheader("Imprimir/Substituir Etiqueta")
        for index, row in df_inventario.iterrows():
            st.write(f"**{row['Descrição']}**")
            col_print = st.checkbox("Emitir Etiqueta", value=True, key=f"print_{index}")
            if col_print:
                st.write("Opções de impressão/substituição...") # Adicione a lógica de impressão aqui

        if not df_inventario.empty:
            st.subheader("Adicionar Bens Acautelados")
            adicionar_acautelados = st.radio("Adicionar bens acautelados", ["Sim", "Não"], key="acautelados")
            if adicionar_acautelados == "Não":
                if st.button("Concluir Levantamento"):
                    st.success("Levantamento concluído!")
                    # Adicionar lógica para salvar os dados do inventário no banco de dados
            else:
                st.warning("Marque 'Não' para adicionar bens acautelados e habilitar a conclusão.")
    else:
        st.info("Nenhum bem foi adicionado ao inventário ainda.")

    # Campo para leitura de serial se for TIC e não tiver serial
    if not df_inventario.empty:
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

if __name__ == "__main__":
    if 'autenticado' not in st.session_state or not st.session_state['autenticado']:
        tela_credenciais()
    else:
        tela_input_dados()