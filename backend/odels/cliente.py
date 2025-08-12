from sqlalchemy import Column, Integer, String, LargeBinary
from config.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    nascimento = Column(String)
    hora_agendada = Column(String)
    instagram = Column(String)
    cantor = Column(String)
    bebida = Column(String)
    epilacao = Column(String)
    alergia = Column(String)
    qual_alergia = Column(String)
    problemas_pele = Column(String)
    tratamento = Column(String)
    tipo_pele = Column(String)
    hidrata = Column(String)
    gravida = Column(String)
    medicamento = Column(String)
    qual_medicamento = Column(String)
    uso = Column(String)
    diabete = Column(String)
    pelos_encravados = Column(String)
    cirurgia = Column(String)
    foliculite = Column(String)
    qual_foliculite = Column(String)
    problema_extra = Column(String)
    qual_problema = Column(String)
    autorizacao_imagem = Column(String)
    assinatura = Column(LargeBinary)
