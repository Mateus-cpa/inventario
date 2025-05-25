#funções executadas
from db import SessionLocal
from models import Levantamento
from schema import LevantamentoSchema


def cadastrar_levantamento(levantamento: LevantamentoSchema):
    """
    Cadastra um levantamento no banco de dados.
    """
    with SessionLocal() as db:
        novo_levantamento = Levantamento(**levantamento.dict())
        db.add(novo_levantamento)
        db.commit()
        db.refresh(novo_levantamento)
    return levantamento