from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    usuario: str = Field(..., description="Nome do usuário")

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, description="Senha do usuário")

class UsuarioLogin(BaseModel):
    usuario: str
    senha: str

class UsuarioRead(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

