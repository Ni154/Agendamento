from pydantic import BaseModel
from typing import List, Optional

class VendaItemBase(BaseModel):
    tipo: str  # "produto" ou "servico"
    item_id: int
    quantidade: int
    preco: float

class VendaItemCreate(VendaItemBase):
    pass

class VendaItemResponse(VendaItemBase):
    id: int

    class Config:
        orm_mode = True

class VendaBase(BaseModel):
    cliente_id: int
    forma_pagamento: Optional[str] = None

class VendaCreate(VendaBase):
    itens: List[VendaItemCreate]

class VendaResponse(VendaBase):
    id: int
    data: str
    total: float
    cancelada: bool
    itens: List[VendaItemResponse]

    class Config:
        orm_mode = True
