from app.entities.status_pedido.entities import StatusPedidoEntities
from app.entities.status_pedido.models import StatusPedido
from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema
from app.adapters.dto.status_pedido_dto import StatusPedidoCreateSchema, StatusPedidoUpdateSchema

class StatusPedidoUseCase:
    def __init__(self, status_entity: StatusPedidoEntities):
        self.status_entity = status_entity

    def criar(self, statusRequest: StatusPedidoCreateSchema) -> StatusPedidoResponseSchema:
        statusCriado: StatusPedido = self.status_entity.criar(status=statusRequest)

        return self._create_response_schema(statusCriado)

    def buscar_por_id(self, id: int) -> StatusPedidoResponseSchema:
        search: StatusPedido = self.status_entity.buscar_por_id(id=id)
        
        if not search:
            raise ValueError("Status não encontrado")
        
        return self._create_response_schema(search)

    def listar_todos(self) -> list[StatusPedidoResponseSchema]:
        fetchedRows = self.status_entity.listar_todos()
        response = []

        for row in fetchedRows:
            response.append(
                self._create_response_schema(row)
            )
        
        return response

    def atualizar(self, id: int,  dataRequest: StatusPedidoUpdateSchema) -> StatusPedidoResponseSchema:
        status_entity: StatusPedido = self.buscar_por_id(id=id)
        
        if not status_entity:
            raise ValueError("Status não encontrado")

        updatedEntity: StatusPedido = self.status_entity.atualizar(id=id, status=dataRequest)
        
        return self._create_response_schema(updatedEntity)

    def deletar(self, id: int) -> None:
        
        self.status_entity.deletar(id=id)

    def _create_response_schema(self, entity) :
        
        return (StatusPedidoResponseSchema(
                id=entity.id, 
                descricao=entity.descricao))