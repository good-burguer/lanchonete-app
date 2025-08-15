from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.db.database import Base

class PedidoProdutoModel(Base):
    __tablename__ = "pedido_produtos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedido.pedido_id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.produto_id"), nullable=False)

    cliente_rel = relationship("Pedido", foreign_keys=[pedido_id])
    produto_rel = relationship("Produto", foreign_keys=[produto_id])