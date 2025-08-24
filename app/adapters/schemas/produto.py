from decimal import Decimal
from pydantic import BaseModel, field_serializer, ConfigDict
from typing import Optional

from app.adapters.schemas.categoria_produto import CategoriaProdutoResponseSchema

class ProdutoResponseSchema(BaseModel):
    produto_id: int
    nome: str
    descricao: Optional[str] = None
    preco: Decimal
    categoria: CategoriaProdutoResponseSchema

    @field_serializer("preco", mode="plain")
    def formatar_preco(self, preco: Decimal) -> str:
        return format(preco, ".2f")
    
    model_config = ConfigDict(from_attributes=True)