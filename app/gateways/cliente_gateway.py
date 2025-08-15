from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.entities.cliente.models import Cliente
from app.entities.cliente.entities import ClienteEntities
from app.models.cliente import Cliente as ClienteORM
from app.adapters.schemas.cliente import ClienteResponseSchema

class ClienteGateway(ClienteEntities):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def criar_cliente(self, cliente: Cliente) -> Cliente:
        try:
            db_cliente = ClienteORM(
                nome=cliente.nome,
                email=cliente.email,
                telefone=cliente.telefone,
                cpf=cliente.cpf
            )
            self.db_session.add(db_cliente)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao criar cliente: {e}")
        
        self.db_session.refresh(db_cliente)
        response = ClienteResponseSchema.model_validate(db_cliente, from_attributes=True)

        return response

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        cliente_orm = self.db_session.query(ClienteORM).filter_by(cpf=cpf).first()

        if not cliente_orm:
            raise ValueError("Cliente não encontrado")
        
        return cliente_orm

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        cliente_orm = self.db_session.query(ClienteORM).filter_by(cliente_id=cliente_id).first()
        
        if not cliente_orm:
            raise ValueError("Cliente não encontrado")
        
        return cliente_orm

    def listar_todos(self) -> List[Cliente]:
        clientes_orm = self.db_session.query(ClienteORM).all()

        return clientes_orm

    def atualizar_cliente(self, cliente: Cliente) -> Cliente:
        cliente_orm = self.db_session.query(ClienteORM).filter_by(cliente_id=cliente.cliente_id).first()

        if not cliente_orm:
            raise ValueError("Cliente não encontrado")
        
        for field, value in cliente.model_dump().items():
            setattr(cliente_orm, field, value)

        self.db_session.commit()
        self.db_session.refresh(cliente_orm)

        return cliente_orm

    def deletar_cliente(self, cliente_id: int) -> None:
        cliente_orm = self.db_session.query(ClienteORM).filter_by(cliente_id=cliente_id).first()

        if not cliente_orm:
            raise ValueError("Cliente não encontrado")
        
        self.db_session.delete(cliente_orm)
        self.db_session.commit()