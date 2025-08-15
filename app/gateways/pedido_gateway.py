from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.entities.pedido.entities import PedidoEntities, Pedido
from app.models.pedido import Pedido as PedidoORM
from app.adapters.enums.status_pedido import StatusPedidoEnum
from app.adapters.schemas.cliente import ClienteResponseSchema
from app.adapters.schemas.pedido import PedidoResponseSchema
from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema

class PedidoGateway(PedidoEntities):
    def __init__(self, db_session):
        self.db_session = db_session

    def criarPedido(self, pedido: Pedido) -> PedidoResponseSchema:
        try:
            self.db_session.add(pedido)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar o pedido: {e}")
        self.db_session.refresh(pedido)

        clienteEntity: ClienteResponseSchema = (ClienteResponseSchema(
                cliente_id=pedido.cliente_id,
                nome=pedido.cliente_rel.nome,
                email=pedido.cliente_rel.email,
                telefone=pedido.cliente_rel.telefone,
                cpf=pedido.cliente_rel.cpf
            ))
        statusOrderEntity: StatusPedidoResponseSchema = (StatusPedidoResponseSchema(
            id=pedido.status_rel.id,
            descricao=pedido.status_rel.descricao
        ))

        pedidoResponse: PedidoResponseSchema = (PedidoResponseSchema(
            pedido_id=pedido.pedido_id, 
            cliente_id=clienteEntity, 
            status=statusOrderEntity, 
            data_criacao=pedido.data_criacao, 
            data_alteracao=pedido.data_alteracao, 
            data_finalizacao=pedido.data_finalizacao
        ))
        
        return pedidoResponse

    def buscar_por_id(self, id: int) -> PedidoResponseSchema:
        db_pedido = self.db_session.query(Pedido).filter(Pedido.pedido_id == id).first()
        
        if not db_pedido:
            raise ValueError("Pedido não encontrado")

        clienteEntity: ClienteResponseSchema = (ClienteResponseSchema(
                cliente_id=db_pedido.cliente_id,
                nome=db_pedido.cliente_rel.nome,
                email=db_pedido.cliente_rel.email,
                telefone=db_pedido.cliente_rel.telefone,
                cpf=db_pedido.cliente_rel.cpf
            ))
        statusOrderEntity: StatusPedidoResponseSchema = (StatusPedidoResponseSchema(
            id=db_pedido.status_rel.id,
            descricao=db_pedido.status_rel.descricao
        ))

        pedidoResponse: PedidoResponseSchema = (PedidoResponseSchema(
            pedido_id=db_pedido.pedido_id, 
            cliente_id=clienteEntity, 
            status=statusOrderEntity, 
            data_criacao=db_pedido.data_criacao, 
            data_alteracao=db_pedido.data_alteracao, 
            data_finalizacao=db_pedido.data_finalizacao
        ))

        return pedidoResponse

    def listar_todos(self) -> list[PedidoResponseSchema]:
        pedidos_prontos = self.db_session.query(Pedido).filter(Pedido.status == 3).order_by(Pedido.data_criacao.asc()).all()
        pedidos_em_preparacao = self.db_session.query(Pedido).filter(Pedido.status == 2).order_by(Pedido.data_criacao.asc()).all()
        pedidos_recebidos = self.db_session.query(Pedido).filter(Pedido.status == 1).order_by(Pedido.data_criacao.asc()).all()
        db_pedidos = pedidos_prontos + pedidos_em_preparacao + pedidos_recebidos

        pedidos = []

        for pedido in db_pedidos:
            clienteEntity: ClienteResponseSchema = (ClienteResponseSchema(
                cliente_id=pedido.cliente_id,
                nome=pedido.cliente_rel.nome,
                email=pedido.cliente_rel.email,
                telefone=pedido.cliente_rel.telefone,
                cpf=pedido.cliente_rel.cpf
            ))
            statusOrderEntity: StatusPedidoResponseSchema = (StatusPedidoResponseSchema(
                id=pedido.status_rel.id,
                descricao=pedido.status_rel.descricao
            ))

            pedidoResponse: PedidoResponseSchema = (PedidoResponseSchema(
                pedido_id=pedido.pedido_id, 
                cliente_id=clienteEntity, 
                status=statusOrderEntity, 
                data_criacao=pedido.data_criacao, 
                data_alteracao=pedido.data_alteracao, 
                data_finalizacao=pedido.data_finalizacao
            ))
            pedidos.append(pedidoResponse)

        return pedidos

    def deletar(self, id: int) -> None:
        db_pedido = self.db_session.query(Pedido).filter(Pedido.pedido_id == id).first()
        
        if not db_pedido:
            raise ValueError("Pedido não encontrado")
        self.db_session.delete(db_pedido)
        self.db_session.commit()
        #self.db_session.flush()

    def atualizarPedido(self, pedido: Pedido) -> PedidoResponseSchema:
        db_pedido = self.db_session.query(PedidoORM).filter_by(pedido_id=pedido.pedido_id).first()

        if (db_pedido.status == int(StatusPedidoEnum.Finalizado.value)):
            raise Exception("Pedido já finalizado")
        
        if not db_pedido:
            raise ValueError("Pedido não encontrado")

        for field, value in pedido.model_dump().items():
            setattr(db_pedido, field, value)

        self.db_session.commit()
        self.db_session.refresh(db_pedido)

        clienteEntity: ClienteResponseSchema = (ClienteResponseSchema(
                cliente_id=db_pedido.cliente_id,
                nome=db_pedido.cliente_rel.nome,
                email=db_pedido.cliente_rel.email,
                telefone=db_pedido.cliente_rel.telefone,
                cpf=db_pedido.cliente_rel.cpf
            ))
        statusOrderEntity: StatusPedidoResponseSchema = (StatusPedidoResponseSchema(
            id=db_pedido.status_rel.id,
            descricao=db_pedido.status_rel.descricao
        ))

        pedidoResponse: PedidoResponseSchema = (PedidoResponseSchema(
            pedido_id=db_pedido.pedido_id, 
            cliente_id=clienteEntity, 
            status=statusOrderEntity, 
            data_criacao=db_pedido.data_criacao, 
            data_alteracao=db_pedido.data_alteracao, 
            data_finalizacao=db_pedido.data_finalizacao
        ))

        return pedidoResponse