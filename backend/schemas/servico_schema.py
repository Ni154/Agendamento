from pydantic import BaseModel, Field
from typing import Optional

class ServicoBase(BaseModel):
    nome: str = Field(..., description="Nome do serviço")
    unidade: str = Field(..., description="Unidade (ex: sessão)")
    quantidade: int = Field(..., ge=0, description="Quantidade disponível")
    valor: float = Field(..., ge=0, description="Valor do serviço")

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    nome: Optional[str]
    unidade: Optional[str]
    quantidade: Optional[int]
    valor: Optional[float]

class ServicoRead(ServicoBase):
    id: int

    class Config:
        orm_mode = True

