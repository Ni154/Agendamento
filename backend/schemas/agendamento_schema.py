from pydantic import BaseModel
from typing import Optional

class AgendamentoBase(BaseModel):
    cliente_id: int
    data: str  # ISO format: "YYYY-MM-DD"
    hora: str  # "HH:MM"
    servicos: str  # pode ser uma lista serializada, aqui string
    status: Optional[str] = "Pendente"

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(BaseModel):
    data: Optional[str]
    hora: Optional[str]
    servicos: Optional[str]
    status: Optional[str]

class AgendamentoRead(AgendamentoBase):
    id: int

    class Config:
        orm_mode = True

