from fastapi import APIRouter, HTTPException, Response, status
from app.use_cases.status.status_pedido_use_case import StatusPedidoUseCase

router = APIRouter(prefix="/status_pedido", tags=["status_pedido"])

class StatusPedidoController:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar(self, dataRequest):
        try:

            return StatusPedidoUseCase(self.db_session).criar(dataRequest=dataRequest)
        except Exception as e:       
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_por_id(self, id):
        try:

            return StatusPedidoUseCase(self.db_session).buscar_por_id(id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:       
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_todos(self):
        try:
            return StatusPedidoUseCase(self.db_session).listar_todos()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar(self, id, data):
        try:

            return StatusPedidoUseCase(self.db_session).atualizar(id=id, dataRequest=data)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def deletar(self, id):
        try:
            StatusPedidoUseCase(self.db_session).deletar(id=id)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))