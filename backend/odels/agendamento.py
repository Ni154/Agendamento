from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class AgendamentoBase(BaseModel):
    cliente_id: int
    data: date
    hora: str  # horário como string "HH:MM"
    servicos: str  # lista serviços separados por vírgula (como no seu código original)
    status: Optional[str] = "agendado"

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(BaseModel):
    data: Optional[date]
    hora: Optional[str]
    servicos: Optional[str]
    status: Optional[str]

class AgendamentoDB(AgendamentoBase):
    id: int

    class Config:
        orm_mode = True

