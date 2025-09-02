from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import get_db
from middleware.auth import get_current_user
from models.produto import Produto
from schemas.produto import ProdutoIn, ProdutoOut

router = APIRouter(prefix="/produto", tags=["produto"])

@router.get("", response_model=list[ProdutoOut])
def list_items(db: Session = Depends(get_db), user = Depends(get_current_user)):
    items = db.execute(select(Produto).where(Produto.tenant_id == user.tenant_id)).scalars().all()
    return [ProdutoOut.model_validate(i) for i in items]

@router.post("", response_model=ProdutoOut)
def create_item(payload: ProdutoIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    obj = Produto(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return ProdutoOut.model_validate(obj)

