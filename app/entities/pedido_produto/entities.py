from abc import ABC, abstractmethod
from app.models.pedido_produto import PedidoProdutoModel

class PedidoProdutoEntities(ABC):
    @abstractmethod
    def criarPedidoProduto(self, pedidoProduto: PedidoProdutoModel): pass

    @abstractmethod
    def buscarPorIdPedido(self, pedido_id: int): pass

    @abstractmethod
    def deletar(self, pedido_produto_id: int): pass
    