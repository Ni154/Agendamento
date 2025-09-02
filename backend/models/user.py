from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from backend.config.database import get_db  # exemplo


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("tenant_id", "email", name="uq_user_email_per_tenant"),)
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="admin")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

