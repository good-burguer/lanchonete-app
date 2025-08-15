from sqlalchemy import Column, Integer, String

from app.infrastructure.db.database import Base

class StatusPedido(Base):
    __tablename__ = "status_pedido"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(50), nullable=False)