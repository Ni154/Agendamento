from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    usuario: str = Field(..., min_length=3, max_length=50)

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6)

class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    senha: Optional[str] = None

class UsuarioDB(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

