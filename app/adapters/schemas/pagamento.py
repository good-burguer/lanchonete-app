from pydantic import BaseModel

class PagamentoCreateSchema(BaseModel):
    pedido_id: int
    
class PagamentoResponseSchema(BaseModel):
    pedido_id: int
    codigo_pagamento:str
    status: str

class PagamentoAtualizaSchema(BaseModel):
    status: str

class PagamentoAtualizaWebhookSchema(BaseModel):
    codigo_pagamento: str
    status: str