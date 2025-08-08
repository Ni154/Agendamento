from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from config.database import supabase_client

router = APIRouter(prefix="/despesas", tags=["Despesas"])

class DespesaCreate(BaseModel):
    data: date
    descricao: str
    valor: float = Field(..., gt=0)

class Despesa(DespesaCreate):
    id: int

@router.post("/", response_model=Despesa)
async def criar_despesa(despesa: DespesaCreate):
    try:
        data = {
            "data": despesa.data.isoformat(),
            "descricao": despesa.descricao,
            "valor": despesa.valor
        }
        response = supabase_client.table("despesas").insert(data).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        novo_id = response.data[0]["id"]
        return {**data, "id": novo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Despesa])
async def listar_despesas():
    try:
        response = supabase_client.table("despesas").select("*").order("data", desc=True).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{despesa_id}")
async def excluir_despesa(despesa_id: int):
    try:
        response = supabase_client.table("despesas").delete().eq("id", despesa_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        if response.count == 0:
            raise HTTPException(status_code=404, detail="Despesa não encontrada")
        return {"detail": "Despesa excluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

