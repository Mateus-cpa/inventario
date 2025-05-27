from typing import Union
from fastapi import FastAPI #type: ignore

app = FastAPI()

@app.get("/")
def read_root():
    return {'Hello': 'World'}

@app.put("/levantamento/{id}")
def read_levantamento():
    #retornar na API o teste_levantamento.db
    return {id: 'teste_levantamento.db'}

@app.get("/items/{item_id}")
def read_item(item_id:int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}

if __name__ == "__main__":
    print(read_item(1, 'teste'))