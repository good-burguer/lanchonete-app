from app.entities.cliente.entities import ClienteEntities
from app.entities.cliente.models import Cliente
from app.adapters.schemas.cliente import ClienteResponseSchema
from app.adapters.dto.cliente_dto import ClienteCreateSchema, ClienteUpdateSchema

class ClienteUseCase:
    def __init__(self, entity: ClienteEntities):
        self.cliente_entities = entity

    def criar_cliente(self, clienteRequest: ClienteCreateSchema) -> ClienteResponseSchema:       
        clienteCriado: Cliente = self.cliente_entities.criar_cliente(cliente=clienteRequest)
        
        return self._create_response_schema(clienteCriado)
    
    def buscar_cliente_por_cpf(self, cpf_cliente: str) -> ClienteResponseSchema:
        clienteBusca: Cliente = self.cliente_entities.buscar_por_cpf(cpf_cliente=cpf_cliente)
        
        if not clienteBusca :
            raise ValueError("Cliente não encontrado")
            
        return self._create_response_schema(clienteBusca)
    
    def buscar_cliente_por_id(self, cliente_id: int) -> ClienteResponseSchema:
        clienteBusca: Cliente = self.cliente_entities.buscar_por_id(cliente_id=cliente_id)
        
        if not clienteBusca :
            raise ValueError("Cliente não encontrado")
        
        return self._create_response_schema(clienteBusca)
    
    def listar_clientes(self) -> list[ClienteResponseSchema]:
        clientesBusca: list[Cliente] = self.cliente_entities.listar_todos()
        clienteResponse: list[ClienteResponseSchema] = []
        
        for row in clientesBusca:
            clienteResponse.append(
                self._create_response_schema(row)
            )
        
        return clienteResponse

    def atualizar_cliente(self, cliente_id: int,  clienteRequest: ClienteUpdateSchema) -> ClienteResponseSchema:
        clienteEntity: Cliente = self.buscar_cliente_por_id(cliente_id=cliente_id)
        
        if not clienteEntity :
            raise ValueError("Cliente não encontrado")
        
        clienteAtualizado: Cliente = self.cliente_entities.atualizar_cliente(cliente_id=cliente_id,cliente=clienteRequest)

        return self._create_response_schema(clienteAtualizado)

    def deletar_cliente(self, cliente_id: int) -> None:
        
        self.cliente_entities.deletar_cliente(cliente_id=cliente_id)

    def _create_response_schema(self, cliente) :
        
        return (ClienteResponseSchema(
                cliente_id=cliente.cliente_id, 
                nome=cliente.nome, 
                email=cliente.email, 
                telefone=cliente.telefone, 
                cpf=cliente.cpf))