from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import date
from ..config.database import get_db
from ..models import venda, despesa

router = APIRouter(prefix="/relatorio", tags=["relatorio"])

@router.get("/vendas", status_code=status.HTTP_200_OK)
def relatorio_vendas(
    data_inicio: Optional[date] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    data_fim: Optional[date] = Query(None, description="Data final no formato YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = db.query(venda.Venda).filter(venda.Venda.cancelada == False)
    if data_inicio:
        query = query.filter(venda.Venda.data >= data_inicio)
    if data_fim:
        query = query.filter(venda.Venda.data <= data_fim)

    vendas = query.all()

    total_vendas = sum(v.total for v in vendas)
    quantidade_vendas = len(vendas)

    return {
        "total_vendas": float(total_vendas),
        "quantidade_vendas": quantidade_vendas,
        "vendas": [{"id": v.id, "cliente_id": v.cliente_id, "data": v.data.isoformat(), "total": float(v.total)} for v in vendas]
    }

@router.get("/despesas", status_code=status.HTTP_200_OK)
def relatorio_despesas(
    data_inicio: Optional[date] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    data_fim: Optional[date] = Query(None, description="Data final no formato YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = db.query(despesa.Despesa)
    if data_inicio:
        query = query.filter(despesa.Despesa.data >= data_inicio)
    if data_fim:
        query = query.filter(despesa.Despesa.data <= data_fim)

    despesas = query.all()

    total_despesas = sum(d.valor for d in despesas)
    quantidade_despesas = len(despesas)

    return {
        "total_despesas": float(total_despesas),
        "quantidade_despesas": quantidade_despesas,
        "despesas": [{"id": d.id, "descricao": d.descricao, "data": d.data.isoformat(), "valor": float(d.valor)} for d in despesas]
    }
