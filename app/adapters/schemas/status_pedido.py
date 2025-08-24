from pydantic import BaseModel

class StatusPedidoResponseSchema(BaseModel):
    id: int
    descricao: str
