from pydantic import BaseModel
from decimal import Decimal

class VendaIn(BaseModel):
    agendamento_id: str | None = None
    total: Decimal = 0
    status: str = "aberta"

class VendaOut(BaseModel):
    id: str
    agendamento_id: str | None = None
    total: Decimal
    status: str
    class Config:
        from_attributes = True

