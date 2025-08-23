# backend/models/produto.py
from datetime import datetime
from backend import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    sku = db.Column(db.String(80), index=True)
    categoria = db.Column(db.String(80), index=True)
    unidade = db.Column(db.String(40))
    preco_custo = db.Column(db.Float, default=0.0)
    preco_venda = db.Column(db.Float, default=0.0)
    estoque_qtd = db.Column(db.Float, default=0.0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sku": self.sku,
            "categoria": self.categoria,
            "unidade": self.unidade,
            "preco_custo": self.preco_custo,
            "preco_venda": self.preco_venda,
            "estoque_qtd": self.estoque_qtd,
        }

