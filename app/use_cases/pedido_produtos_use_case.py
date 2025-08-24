from app.entities.pedido_produto.entities import PedidoProdutoEntities
from app.models.pedido_produto import PedidoProdutoModel
from app.adapters.schemas.pedido_produto import ProdutoPedidoResponseSchema
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.gateways.produto_gateway import ProdutoGateway
from app.adapters.schemas.categoria_produto import CategoriaProdutoResponseSchema

from app.adapters.utils.debug import var_dump_die

class PedidoProdutosUseCase:
    def __init__(self, pedido_produtos_gateway: PedidoProdutoEntities):
        self.pedido_produtos_gateway = pedido_produtos_gateway

    def criarPedidoProdutos(self, pedido_id: int, produtos: list, produtoGateway: ProdutoGateway) -> ProdutoPedidoResponseSchema:
        if isinstance(produtos, list):
            produtosCriados = [];
            
            for produto in produtos:
                produtosCriados.append(
                    (self._criarPedidoProduto(
                        pedido_id=pedido_id, 
                        produto_id=produto, 
                        produtoRepository=produtoGateway)))

        return produtosCriados
    
    def _criarPedidoProduto(self, pedido_id: int, produto_id: list, produtoRepository: ProdutoGateway) -> ProdutoResponseSchema: 
        pedidoProdutoCriado: PedidoProdutoEntities = (self.pedido_produtos_gateway
                                                      .criarPedidoProduto(pedido_id=pedido_id, produto_id=produto_id))
        
        produtoResponse = produtoRepository.buscar_por_id(pedidoProdutoCriado.produto_id)
        
        return self._create_response_schema(produtoResponse)
    
    def buscarPorIdPedido(self, pedido_id: int, produtoRepository: ProdutoGateway) -> ProdutoPedidoResponseSchema:
        pedidoProdutos: PedidoProdutoModel = self.pedido_produtos_gateway.buscarPorIdPedido(pedido_id=pedido_id)
        produtos = []
        
        for produto in pedidoProdutos:
            produtos.append(
                self._create_response_schema(
                    produtoRepository.buscar_por_id(produto.produto_id)
                )
            )

        return produtos
    
    def deletarPorPedido(self, pedido_id: int) -> None:
        pedidoProdutos: PedidoProdutoModel = self.pedido_produtos_gateway.buscarPorIdPedido(pedido_id=pedido_id)
        
        if pedidoProdutos:
            for pedidoProduto in pedidoProdutos:
                self.pedido_produtos_gateway.deletar(id=pedidoProduto.id)

    def _create_response_schema(self, produto) :
        categoriaProduto: CategoriaProdutoResponseSchema = (CategoriaProdutoResponseSchema(
            id=produto.categoria_rel.id, 
            nome=produto.categoria_rel.nome
        ))
        
        return (ProdutoResponseSchema(
            produto_id=produto.produto_id,
            nome=produto.nome,
            descricao=produto.descricao,
            preco=produto.preco,
            categoria=categoriaProduto
        )) 