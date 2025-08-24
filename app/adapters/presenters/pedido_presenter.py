from pydantic import BaseModel

from app.adapters.schemas.pedido import PedidoProdutosResponseSchema, PedidoResponseSchema

class PedidoResponse(BaseModel):
    status: str
    data: PedidoProdutosResponseSchema

class PedidoResponseList(BaseModel):
    status: str
    data: list[PedidoResponseSchema]