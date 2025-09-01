
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ..config.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str | None] = mapped_column(String(160), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
