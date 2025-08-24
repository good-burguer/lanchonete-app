from app.entities.pedido.entities import PedidoEntities
from app.adapters.schemas.pedido import PedidoResponseSchema
from app.adapters.schemas.cliente import ClienteResponseSchema
from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema
from app.adapters.dto.pedido_dto import PedidoAtualizaSchema

from app.adapters.utils.debug import var_dump_die

class PedidoUseCase:
    def __init__(self, entity: PedidoEntities):
        self.pedido_entity = entity

    def criar_pedido(self, pedido) :
        pedidoCriado = self.pedido_entity.criar_pedido(pedido)
        
        return self._prepare_response(pedidoCriado)
    
    def listar_todos(self) :
        db_pedidos = self.pedido_entity.listar_todos()
        pedidos = []

        for pedido in db_pedidos:
            pedidoResponse = self._prepare_response(pedido)
            pedidos.append(pedidoResponse)

        return pedidos

    def buscar_por_id(self, pedido_id: int) -> PedidoResponseSchema:
        pedido = self.pedido_entity.buscar_por_id(id=pedido_id)
        
        if not pedido :
            raise ValueError("Pedido não encontrado")
        
        return self._prepare_response(pedido)
    
    def atualizar_pedido(self, pedido_id: int,  pedidoRequest: PedidoAtualizaSchema) -> PedidoResponseSchema:
        pedidoEntity = self.pedido_entity.atualizar_pedido(pedido_id, pedidoRequest)
        
        if not pedidoEntity:
            raise ValueError("Pedido não encontrado")

        return self._prepare_response(pedidoEntity)
    
    def deletar_pedido(self, pedido_id: int) -> None:
        
        return self.pedido_entity.deletar_pedido(pedido_id)

    def _prepare_response(self, pedido) :
        clienteEntity: ClienteResponseSchema = (ClienteResponseSchema(
            cliente_id=pedido.cliente_id,
            nome=pedido.cliente_rel.nome,
            email=pedido.cliente_rel.email,
            telefone=pedido.cliente_rel.telefone,
            cpf=pedido.cliente_rel.cpf
        ))

        statusOrderEntity: StatusPedidoResponseSchema = (StatusPedidoResponseSchema(
            id=pedido.status_rel.id,
            descricao=pedido.status_rel.descricao
        ))

        pedidoResponse: PedidoResponseSchema = (PedidoResponseSchema(
            pedido_id=pedido.pedido_id, 
            cliente_id=clienteEntity, 
            status=statusOrderEntity, 
            data_criacao=pedido.data_criacao, 
            data_alteracao=pedido.data_alteracao, 
            data_finalizacao=pedido.data_finalizacao
        ))
        
        return pedidoResponse