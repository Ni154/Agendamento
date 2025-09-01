from pydantic import BaseModel

class ClienteIn(BaseModel):
    nome: str
    email: str | None = None
    telefone: str | None = None

class ClienteOut(BaseModel):
    id: str
    nome: str
    email: str | None = None
    telefone: str | None = None
    class Config:
        from_attributes = True

