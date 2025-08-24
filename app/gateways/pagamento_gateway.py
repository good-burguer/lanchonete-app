from sqlalchemy.exc import IntegrityError

from app.entities.pagamento.entities import PagamentoEntities
from app.models.pagamento import Pagamento
from typing import List, Optional
from app.dao.pagamento_dao import PagamentoDAO

class PagamentoGateway(PagamentoEntities):
    def __init__(self, db_session):
        self.dao = PagamentoDAO(db_session)

    def criar_pagamento(self, pagamento: Pagamento) -> Pagamento:
        
        return self.dao.criar_pagamento(pagamento)
    
    def buscar_pagamento(self, codigo_pagamento: str) -> Optional[Pagamento]: 
        
        return self.dao.buscar_pagamento_por_codigo(codigo_pagamento = codigo_pagamento)
    
    def listar_todos_pagamentos(self)-> List[Pagamento]:
        
        return self.dao.listar_todos_pagamentos()
    
    def atualizar_pagamento(self, pagamentoDTO) -> Pagamento: 
        
        return self.dao.atualizar_pagamento(pagamentoDTO)
    
    def deletar_pagamento(self, codigo_pagamento: str): 
        
        return self.dao.deletar_pagamento(codigo_pagamento)