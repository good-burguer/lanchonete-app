from fastapi import HTTPException, Response, status
from app.use_cases.produto.produto_use_case import ProdutoUseCase

class ProdutoController:
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def criar_produto(self, produto):
        try:
            return ProdutoUseCase(self.db_session).criar_produto(produto)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_todos(self):
        try:
            return ProdutoUseCase(self.db_session).listar_todos()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_produtos_por_categoria(self, categoria):
        try:

            return ProdutoUseCase(self.db_session).listar_por_categoria(categoria)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_produto(self, produto_id):
        try:

            return ProdutoUseCase(self.db_session).buscar_por_id(produto_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar_produto(self, produto_id, produto):
        try:

            return ProdutoUseCase(self.db_session).atualizar_produto(produto_id, produto_data=produto)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def deletar_produto(self, produto_id):
        try:
            ProdutoUseCase(self.db_session).deletar_produto(produto_id)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))