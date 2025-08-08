from pydantic import BaseModel, Field
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str = Field(..., example="Cera depilatória")
    quantidade: int = Field(..., ge=0, example=10)
    preco_venda: float = Field(..., ge=0, example=59.90)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoDB(ProdutoBase):
    id: int

    class Config:
        orm_mode = True

