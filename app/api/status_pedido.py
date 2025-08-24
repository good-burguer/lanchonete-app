from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.db.database import get_db
from app.gateways.status_pedido_gateway import StatusPedidoGateway
from app.adapters.presenters.status_pedido_presenter import StatusPedidoResponse
from app.adapters.dto.status_pedido_dto import StatusPedidoCreateSchema, StatusPedidoUpdateSchema
from app.controllers.status_pedido_controller import StatusPedidoController

router = APIRouter(prefix="/status_pedido", tags=["status_pedido"])

def get_status_repository(database: Session = Depends(get_db)) -> StatusPedidoGateway:
    
    return StatusPedidoGateway(db_session=database)

@router.post("/", response_model=StatusPedidoResponse, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao criar o status"
                }
            }
        }
    }
})
def criar(data: StatusPedidoCreateSchema, gateway: StatusPedidoGateway = Depends(get_status_repository)):
    try:
        return StatusPedidoController(db_session=gateway).criar(dataRequest=data)
    except Exception as e:       
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id}", response_model=StatusPedidoResponse, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar o status"
                }
            }
        }
    },
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Status não encontrado"
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def buscar_status(id: int, gateway: StatusPedidoGateway = Depends(get_status_repository)):
    try:

        return StatusPedidoController(db_session=gateway).buscar_por_id(id=id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:       
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar os statuses"
                }
            }
        }
    }
}
,openapi_extra={
    "responses": {
        "422": None
    }
})
def listar_todos(gateway: StatusPedidoGateway = Depends(get_status_repository)):
    try:

        return StatusPedidoController(db_session=gateway).listar_todos()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}", response_model=StatusPedidoResponse, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Status não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao atualizar o status"
                }
            }
        }
    }
})
def atualizar(id: int, data: StatusPedidoUpdateSchema, gateway: StatusPedidoGateway = Depends(get_status_repository)):
    try:

        return StatusPedidoController(db_session=gateway).atualizar(id=id, data=data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Status não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao excluir o status"
                }
            }
        }
    },
    204: {
        "description": "Status deletado com sucesso",
        "content": {
            "application/json": {
                "example": {}
            }
        }
    }
})
def deletar(id: int, gateway: StatusPedidoGateway = Depends(get_status_repository)):
    try:
        
        return StatusPedidoController(db_session=gateway).deletar(id=id)       
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))