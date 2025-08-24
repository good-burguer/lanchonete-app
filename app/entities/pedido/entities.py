from abc import ABC, abstractmethod
from app.models.pedido import Pedido

class PedidoEntities(ABC):
    @abstractmethod
    def criar_pedido(self, pedido: Pedido): pass

    @abstractmethod
    def listar_todos(self): pass

    @abstractmethod
    def buscar_por_id(self, id: int): pass

    @abstractmethod
    def atualizar_pedido(self, pedido: Pedido): pass

    @abstractmethod
    def deletar_pedido(self, id: int): pass