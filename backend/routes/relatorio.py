 from fastapi import APIRouter, Depends, Query, HTTPException, status
 from sqlalchemy.orm import Session
 from sqlalchemy import func, and_
 from typing import Optional
 from datetime import date
+
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
-    data_inicio: Optional[date] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
-    data_fim: Optional[date] = Query(None, description="Data final no formato YYYY-MM-DD"),
+    data_inicio: Optional[date] = Query(
+        None, description="Data inicial no formato YYYY-MM-DD"
+    ),
+    data_fim: Optional[date] = Query(
+        None, description="Data final no formato YYYY-MM-DD"
+    ),
+    revenda: bool = Query(
+        False, description="Se verdadeiro, agrupa totais de revenda por produto"
+    ),
     db: Session = Depends(get_db),
 ):
+    """Retorna relatório de despesas.
+
+    Quando ``revenda`` for ``True`` as despesas marcadas como revenda são
+    agrupadas por produto e os valores de custo e venda são somados para
+    cada item.
+    """
+
     query = db.query(despesa.Despesa)
     if data_inicio:
         query = query.filter(despesa.Despesa.data >= data_inicio)
     if data_fim:
         query = query.filter(despesa.Despesa.data <= data_fim)
 
+    if revenda:
+        query = (
+            query.filter(despesa.Despesa.revenda == True)
+            .with_entities(
+                despesa.Despesa.descricao.label("descricao"),
+                despesa.Despesa.fornecedor,
+                despesa.Despesa.cnpj,
+                despesa.Despesa.categoria_id,
+                despesa.Despesa.revenda,
+                func.sum(despesa.Despesa.preco_custo).label("preco_custo"),
+                func.sum(despesa.Despesa.preco_venda).label("preco_venda"),
+                func.sum(despesa.Despesa.valor).label("valor"),
+            )
+            .group_by(
+                despesa.Despesa.descricao,
+                despesa.Despesa.fornecedor,
+                despesa.Despesa.cnpj,
+                despesa.Despesa.categoria_id,
+                despesa.Despesa.revenda,
+            )
+        )
+    else:
+        query = query.with_entities(
+            despesa.Despesa.id,
+            despesa.Despesa.descricao,
+            despesa.Despesa.data,
+            despesa.Despesa.valor,
+            despesa.Despesa.fornecedor,
+            despesa.Despesa.cnpj,
+            despesa.Despesa.categoria_id,
+            despesa.Despesa.revenda,
+            despesa.Despesa.preco_custo,
+            despesa.Despesa.preco_venda,
+        )
+
     despesas = query.all()
 
     total_despesas = sum(d.valor for d in despesas)
     quantidade_despesas = len(despesas)
 
+    resultado = []
+    for d in despesas:
+        item = {
+            "id": getattr(d, "id", None),
+            "descricao": d.descricao,
+            "valor": float(d.valor),
+            "fornecedor": getattr(d, "fornecedor", None),
+            "cnpj": getattr(d, "cnpj", None),
+            "categoria_id": getattr(d, "categoria_id", None),
+            "revenda": getattr(d, "revenda", None),
+            "preco_custo": float(getattr(d, "preco_custo", 0) or 0),
+            "preco_venda": float(getattr(d, "preco_venda", 0) or 0),
+        }
+        data_valor = getattr(d, "data", None)
+        if data_valor is not None and not revenda:
+            # Em bancos onde data é um Date, garantimos que seja serializado
+            try:
+                item["data"] = data_valor.isoformat()  # type: ignore[attr-defined]
+            except AttributeError:
+                item["data"] = data_valor
+        resultado.append(item)
+
     return {
         "total_despesas": float(total_despesas),
         "quantidade_despesas": quantidade_despesas,
-        "despesas": [{"id": d.id, "descricao": d.descricao, "data": d.data.isoformat(), "valor": float(d.valor)} for d in despesas]
+        "despesas": resultado,
     }
 
EOF
)
