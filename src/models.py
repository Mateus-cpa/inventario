#representação do bando de dados
from sqlalchemy import Column, Integer, String, DateTime #type: ignore
from sqlalchemy.sql import func #type: ignore
from db import Base

class Levantamento(Base):
    __tablename__ = "levantamento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    num_tombamento = Column(Integer, nullable=False)
    local_inventario = Column(String, nullable=False)
    horario_inventario = Column(DateTime, server_default=func.now())
    user = Column(String, nullable=False)
