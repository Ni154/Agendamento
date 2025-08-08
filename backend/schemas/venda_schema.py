from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class VendaItemBase(BaseModel):
    tipo: str = Field(..., description="Tipo do item: produto ou servico")
    item_id: int = Field(..., description="ID do produto ou serviço")
    quantidade: int = Field(..., gt=0)
    preco: float = Field(..., gt=0)

class VendaItemCreate(VendaItemBase):
    pass

class VendaItemRead(VendaItemBase):
    id: int

    class Config:
        orm_mode = True

class VendaBase(BaseModel):
    cliente_id: int
    data: date
    forma_pagamento: Optional[str] = None

class VendaCreate(VendaBase):
    itens: List[VendaItemCreate]

class VendaRead(VendaBase):
    id: int
    total: float
    cancelada: bool
    itens: List[VendaItemRead]

    class Config:
        orm_mode = True

