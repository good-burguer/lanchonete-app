from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional

from app.entities.status_pedido.entities import StatusPedidoEntities
from app.entities.status_pedido.models import StatusPedido
from app.models.status_pedido import StatusPedido as StatusPedidoORM
from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema

class StatusPedidoRepository(StatusPedidoEntities):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def criar(self, status: StatusPedido):
        try:
            db_status = StatusPedidoORM(
                descricao=status.descricao
            )
            self.db_session.add(db_status)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao criar o status: {e}")
        
        self.db_session.refresh(db_status)
        response = StatusPedidoResponseSchema.model_validate(db_status, from_attributes=True)
        
        return response

    def buscar_por_id(self, id: int) -> Optional[StatusPedido]:
        orm = self.db_session.query(StatusPedidoORM).filter_by(id=id).first()
        
        if not orm:
            raise ValueError("Status não encontrado")
        
        return orm

    def listar_todos(self) -> List[StatusPedido]:
        orm = self.db_session.query(StatusPedidoORM).all()

        return orm
    
    def atualizar(self, status: StatusPedido) -> StatusPedido:
        orm = self.db_session.query(StatusPedidoORM).filter_by(id=status.id).first()

        if not orm:
            raise ValueError("Status não encontrado")
        
        for field, value in status.model_dump().items():
            setattr(orm, field, value)

        self.db_session.commit()
        self.db_session.refresh(orm)

        return orm

    def deletar(self, id: int) -> None:
        orm = self.db_session.query(StatusPedidoORM).filter_by(id=id).first()

        if not orm:
            raise ValueError("Status não encontrado")
        
        self.db_session.delete(orm)
        self.db_session.commit()