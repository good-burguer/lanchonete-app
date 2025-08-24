from typing import List

from app.entities.produto.entities import ProdutoEntities
from app.models.produto import Produto
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.adapters.dto.produto_dto import ProdutoCreateSchema
from app.adapters.schemas.categoria_produto import CategoriaProdutoResponseSchema

class ProdutoUseCase:
    def __init__(self, entity: ProdutoEntities):
        self.produto_entity = entity

    def criar_produto(self, produto):
        produto = self.produto_entity.criar_produto(produto)
        
        return self._create_response_schema(produto)       
   
    def listar_todos(self) -> List[ProdutoResponseSchema]:
        produtos = self.produto_entity.listar_todos()
        produtos_response = []
        
        for produto in produtos:
            produto = self._create_response_schema(produto)
            produtos_response.append(produto)
            
        return produtos_response
    
    def listar_por_categoria(self, categoria: str) -> List[ProdutoResponseSchema]:
        produtos = self.produto_entity.listar_por_categoria(categoria)
        produtos_response = []

        for produto in produtos:
            produto = self._create_response_schema(produto)
            produtos_response.append(produto)

        return produtos_response
    
    def buscar_por_id(self, produto_id: int) -> ProdutoResponseSchema:
        produto = self.produto_entity.buscar_por_id(produto_id)
        
        if not produto:
            raise ValueError("Produto não encontrado")

        return self._create_response_schema(produto)
    
    def atualizar_produto(self, produto_id: int, produto_data: ProdutoCreateSchema) -> ProdutoResponseSchema:
        produto = self.produto_entity.atualizar_produto(produto_id, produto_data)
        
        if not produto:
            raise ValueError("Produto não encontrado")

        return self._create_response_schema(produto)
    
    def deletar_produto(self, produto_id: int):

        return self.produto_entity.deletar_produto(produto_id)
    
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