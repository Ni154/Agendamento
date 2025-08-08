from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date
from config.database import supabase_client

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/vendas/total")
async def total_vendas():
    # Soma total das vendas não canceladas
    response = supabase_client.table("vendas").select("total", count="exact").neq("cancelada", 1).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    total = sum(v["total"] for v in response.data) if response.data else 0.0
    return {"total_vendas": total}

@router.get("/vendas/periodo")
async def vendas_periodo(data_inicio: date, data_fim: date):
    if data_inicio > data_fim:
        raise HTTPException(status_code=400, detail="Data início maior que data fim")
    response = supabase_client.table("vendas")\
        .select("*")\
        .gte("data", data_inicio.isoformat())\
        .lte("data", data_fim.isoformat())\
        .neq("cancelada", 1)\
        .execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"vendas": response.data}

@router.get("/produtos/mais_vendidos")
async def produtos_mais_vendidos(limit: Optional[int] = 10):
    # Consulta itens vendidos, somando quantidade, ordenando decrescente
    query = """
        SELECT item_id, SUM(quantidade) as total_vendido
        FROM venda_itens
        WHERE tipo = 'produto'
        GROUP BY item_id
        ORDER BY total_vendido DESC
        LIMIT %s
    """ % limit
    response = supabase_client.rpc("exec_sql", {"sql": query}).execute()
    # Nota: Supabase não suporta exec direto SQL na API pública, isso é ilustrativo.
    # Você deve criar uma função RPC no Postgres para isso ou adaptar via client SQL.
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"produtos_mais_vendidos": response.data}

