from sqlalchemy import Column, Integer, String, Float
from ..config.database import Base

class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)  # pode ser Date se quiser
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
