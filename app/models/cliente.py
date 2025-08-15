from sqlalchemy import Column, Integer, String

from app.infrastructure.db.database import Base

class Cliente(Base):
    __tablename__ = "cliente"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    telefone = Column(String(11), nullable=True)
    cpf = Column(String(11), unique=True, nullable=True)


    def __init__(self, nome: String, email: String, telefone: String, cpf: String):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cpf = cpf