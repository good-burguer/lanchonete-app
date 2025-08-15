from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.gateways.cliente_gateway import ClienteGateway
from app.infrastructure.db.database import get_db
from app.adapters.schemas.cliente import ClienteCreateSchema, ClienteResponseSchema, ClienteUpdateSchema
from app.controllers.cliente_controller import ClienteController

router = APIRouter(prefix="/clientes", tags=["clientes"])

# Dependência para injetar o service
def get_cliente_gateway(db: Session = Depends(get_db)) -> ClienteGateway:
    
    return ClienteGateway(db_session=db)

@router.post("/", response_model=ClienteResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao criar cliente"
                }
            }
        }
    }
})
def criar_cliente(cliente_data: ClienteCreateSchema, gateway: ClienteGateway = Depends(get_cliente_gateway)):
    try:
        return ClienteController.criar_cliente(cliente_data, gateway)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/cpf/{cpf}", response_model=ClienteResponseSchema, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Cliente não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": ""
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def buscar_cliente_por_cpf(cpf: str, gateway: ClienteGateway = Depends(get_cliente_gateway)):
    try:

        return ClienteController.buscar_cliente_por_cpf(cpf, gateway)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{cliente_id}", response_model=ClienteResponseSchema, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Cliente não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": ""
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def buscar_cliente(cliente_id: int, gateway: ClienteGateway = Depends(get_cliente_gateway)):
    try:

        return ClienteController.buscar_cliente(cliente_id, gateway)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ClienteResponseSchema], responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": ""
                }
            }
        }
    }
}, 
openapi_extra={
    "responses": {
        "422": None  
    }
})
def listar_clientes(gateway: ClienteGateway = Depends(get_cliente_gateway)):
    try:

        return ClienteController.listar_clientes(gateway)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{cliente_id}", response_model=ClienteResponseSchema, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Cliente não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao atualizar o cliente"
                }
            }
        }
    }
})
def atualizar_cliente(cliente_id: int, cliente_data: ClienteUpdateSchema, gateway: ClienteGateway = Depends(get_cliente_gateway)):
    try:
        return ClienteController.atualizar_cliente(cliente_id=cliente_id, cliente_data=cliente_data, gateway=gateway)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Cliente não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao deletar o cliente"
                }
            }
        }
    },
    204: {
        "description": "Pedido deletado com sucesso",
        "content": {
            "application/json": {
                "example": {}
            }
        }
    }
})
def deletar_cliente(cliente_id: int, gateway: ClienteGateway = Depends(get_cliente_gateway)):
    try:
        ClienteController.deletar_cliente(cliente_id=cliente_id, gateway=gateway)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))