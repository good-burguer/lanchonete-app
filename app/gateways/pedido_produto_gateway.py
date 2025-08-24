from sqlalchemy.orm import Session

from app.entities.pedido_produto.entities import PedidoProdutoEntities
from app.entities.pedido_produto.models import PedidoProduto
from app.models.pedido_produto import PedidoProdutoModel
from app.dao.pedido_produto_dao import PedidoProdutoDAO

class PedidoProdutoGateway(PedidoProdutoEntities):
    def __init__(self, db_session: Session):
        self.dao = PedidoProdutoDAO(db_session)

    def criarPedidoProduto(self, pedido_id: int, produto_id: int) -> PedidoProdutoModel:
        
        return self.dao.criar_pedido_produto(pedido_id, produto_id)
    
    def buscarPorIdPedido(self, pedido_id: int) -> PedidoProduto:       
        
        return self.dao.buscarPorIdPedido(pedido_id)
   
    def deletar(self, id: int) -> None:
        
        return self.dao.deletar(id)