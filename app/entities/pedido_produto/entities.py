from abc import ABC, abstractmethod
from app.models.pedido_produto import PedidoProdutoModel

class PedidoProdutoEntities(ABC):
    @abstractmethod
    def criarPedidoProduto(self, pedido_id: int, produto_id: int): pass

    @abstractmethod
    def buscarPorIdPedido(self, pedido_id: int): pass

    @abstractmethod
    def deletar(self, pedido_produto_id: int): pass
    