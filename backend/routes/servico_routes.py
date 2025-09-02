from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import get_db
from middleware.auth import get_current_user
from models.servico import Servico
from schemas.servico import ServicoIn, ServicoOut

router = APIRouter(prefix="/servico", tags=["servico"])

@router.get("", response_model=list[ServicoOut])
def list_items(db: Session = Depends(get_db), user = Depends(get_current_user)):
    items = db.execute(select(Servico).where(Servico.tenant_id == user.tenant_id)).scalars().all()
    return [ServicoOut.model_validate(i) for i in items]

@router.post("", response_model=ServicoOut)
def create_item(payload: ServicoIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    obj = Servico(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return ServicoOut.model_validate(obj)

