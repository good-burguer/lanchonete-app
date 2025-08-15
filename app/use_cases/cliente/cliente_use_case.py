from app.entities.cliente.entities import ClienteEntities
from app.entities.cliente.models import Cliente
from app.adapters.schemas.cliente import ClienteCreateSchema, ClienteResponseSchema, ClienteUpdateSchema

class ClienteUseCase:
    def __init__(self, entities: ClienteEntities):
        self.cliente_entities = entities

    def criar_cliente(self, clienteRequest: ClienteCreateSchema) -> ClienteCreateSchema:
        clienteEntity: Cliente = Cliente(nome=clienteRequest.nome, email=clienteRequest.email, telefone=clienteRequest.telefone, cpf=clienteRequest.cpf)
        clienteCriado: Cliente = self.cliente_entities.criar_cliente(cliente=clienteEntity)
        clienteResponse: ClienteResponseSchema = ClienteResponseSchema(cliente_id=clienteCriado.cliente_id, nome=clienteCriado.nome, email=clienteCriado.email, telefone=clienteCriado.telefone, cpf=clienteCriado.cpf)

        return clienteResponse
    
    def buscar_cliente_por_cpf(self, cpf: str) -> ClienteResponseSchema:
        clienteBusca: Cliente = self.cliente_entities.buscar_por_cpf(cpf=cpf)
        clienteResponse: ClienteResponseSchema = ClienteResponseSchema(cliente_id=clienteBusca.cliente_id, nome=clienteBusca.nome, email=clienteBusca.email, telefone=clienteBusca.telefone, cpf=clienteBusca.cpf)

        return clienteResponse
    
    def buscar_cliente_por_id(self, cliente_id: int) -> ClienteResponseSchema:
        clienteBusca: Cliente = self.cliente_entities.buscar_por_id(cliente_id=cliente_id)
        clienteResponse: ClienteResponseSchema = ClienteResponseSchema(cliente_id=clienteBusca.cliente_id, nome=clienteBusca.nome, email=clienteBusca.email, telefone=clienteBusca.telefone, cpf=clienteBusca.cpf)

        return clienteResponse
    
    def listar_clientes(self) -> list[ClienteResponseSchema]:
        clientesBusca: list[Cliente] = self.cliente_entities.listar_todos()
        clienteResponse: list[ClienteResponseSchema] = []
        
        for row in clientesBusca:
            clienteResponse.append(
                ClienteResponseSchema(cliente_id=row.cliente_id, nome=row.nome, email=row.email, telefone=row.telefone, cpf=row.cpf)
            )
        
        return clienteResponse

    def atualizar_cliente(self, cliente_id: int,  clienteRequest: ClienteUpdateSchema) -> ClienteResponseSchema:
        clienteEntity: Cliente = self.buscar_cliente_por_id(cliente_id=cliente_id)
        clienteEntity.cliente_id = cliente_id
        clienteEntity.nome = clienteRequest.nome
        clienteEntity.email = clienteRequest.email
        clienteEntity.telefone = clienteRequest.telefone
        clienteEntity.cpf = clienteRequest.cpf
        
        clienteAtualizado: Cliente = self.cliente_entities.atualizar_cliente(cliente=clienteEntity)
        clienteResponse: ClienteResponseSchema = ClienteResponseSchema(cliente_id=clienteAtualizado.cliente_id, nome=clienteAtualizado.nome, email=clienteAtualizado.email, telefone=clienteAtualizado.telefone, cpf=clienteAtualizado.cpf)

        return clienteResponse

    def deletar_cliente(self, cliente_id: int) -> None:
        
        self.cliente_entities.deletar_cliente(cliente_id=cliente_id)