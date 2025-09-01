from pydantic import BaseModel
from decimal import Decimal

class ProdutoIn(BaseModel):
    nome: str
    sku: str | None = None
    preco: Decimal = 0

class ProdutoOut(BaseModel):
    id: str
    nome: str
    sku: str | None = None
    preco: Decimal
    class Config:
        from_attributes = True

