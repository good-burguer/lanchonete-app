from sqlalchemy.exc import IntegrityError

from app.entities.pagamento.entities import PagamentoEntities
from app.models.pagamento import Pagamento
from typing import List, Optional
from app.adapters.schemas.pagamento import PagamentoResponseSchema

class PagamentoGateway(PagamentoEntities):
    def __init__(self, db_session):
        
        self.db_session = db_session

    def criar_pagamento(self, pagamento: Pagamento) -> Pagamento:
        self.db_session.add(pagamento)
        
        try:
            self.db_session.commit()           
        except IntegrityError as e:            
            self.db_session.rollback()
            
            raise Exception(f"Erro de integridade ao salvar pagamento: {e}")
        self.db_session.refresh(pagamento)

        return pagamento
    
    def listar_todos_pagamentos(self)-> List[Pagamento]:
        
        return self.db_session.query(Pagamento).all()
    
    def buscar_pagamento_por_codigo(self, codigo_pagamento: str) -> Optional[Pagamento]: 
        consulta_pagamento = self.db_session.query(Pagamento).filter(Pagamento.codigo_pagamento == codigo_pagamento).first()

        if not consulta_pagamento:
            raise ValueError("Pagamento não encontrado")
        
        return consulta_pagamento
    
    def atualizar_pagamento(self, codigo: str, pagamento: Pagamento) -> Pagamento: 
        pagamento_entity = self.db_session.query(Pagamento).filter(Pagamento.codigo_pagamento == codigo).first()
        
        if not pagamento_entity:
            raise ValueError("Pagamento não encontrado")
        
        pagamento_entity.status = pagamento.status
        
        self.db_session.commit()
        self.db_session.refresh(pagamento_entity)
        
        response: PagamentoResponseSchema = (PagamentoResponseSchema(
                pedido_id = pagamento_entity.pedido, 
                codigo_pagamento = pagamento_entity.codigo_pagamento, 
                status = pagamento_entity.status
            ))
        
        return response
    
    def deletar_pagamento(self, codigo_pagamento: str): 
        pagamento_deletar = self.db_session.query(Pagamento).filter(Pagamento.codigo_pagamento == codigo_pagamento).first()

        if not pagamento_deletar:
            raise ValueError("Pagamento não encontrado")
        
        self.db_session.delete(pagamento_deletar)
        self.db_session.commit()