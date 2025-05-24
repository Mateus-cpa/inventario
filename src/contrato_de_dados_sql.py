import requests #type: ignore
from pydantic import BaseModel #type: ignore

class LevantamentoSchema(BaseModel):
    num_tombamento: int
    local_inventario: str
    horario_inventario: str
    user: str

    class Config:
        orm_mode = True

def cadastrar_levantamento(levantamento: LevantamentoSchema):
    """
    Cadastra um levantamento no banco de dados.
    """
    try:
        response = requests.post("http://localhost:8000/levantamento/", json=levantamento.dict())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao cadastrar levantamento: {e}")
        return None

if __name__ == "__main__":
    # Exemplo de uso
    levantamento = LevantamentoSchema(
        num_tombamento=2010220001,
        local_inventario="Local A",
        horario_inventario="2023-10-01 12:00:00",
        user="getulio.gqw"
    )
    resultado = cadastrar_levantamento(levantamento)
    if resultado:
        print("Levantamento cadastrado com sucesso:", resultado)
    else:
        print("Falha ao cadastrar levantamento.")