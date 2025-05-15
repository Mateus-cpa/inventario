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
    print(f"Importação Usuário e Senha: OK")
else:
    print("Variáveis DATABASE_USER ou DATABASE_PASSWORD não definidas no .env")

class Levantamento(SQLModel, table=True):
    num_tombamento: int = Field(default=None, primary_key=True)
    local_inventario: str
    horario_inventario: str

#engine = create_engine("sqlite:///teste_levantamento.db", echo=True)
engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@host:5432/inventario", echo=True)
#print("Conexão com o PostgreSQL estabelecida com sucesso!")



locais = ["Local A", "Local B", "Local C", "Local D", "Local E"]

SQLModel.metadata.create_all(engine)

#pegar o ultimo patrimonio em teste_levantamento.db e salvar na variavel patrimonio
connection = engine.connect()
cursor = connection.connection.cursor()  # Use connection.connection to access the raw DB-API connection
cursor.execute("SELECT num_tombamento FROM levantamento ORDER BY num_tombamento DESC LIMIT 1")
patrimonio = cursor.fetchone()
cursor.close()
if patrimonio != None:
    patrimonio = patrimonio[0]
else:
    patrimonio = 2010220001
print(f"Ultimo patrimonio: {patrimonio}")

for i in range (1, 20):
    x= i
    levantamento = Levantamento(num_tombamento=patrimonio+x, 
                                local_inventario=locais[randint(0, 4)], 
                                horario_inventario=dt.now().strftime("%H:%M:%S"))
    with Session(engine) as session:
        session.add(levantamento)
        session.commit()
    time.sleep(1)


