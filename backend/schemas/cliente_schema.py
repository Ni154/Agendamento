from pydantic import BaseModel, Field
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    nascimento: Optional[str] = None  # ISO format "YYYY-MM-DD"
    hora_agendada: Optional[str] = None  # "HH:MM"
    instagram: Optional[str] = None
    cantor: Optional[str] = None
    bebida: Optional[str] = None
    epilacao: Optional[str] = None
    alergia: Optional[str] = None
    qual_alergia: Optional[str] = None
    problemas_pele: Optional[str] = None
    tratamento: Optional[str] = None
    tipo_pele: Optional[str] = None
    hidrata: Optional[str] = None
    gravida: Optional[str] = None
    medicamento: Optional[str] = None
    qual_medicamento: Optional[str] = None
    uso: Optional[str] = None
    diabete: Optional[str] = None
    pelos_encravados: Optional[str] = None
    cirurgia: Optional[str] = None
    foliculite: Optional[str] = None
    qual_foliculite: Optional[str] = None
    problema_extra: Optional[str] = None
    qual_problema: Optional[str] = None
    autorizacao_imagem: Optional[str] = None
    assinatura: Optional[bytes] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str]
    telefone: Optional[str]
    nascimento: Optional[str]
    hora_agendada: Optional[str]
    instagram: Optional[str]
    cantor: Optional[str]
    bebida: Optional[str]
    epilacao: Optional[str]
    alergia: Optional[str]
    qual_alergia: Optional[str]
    problemas_pele: Optional[str]
    tratamento: Optional[str]
    tipo_pele: Optional[str]
    hidrata: Optional[str]
    gravida: Optional[str]
    medicamento: Optional[str]
    qual_medicamento: Optional[str]
    uso: Optional[str]
    diabete: Optional[str]
    pelos_encravados: Optional[str]
    cirurgia: Optional[str]
    foliculite: Optional[str]
    qual_foliculite: Optional[str]
    problema_extra: Optional[str]
    qual_problema: Optional[str]
    autorizacao_imagem: Optional[str]
    assinatura: Optional[bytes]

class ClienteRead(ClienteBase):
    id: int

    class Config:
        orm_mode = True

