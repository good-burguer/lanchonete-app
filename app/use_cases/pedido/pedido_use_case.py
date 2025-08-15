import datetime

from app.entities.pedido.entities import PedidoEntities
from app.adapters.enums.status_pedido import StatusPedidoEnum
from app.models.pedido import Pedido
from app.adapters.schemas.pedido import PedidoCreateSchema, PedidoResponseSchema, PedidoAtualizaSchema

class PedidoUseCase:
    def __init__(self, entities: PedidoEntities):
        self.pedido_entities = entities

    def criarPedido(self, pedidoRequest: PedidoCreateSchema) -> PedidoResponseSchema:
        pedidoEntity: Pedido = Pedido(cliente_id=pedidoRequest.cliente_id, status=1)
        pedidoEntity.status = str(StatusPedidoEnum.Recebido.value)
        pedidoEntity.data_criacao = datetime.datetime.now()

        pedidoCriado: Pedido = self.pedido_entities.criarPedido(pedido=pedidoEntity)
        
        return pedidoCriado

    def buscar_por_id(self, pedido_id: int) -> PedidoResponseSchema:
        pedidoBusca: Pedido = self.pedido_entities.buscar_por_id(id=pedido_id)
        
        return pedidoBusca
    
    def listar_todos(self) -> list[PedidoResponseSchema]:
        pedidosBusca: list[Pedido] = self.pedido_entities.listar_todos()
        
        return pedidosBusca
    
    def atualiza(self, pedido_id: int,  pedidoRequest: PedidoAtualizaSchema) -> PedidoResponseSchema:
        pedidoEntity: Pedido = self.buscar_por_id(pedido_id=pedido_id)
        pedidoEntity.pedido_id = pedido_id
        pedidoEntity.status = pedidoRequest.status
        pedidoEntity.data_alteracao = datetime.datetime.now()
        pedidoEntity.cliente_id = pedidoEntity.cliente_id.cliente_id

        if int(pedidoRequest.status) == int(StatusPedidoEnum.Finalizado):
            pedidoEntity.data_finalizacao = datetime.datetime.now()

        return self.pedido_entities.atualizarPedido(pedido=pedidoEntity)
    
    def deletar(self, pedido_id: int) -> None:
        self.pedido_entities.deletar(id=pedido_id)