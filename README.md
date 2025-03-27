# Projeto de Tratamento de Dados Patrimoniais

## Estrutura do Projeto

Este projeto utiliza Streamlit para criar uma aplicação web que permite:

* Visualizar a situação do levantamento patrimonial (inventário).
* Cadastrar levantamentos in loco.
* Exportar dados em txt para carga no eLog

## Tecnologias

* Python
* Streamlit
* Pandas
* SQLite (ou outro banco de dados SQL)
* Docker (nao implementado na primeira etapa)

## Pré-requisitos

* Python 3.7+
* Pip

## Instalação

1.  Clone o repositório:

    ```bash
    git clone git@github.com:Mateus-cpa/inventario.git
    cd <nome_do_repositório>
    ```

2.  Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate # No Linux/macOS
    venv\Scripts\activate # No Windows
    ```

3.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Execução

1.  Execute o aplicativo Streamlit:

    ```bash
    streamlit run app.py
    ```

2.  Acesse o aplicativo no seu navegador: `http://localhost:8501`

