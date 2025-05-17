from sqlmodel import SQLModel, create_engine, Session #type: ignore
from sqlalchemy import text #type: ignore

#carregando o banco de dados
engine = create_engine("sqlite:///teste_levantamento.db", echo=True)

#criando sessão
with Session(engine) as session:
    # Executando uma consulta SQL
    results = session.exec(text("SELECT local_inventario, count (num_tombamento) FROM levantamento group by local_inventario"))
    local = results.fetchall()
    # Imprimindo os resultados
    for row in local:
        print(row)