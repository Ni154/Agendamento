from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import get_db
from middleware.auth import get_current_user
from models.venda import Venda
from schemas.venda import VendaIn, VendaOut

router = APIRouter(prefix="/vendas", tags=["vendas"])

@router.get("", response_model=list[VendaOut])
def list_vendas(db: Session = Depends(get_db), user = Depends(get_current_user)):
    items = db.execute(select(Venda).where(Venda.tenant_id == user.tenant_id)).scalars().all()
    return [VendaOut.model_validate(i) for i in items]

@router.post("", response_model=VendaOut)
def create_venda(payload: VendaIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    obj = Venda(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return VendaOut.model_validate(obj)

