from pydantic import BaseModel
from decimal import Decimal

class ServicoIn(BaseModel):
    nome: str
    valor: Decimal = 0

class ServicoOut(BaseModel):
    id: str
    nome: str
    valor: Decimal
    class Config:
        from_attributes = True

