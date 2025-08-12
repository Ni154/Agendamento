from fastapi import APIRouter, HTTPException, Depends
from typing import List
from supabase import Client
from ..schemas.cliente_schema import ClienteCreate, ClienteOut, ClienteUpdate
from ..config.database import supabase

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteOut)
def criar_cliente(cliente: ClienteCreate):
    data = cliente.dict()
    response = supabase.table("clientes").insert(data).execute()
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Erro ao criar cliente")
    cliente_db = response.data[0]
    return cliente_db

@router.get("/", response_model=List[ClienteOut])
def listar_clientes():
    response = supabase.table("clientes").select("*").execute()
    return response.data

@router.get("/{cliente_id}", response_model=ClienteOut)
def obter_cliente(cliente_id: int):
    response = supabase.table("clientes").select("*").eq("id", cliente_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return response.data

@router.put("/{cliente_id}", response_model=ClienteOut)
def atualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    response = supabase.table("clientes").update(cliente.dict(exclude_unset=True)).eq("id", cliente_id).execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao atualizar cliente")
    return response.data[0]

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int):
    response = supabase.table("clientes").delete().eq("id", cliente_id).execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao deletar cliente")
    return {"detail": "Cliente deletado com sucesso"}
