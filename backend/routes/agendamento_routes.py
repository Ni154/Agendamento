from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..config.database import get_db
from ..middleware.auth import get_current_user
from ..models.agendamento import Agendamento
from ..schemas.agendamento import AgendamentoIn, AgendamentoOut

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"])

@router.get("", response_model=list[AgendamentoOut])
def list_agendamentos(db: Session = Depends(get_db), user = Depends(get_current_user)):
    items = db.execute(select(Agendamento).where(Agendamento.tenant_id == user.tenant_id)).scalars().all()
    return [AgendamentoOut.model_validate(i) for i in items]

@router.post("", response_model=AgendamentoOut)
def create_agendamento(payload: AgendamentoIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    obj = Agendamento(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return AgendamentoOut.model_validate(obj)

