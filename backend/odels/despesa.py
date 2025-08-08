from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class DespesaBase(BaseModel):
    data: date
    descricao: str
    valor: float = Field(..., gt=0)

class DespesaCreate(DespesaBase):
    pass

class DespesaUpdate(BaseModel):
    data: Optional[date]
    descricao: Optional[str]
    valor: Optional[float]

class DespesaDB(DespesaBase):
    id: int

    class Config:
        orm_mode = True

