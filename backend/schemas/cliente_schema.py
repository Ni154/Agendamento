from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    nascimento: Optional[str] = None
    hora_agendada: Optional[str] = None
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

class ClienteCreate(ClienteBase):
    assinatura: Optional[bytes] = None

class ClienteUpdate(ClienteBase):
    assinatura: Optional[bytes] = None

class ClienteOut(ClienteBase):
    id: int
    assinatura: Optional[bytes] = None

    class Config:
        orm_mode = True
