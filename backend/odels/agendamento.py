from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .cliente import Cliente  # Importa modelo Cliente para FK
from ..config.database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data = Column(String, nullable=False)  # pode ser date se preferir, mas manter string por compatibilidade
    hora = Column(String, nullable=False)
    servicos = Column(String)  # Lista ou texto com serviços agendados
    status = Column(String, default="pendente")

    cliente = relationship("Cliente", back_populates="agendamentos")
