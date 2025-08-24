from fastapi import status, HTTPException, Response

from app.use_cases.pedido_use_case import PedidoUseCase
from app.use_cases.pedido_produtos_use_case import PedidoProdutosUseCase
from app.adapters.presenters.pedido_presenter import PedidoResponse, PedidoResponseList
from app.adapters.schemas.pedido import PedidoProdutosResponseSchema

class PedidoController:
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def criar_pedido(self, pedido, pedidoProdutosGateway, produtoGateway):
        try:
            orderUseCase = PedidoUseCase(self.db_session).criar_pedido(pedido)
            
            productOrderUseCase = (PedidoProdutosUseCase(pedidoProdutosGateway)
                .criarPedidoProdutos(orderUseCase.pedido_id, pedido.produtos, produtoGateway))
            
            response = self._create_response_schema(orderUseCase, productOrderUseCase)
            
            return PedidoResponse(status = 'success', data = response)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_todos(self):
        try:
            result = PedidoUseCase(self.db_session).listar_todos()

            return PedidoResponseList(status = 'sucess', data = result)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_por_id(self, pedido_id, pedidoProdutosGateway, produtoRepository):
        try:
            orderUseCase = (PedidoUseCase(self.db_session)
                                .buscar_por_id(pedido_id=pedido_id))
            
            productOrderUseCase = (PedidoProdutosUseCase(pedidoProdutosGateway)
                                    .buscarPorIdPedido(pedido_id=orderUseCase.pedido_id, 
                                                       produtoRepository=produtoRepository))
            
            response = self._create_response_schema(orderUseCase, productOrderUseCase)

            return PedidoResponse(status = 'success', data = response)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar_pedido(self, pedido_id, pedidoRequest, pedidoProdutosGateway, produtoRepository):
        try:
            orderUseCase = PedidoUseCase(self.db_session).atualizar_pedido(pedido_id=pedido_id, pedidoRequest=pedidoRequest)
            
            productOrderUseCase = (PedidoProdutosUseCase(pedidoProdutosGateway)
                                    .buscarPorIdPedido(pedido_id=orderUseCase.pedido_id, 
                                                       produtoRepository=produtoRepository))
            
            response = self._create_response_schema(orderUseCase, productOrderUseCase)

            return PedidoResponse(status = 'success', data = response)       
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def deletar(self, pedido_id, repositoryProductOrder):
        try:
            PedidoProdutosUseCase(repositoryProductOrder).deletarPorPedido(pedido_id)
            PedidoUseCase(self.db_session).deletar_pedido(pedido_id)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    def _create_response_schema(self, pedido, pedidoProduto) :
        
        return PedidoProdutosResponseSchema(
                pedido_id=pedido.pedido_id,
                cliente_id=pedido.cliente_id,
                status=pedido.status,
                data_criacao=pedido.data_criacao,
                data_alteracao=pedido.data_alteracao,
                data_finalizacao=pedido.data_finalizacao,
                produtos=pedidoProduto
            )
