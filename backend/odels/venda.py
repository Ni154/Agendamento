from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..config.database import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    data = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, default=0)
    cancelada = Column(Boolean, default=False)
    forma_pagamento = Column(String, nullable=True)

    itens = relationship("VendaItem", back_populates="venda")

class VendaItem(Base):
    __tablename__ = "venda_itens"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    tipo = Column(String)  # "produto" ou "servico"
    item_id = Column(Integer)  # id do produto ou serviço
    quantidade = Column(Integer, default=1)
    preco = Column(Float)

    venda = relationship("Venda", back_populates="itens")
