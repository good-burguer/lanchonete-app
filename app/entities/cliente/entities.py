from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.cliente.models import Cliente

class ClienteEntities(ABC):
    @abstractmethod
    def criar_cliente(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def buscar_por_cpf(self, cpf_cliente: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Cliente]:
        pass

    @abstractmethod
    def atualizar_cliente(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def deletar_cliente(self, cliente_id: int) -> None:
        pass