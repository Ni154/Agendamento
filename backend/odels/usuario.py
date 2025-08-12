from sqlalchemy import Column, Integer, String
from backend.config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    role = Column(String, default="user")  # Pode ser admin, user, etc
