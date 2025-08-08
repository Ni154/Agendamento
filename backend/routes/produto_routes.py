from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field
from config.database import supabase_client

router = APIRouter(prefix="/produtos", tags=["Produtos"])

class ProdutoCreate(BaseModel):
    nome: str
    quantidade: int = Field(ge=0)
    preco_venda: float = Field(ge=0.0)

class Produto(ProdutoCreate):
    id: int

@router.post("/", response_model=Produto)
async def criar_produto(produto: ProdutoCreate):
    data = produto.dict()
    response = supabase_client.table("produtos").insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    novo_id = response.data[0]["id"]
    return {**data, "id": novo_id}

@router.get("/", response_model=List[Produto])
async def listar_produtos():
    response = supabase_client.table("produtos").select("*").order("nome").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.put("/{produto_id}", response_model=Produto)
async def atualizar_produto(produto_id: int, produto: ProdutoCreate):
    data = produto.dict()
    response = supabase_client.table("produtos").update(data).eq("id", produto_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    if response.count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {**data, "id": produto_id}

@router.delete("/{produto_id}")
async def excluir_produto(produto_id: int):
    response = supabase_client.table("produtos").delete().eq("id", produto_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    if response.count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"detail": "Produto excluído com sucesso"}

