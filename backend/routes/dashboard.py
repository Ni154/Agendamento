from fastapi import APIRouter, HTTPException
from config.database import supabase_client

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/metrics")
async def obter_metricas():
    try:
        total_clientes = supabase_client.table("clientes").select("id", count="exact").execute()
        total_vendas = supabase_client.table("vendas").select("id", count="exact").eq("cancelada", 0).execute()
        total_produtos = supabase_client.table("produtos").select("id", count="exact").execute()
        total_servicos = supabase_client.table("servicos").select("id", count="exact").execute()
        total_despesas = supabase_client.table("despesas").select("valor").execute()
        total_faturamento = supabase_client.table("vendas").select("total").eq("cancelada", 0).execute()

        if any(r.error for r in [total_clientes, total_vendas, total_produtos, total_servicos, total_despesas, total_faturamento]):
            raise HTTPException(status_code=500, detail="Erro ao consultar métricas")

        clientes_count = total_clientes.count
        vendas_count = total_vendas.count
        produtos_count = total_produtos.count
        servicos_count = total_servicos.count

        despesas_sum = sum(item["valor"] for item in total_despesas.data) if total_despesas.data else 0
        faturamento_sum = sum(item["total"] for item in total_faturamento.data) if total_faturamento.data else 0
        lucro_liquido = faturamento_sum - despesas_sum

        return {
            "total_clientes": clientes_count,
            "total_vendas": vendas_count,
            "total_produtos": produtos_count,
            "total_servicos": servicos_count,
            "total_despesas": despesas_sum,
            "total_faturamento": faturamento_sum,
            "lucro_liquido": lucro_liquido,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vendas-status")
async def vendas_por_status():
    try:
        dados = supabase_client.rpc('vendas_por_status').execute()
        # Caso não tenha a função RPC criada, podemos fazer no código:
        # Outra forma manual:
        canceladas = supabase_client.table("vendas").select("id", count="exact").eq("cancelada", 1).execute()
        realizadas = supabase_client.table("vendas").select("id", count="exact").eq("cancelada", 0).execute()
        if canceladas.error or realizadas.error:
            raise HTTPException(status_code=500, detail="Erro ao consultar status das vendas")

        return {
            "canceladas": canceladas.count,
            "realizadas": realizadas.count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

