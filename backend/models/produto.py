from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from backend.config.database import get_db  # exemplo

class Produto(Base):
    __tablename__ = "produtos"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(160), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(80), nullable=True)
    preco: Mapped[float] = mapped_column(Numeric(12,2), nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

