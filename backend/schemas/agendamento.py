from pydantic import BaseModel

class AgendamentoIn(BaseModel):
    cliente_id: str
    data: str
    status: str = "pendente"

class AgendamentoOut(BaseModel):
    id: str
    cliente_id: str
    data: str
    status: str
    class Config:
        from_attributes = True

