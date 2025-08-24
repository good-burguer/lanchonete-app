from pydantic import BaseModel, EmailStr, constr, ConfigDict

import datetime
from typing import Optional
from typing import List

from app.adapters.presenters.cliente_presenter import *
from app.adapters.schemas.produto import *
from app.adapters.schemas.cliente import ClienteResponseSchema
from app.adapters.schemas.produto import ProdutoResponseSchema
from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema

class PedidoResponseSchema(BaseModel):
    pedido_id: int
    cliente_id: ClienteResponseSchema
    status: StatusPedidoResponseSchema
    data_criacao: datetime.time
    data_alteracao: Optional[datetime.time]
    data_finalizacao: Optional[datetime.time]
    
    class Config:
        allow_population_by_field_name = True
    
class PedidoProdutosResponseSchema(BaseModel):
    pedido_id: int
    cliente_id: ClienteResponseSchema
    status: StatusPedidoResponseSchema
    data_criacao: datetime.time
    data_alteracao: Optional[datetime.time]
    data_finalizacao: Optional[datetime.time]
    produtos: Optional[List[ProdutoResponseSchema]]
    
    class Config:
        allow_population_by_field_name = True

