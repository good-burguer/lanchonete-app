from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.gateways.produto_gateway import ProdutoGateway
from app.adapters.presenters.produto_presenter import ProdutoResponse
from app.adapters.dto.produto_dto import ProdutoCreateSchema, ProdutoUpdateSchema
from app.controllers.produto_controller import ProdutoController

router = APIRouter(prefix="/produtos", tags=["produtos"])

def get_produto_gateway(database: Session = Depends(get_db)) -> ProdutoGateway:
    
    return ProdutoGateway(db_session=database)

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao criar o produto"
                }
            }
        }
    }
})
def criar_produto(produto_data: ProdutoCreateSchema, gateway: ProdutoGateway = Depends(get_produto_gateway)):
    try:

        return (ProdutoController(db_session=gateway)
                    .criar_produto(produto_data))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#! Corrigir swagger
@router.get("/", responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar os produtos"
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def listar_produtos(gateway: ProdutoGateway = Depends(get_produto_gateway)):
    try:
        
        return (ProdutoController(db_session=gateway)
                    .listar_todos())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#! Corrigir swagger
@router.get("/categoria/{categoria}", responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar o produto"
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def listar_produtos_por_categoria(categoria: int, gateway: ProdutoGateway = Depends(get_produto_gateway)):
    try:
        
        return (ProdutoController(db_session=gateway)
                    .listar_produtos_por_categoria(categoria))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{produto_id}", responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar o produto"
                }
            }
        }
    },
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Produto não encontrado"
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def buscar_produto(produto_id: int, gateway: ProdutoGateway = Depends(get_produto_gateway)):
    try:
        
        return (ProdutoController(db_session=gateway)
                    .buscar_produto(produto_id))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{produto_id}", response_model=ProdutoResponse, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Produto não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao atualizar o produto"
                }
            }
        }
    }
})
def atualizar_produto(produto_id: int, produto: ProdutoUpdateSchema, gateway: ProdutoGateway = Depends(get_produto_gateway)):
    try:
        
        return (ProdutoController(db_session=gateway)
                    .atualizar_produto(produto_id, produto=produto))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Produto não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao remover o produto"
                }
            }
        }
    },
    204: {
        "description": "Produto deletado com sucesso",
        "content": {
            "application/json": {
                "example": {}
            }
        }
    }
})
def deletar_produto(produto_id: int, gateway: ProdutoGateway = Depends(get_produto_gateway)):
    try:
        ProdutoController(db_session=gateway).deletar_produto(produto_id)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))