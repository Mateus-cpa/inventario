# Projeto de Inventário Patrimonial

## Estrutura do Projeto

Este projeto utiliza Streamlit para criar uma aplicação web que permite:
### 1. Carregar dados brutos do eLog
Nesta etapa será recebida a base de dados em excel exportada pelo eLog e carregada no sistema.

#### 1.1. Salvar na planilha de levantamento (temporário até a migração total)
A base tratada será salva na planilha de levantamento para disponibilizar às equipes até o painel streamlit estar pronto.

### 2. Tratar dados de forma a padronizar independentemente das colunas de entrada

### 3. Carregar base no SQLite

### 4. Visualizar a situação do levantamento patrimonial (inventário)

### 5. Cadastrar levantamentos in loco
- Tela de cadastramento.

### 6. Conciliação eLog
- Exportar dados em txt para carga no eLog.
Serão criados filtros de levantamentos por dia e levantamentos não carregados.
- Verificar bens inventariados por outras UGs

## Tecnologias

* Python
* Streamlit
* Pandas
* SQLite (ou outro banco de dados SQL)
* Docker (não implementado na primeira etapa)

## Pré-requisitos

* Python 3.13.0
* Pip

## Instalação (pyenv)

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

### Com Poetry:
```bash
python -m venv .venv
poetry init
pyenv local 3.13.0
poetry shell
poetry install
.
```

## Execução

1.  Execute o aplicativo Streamlit:

    ```bash
    streamlit run app.py
    ```

2.  Acesse o aplicativo no seu navegador: `http://localhost:8501`

