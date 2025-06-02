import streamlit as st #type: ignore
import pandas as pd #type: ignore
#from tqdm import tqdm
import os
from datetime import datetime, timedelta
import json

# Funções utilitárias (copiadas do seu tratamento.py)
def pega_tamanho_em_mb(caminho: str):
    return os.path.getsize(caminho) / (1024 * 1024)

def ler_arquivo_xlsx_com_progresso_streamlit(uploaded_file):
    resultados = {}
    tamanho_inicial = uploaded_file.size / (1024 * 1024)
    resultados['tamanho_inicial_mb'] = tamanho_inicial
    with open('data_bronze/resultados.json', 'w') as f:
        json.dump(resultados, f, indent=4)
    # Lê o arquivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='calamine')
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None
    return df

def repor_virgula_por_ponto(valor):
    if isinstance(valor, str):
        novo_valor = valor.replace('.', '').replace(',', '.')
        return novo_valor
    else:
        return valor

# (Cole aqui as funções processa_planilha, salva_estatisticas_levantamento, salva_dataframe, adaptando para uso com Streamlit)

def processa_planilha(df):    
    with open('data_bronze/resultados.json', 'r') as f:
        resultados = json.load(f)
    resultados['qtde_colunas_inicial'] = df.shape[1]
    resultados['qtde_de_linhas_inicial'] = df.shape[0]
    st.write(f'Quantidade de linhas: {resultados["qtde_de_linhas_inicial"]}')
    st.write(f'Quantidade inicial de colunas: {resultados['qtde_colunas_inicial']}')
    st.write(f'Lista de colunas: {df.columns.tolist()}')
    
 
    #checar se colunas de números de série existem na planilha
    cols_to_check = ['imei','n de serie', 'numero de serie',
                'numero de serie.1', 'numero de serie  ',
                 'num serie', 'placa', 'placa  ', 'placa vinculada',
                 'placa oficial', 'placa ','numero de serie.2',
                 'n  serie', ' placa ',  ' serie', 'serie',
                  'n  serie.1', 'numero de serie.3','numero serie']
    existing_serie_cols = [col for col in cols_to_check if col in df.columns]
    #resultados['colunas_existentes_numeros_serie'] = [existing_serie_cols]

    #checar se colunas de modelo existem na planilha
    cols_to_check = ['modelo', 'modelo  ', 'modelo    ', 
                     'modelo1', 'modelo.1', 'modelo ']
    existing_modelo_cols = [col for col in cols_to_check if col in df.columns]
    #resultados['existing_modelo_cols'] = [existing_modelo_cols]
    
    # checar se colunas de marca existem na planilha
    cols_to_check = ['marca','marca.1', 'marca1']
    existing_marca_cols = [col for col in cols_to_check if col in df.columns]
    #resultados['existing_marca_cols'] = [existing_marca_cols]
    
    #checar se colunas de tombo antigo existem na planilha
    cols_to_check = ['tombo antigo', 'tombo antigo.1']
    existing_tombo_antigo_cols = [col for col in cols_to_check if col in df.columns]
    #resultados['existing_tombo_antigo_cols'] = [existing_tombo_antigo_cols]

    # checar se colunas de especificações na planilha
    cols_to_check = ['observacao bloqueio', 'matriz', 'qtd de rodas',
                'acabamento da estrutura', 'altura', 'ano de fabricacao',
                'ano do modelo', 'aplicacao', 'bordas', 'calibre', 'calibre  ',
                'carga', 'data de validade', 'destino', 'genero', 'largura',
                'lote  numeros e letras sem espacos e caracteres especiais ',
                'material', 'material do assento e encosto',
                'material revestimento assento e encosto',
                'memoria de armazenamento', 'necessita ser substituido', 'nivel de protecao',
                'numero de chassis', 'numero de raias',
                    'num serie  chassis',
                'ostensivo', 'profundidade', 'qtd de gavetas',
                'qtd de passageiros', 'qtd de portas', 'renavam',
                'sentido das raias', 'servidor responsavel', 'tamanho  novo ',
                'tipo de veiculo', 'alcance',
                'ano de fabricacao.1', 'aplicacao.1', 'blindagem', 'calibre.1',
                'capacidade', 'capacidade de tiros', 'combustivel',
                'compartimento cela', 'contraste', 'cor', 'cor predominante',
                'dimensao', 'espaco disco rigido', 'faixa de operacao',
                'frequencia', 'heavy duty', 'impedancia', 'interface',
                'largura de leitura', 'material.1', 'material da estrutura',
                'meio de aquisicao', 'numero de portas',
                'padrao de leitura', 'peso',
                'polegadas', 'potencia', 'potencia  cv ', 'qtd de canais',
                'qtd de nivel', 'qtd memoria ram', 'resolucao', 'revestimento',
                'tamanho da tela', 'taxa de transferencia', 'tensao',
                'tensao de alimentacao', 'tipo', 'tipo de identificacao',
                'tipo de propriedade', 'velocidade de varredura', 'voltagem',
                'zoom otico', 'nivel de protecao da placa', 'tipo do monitor',
                'carga.1',	'classe',	'portas',	'tanque',	'velocidade',
                'volume', 'bitola do pneu', 'numero do registro', 'qtde de canais',
                'nome da embarcacao', 'numero de registro','tipo de veiculo.1',
                'descritor especial','temporario','referencia do cartucho',
                'versao', 'aplicacao.2','material de fabricacao',
                 'peso.1', 'potencia.1', 'tamanho da maleta',
                 'velocidade de impressao', 'voltagem.1']
    existing_especificacoes_cols = [col for col in cols_to_check if col in df.columns]
    #resultados['existing_especificacoes_cols'] = [existing_especificacoes_cols]

    # criar coluna de serie que compilará os demais números de série
    df['serie_total'] = None
    df['modelo_total'] = None
    df['especificacoes'] = None
    df['tombo_antigo'] = None
    df['marca_total'] = None

    #lista_colunas_exibir = ['denominacao','serie_total', 'modelo_total', 'tombo_antigo', 'marca_total', 'especificacoes']

    #define as funções
    def create_especificacoes(row):
        especificacoes = {}
        for col in existing_especificacoes_cols:
            if col in row and not pd.isna(row[col]):
                especificacoes[col] = row[col]
        return especificacoes

    def compile_series(row, existing_serie_cols):
        lista_numero_series = []
        for col in existing_serie_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                lista_numero_series.append(str(value).strip())

        lista_numero_series = list(set(lista_numero_series))
        return ', '.join(lista_numero_series)

    def compile_modelo(row, existing_modelo_cols):
        lista_modelo = []
        for col in existing_modelo_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                lista_modelo.append(str(value).strip())

        lista_modelo = list(set(lista_modelo))
        return ', '.join(lista_modelo)

    def compile_marca(row, existing_marca_cols):
        lista_marca = []
        for col in existing_marca_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                lista_marca.append(str(value).strip())

        lista_marca = list(set(lista_marca))
        return ', '.join(lista_marca)

    def compile_tombo_antigo(row, existing_tombo_antigo_cols):
        lista_tombo_antigo = []
        for col in existing_tombo_antigo_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                for char in str(value):
                    value = str(value).lstrip('P')
                    value = str(value).lstrip('S')
                    value = str(value).lstrip('0')
                lista_tombo_antigo.append(str(value).strip())

        lista_tombo_antigo = list(set(lista_tombo_antigo))
        return ', '.join(lista_tombo_antigo)

    #chamar as funções
    df['especificacoes'] = df.apply(create_especificacoes, axis=1)
    df['serie_total'] = df.apply(compile_series, axis=1, args=(existing_serie_cols,))
    df['modelo_total'] = df.apply(compile_modelo, axis=1, args=(existing_modelo_cols,))
    df['marca_total'] = df.apply(compile_marca, axis=1, args=(existing_marca_cols,))
    df['tombo_antigo'] = df[existing_tombo_antigo_cols].apply(compile_tombo_antigo, axis=1, args=(existing_tombo_antigo_cols,))

    #exclui as colunas compiladas
    df.drop(columns=existing_tombo_antigo_cols, inplace=True)
    df.drop(columns=existing_modelo_cols, inplace=True)
    df.drop(columns=existing_serie_cols, inplace=True)
    df.drop(columns=existing_marca_cols, inplace=True)
    df.drop(columns=existing_especificacoes_cols, inplace=True)

    # dividir a célula e retornar a última parte após '-' para retitrar a sigla
    df['sigla'] = df['unidade responsavel material'].apply(lambda x: x.split('-')[-1].strip())

   
    
    # salvar dados em resultados
    resultados['qtde_colunas_final'] = df.shape[1]
    resultados['qtde_de_linhas_final'] = df.shape[0]
    with open('data_bronze/resultados.json', 'w') as f:
        json.dump(resultados, f, indent=4) 

    #trazer o tombo novo para a 1ª coluna (para o PROCV do excel)
    df = df.reindex(columns=['num tombamento'] + [col for col in df.columns if col != 'num tombamento'])
    
    #configura índice
    df.set_index('num tombamento', inplace=True, drop=False)
    df.index.name = 'index'    
    if 'num tombamento.1' in df.columns:
        #renomeia a coluna 'num tombamento.1' para 'num_tombamento'
        df.rename(columns={'num tombamento.1': 'num_tombamento'}, inplace=True)

    #transformar colunas em astype(str)
    colunas_astype = ['denominacao', 'especificacoes', 'marca_total', 'modelo_total', 'serie_total']
    df[colunas_astype] = df[colunas_astype].astype(str)
    
    #Preencher campos vazios das colunas
    df['localidade'] = df['localidade'].fillna('Sem localidade') #TypeError: sequence item 0: expected str instance, float found
    df['ultimo levantamento'] = df['ultimo levantamento'].fillna("0000 / 2010")
    df['modelo_total'] = df['modelo_total'].fillna('Sem modelo')
    df['serie_total'] = df['serie_total'].replace('', 'Sem serial cadastrado')
    df['acautelado para'] = df['acautelado para'].replace('','Sem acautelamento')
    
    #Remover coluinas com nome 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    #salvar csv de localidades únicas como lista
    localidades = df['localidade'].unique()
    localidades = pd.Series(localidades, name='localidade')
    pd.concat([localidades,pd.Series(['Nova localidade'])])
    localidades.to_csv('data_bronze/localidades.csv', index=False, header=False)

    
    #trnasforma valores numéricos em float -> '.' => ''' e ',' => '.'
    colunas_valores = ['valor', 'valor entrada', 'valor acumulado', 'valor depreciacao acumulada']
    for col in colunas_valores:
        df[col] = df[col].apply(lambda x: repor_virgula_por_ponto(x))
    
    st.write(f"Quantidade de colunas após processamento: {df.shape[1]}")
    st.write(f"Lista de colunas após processamento: {df.columns.tolist()}")

    if df.shape[1] > 45:
        st.error("O DataFrame resultante tem mais de 45 colunas. Solicite a correção do código.")
        #informa colunas não esperadas
        colunas_nao_esperadas = df.columns.difference(['num tombamento', 'unidade responsavel material', 
                                                       'codigo', 'grupo de material', 'codigo material', 
                                                       'subgrupo de material', 'acautelado para', 'matricula detentor', 
                                                       'validado eletron', 'data assinatura', 'lotacao detentor', 
                                                       'data acautelamento', 'data cadastro', 'denominacao', 
                                                       'especificacao', 'observacao', 'anulado', 'estado bem', 
                                                       'status', 'bem terceiros', 'data balanco', 'data inicio uso', 
                                                       'ano balanco', 'garantia', 'data fabricacao', 'data validade', 
                                                       'localidade', 'ultimo levantamento', 'unidade tombamento', 
                                                       'valor', 'valor entrada', 'valor acumulado', 'depreciavel', 
                                                       'valor depreciacao acumulada', 'data ultimo ajuste', 'vida util',
                                                         'vida util base depreciacao', 'data ultimo ajuste depreciacao', 
                                                         'tipo bloqueio', 'serie_total', 'modelo_total', 'especificacoes', 
                                                         'tombo_antigo', 'marca_total', 'sigla'])
        st.write("Colunas não esperadas:")
        st.write(colunas_nao_esperadas.tolist())

    return df


def salva_dataframe(df_processado):
    #df_processado.to_csv('data_bronze/lista_bens-processado.csv')
    #df_processado.to_json('data_bronze/lista_bens-processado.json', orient='records', lines=True)
    df_processado.to_excel('data_bronze/lista_bens-processado.xlsx', engine='openpyxl', index=False)
    with open('data_bronze/resultados.json', 'r') as f:
        resultados = json.load(f)
    resultados['tamanho_final_csv_mb'] = pega_tamanho_em_mb(caminho='data_bronze/lista_bens-processado.csv')
    resultados['tamanho_final_json_mb'] = pega_tamanho_em_mb(caminho='data_bronze/lista_bens-processado.json')
    resultados['tamanho_final_xlsx_mb'] = pega_tamanho_em_mb(caminho='data_bronze/lista_bens-processado.xlsx')
    resultados['data_processamento'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('data_bronze/resultados.json', 'w') as f:
        json.dump(resultados, f, indent=4)
    col1, col2 = st.columns(2)
    col1.download_button(
        label="Baixar planilha processada",
        data=open('data_bronze/lista_bens-processado.xlsx', 'rb'),
        file_name='lista_bens-processado.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    col2.download_button(
        label="Baixar resultados",
        data=open('data_bronze/resultados.json', 'rb'),
        file_name='resultados.json',
        mime='application/json'
    )


# ------------------- STREAMLIT APP -------------------

st.title("Processamento de Listagem geral de bens do eLog")

uploaded_file = st.file_uploader("Selecione o arquivo Excel para processar", type=["xlsx"])

if uploaded_file is not None:
    st.info("Lendo arquivo Excel...")
    df_lista_materiais = ler_arquivo_xlsx_com_progresso_streamlit(uploaded_file)
    if df_lista_materiais is not None:
        st.success("Arquivo lido com sucesso!")
        df_processado = processa_planilha(df_lista_materiais)
        st.success("Planilha processada!")
        st.info("Gerando planilha processada...")
        salva_dataframe(df_processado)
        st.success("Processamento concluído!")
        
else:
    st.warning("Faça upload de um arquivo Excel para começar.")