from decimal import Decimal
from sqlalchemy.orm import Session

from app.entities.pedido.entities import PedidoEntities, Pedido
from app.adapters.schemas.pedido import PedidoResponseSchema 
from app.adapters.dto.pedido_dto import PedidoAtualizaSchema
from app.dao.pedido_dao import PedidoDAO

class PedidoGateway(PedidoEntities):
    def __init__(self, db_session: Session):
        self.dao = PedidoDAO(db_session)

    def criar_pedido(self, pedido: Pedido) -> Pedido:
        
        return self.dao.criar_pedido(pedido)       

    def listar_todos(self) -> list[PedidoResponseSchema]:
        pedidos_prontos = self.dao.busca_por_status(3)
        pedidos_em_preparacao = self.dao.busca_por_status(2)
        pedidos_recebidos = self.dao.busca_por_status(1)
        db_pedidos = pedidos_prontos + pedidos_em_preparacao + pedidos_recebidos

        return db_pedidos

    def buscar_por_id(self, id: int) -> PedidoResponseSchema:
        
        return self.dao.buscar_por_id(id)

    def atualizar_pedido(self, pedido_id: int,  pedidoRequest: PedidoAtualizaSchema) -> PedidoResponseSchema:
        
        return self.dao.atualizar_pedido(pedido_id, pedidoRequest)

    def deletar_pedido(self, id: int) -> None:
        
        return self.dao.deletar_pedido(id)