import streamlit as st
import pandas as pd
from menu import ler_base_processada
import os
import datetime as dt
import altair as alt


def pagina_principal(df):
    """Configura as propriedades da página no Streamlit."""
    st.set_page_config(
        page_title='Status da Base Processada',
        page_icon='📊',
        layout='wide'
    )

    #variaveis
    df_ativos = df[df['status'].isin(['EFETIVADO','ACAUTELADO','BEM NÃO LOCALIZADO'])]
    
    # gráfico levantamento geral em relação ao estimado
    st.title('Status da Base Processada')

    col1,col2 = st.columns(2)
    filtro_todos_bens = col1.button('Incluir inativos')
    if filtro_todos_bens:
        df_ativos = df.copy()
    filtro_unidade = col2.multiselect('Filtrar por Unidade: ', df_ativos['sigla'].unique())
    if filtro_unidade:
        df_ativos = df_ativos[df_ativos['sigla'].isin(filtro_unidade)]
    #else:
        #mostrar gráfico de levantamento geral em relação ao estimado
        #ler histórico de levantamentos em data_silver
        # criar reta de estimativa de levantamento por dia sendo 312 por dia a partir de 14/04/2025

    #variável
    qtde_bens_inventariados = df_ativos[df_ativos['ano do levantamento'] == dt.date.today().year].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric('Qtd. de Bens', df_ativos.shape[0])
    #bens inventariados no ano atual
    col2.metric('Qtd. de Bens Inventariados', qtde_bens_inventariados)
    col3.metric('Percentual de Bens Inventariados', f'{round(df_ativos[df_ativos['ano do levantamento'] == dt.date.today().year].shape[0]/df_ativos.shape[0]*100,2)} %')
    
    
    #dataframe de quantidade levantado por ano de levantamento
    st.subheader('Quantidade levantada por ano')
    df_lev = df_ativos.groupby('ano do levantamento').size().reset_index(name='quantidade')
    df_lev['ano do levantamento'] = df_lev['ano do levantamento'].astype(str)
    df_lev = df_lev.sort_values(by='ano do levantamento')
    #gráfico de barras com os anos de levantamento
    chart = alt.Chart(df_lev).mark_bar().encode(
        x=alt.X('ano do levantamento', title='Ano do Levantamento'),
        y=alt.Y('quantidade', title='Quantidade de Bens'),
        color=alt.Color('ano do levantamento', legend=None),
        tooltip=['ano do levantamento', 'quantidade']
    ).properties(
        width=600,
        height=400
    )
    # Adicionar rótulos com os valores
    text = alt.Chart(df_lev).mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('ano do levantamento'),
        y=alt.Y('quantidade'),
        text=alt.Text('quantidade:Q')  # Exibe os valores
    )
    # Combinar o gráfico de barras com os rótulos
    chart_with_text = (chart + text).configure_view(
        fill='white')
    st.altair_chart(chart_with_text, use_container_width=True)
    """Legenda: Último levantamento em 2010 significa que nunca foi inventariado"""
        
    #criar botão de salvar gráfico como imagem em graficos_levantamento com a data atual
    botao_salvar_imagem = st.button('Salvar gráfico como imagem')
    if botao_salvar_imagem:
        chart.save(f'graficos_levantamento/grafico_levantamento_{dt.date.today()}.png')
    st.divider()
    
    # -- Histórico de levantamento --
    st.header('Evolução do Levantamento')
    #pegar os dados de data_silver e concatenar em um dataframe
    df_levantamento_historico = pd.DataFrame()
    for arq in os.listdir('data_silver'):
        if arq.endswith('.json'):
            df_levantamento_parcial = pd.read_json(os.path.join('data_silver', arq)).T
            
            #adicionar coluna de data de levantamento pelo nome do arquivo
            df_levantamento_parcial['data_levantamento'] = arq.split('_')[2].split('.')[0]
            #converter para datetime
            df_levantamento_parcial['data_levantamento'] = pd.to_datetime(df_levantamento_parcial['data_levantamento'], format='%Y-%m-%d')
            #indexar com data, mas somente yyyy-mm-dd
            df_levantamento_parcial['data_levantamento'] = df_levantamento_parcial['data_levantamento'].dt.date
            df_levantamento_parcial['unidade'] = df_levantamento_parcial.index
            
            #transformar data_levantamento em índice
            df_levantamento_parcial.set_index('data_levantamento', drop=True, inplace=True)
            df_levantamento_parcial['perc_levantado'] = df_levantamento_parcial['perc_levantado']*100
            df_levantamento_historico = pd.concat([df_levantamento_historico, df_levantamento_parcial])

    
    # -- Seção evolução do levantamento --
    st.header('Levantamento histórico')
    #criar coluna no dataframe onde inicia com levantamento estimado e vai até o último levantamento somando 320 por dia
    levantamento_diario_estimado = 320
    df_levantamento_historico_geral = df_levantamento_historico[['qtde_levantado','perc_levantado']].groupby('data_levantamento').sum().reset_index()
    for i in range(len(df_levantamento_historico_geral)):
        if i == 0:
            df_levantamento_historico_geral['levantamento_estimado'] = levantamento_diario_estimado
        else:
            df_levantamento_historico_geral['levantamento_estimado'][i] = df_levantamento_historico_geral['levantamento_estimado'][i-1] + levantamento_diario_estimado
    df_levantamento_historico_geral.drop(columns=['perc_levantado'], inplace=True)

    #guardar o valor máximo entre qtde levantada e levantamento estimado
    valor_maximo = df_levantamento_historico_geral[['qtde_levantado','levantamento_estimado']].max().max()

    # criar gráfico de área onde o eixo x é a data de levantamento e o eixo y é a quantidade levantada e a quantidade estimada
    linha_levantamento = alt.Chart(df_levantamento_historico_geral).mark_area(opacity=0.5).encode(
        x=alt.X('data_levantamento:T', title='Data do Levantamento'),
        y=alt.Y('qtde_levantado:Q', title='Quantidade Levantada', scale=alt.Scale(domain=[0, valor_maximo])),
        tooltip=['data_levantamento', 'qtde_levantado']
    ).properties(
        width=800,
        height=400
    )
    # Adicionar a linha de levantamento estimado
    linha_estimativa = alt.Chart(df_levantamento_historico_geral).mark_line(color='red').encode(
        x=alt.X('data_levantamento:T', title='Data do Levantamento'),
        y=alt.Y('levantamento_estimado:Q', title='Levantamento Estimado', scale=alt.Scale(domain=[0, valor_maximo])),
        tooltip=['data_levantamento', 'levantamento_estimado']
    ).properties(
        width=800,
        height=400
    )
    # Adicionar rótulos com os valores da quantidade levantada
    text = alt.Chart(df_levantamento_historico_geral).mark_text(
        align='center',
        baseline='bottom', # Alterado para 'bottom' para posicionar acima da área
        dy=-5  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('data_levantamento:T'),
        y=alt.Y('qtde_levantado:Q'),
        text=alt.Text('qtde_levantado:Q'),  # Exibe os valores
        color=alt.value('black') # Define a cor do texto
    )
    # Mergir os três gráficos (área, linha e texto) e aplicar a configuração de grade
    grafico_levantamento = (linha_levantamento + linha_estimativa + text).configure_axis(
        grid=True
    )
    # Exibir o gráfico no Streamlit
    st.altair_chart(grafico_levantamento, use_container_width=True)
        


    # -- Seção levantamento de cada unidade -- 
    st.header('Levantamento relativo de cada unidade')
    #criar gráfico de linha do tempo onde cada unidade é uma linha e o valor é perc_levantado
    st.subheader('Gráfico de Linha do Tempo por Unidade')

    # Resetar o índice para garantir que as colunas necessárias estejam disponíveis
    df_levantamento_historico_reset = df_levantamento_historico.reset_index()

    col1, col2 = st.columns([0.2, 0.8])
    # retirar dados de levantamnto zerados

    retirar_zerados = col1.button('Retirar levantamentos zerados')
    if retirar_zerados:
        df_levantamento_historico_reset = df_levantamento_historico_reset[df_levantamento_historico_reset['perc_levantado'] > 0]
        st.success('Levantamentos zerados retirados')
    #filtrar por unidade
    filtro_unidade = col2.multiselect('Filtrar por Unidade: ', df_levantamento_historico_reset['unidade'].unique())
    if filtro_unidade:
        df_levantamento_historico_reset = df_levantamento_historico_reset[df_levantamento_historico_reset['unidade'].isin(filtro_unidade)]
    # Criar o gráfico com Altair
    line_chart = alt.Chart(df_levantamento_historico_reset).mark_line().encode(
        x=alt.X('data_levantamento:T', title='Data do Levantamento'),
        y=alt.Y('perc_levantado:Q', title='Percentual Levantado', scale=alt.Scale(domain=[0, 100])),
        color=alt.Color('unidade:N', title='Unidade'),
        tooltip=['data_levantamento', 'unidade', 'perc_levantado']
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        grid=True
    )   
    # Exibir o gráfico no Streamlit
    st.altair_chart(line_chart, use_container_width=True)
    

    st.subheader('Maiores percentuais Levantados')
    # criar rank de unidades com maior percentual levantado na última data de levantamento
    #pegar a última data de levantamento
    ultima_data_levantamento = df_levantamento_historico.index[-1]
    #filtrar o dataframe pela última data de levantamento
    df_ultimo_levantamento = df_levantamento_historico[df_levantamento_historico.index == ultima_data_levantamento]
    #ordenar pelo percentual levantado
    df_ultimo_levantamento = df_ultimo_levantamento.sort_values(by='perc_levantado', ascending=False)
    #pegar as 10 primeiras unidades
    df_ultimo_levantamento = df_ultimo_levantamento.head(10)
    #criar gráfico de barras com as unidades e o percentual levantado
    chart = alt.Chart(df_ultimo_levantamento).mark_bar().encode(
        x=alt.X('unidade:N', title='Unidade'),
        y=alt.Y('perc_levantado:Q', title='Percentual Levantado', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('unidade:N', legend=None),
        tooltip=['unidade', 'perc_levantado']
    ).properties(
        width=600,
        height=400
    )
    # Adicionar rótulos com os valores
    text = alt.Chart(df_ultimo_levantamento).mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('unidade:N'),
        y=alt.Y('perc_levantado:Q'),
        text=alt.Text('perc_levantado:Q')  # Exibe os valores
    )
    # Combinar o gráfico de barras com os rótulos
    chart_with_text = (chart + text).configure_view(
        fill='white')
    st.altair_chart(chart_with_text, use_container_width=True)
    
    # Menores percentuais Levantados
    st.subheader('Menores percentuais Levantados')
    # criar rank de unidades com menor percentual levantado na última data de levantamento
    df_ultimo_levantamento = df_levantamento_historico.sort_values(by='perc_levantado', ascending=True)
    #pegar as 10 primeiras unidades
    df_ultimo_levantamento = df_ultimo_levantamento.head(10)
    #criar gráfico de barras com as unidades e o percentual levantado
    chart = alt.Chart(df_ultimo_levantamento).mark_bar().encode(
        x=alt.X('unidade:N', title='Unidade'),
        y=alt.Y('perc_levantado:Q', title='Percentual Levantado', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('unidade:N', legend=None),
        tooltip=['unidade', 'perc_levantado']
    ).properties(
        width=600,
        height=400
    )
    # Adicionar rótulos com os valores
    text = alt.Chart(df_ultimo_levantamento).mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Ajusta a posição vertical do texto
    ).encode(
        x=alt.X('unidade:N'),
        y=alt.Y('perc_levantado:Q'),
        text=alt.Text('perc_levantado:Q')  # Exibe os valores
    )
    # Combinar o gráfico de barras com os rótulos
    chart_with_text = (chart + text).configure_view(
        fill='white')
    st.altair_chart(chart_with_text, use_container_width=True)

    

if __name__ == '__main__':
    CAMINHO_ARQ_PROCESSADO = 'data_bronze\lista_bens-processado.csv'
    df = ler_base_processada(CAMINHO_ARQ_PROCESSADO)
    pagina_principal(df)