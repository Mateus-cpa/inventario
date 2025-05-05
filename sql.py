#from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine #type: ignore

class Levantamento(SQLModel, table=True):
    num_tombamento: int = Field(default=None, primary_key=True)
    local_inventario: str
    horario_inventario: str

engine = create_engine("sqlite:///teste_levantamento.db", echo=True)

SQLModel.metadata.create_all(engine)

levantamento1 = Levantamento(num_tombamento=1, local_inventario="Local A", horario_inventario="10:00")
levantamento2 = Levantamento(num_tombamento=2, local_inventario="Local B", horario_inventario="11:00")
levantamento3 = Levantamento(num_tombamento=3, local_inventario="Local C", horario_inventario="12:00")

with Session(engine) as session:
    session.add(levantamento1)
    session.add(levantamento2)
    session.add(levantamento3)
    session.commit()

