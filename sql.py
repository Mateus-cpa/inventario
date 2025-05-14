#from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine #type: ignore
from sqlalchemy import create_engine #type: ignore
import os
from dotenv import load_dotenv #type: ignore /// carrega dados de .env para variáveis de ambiente
from datetime import datetime as dt #type: ignore
import time
from random import randint

load_dotenv()

usuario = os.getenv("DATABASE_USER")
senha = os.getenv("DATABASE_PASSWORD")

if usuario and senha:
    print(f"Usuário: OK, Senha: OK")
else:
    print("Variáveis DATABASE_USER ou DATABASE_PASSWORD não definidas no .env")

class Levantamento(SQLModel, table=True):
    num_tombamento: int = Field(default=None, primary_key=True)
    local_inventario: str
    horario_inventario: str

engine = create_engine("sqlite:///teste_levantamento.db", echo=True)
#engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@host:5432/inventario", echo=True)
#print("Conexão com o PostgreSQL estabelecida com sucesso!")

#conn =

SQLModel.metadata.create_all(engine)

locais = ["Local A", "Local B", "Local C", "Local D", "Local E"]
patrimonio = 2010220039
for i in range (0, 10):
    x= i+i
    levantamento = Levantamento(num_tombamento=patrimonio+x, 
                                local_inventario=locais[randint(0, 4)], 
                                horario_inventario=dt.now().strftime("%H:%M:%S"))
    with Session(engine) as session:
        session.add(levantamento)
        session.commit()
    time.sleep(1)


