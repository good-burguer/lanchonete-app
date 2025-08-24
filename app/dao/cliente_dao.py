from sqlalchemy.exc import IntegrityError

from app.models.cliente import Cliente
from app.models.cliente import Cliente as ClienteModel

class ClienteDAO:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar_cliente(self, cliente : Cliente):
        try:
            cliente_model = ClienteModel(
                nome=cliente.nome,
                email=cliente.email,
                telefone=cliente.telefone,
                cpf=cliente.cpf
            )
            self.db_session.add(cliente_model)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao criar cliente: {e}")
        
        self.db_session.refresh(cliente_model)

        return cliente_model

    def buscar_por_cpf(self, cpf_cliente) -> Cliente | None:
        
        return (self.db_session
                .query(ClienteModel)
                .filter_by(cpf=cpf_cliente)
                .first())

    def buscar_por_id(self, cliente_id) -> Cliente | None :
        
        return (self.db_session
                .query(ClienteModel)
                .filter_by(cliente_id=cliente_id)
                .first())

    def listar_todos(self) -> Cliente | None : 
        
        return (self.db_session
                .query(Cliente)
                .all())

    def atualizar_cliente(self, cliente_id: int, cliente) -> Cliente | None:
        cliente_busca = self.buscar_por_id(cliente_id)

        if cliente : 
            for field, value in cliente.model_dump().items():
                setattr(cliente_busca, field, value)

            self.db_session.commit()
            self.db_session.refresh(cliente_busca)
        
        return cliente_busca

    def deletar_cliente(self, cliente_id) -> None:
        cliente_busca = self.buscar_por_id(cliente_id)

        if not cliente_busca:
            raise ValueError("Cliente não encontrado")
        
        self.db_session.delete(cliente_busca)
        self.db_session.commit()
