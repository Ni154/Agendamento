from pydantic import BaseModel
from typing import Optional

class DespesaBase(BaseModel):
    data: str
    descricao: str
    valor: float

class DespesaCreate(DespesaBase):
    pass

class DespesaUpdate(BaseModel):
    data: Optional[str]
    descricao: Optional[str]
    valor: Optional[float]

class DespesaOut(DespesaBase):
    id: int

    class Config:
        orm_mode = True
