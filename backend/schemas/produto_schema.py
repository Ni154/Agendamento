
from pydantic import BaseModel, Field
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str = Field(..., description="Nome do produto")
    quantidade: int = Field(..., ge=0, description="Quantidade em estoque")
    preco_venda: float = Field(..., ge=0, description="Preço de venda")

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str]
    quantidade: Optional[int]
    preco_venda: Optional[float]

class ProdutoRead(ProdutoBase):
    id: int

    class Config:
        orm_mode = True
