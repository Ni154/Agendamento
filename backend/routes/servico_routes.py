from fastapi import APIRouter, HTTPException
from typing import List
from schemas.servico_schema import ServicoCreate, ServicoRead, ServicoUpdate
from config.database import supabase_client

router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.get("/", response_model=List[ServicoRead])
async def listar_servicos():
    response = supabase_client.table("servicos").select("*").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.post("/", response_model=ServicoRead)
async def criar_servico(servico: ServicoCreate):
    response = supabase_client.table("servicos").insert(servico.dict()).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]

@router.put("/{servico_id}", response_model=ServicoRead)
async def atualizar_servico(servico_id: int, servico: ServicoUpdate):
    response = supabase_client.table("servicos").update(servico.dict()).eq("id", servico_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]

@router.delete("/{servico_id}")
async def deletar_servico(servico_id: int):
    response = supabase_client.table("servicos").delete().eq("id", servico_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"msg": "Serviço excluído com sucesso."}

