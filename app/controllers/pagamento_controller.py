from fastapi import status, HTTPException, Response

from app.use_cases.pagamento_use_case import PagamentoUseCase
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema
from app.adapters.presenters.pagamento_presenter import PagamentoResponse, PagamentoResponseList

class PagamentoController:
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def criar_pagamento(self, cliente_data: PagamentoCreateSchema):
        try:
            result = PagamentoUseCase(self.db_session).criar_pagamento(cliente_data)

            return PagamentoResponse(status='success', data = result)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    def buscar_pagamento(self, codigo_pagamento: int):
        try:
            result = PagamentoUseCase(self.db_session).buscar_pagamento(codigo_pagamento)

            return PagamentoResponse(status='success', data = result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            
    def listar_todos_pagamentos(self):
        try:
            result = PagamentoUseCase(self.db_session).listar_todos_pagamentos()

            return PagamentoResponseList(status='success', data = result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar_pagamento(self, codigo: int, pagamento_request):
        try:
            result = PagamentoUseCase(self.db_session).atualizar_pagamento(codigo=codigo, pagamento_request=pagamento_request)

            return PagamentoResponse(status='success', data = result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def deletar_pagamento(self, codigo_pagamento: int):
        try:
            PagamentoUseCase(self.db_session).deletar_pagamento(codigo_pagamento=codigo_pagamento)
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
