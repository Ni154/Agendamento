from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    quantidade: int
    preco_venda: float

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: str | None = None
    quantidade: int | None = None
    preco_venda: float | None = None

class ProdutoOut(ProdutoBase):
    id: int

    class Config:
        orm_mode = True
