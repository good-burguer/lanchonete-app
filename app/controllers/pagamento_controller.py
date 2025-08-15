from fastapi import status, HTTPException
from app.use_cases.pagamento.pagamento_use_case import PagamentoUseCase

class PagamentoController:
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def criar_pagamento(self, cliente_data):
        
        try:
            return PagamentoUseCase(self.db_session).criar_pagamento(cliente_data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def listar_todos_pagamentos(self):
        
        try:
            return PagamentoUseCase(self.db_session).listar_todos_pagamentos()
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_pagamento_por_codigo(self, codigo_pagamento: int):
        
        try:
            return PagamentoUseCase(self.db_session).buscar_pagamento_por_codigo(codigo_pagamento)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar_pagamento(self, codigo: int, pagamento_request):
        
        try:
            return PagamentoUseCase(self.db_session).atualizar_pagamento(codigo=codigo, pagamento_request=pagamento_request)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def deletar_pagamento(self, codigo_pagamento: int):
        
        try:
            return PagamentoUseCase(self.db_session).deletar_pagamento(codigo_pagamento=codigo_pagamento)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    @staticmethod
    def atualizar_pagamento_webhook(self, codigo: int, pagamento_request):
        
        try:
            return PagamentoUseCase(self.db_session).atualizar_pagamento(codigo=codigo, pagamento_request=pagamento_request)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
