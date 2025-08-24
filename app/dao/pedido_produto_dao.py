from sqlalchemy.exc import IntegrityError

from app.models.pedido_produto import PedidoProdutoModel

class PedidoProdutoDAO:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar_pedido_produto(self, pedido_id, produto_id) -> PedidoProdutoModel:
        try:
            entity: PedidoProdutoModel = (PedidoProdutoModel(pedido_id=pedido_id, 
                                                             produto_id=produto_id))

            self.db_session.add(entity)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar produtos no pedido: {e}")
        
        self.db_session.refresh(entity)

        return entity
    
    def buscarPorIdPedido(self, pedido_id: int) -> PedidoProdutoModel:       
        
        return (self.db_session
                .query(PedidoProdutoModel)
                .filter(PedidoProdutoModel.pedido_id == pedido_id)
                .all())
    
    def deletar(self, id: int) -> None:
        db_pedido_produtos = self.db_session.query(PedidoProdutoModel).filter(PedidoProdutoModel.id == id).first()

        if db_pedido_produtos:
            self.db_session.delete(db_pedido_produtos)
            self.db_session.commit()       
            #self.db_session.flush()