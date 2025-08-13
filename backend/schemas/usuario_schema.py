from pydantic import BaseModel

class UsuarioLogin(BaseModel):
    usuario: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
