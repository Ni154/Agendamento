from pydantic import BaseModel
from typing import Optional

class AgendamentoBase(BaseModel):
    cliente_id: int
    data: str
    hora: str
    servicos: Optional[str] = None
    status: Optional[str] = "pendente"

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(BaseModel):
    data: Optional[str] = None
    hora: Optional[str] = None
    servicos: Optional[str] = None
    status: Optional[str] = None

class AgendamentoOut(AgendamentoBase):
    id: int

    class Config:
        orm_mode = True
