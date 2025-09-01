from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from ..config.database import Base

class Venda(Base):
    __tablename__ = "vendas"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True, nullable=False)
    agendamento_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    total: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    status: Mapped[str] = mapped_column(String(40), default="aberta")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

