from pydantic import BaseModel

from app.adapters.schemas.produto import ProdutoResponseSchema

class ProdutoResponse(BaseModel):
    status: str
    data: ProdutoResponseSchema

class ProdutoResponseList(BaseModel):
    status: str
    data: list[ProdutoResponseSchema]