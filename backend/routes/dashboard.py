from fastapi import APIRouter, Depends, HTTPException, status
from ..config.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import cliente, venda, produto, servico, despesa

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_dashboard_data(db: Session = Depends(get_db)):

    total_clientes = db.query(func.count(cliente.Cliente.id)).scalar()
    total_vendas = db.query(func.count(venda.Venda.id)).filter(venda.Venda.cancelada == False).scalar()
    total_produtos = db.query(func.count(produto.Produto.id)).scalar()
    total_servicos = db.query(func.count(servico.Servico.id)).scalar()
    total_despesas = db.query(func.coalesce(func.sum(despesa.Despesa.valor), 0)).scalar()
    total_faturamento = db.query(func.coalesce(func.sum(venda.Venda.total), 0)).filter(venda.Venda.cancelada == False).scalar()
    lucro_liquido = total_faturamento - total_despesas

    return {
        "total_clientes": total_clientes,
        "total_vendas": total_vendas,
        "total_produtos": total_produtos,
        "total_servicos": total_servicos,
        "total_despesas": float(total_despesas),
        "total_faturamento": float(total_faturamento),
        "lucro_liquido": float(lucro_liquido)
    }
