from sqlalchemy import Column, Integer, String, Float
from ..config.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    unidade = Column(String, nullable=True)
    quantidade = Column(Integer, default=0)
    valor = Column(Float, nullable=False)
