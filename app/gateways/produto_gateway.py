from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.entities.produto.entities import ProdutoEntities
from app.entities.produto.models import Produto
from app.adapters.enums.categoria_produto import CategoriaProdutoEnum
from app.models.produto import Produto
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.adapters.schemas.categoria_produto import CategoriaProdutoResponseSchema
# from app.models.produto import Produto

class ProdutoGateway(ProdutoEntities):
    def __init__(self, db_session):
        self.db_session = db_session

    def criar_produto(self, produto: Produto) -> Produto:
        db_produto = Produto(
            nome=produto.nome,
            descricao=produto.descricao,
            preco=Decimal(produto.preco),
            categoria=produto.categoria
        )
        self.db_session.add(db_produto)

        try:
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar o produto: {e}")
        
        self.db_session.refresh(db_produto)
        
        categoriaProduto: CategoriaProdutoResponseSchema = (CategoriaProdutoResponseSchema(
            id=db_produto.categoria_rel.id, 
            nome=db_produto.categoria_rel.nome
        ))

        produto: ProdutoResponseSchema = (ProdutoResponseSchema(
            produto_id=db_produto.produto_id,
            nome=db_produto.nome,
            descricao=db_produto.descricao,
            preco=db_produto.preco,
            categoria=categoriaProduto
        ))

        return produto

    def buscar_por_id(self, produto_id: int) -> Produto:
        db_produto = (self.db_session.query(Produto)
                      .filter(Produto.produto_id == produto_id)
                      .first())
        
        if not db_produto:
            raise ValueError("Produto não encontrado")
        
        categoriaProduto: CategoriaProdutoResponseSchema = CategoriaProdutoResponseSchema(id=db_produto.categoria_rel.id, nome=db_produto.categoria_rel.nome)
        produto: ProdutoResponseSchema = (ProdutoResponseSchema(
            produto_id=db_produto.produto_id,
            nome=db_produto.nome,
            descricao=db_produto.descricao,
            preco=db_produto.preco,
            categoria=categoriaProduto
        ))
        
        return produto

    def listar_todos(self) -> list[Produto]:
        db_produtos = self.db_session.query(Produto).all()
        produtos = []
        
        for db_produto in db_produtos:
            categoriaProduto: CategoriaProdutoResponseSchema = CategoriaProdutoResponseSchema(id=db_produto.categoria_rel.id, nome=db_produto.categoria_rel.nome)
            produto: ProdutoResponseSchema = (ProdutoResponseSchema(
                produto_id=db_produto.produto_id,
                nome=db_produto.nome,
                descricao=db_produto.descricao,
                preco=db_produto.preco,
                categoria=categoriaProduto
            ))
            produtos.append(produto)
            
        return produtos

    def deletar_produto(self, produto_id: int) -> None:
        db_produto = self.db_session.query(Produto).filter(Produto.produto_id == produto_id).first()
        
        if not db_produto:
            raise ValueError("Produto não encontrado")
        self.db_session.delete(db_produto)
        self.db_session.commit()
        #self.db_session.flush()

    def atualizar_produto(self, produto_id: int, produto_data: Produto) -> Produto:
        db_produto = self.db_session.query(Produto).filter(Produto.produto_id == produto_id).first()
        if not db_produto:
            raise ValueError("Produto não encontrado")

        db_produto.nome = produto_data.nome
        db_produto.descricao = produto_data.descricao
        db_produto.preco = Decimal(produto_data.preco)
        db_produto.categoria = produto_data.categoria

        try:
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            raise Exception(f"Erro de integridade ao atualizar o produto: {e}")
        self.db_session.refresh(db_produto)

        categoriaProduto: CategoriaProdutoResponseSchema = CategoriaProdutoResponseSchema(id=db_produto.categoria_rel.id, nome=db_produto.categoria_rel.nome)
        produto: ProdutoResponseSchema = (ProdutoResponseSchema(
            produto_id=db_produto.produto_id,
            nome=db_produto.nome,
            descricao=db_produto.descricao,
            preco=db_produto.preco,
            categoria=categoriaProduto
        ))
        
        return produto
    
    def listar_por_categoria(self, categoria: CategoriaProdutoEnum) -> list[Produto]:
        db_produtos = self.db_session.query(Produto).filter(Produto.categoria == categoria).all()
        produtos = []

        for db_produto in db_produtos:
            categoriaProduto: CategoriaProdutoResponseSchema = CategoriaProdutoResponseSchema(id=db_produto.categoria_rel.id, nome=db_produto.categoria_rel.nome)
            produto: ProdutoResponseSchema = (ProdutoResponseSchema(
                produto_id=db_produto.produto_id,
                nome=db_produto.nome,
                descricao=db_produto.descricao,
                preco=db_produto.preco,
                categoria=categoriaProduto
            ))
            produtos.append(produto)

        return produtos