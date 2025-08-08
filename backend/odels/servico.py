
from pydantic import BaseModel, Field
from typing import Optional

class ServicoBase(BaseModel):
    nome: str = Field(..., example="Depilação facial")
    unidade: str = Field(..., example="sessão")
    quantidade: int = Field(..., ge=0, example=5)
    valor: float = Field(..., ge=0, example=120.00)

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(ServicoBase):
    pass

class ServicoDB(ServicoBase):
    id: int

    class Config:
        orm_mode = True
