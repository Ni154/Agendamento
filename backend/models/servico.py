from datetime import datetime
from backend import db


class Servico(db.Model):
    __tablename__ = "servicos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    categoria = db.Column(db.String(80))
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Float, default=0.0)
    duracao_min = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id, "nome": self.nome, "categoria": self.categoria,
            "descricao": self.descricao, "preco": self.preco,
            "duracao_min": self.duracao_min
        }

