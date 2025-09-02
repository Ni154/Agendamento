from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.config.database import get_db  # exemplo


class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    subdomain: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(32), default="basic")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    settings = relationship("TenantSettings", back_populates="tenant", uselist=False)

class TenantSettings(Base):
    __tablename__ = "tenant_settings"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)
    logo_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
    theme_primary: Mapped[str | None] = mapped_column(String(20), nullable=True, default="#0ea5e9")
    theme_secondary: Mapped[str | None] = mapped_column(String(20), nullable=True, default="#1f2937")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    tenant = relationship("Tenant", back_populates="settings", primaryjoin="TenantSettings.tenant_id==Tenant.id")

