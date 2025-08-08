from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class DespesaBase(BaseModel):
    data: date = Field(..., description="Data da despesa")
    descricao: str = Field(..., description="Descrição da despesa")
    valor: float = Field(..., gt=0, description="Valor da despesa")

class DespesaCreate(DespesaBase):
    pass

class DespesaUpdate(BaseModel):
    data: Optional[date]
    descricao: Optional[str]
    valor: Optional[float]

class DespesaRead(DespesaBase):
    id: int

    class Config:
        orm_mode = True

