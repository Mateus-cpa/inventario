from controller import cadastrar_levantamento
from fastapi import FastAPI, HTTPException, Depends #type: ignore
import models
from sqlalchemy.orm import Session #type: ignore

#apenas durante testes de lançamento
from random import randint 
import time 
from datetime import datetime as dt
from sqlalchemy import create_engine #type: ignore 
from db import Base
from schema import LevantamentoSchema, LevantamentoCreate


app = FastAPI()

models.Base.metadata.create_all(bind=Base.engine)

@app.post("/id/", response_model = id)
def criar_levantamento_aleatorio_e_cadastrar(id: LevantamentoCreate, db: Session = Depends(Base)):    
    engine = create_engine("sqlite:///teste_levantamento.db", echo=True)
    Base.metadata.create_all(engine)  # Cria as tabelas no banco de dados
    #Preparar dados aleatórios para incluir no banco
    locais = ["Local A", "Local B", "Local C", "Local D", "Local E"]
    users = ["getulio.gqw", "fernando.sdfe", "mateus.marg", "flavio.fswf", 'domingues.qdd',"eduardo.serf"]
    connection = engine.connect() #Conecta na base para pegar o último patrimônio cadastrado
    cursor = connection.connection.cursor()
    cursor.execute("SELECT num_tombamento FROM levantamento ORDER BY id DESC LIMIT 1")
    patrimonio = cursor.fetchone()
    cursor.close()
    if patrimonio is None:
        patrimonio = 2010220001  # Valor inicial se não houver registros
    else:
        patrimonio = patrimonio[0]
    
    #Cria lista de levantamentos aleatórios
    
    for i in range (1, 30):
        levantamento_schema = LevantamentoSchema(
            num_tombamento=patrimonio + randint(0,100),
            local_inventario=locais[randint(0, 4)],
            horario_inventario=dt.now(),
            user=users[randint(0, 5)]
        )
        cadastrar_levantamento(levantamento_schema)
        time.sleep(1)
        patrimonio += i
    


if __name__ == "__main__":
    criar_levantamento_aleatorio_e_cadastrar()
    #cadastrar_levantamento(levantamento_schema)
    print('itens cadastrados com sucesso!')
