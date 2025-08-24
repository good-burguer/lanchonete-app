from sqlalchemy.exc import IntegrityError

from app.models.status_pedido import StatusPedido
from app.models.status_pedido import StatusPedido as StatusPedidoModel

class StatusPedidoDAO:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar(self, status: StatusPedido):
        try:
            status_pedido = StatusPedidoModel(
                descricao=status.descricao
            )
            self.db_session.add(status_pedido)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao criar o status: {e}")
        
        self.db_session.refresh(status_pedido)
        
        return status_pedido

    def buscar_por_id(self, id: int) -> StatusPedido | None :
        
        return self.db_session.query(StatusPedidoModel).filter_by(id=id).first()
    
    def listar_todos(self) -> StatusPedido | None :

        return (self.db_session
                .query(StatusPedido)
                .all())

    def atualizar(self, id : int, status: StatusPedido) -> StatusPedido:
        entity = self.db_session.query(StatusPedidoModel).filter_by(id=id).first()

        if entity :
            for field, value in status.model_dump().items():
                setattr(entity, field, value)

            self.db_session.commit()
            self.db_session.refresh(entity)
        
        return entity

    def deletar(self, id: int) -> None:
        entity = self.db_session.query(StatusPedidoModel).filter_by(id=id).first()

        if entity:           
            self.db_session.delete(entity)
            self.db_session.commit()