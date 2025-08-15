from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.status_pedido.models import StatusPedido

class StatusPedidoEntities(ABC):

    @abstractmethod
    def criar(self, status: StatusPedido) -> StatusPedido:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[StatusPedido]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[StatusPedido]:
        pass

    @abstractmethod
    def atualizar(self, status: StatusPedido) -> StatusPedido:
        pass

    @abstractmethod
    def deletar(self, id: int) -> None:
        pass