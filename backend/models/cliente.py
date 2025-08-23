# backend/models/cliente.py
from datetime import datetime, date
from backend import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    # principais
    nome       = db.Column(db.String(120), nullable=False)
    apelido    = db.Column(db.String(120))
    email      = db.Column(db.String(120), index=True)
    telefone   = db.Column(db.String(40))
    whatsapp   = db.Column(db.String(40))
    cpf        = db.Column(db.String(20), index=True)
    nascimento = db.Column(db.Date)

    # endereço
    endereco = db.Column(db.String(255))
    bairro   = db.Column(db.String(120))
    cidade   = db.Column(db.String(120))
    uf       = db.Column(db.String(2))
    cep      = db.Column(db.String(15))

    observacoes = db.Column(db.Text)

    criado_em     = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "apelido": self.apelido,
            "email": self.email,
            "telefone": self.telefone,
            "whatsapp": self.whatsapp,
            "cpf": self.cpf,
            "nascimento": self.nascimento.isoformat() if isinstance(self.nascimento, date) and self.nascimento else None,
            "endereco": self.endereco,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "cep": self.cep,
            "observacoes": self.observacoes,
        }

