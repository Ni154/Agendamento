from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from ..config.database import Base

class Despesa(Base):
    __tablename__ = "despesas"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String(16), nullable=False)  # 'PRODUTO' ou 'SERVICO'

    # Comuns
    fornecedor_razao: Mapped[str | None] = mapped_column(String(160), nullable=True)
    fornecedor_cnpj: Mapped[str | None] = mapped_column(String(20), nullable=True)
    data_emissao: Mapped[str | None] = mapped_column(String(20), nullable=True)
    valor_total: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    centro_custo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    forma_pagto: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # NFe (produto)
    numero: Mapped[str | None] = mapped_column(String(20), nullable=True)
    serie: Mapped[str | None] = mapped_column(String(10), nullable=True)
    chave_acesso: Mapped[str | None] = mapped_column(String(60), nullable=True)

    # NFS-e (serviço)
    numero_rps: Mapped[str | None] = mapped_column(String(30), nullable=True)
    municipio: Mapped[str | None] = mapped_column(String(80), nullable=True)
    aliquota_iss: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    discriminacao_servico: Mapped[str | None] = mapped_column(String(400), nullable=True)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

