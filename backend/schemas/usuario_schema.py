from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    usuario: str
    senha: str
    role: str = "user"

class UsuarioLogin(BaseModel):
    usuario: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    role: str

    class Config:
        orm_mode = True
