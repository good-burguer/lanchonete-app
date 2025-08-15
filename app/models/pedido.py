from sqlalchemy import Column, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.infrastructure.db.database import Base

class Pedido(Base):
    __tablename__ = "pedido"

    pedido_id = Column(Integer, primary_key=True)  
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=True)
    status = Column(Integer, ForeignKey("status_pedido.id"), nullable=True)
    data_criacao = Column(Time, nullable=False)
    data_alteracao = Column(Time, nullable=True)
    data_finalizacao = Column(Time, nullable=True)

    cliente_rel = relationship("Cliente", backref="pedido")
    status_rel = relationship("StatusPedido", backref="pedido")

    def __init__(self, cliente_id: Integer, status: Integer):
        self.cliente_id = cliente_id
        self.status = status
        