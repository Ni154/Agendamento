from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class VendaItemModel(BaseModel):
    tipo: str  # "produto" ou "servico"
    item_id: int
    quantidade: int = Field(..., gt=0)
    preco: float = Field(..., gt=0)

class VendaModel(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    data: date
    total: Optional[float] = 0.0
    cancelada: Optional[bool] = False
    forma_pagamento: Optional[str] = None
    itens: List[VendaItemModel] = []

