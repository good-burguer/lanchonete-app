from typing import List

from app.entities.produto.entities import ProdutoEntities
from app.models.produto import Produto
from app.adapters.schemas.produto import ProdutoResponseSchema, ProdutoCreateSchema

class ProdutoUseCase:
    def __init__(self, produto_repository: ProdutoEntities):
        self.produto_repository = produto_repository

    def criar_produto(self, produto):
        produto = Produto(nome=produto.nome, descricao=produto.descricao, preco=produto.preco, categoria=produto.categoria)
        
        return self.produto_repository.criar_produto(produto)
    
    def listar_todos(self) -> List[ProdutoResponseSchema]:
        produtos = self.produto_repository.listar_todos()

        return [ProdutoResponseSchema.model_validate(produto) for produto in produtos]
    
    def listar_por_categoria(self, categoria: str) -> List[ProdutoResponseSchema]:
        produtos = self.produto_repository.listar_por_categoria(categoria)

        return [ProdutoResponseSchema.model_validate(produto) for produto in produtos]
    
    def buscar_por_id(self, produto_id: int) -> ProdutoResponseSchema:
        produto = self.produto_repository.buscar_por_id(produto_id)

        return ProdutoResponseSchema.model_validate(produto)
    
    def atualizar_produto(self, produto_id: int, produto_data: ProdutoCreateSchema) -> ProdutoResponseSchema:
        produto_atualizado = self.produto_repository.atualizar_produto(produto_id, produto_data)

        return ProdutoResponseSchema.model_validate(produto_atualizado)
    
    def deletar_produto(self, produto_id: int):

        return self.produto_repository.deletar_produto(produto_id)