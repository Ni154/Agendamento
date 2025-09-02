from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import get_db
from middleware.auth import get_current_user
from models.cliente import Cliente
from schemas.cliente import ClienteIn, ClienteOut

router = APIRouter(prefix="/cliente", tags=["cliente"])

@router.get("", response_model=list[ClienteOut])
def list_items(db: Session = Depends(get_db), user = Depends(get_current_user)):
    items = db.execute(select(Cliente).where(Cliente.tenant_id == user.tenant_id)).scalars().all()
    return [ClienteOut.model_validate(i) for i in items]

@router.post("", response_model=ClienteOut)
def create_item(payload: ClienteIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    obj = Cliente(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return ClienteOut.model_validate(obj)

