from fastapi import HTTPException, status, Response

from app.use_cases.status_pedido_use_case import StatusPedidoUseCase
from app.adapters.presenters.status_pedido_presenter import StatusPedidoResponse, StatusPedidoResponseList
from app.adapters.dto.status_pedido_dto import StatusPedidoCreateSchema, StatusPedidoUpdateSchema

class StatusPedidoController:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar(self, dataRequest: StatusPedidoCreateSchema):
        try:
            result = StatusPedidoUseCase(self.db_session).criar(statusRequest=dataRequest)
            
            return StatusPedidoResponse(status='success', data=result)
        except Exception as e:       
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_por_id(self, id: int):
        try:
            result = StatusPedidoUseCase(self.db_session).buscar_por_id(id)

            return StatusPedidoResponse(status='success', data=result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:       
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_todos(self):
        try:
            result = StatusPedidoUseCase(self.db_session).listar_todos()
            
            return StatusPedidoResponseList(status='success', data=result)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar(self, id: int, data: StatusPedidoUpdateSchema):
        try:
            result = StatusPedidoUseCase(self.db_session).atualizar(id=id, dataRequest=data)

            return StatusPedidoResponse(status='success', data=result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def deletar(self, id: int):
        try:
            StatusPedidoUseCase(self.db_session).deletar(id=id)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))