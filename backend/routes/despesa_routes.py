from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas.despesa_schema import DespesaCreate, DespesaOut, DespesaUpdate
from ..models.despesa import Despesa
from ..config.database import get_db

router = APIRouter(prefix="/despesas", tags=["despesas"])

@router.post("/", response_model=DespesaOut, status_code=status.HTTP_201_CREATED)
def criar_despesa(despesa: DespesaCreate, db: Session = Depends(get_db)):
    nova_despesa = Despesa(**despesa.dict())
    db.add(nova_despesa)
    db.commit()
    db.refresh(nova_despesa)
    return nova_despesa

@router.get("/", response_model=List[DespesaOut])
def listar_despesas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    despesas = db.query(Despesa).offset(skip).limit(limit).all()
    return despesas

@router.get("/{despesa_id}", response_model=DespesaOut)
def buscar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    despesa = db.query(Despesa).filter(Despesa.id == despesa_id).first()
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return despesa

@router.put("/{despesa_id}", response_model=DespesaOut)
def atualizar_despesa(despesa_id: int, despesa_atualizada: DespesaUpdate, db: Session = Depends(get_db)):
    despesa = db.query(Despesa).filter(Despesa.id == despesa_id).first()
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    update_data = despesa_atualizada.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(despesa, key, value)

    db.commit()
    db.refresh(despesa)
    return despesa

@router.delete("/{despesa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    despesa = db.query(Despesa).filter(Despesa.id == despesa_id).first()
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    db.delete(despesa)
    db.commit()
    return None
