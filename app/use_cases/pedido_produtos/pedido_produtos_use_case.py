from app.entities.pedido_produto.entities import PedidoProdutoEntities
from app.models.pedido_produto import PedidoProdutoModel
from app.adapters.schemas.pedido_produto import ProdutoPedidoResponseSchema
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.gateways.produto_gateway import ProdutoGateway

class PedidoProdutosUseCase:
    def __init__(self, pedido_produtos_repository: PedidoProdutoEntities):
        self.pedido_produtos_repository = pedido_produtos_repository

    def criarPedidoProdutos(self, pedido_id: int, produtos: list, produtoGateway: ProdutoGateway) -> ProdutoPedidoResponseSchema:
        if isinstance(produtos, list):
            produtosCriados = [];
            
            for produto in produtos:
                produtosCriados.append(self._criarPedidoProduto(pedido_id=pedido_id, produto_id=produto, produtoRepository=produtoGateway));

        return produtosCriados
    
    def _criarPedidoProduto(self, pedido_id: int, produto_id: list, produtoRepository: ProdutoGateway) -> ProdutoResponseSchema: 
        pedidoProdutosEntity: PedidoProdutoModel = PedidoProdutoModel(pedido_id=pedido_id, produto_id=produto_id)  
        pedidoProdutosEntity.pedido_id = pedido_id
        pedidoProdutosEntity.produto_id = produto_id

        pedidoProdutoCriado: PedidoProdutoEntities = self.pedido_produtos_repository.criarPedidoProduto(pedidoProduto=pedidoProdutosEntity)
        produtoResponse = produtoRepository.buscar_por_id(pedidoProdutoCriado.produto_id)

        return produtoResponse
    
    def buscarPorIdPedido(self, pedido_id: int, produtoRepository: ProdutoGateway) -> ProdutoPedidoResponseSchema:
        pedidoProdutos: PedidoProdutoModel = self.pedido_produtos_repository.buscarPorIdPedido(pedido_id=pedido_id)
        
        produtos = []
        
        for produto in pedidoProdutos:
            produtoResponse = produtoRepository.buscar_por_id(produto.produto_id)
            
            produtos.append(produtoResponse)

        return produtos
    
    def deletarPorPedido(self, pedido_id: int) -> None:
        pedidoProdutos: PedidoProdutoModel = self.pedido_produtos_repository.buscarPorIdPedido(pedido_id=pedido_id)
        
        if pedidoProdutos:
            for pedidoProduto in pedidoProdutos:
                self.pedido_produtos_repository.deletar(id=pedidoProduto.id)