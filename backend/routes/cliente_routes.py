
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteOut
from config.database import supabase_client

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteOut)
async def criar_cliente(cliente: ClienteCreate):
    res = supabase_client.table("clientes").insert(cliente.dict()).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    data = res.data[0]
    return data

@router.get("/", response_model=List[ClienteOut])
async def listar_clientes():
    res = supabase_client.table("clientes").select("*").order("nome").execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data

@router.get("/{cliente_id}", response_model=ClienteOut)
async def buscar_cliente(cliente_id: int):
    res = supabase_client.table("clientes").select("*").eq("id", cliente_id).single().execute()
    if res.error or not res.data:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return res.data

@router.put("/{cliente_id}", response_model=ClienteOut)
async def atualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    res = supabase_client.table("clientes").update(cliente.dict(exclude_unset=True)).eq("id", cliente_id).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    if not res.data:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return res.data[0]

@router.delete("/{cliente_id}")
async def deletar_cliente(cliente_id: int):
    res = supabase_client.table("clientes").delete().eq("id", cliente_id).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return {"message": "Cliente deletado com sucesso"}
