from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.gateways.pedido_gateway import PedidoGateway
from app.gateways.pedido_produto_gateway import PedidoProdutoGateway
from app.gateways.produto_gateway import ProdutoGateway
from app.controllers.pedido_controller import PedidoController
from app.adapters.schemas.pedido import PedidoCreateSchema, PedidoResponseSchema, PedidoAtualizaSchema, PedidoProdutosResponseSchema

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

def get_pedido_gateway(db: Session = Depends(get_db)) -> PedidoGateway:
    return PedidoGateway(db_session=db)

def get_pedido_produto_gateway(db: Session = Depends(get_db)) -> PedidoProdutoGateway:
    return PedidoProdutoGateway(db_session=db)

def get_produto_gateway(db: Session = Depends(get_db)) -> ProdutoGateway:
    return ProdutoGateway(db_session=db)

@router.post("/", response_model=PedidoProdutosResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao salvar o pedido | Erro de integridade ao salvar produtos no pedido"
                }
            }
        }
    }
})
def criar_pedido(
        pedido: PedidoCreateSchema, 
        pedidoGateway: PedidoGateway = Depends(get_pedido_gateway), 
        pedidoProdutosGateway: PedidoProdutoGateway = Depends(get_pedido_produto_gateway), 
        produtoGateway: ProdutoGateway = Depends(get_produto_gateway)
    ):
    
    try:
        return PedidoController(pedidoGateway).criarPedido(pedido=pedido, pedidoProdutosGateway=pedidoProdutosGateway, produtoGateway=produtoGateway)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[PedidoResponseSchema], responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": ""
                }
            }
        }
    },
}, 
openapi_extra={
    "responses": {
        "422": None  
    }
})
def listar_pedidos(repository: PedidoGateway = Depends(get_pedido_gateway)):
    try:
        return PedidoController(repository).listar_todos()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{pedido_id}", response_model=PedidoProdutosResponseSchema, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Pedido não encontrado | Produto(s) do pedido não encontrado(s)"
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
def buscar_pedido(
        pedido_id: int, 
        gateway: PedidoGateway = Depends(get_pedido_gateway), 
        pedidoProdutosGateway: PedidoProdutoGateway = Depends(get_pedido_produto_gateway),
        produtoGateway: ProdutoGateway = Depends(get_produto_gateway)
    ):
    try:
        return PedidoController(db_session=gateway).buscar_por_id(pedido_id=pedido_id, pedidoProdutosRepository=pedidoProdutosGateway, produtoRepository=produtoGateway)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{pedido_id}", response_model=PedidoResponseSchema, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Pedido não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Pedido já finalizado"
                }
            }
        }
    }
})
def atualizar_pedido(pedido_id: int, pedido: PedidoAtualizaSchema, gateway: PedidoGateway = Depends(get_pedido_gateway)):
    try:

        return PedidoController(db_session=gateway).atualiza(pedido_id=pedido_id, pedidoRequest=pedido)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Pedido não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao deletar o pedido"
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
def deletar_pedido(pedido_id: int, gateway: PedidoGateway = Depends(get_pedido_gateway), repositoryProductOrder: PedidoProdutoGateway = Depends(get_pedido_produto_gateway)):
    try:
        return PedidoController(db_session=gateway).deletar(pedido_id=pedido_id, repositoryProductOrder=repositoryProductOrder)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    