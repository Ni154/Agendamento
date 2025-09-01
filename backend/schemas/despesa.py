from pydantic import BaseModel
from decimal import Decimal

class DespesaIn(BaseModel):
    tipo: str  # 'PRODUTO' ou 'SERVICO'
    fornecedor_razao: str | None = None
    fornecedor_cnpj: str | None = None
    data_emissao: str | None = None
    valor_total: Decimal = 0
    centro_custo: str | None = None
    forma_pagto: str | None = None
    numero: str | None = None
    serie: str | None = None
    chave_acesso: str | None = None
    numero_rps: str | None = None
    municipio: str | None = None
    aliquota_iss: Decimal | None = None
    discriminacao_servico: str | None = None

class DespesaOut(BaseModel):
    id: str
    tipo: str
    fornecedor_razao: str | None = None
    fornecedor_cnpj: str | None = None
    data_emissao: str | None = None
    valor_total: Decimal
    centro_custo: str | None = None
    forma_pagto: str | None = None
    numero: str | None = None
    serie: str | None = None
    chave_acesso: str | None = None
    numero_rps: str | None = None
    municipio: str | None = None
    aliquota_iss: Decimal | None = None
    discriminacao_servico: str | None = None
    class Config:
        from_attributes = True

