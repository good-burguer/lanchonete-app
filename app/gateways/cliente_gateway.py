from typing import List, Optional
from sqlalchemy.orm import Session

from app.entities.cliente.models import Cliente
from app.entities.cliente.entities import ClienteEntities
from app.models.cliente import Cliente as ClienteORM
from app.adapters.presenters.cliente_presenter import ClienteResponseSchema
from app.dao.cliente_dao import ClienteDAO

class ClienteGateway(ClienteEntities):
    def __init__(self, db_session: Session):
        self.dao = ClienteDAO(db_session)

    def criar_cliente(self, cliente: Cliente) -> Cliente:
        
        return self.dao.criar_cliente(cliente)

    def buscar_por_cpf(self, cpf_cliente: str) -> Optional[Cliente]:

        return self.dao.buscar_por_cpf(cpf_cliente)

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        
        return self.dao.buscar_por_id(cliente_id)

    def listar_todos(self) -> List[Cliente]:
        
        return self.dao.listar_todos()

    def atualizar_cliente(self, cliente_id:int, cliente: Cliente) -> Cliente:

        return self.dao.atualizar_cliente(cliente_id, cliente)

    def deletar_cliente(self, cliente_id: int) -> None:
        
        return self.dao.deletar_cliente(cliente_id)