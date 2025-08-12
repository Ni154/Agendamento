from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.produto_schema import ProdutoCreate, ProdutoOut, ProdutoUpdate
from ..config.database import supabase

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoOut)
def criar_produto(produto: ProdutoCreate):
    data = produto.dict()
    response = supabase.table("produtos").insert(data).execute()
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Erro ao criar produto")
    return response.data[0]

@router.get("/", response_model=List[ProdutoOut])
def listar_produtos():
    response = supabase.table("produtos").select("*").execute()
    return response.data

@router.get("/{produto_id}", response_model=ProdutoOut)
def obter_produto(produto_id: int):
    response = supabase.table("produtos").select("*").eq("id", produto_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return response.data

@router.put("/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate):
    response = supabase.table("produtos").update(produto.dict(exclude_unset=True)).eq("id", produto_id).execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao atualizar produto")
    return response.data[0]

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int):
    response = supabase.table("produtos").delete().eq("id", produto_id).execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao deletar produto")
    return {"detail": "Produto deletado com sucesso"}
