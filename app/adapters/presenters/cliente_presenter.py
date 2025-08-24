from pydantic import BaseModel
from app.adapters.schemas.cliente import ClienteResponseSchema

class ClienteResponse(BaseModel):
    status: str
    data: ClienteResponseSchema

class ClienteResponseList(BaseModel):
    status: str
    data: list[ClienteResponseSchema]