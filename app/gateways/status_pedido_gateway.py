from sqlalchemy.orm import Session
from typing import List, Optional

from app.entities.status_pedido.entities import StatusPedidoEntities
from app.entities.status_pedido.models import StatusPedido
from app.dao.status_pedido_dao import StatusPedidoDAO

class StatusPedidoGateway(StatusPedidoEntities):
    
    def __init__(self, db_session: Session):
        self.dao = StatusPedidoDAO(db_session)

    def criar(self, status: StatusPedido):
        
        return self.dao.criar(status)

    def buscar_por_id(self, id: int) -> Optional[StatusPedido]:
        
        return self.dao.buscar_por_id(id)

    def listar_todos(self) -> List[StatusPedido]:
        
        return self.dao.listar_todos()
    
    def atualizar(self, id: int, status: StatusPedido) -> StatusPedido:
        
        return self.dao.atualizar(id, status)

    def deletar(self, id: int) -> None:
        
        return self.dao.deletar(id)