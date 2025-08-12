from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import servico_schema
from ..models import servico
from ..config.database import get_db

router = APIRouter(prefix="/servicos", tags=["servicos"])

@router.post("/", response_model=servico_schema.ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(servico_data: servico_schema.ServicoCreate, db: Session = Depends(get_db)):
    novo_servico = servico.Servico(**servico_data.dict())
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return novo_servico

@router.get("/", response_model=List[servico_schema.ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    servicos = db.query(servico.Servico).all()
    return servicos

@router.get("/{servico_id}", response_model=servico_schema.ServicoResponse)
def obter_servico(servico_id: int, db: Session = Depends(get_db)):
    servico_db = db.query(servico.Servico).filter(servico.Servico.id == servico_id).first()
    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return servico_db

@router.put("/{servico_id}", response_model=servico_schema.ServicoResponse)
def atualizar_servico(servico_id: int, servico_data: servico_schema.ServicoUpdate, db: Session = Depends(get_db)):
    servico_db = db.query(servico.Servico).filter(servico.Servico.id == servico_id).first()
    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    for key, value in servico_data.dict(exclude_unset=True).items():
        setattr(servico_db, key, value)
    db.commit()
    db.refresh(servico_db)
    return servico_db

@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(servico_id: int, db: Session = Depends(get_db)):
    servico_db = db.query(servico.Servico).filter(servico.Servico.id == servico_id).first()
    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    db.delete(servico_db)
    db.commit()
    return None
