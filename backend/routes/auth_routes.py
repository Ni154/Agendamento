from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.schemas.usuario_schema import UsuarioLogin, TokenResponse
from backend.utils.auth import verify_password, create_access_token
from backend.models.usuario import Usuario

router = APIRouter()

@router.post("/login", response_model=TokenResponse, summary="Login e obtenção de JWT")
def login(payload: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == payload.usuario).first()
    if not user or not verify_password(payload.senha, user.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token, token_type="bearer")
