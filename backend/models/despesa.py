from datetime import datetime
from backend import db
# ajuste os nomes conforme seu arquivo despesa.py exporta

try:
    from .despesa import DespesaItem  # se existir
except Exception:
    pass



class Despesa(db.Model):
    __tablename__ = "despesas"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    fornecedor = db.Column(db.String(160))
    categoria = db.Column(db.String(40), nullable=False)   # "revenda" | "uso"
    observacoes = db.Column(db.String(255))
    total = db.Column(db.Float, default=0.0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    itens = db.relationship("DespesaItem", backref="despesa", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id, "data": self.data.isoformat(), "fornecedor": self.fornecedor,
            "categoria": self.categoria, "observacoes": self.observacoes, "total": self.total,
            "itens": [i.to_dict() for i in self.itens]
        }

class DespesaItem(db.Model):
    __tablename__ = "despesa_itens"
    id = db.Column(db.Integer, primary_key=True)
    despesa_id = db.Column(db.Integer, db.ForeignKey("despesas.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=True)
    descricao = db.Column(db.String(160))
    qtd = db.Column(db.Float, default=0.0)
    custo_unit = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id, "produto_id": self.produto_id, "descricao": self.descricao,
            "qtd": self.qtd, "custo_unit": self.custo_unit, "total": self.total
        }

