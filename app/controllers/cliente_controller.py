from fastapi import status, HTTPException, Response

from app.use_cases.cliente_use_case import ClienteUseCase
from app.adapters.presenters.cliente_presenter import ClienteResponse, ClienteResponseList
from app.adapters.dto.cliente_dto import ClienteCreateSchema, ClienteUpdateSchema

class ClienteController:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar_cliente(self, cliente_data : ClienteCreateSchema):
        try:
            result = ClienteUseCase(self.db_session).criar_cliente(cliente_data)

            return ClienteResponse(status = 'success', data = result)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def buscar_cliente_por_cpf(self, cpf_cliente: str):
        try:
            result = ClienteUseCase(self.db_session).buscar_cliente_por_cpf(cpf_cliente)

            return ClienteResponse(status = 'success', data = result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_cliente(self, cliente_id: int):
        try:
            result = ClienteUseCase(self.db_session).buscar_cliente_por_id(cliente_id)

            return ClienteResponse(status = 'success', data = result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_clientes(self):
        try:
            result = ClienteUseCase(self.db_session).listar_clientes()

            return ClienteResponseList(status = 'succes', data = result)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdateSchema):
        try:
            result = ClienteUseCase(self.db_session).atualizar_cliente(cliente_id=cliente_id, clienteRequest=cliente_data)

            return ClienteResponse(status = 'succes', data = result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def deletar_cliente(self, cliente_id: int):
        try:
            ClienteUseCase(self.db_session).deletar_cliente(cliente_id=cliente_id)
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
