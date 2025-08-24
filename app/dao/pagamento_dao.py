from sqlalchemy.exc import IntegrityError
import uuid

from app.models.pagamento import Pagamento
from app.models.pagamento import Pagamento as PagamentoModel
from app.adapters.enums.status_pagamento import PagamentoStatusEnum

class PagamentoDAO:
    
    def __init__(self, db_session):
        
        self.db_session = db_session

    def criar_pagamento(self, pagamento: Pagamento) -> Pagamento | None:
        pagamentoModel = PagamentoModel(
            pedido=pagamento.pedido_id, 
            codigo_pagamento = str(uuid.uuid4()),
            status = PagamentoStatusEnum.EmAndamento
        )
        
        try:
            self.db_session.add(pagamentoModel)
            self.db_session.commit()           
        except IntegrityError as e:            
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar pagamento: {e}")
        self.db_session.refresh(pagamento)

        return pagamento
    
    def listar_todos_pagamentos(self) -> Pagamento | None :

        return (self.db_session
                    .query(Pagamento)
                    .all())
    
    def buscar_pagamento_por_codigo(self, codigo_pagamento: str) -> Pagamento | None: 
        
        return (self.db_session
                .query(Pagamento)
                .filter(Pagamento.codigo_pagamento == codigo_pagamento)
                .first())
    
    def atualizar_pagamento(self, pagamentoDTO) -> Pagamento | None:
        pagamento_entity = self.buscar_pagamento_por_codigo(codigo_pagamento = pagamentoDTO.codigo_pagamento)

        if pagamento_entity :
            pagamento_entity.status = pagamentoDTO.status

            self.db_session.commit()
            self.db_session.refresh(pagamento_entity)
        
        return pagamento_entity
    
    def deletar_pagamento(self, codigo_pagamento: str) -> Pagamento | None: 
        try :
            pagamento_deletar = self.buscar_pagamento_por_codigo(codigo_pagamento = codigo_pagamento.codigo_pagamento)

            if not pagamento_deletar:
                raise ValueError("Pagamento não encontrado")
            
            self.db_session.delete(pagamento_deletar)
            self.db_session.commit()
        except IntegrityError as e:            
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao deletar pagamento: {e}")