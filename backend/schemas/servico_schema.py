from pydantic import BaseModel

class ServicoBase(BaseModel):
    nome: str
    unidade: str | None = None
    quantidade: int | None = 0
    valor: float

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(ServicoBase):
    pass

class ServicoResponse(ServicoBase):
    id: int

    class Config:
        orm_mode = True
