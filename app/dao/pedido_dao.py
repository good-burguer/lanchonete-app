from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.entities.pedido.entities import Pedido
from app.adapters.dto.pedido_dto import PedidoAtualizaSchema
from app.adapters.enums.status_pedido import StatusPedidoEnum
from app.adapters.utils.debug import var_dump_die

class PedidoDAO:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def criar_pedido(self, pedido: Pedido) -> Pedido:
        pedidoEntity: Pedido = Pedido(cliente_id=pedido.cliente_id, status=1)
        pedidoEntity.status = str(StatusPedidoEnum.Recebido.value)
        pedidoEntity.data_criacao = datetime.now()
        
        try:
            self.db_session.add(pedidoEntity)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar o pedido: {e}")
        
        self.db_session.refresh(pedidoEntity)
        
        return pedidoEntity

    def busca_por_status(self, status) : 

        return (self.db_session
                .query(Pedido)
                .filter(Pedido.status == status)
                .order_by(Pedido.data_criacao.asc())
                .all())
    
    def buscar_por_id(self, id: int) :

        return (self.db_session
                .query(Pedido)
                .filter(Pedido.pedido_id == id)
                .first()) 

    def atualizar_pedido(self, pedido_id: int,  pedidoRequest: PedidoAtualizaSchema) :
        pedidoEntity = self.buscar_por_id(pedido_id)
        
        if pedidoEntity :
            if (pedidoEntity.status == int(StatusPedidoEnum.Finalizado.value)):
                raise Exception("Pedido já finalizado")
            
            pedidoEntity.status = pedidoRequest.status
            pedidoEntity.data_alteracao = datetime.now()
            pedidoEntity.cliente_id = pedidoEntity.cliente_id

            if int(pedidoRequest.status) == int(StatusPedidoEnum.Finalizado):
                pedidoEntity.data_finalizacao = datetime.now()

            for field, value in pedidoRequest.model_dump().items():
                setattr(pedidoEntity, field, value)

            self.db_session.commit()
            self.db_session.refresh(pedidoEntity)
        
        return pedidoEntity

    def deletar_pedido(self, pedido_id: int) -> None :
        pedidoEntity = self.buscar_por_id(pedido_id)
        
        if not pedidoEntity:
            raise ValueError("Pedido não encontrado")
        
        self.db_session.delete(pedidoEntity)
        self.db_session.commit()