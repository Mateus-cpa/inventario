import os
from datetime import datetime as dt
import time
from random import randint


from sqlalchemy import create_engine, Column, Integer, String #type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore
from sqlalchemy.orm import sessionmaker #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from dotenv import load_dotenv #type: ignore

load_dotenv()

usuario = os.getenv("DATABASE_USER")
senha = os.getenv("DATABASE_PASSWORD")

if usuario and senha:
    print(f"Importação Usuário e Senha: OK")
else:
    print("Variáveis DATABASE_USER ou DATABASE_PASSWORD não definidas no .env")

Base = declarative_base()

class Levantamento(Base):
    __tablename__ = "levantamento"
    num_tombamento = Column(Integer, primary_key=True)
    local_inventario = Column(String)
    horario_inventario = Column(String)
    user = Column(String)

engine = create_engine("sqlite:///teste_levantamento.db", echo=True)
print("Conexão com o banco local estabelecida com sucesso!")
#engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@host:5432/inventario", echo=True)
#print("Conexão com o PostgreSQL estabelecida com sucesso!")

locais = ["Local A", "Local B", "Local C", "Local D", "Local E"]
users = ["getulio.gqw", "fernando.sdfe", "mateus.marg", "flavio.fswf", 'domingues.qdd',"eduardo.serf"]
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
#Conecta na base para pegar o último patrimônio cadastrado
connection = engine.connect()
cursor = connection.connection.cursor()
cursor.execute("SELECT num_tombamento FROM levantamento ORDER BY num_tombamento DESC LIMIT 1")
patrimonio = cursor.fetchone()
cursor.close()
if patrimonio != None:
    patrimonio = patrimonio[0]
else:
    patrimonio = 2010220001

#Cadastra levantamentos aleatórios
levantamento = []
for i in range (1, 30):
    levantamento.append(Levantamento(
        num_tombamento=patrimonio + i,
        local_inventario=locais[randint(0, 4)],
        horario_inventario=dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        user=users[randint(0, 5)]
    ))
    time.sleep(1)
    patrimonio += i
print(levantamento)
# Adicionando o levantamento à sessão e commitando
try:
    with Session() as session:
        session.add_all(levantamento)
        session.commit()
except SQLAlchemyError as e:
    print(f"Erro ao adicionar levantamento: {e}")
    