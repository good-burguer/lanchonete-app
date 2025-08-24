from abc import ABC, abstractmethod

from .models import Produto
from app.adapters.presenters.produto_presenter import ProdutoResponse

class ProdutoEntities(ABC):
    @abstractmethod
    def criar_produto(self, produto: Produto): pass
    
    @abstractmethod
    def listar_todos(self): pass
    
    @abstractmethod
    def buscar_por_id(self, produto_id: int): pass
    
    @abstractmethod
    def atualizar_produto(self, produto_id: int, produto_data: Produto): pass
    
    @abstractmethod
    def deletar_produto(self, produto_id: int): pass

class ProdutoOutputPort(ABC):
    @abstractmethod
    def apresentar(self, produto: Produto) -> ProdutoResponse: pass