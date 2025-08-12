from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas.agendamento_schema import AgendamentoCreate, AgendamentoOut, AgendamentoUpdate
from ..models.agendamento import Agendamento
from ..config.database import get_db

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"])

@router.post("/", response_model=AgendamentoOut, status_code=status.HTTP_201_CREATED)
def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    novo_agendamento = Agendamento(**agendamento.dict())
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    return novo_agendamento

@router.get("/", response_model=List[AgendamentoOut])
def listar_agendamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agendamentos = db.query(Agendamento).offset(skip).limit(limit).all()
    return agendamentos

@router.get("/{agendamento_id}", response_model=AgendamentoOut)
def buscar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento

@router.put("/{agendamento_id}", response_model=AgendamentoOut)
def atualizar_agendamento(agendamento_id: int, agendamento_atualizado: AgendamentoUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    update_data = agendamento_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(agendamento, key, value)

    db.commit()
    db.refresh(agendamento)
    return agendamento

@router.delete("/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    db.delete(agendamento)
    db.commit()
    return None
