from abc import ABC, abstractmethod
from app.models.pedido import Pedido

class PedidoEntities(ABC):
    @abstractmethod
    def criarPedido(self, pedido: Pedido): pass
    @abstractmethod
    def listar_todos(self): pass
    @abstractmethod
    def buscar_por_id(self, id: int): pass
    @abstractmethod
    def deletar(self, id: int): pass
    @abstractmethod
    def atualizarPedido(self, pedido: Pedido): pass
