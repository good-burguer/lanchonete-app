from pydantic import BaseModel

class StatusPedidoCreateSchema(BaseModel):
    descricao: str

class StatusPedidoResponseSchema(StatusPedidoCreateSchema):
    id: int
    descricao: str

class StatusPedidoUpdateSchema(BaseModel):
    descricao: str
