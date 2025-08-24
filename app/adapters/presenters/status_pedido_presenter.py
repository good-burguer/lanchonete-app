from pydantic import BaseModel
from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema

class StatusPedidoResponse(BaseModel): 
    status: str
    data: StatusPedidoResponseSchema

class StatusPedidoResponseList(BaseModel):
    status: str
    data: list[StatusPedidoResponseSchema]