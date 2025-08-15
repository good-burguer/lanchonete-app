from fastapi import status, HTTPException, Response
from app.use_cases.pedido.pedido_use_case import PedidoUseCase
from app.use_cases.pedido_produtos.pedido_produtos_use_case import PedidoProdutosUseCase
from app.adapters.schemas.pedido import PedidoCreateSchema, PedidoResponseSchema, PedidoAtualizaSchema, PedidoProdutosResponseSchema

class PedidoController:
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def criarPedido(self, pedido, pedidoProdutosGateway, produtoGateway):
    
        orderUseCase = PedidoUseCase(self.db_session).criarPedido(pedidoRequest=pedido)

        productOrderUseCase = (PedidoProdutosUseCase(pedidoProdutosGateway)
            .criarPedidoProdutos(orderUseCase.pedido_id, pedido.produtos, produtoGateway=produtoGateway))

        pedidoResponse: PedidoProdutosResponseSchema = PedidoProdutosResponseSchema(
            pedido_id=orderUseCase.pedido_id,
            cliente_id=orderUseCase.cliente_id,
            status=orderUseCase.status,
            data_criacao=orderUseCase.data_criacao,
            data_alteracao=orderUseCase.data_alteracao,
            data_finalizacao=orderUseCase.data_finalizacao,
            produtos=productOrderUseCase
        )

        return pedidoResponse

    def listar_todos(self):
        try:

            return PedidoUseCase(self.db_session).listar_todos()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_por_id(self, pedido_id, pedidoProdutosRepository, produtoRepository):
        try:
            orderUseCase = PedidoUseCase(self.db_session).buscar_por_id(pedido_id=pedido_id)
            productOrderUseCase = PedidoProdutosUseCase(pedidoProdutosRepository).buscarPorIdPedido(pedido_id=orderUseCase.pedido_id, produtoRepository=produtoRepository)

            pedidoResponse: PedidoProdutosResponseSchema = PedidoProdutosResponseSchema(
                pedido_id=orderUseCase.pedido_id,
                cliente_id=orderUseCase.cliente_id,
                status=orderUseCase.status,
                data_criacao=orderUseCase.data_criacao,
                data_alteracao=orderUseCase.data_alteracao,
                data_finalizacao=orderUseCase.data_finalizacao,
                produtos=productOrderUseCase 
            )
            
            return pedidoResponse
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualiza(self, pedido_id, pedidoRequest):
        try:

            return PedidoUseCase(self.db_session).atualiza(pedido_id=pedido_id, pedidoRequest=pedidoRequest)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def deletar(self, pedido_id, repositoryProductOrder):
        try:
            PedidoProdutosUseCase(repositoryProductOrder).deletarPorPedido(pedido_id)
            PedidoUseCase(self.db_session).deletar(pedido_id)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
