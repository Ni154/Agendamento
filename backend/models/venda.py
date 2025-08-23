from datetime import datetime
from backend import db


class Venda(db.Model):
    __tablename__ = "vendas"
    id = db.Column(db.Integer, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cliente_id = db.Column(db.Integer, nullable=True)
    total = db.Column(db.Float, default=0.0)
    forma_pagamento = db.Column(db.String(20), nullable=False)  # dinheiro|credito|debito|pix
    observacoes = db.Column(db.String(255))

    itens = db.relationship("VendaItem", backref="venda", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id, "criado_em": self.criado_em.isoformat(), "cliente_id": self.cliente_id,
            "total": self.total, "forma_pagamento": self.forma_pagamento,
            "observacoes": self.observacoes, "itens": [i.to_dict() for i in self.itens]
        }

class VendaItem(db.Model):
    __tablename__ = "venda_itens"
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey("vendas.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=True)
    servico_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=True)
    descricao = db.Column(db.String(160))
    qtd = db.Column(db.Float, default=0.0)
    preco_unit = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id, "produto_id": self.produto_id, "servico_id": self.servico_id,
            "descricao": self.descricao, "qtd": self.qtd,
            "preco_unit": self.preco_unit, "total": self.total
        }

