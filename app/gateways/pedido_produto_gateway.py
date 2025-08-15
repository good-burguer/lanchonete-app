from sqlalchemy.exc import IntegrityError

from app.entities.pedido_produto.entities import PedidoProdutoEntities
from app.entities.pedido_produto.models import PedidoProduto
from app.models.pedido_produto import PedidoProdutoModel

class PedidoProdutoGateway(PedidoProdutoEntities):
    def __init__(self, db_session):
        self.db_session = db_session

    def criarPedidoProduto(self, pedidoProduto: PedidoProduto) -> PedidoProduto:
        try:
            self.db_session.add(pedidoProduto)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar produtos no pedido: {e}")
        self.db_session.refresh(pedidoProduto)

        return pedidoProduto
    
    def buscarPorIdPedido(self, pedido_id: int) -> PedidoProduto:
        
        db_pedido_produtos = self.db_session.query(PedidoProdutoModel).filter(PedidoProdutoModel.pedido_id == pedido_id).all()
        print(db_pedido_produtos)

        if not db_pedido_produtos:
            raise ValueError("Produto(s) do pedido não encontrado(s)")

        return db_pedido_produtos
    
    def deletar(self, id: int) -> None:
        db_pedido_produtos = self.db_session.query(PedidoProdutoModel).filter(PedidoProdutoModel.id == id).first()

        if db_pedido_produtos:
            self.db_session.delete(db_pedido_produtos)
            self.db_session.commit()       
            #self.db_session.flush()