from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ..config.database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True, nullable=False)
    cliente_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    data: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="pendente")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

