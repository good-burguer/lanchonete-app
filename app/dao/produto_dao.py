from sqlalchemy.exc import IntegrityError
from decimal import Decimal

from app.models.produto import Produto
from app.adapters.enums.categoria_produto import CategoriaProdutoEnum

class ProdutoDAO:
    
    def __init__(self, db_session):
        
        self.db_session = db_session

    def criar_produto(self, produto: Produto) :
        db_produto = Produto(
            nome=produto.nome,
            descricao=produto.descricao,
            preco=Decimal(produto.preco),
            categoria=produto.categoria
        )

        try:
            self.db_session.add(db_produto)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar o produto: {e}")
        
        self.db_session.refresh(db_produto)
        
        return db_produto
    
    def listar_todos(self) -> Produto | None :
        
        return (self.db_session
                .query(Produto)
                .all())

    def listar_por_categoria(self, categoria: CategoriaProdutoEnum) -> Produto | None :
        
        return (self.db_session
                .query(Produto)
                .filter(Produto.categoria == categoria)
                .all())

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        
        return (self.db_session.query(Produto)
                .filter(Produto.produto_id == produto_id)
                .first())

    def atualizar_produto(self, produto_id: int, produto_data: Produto) -> Produto:
        produto = self.buscar_por_id(produto_id)
        
        if produto:
            produto.nome = produto_data.nome
            produto.descricao = produto_data.descricao
            produto.preco = Decimal(produto_data.preco)
            produto.categoria = produto_data.categoria

            try:
                self.db_session.commit()
            except IntegrityError as e:
                self.db_session.rollback()

                raise Exception(f"Erro de integridade ao atualizar o produto: {e}")
            
            self.db_session.refresh(produto)

        return produto

    def deletar_produto(self, produto_id: int) -> None :
        produto = self.buscar_por_id(produto_id)
        
        if not produto:
            raise ValueError("Produto não encontrado")
        
        self.db_session.delete(produto)
        self.db_session.commit()