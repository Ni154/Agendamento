
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date

from config.database import supabase_client
from models.agendamento import Agendamento
from schemas.agendamento_schema import AgendamentoCreate, AgendamentoUpdate, AgendamentoOut

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=AgendamentoOut)
async def criar_agendamento(agendamento: AgendamentoCreate):
    data = agendamento.dict()
    # Insere no Supabase, retorna id
    response = supabase_client.table("agendamentos").insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    novo_id = response.data[0]["id"]
    return {**data, "id": novo_id}

@router.get("/", response_model=List[AgendamentoOut])
async def listar_agendamentos(data_inicio: date = None, data_fim: date = None):
    query = supabase_client.table("agendamentos").select("*")
    if data_inicio and data_fim:
        query = query.gte("data", data_inicio.isoformat()).lte("data", data_fim.isoformat())
    response = query.execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.get("/{agendamento_id}", response_model=AgendamentoOut)
async def buscar_agendamento(agendamento_id: int):
    response = supabase_client.table("agendamentos").select("*").eq("id", agendamento_id).single().execute()
    if response.error or not response.data:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return response.data

@router.put("/{agendamento_id}", response_model=AgendamentoOut)
async def atualizar_agendamento(agendamento_id: int, agendamento: AgendamentoUpdate):
    data = agendamento.dict(exclude_unset=True)
    response = supabase_client.table("agendamentos").update(data).eq("id", agendamento_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]

@router.delete("/{agendamento_id}")
async def deletar_agendamento(agendamento_id: int):
    response = supabase_client.table("agendamentos").delete().eq("id", agendamento_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"detail": "Agendamento excluído com sucesso"}
