from pydantic import BaseModel, ConfigDict

from typing import Optional

class PedidoCreateSchema(BaseModel):
    cliente_id: Optional[int]
    produtos: list

class PedidoAtualizaSchema(BaseModel):
    status: int
    
    model_config = ConfigDict(arbitrary_types_allowed=True)