from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class ClienteBase(BaseModel):
    nome: str = Field(..., example="Maria Silva")
    telefone: Optional[str] = None
    nascimento: Optional[date] = None
    hora_agendada: Optional[str] = None
    instagram: Optional[str] = None
    cantor: Optional[str] = None
    bebida: Optional[str] = None
    epilacao: Optional[str] = None  # SIM / NÃO
    alergia: Optional[str] = None
    qual_alergia: Optional[str] = None
    problemas_pele: Optional[str] = None
    tratamento: Optional[str] = None
    tipo_pele: Optional[str] = None
    hidrata: Optional[str] = None
    gravida: Optional[str] = None
    medicamento: Optional[str] = None
    qual_medicamento: Optional[str] = None
    uso: Optional[str] = None  # DIU, Marca-passo, Nenhum
    diabete: Optional[str] = None
    pelos_encravados: Optional[str] = None
    cirurgia: Optional[str] = None
    foliculite: Optional[str] = None
    qual_foliculite: Optional[str] = None
    problema_extra: Optional[str] = None
    qual_problema: Optional[str] = None
    autorizacao_imagem: Optional[str] = None
    assinatura: Optional[bytes] = None  # BLOB em DB, base64 no transporte pode ser melhor

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteDB(ClienteBase):
    id: int

    class Config:
        orm_mode = True

