import bleach
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, field_serializer, field_validator, ConfigDict, Field
from typing import Optional

from app.adapters.enums.categoria_produto import CategoriaProdutoEnum

class ProdutoCreateSchema(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = None
    categoria: int

    @field_validator("descricao", mode="before")
    @classmethod
    def limpar_html(cls, valor: Optional[str]) -> Optional[str]:
        return bleach.clean(valor) if valor else valor

    preco: Decimal = Field(..., gt=0, description="Preço deve ser maior que zero")

    @field_serializer("preco", mode="plain")
    def arredondar_preco(self, preco: Decimal) -> str:
        return format(preco.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f")
    
    model_config = ConfigDict(extra="forbid", from_attributes=True)

class ProdutoUpdateSchema(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = None
    categoria: Optional[CategoriaProdutoEnum] = None
    preco: Optional[Decimal] = Field(None, gt=0, description="Preço deve ser maior que zero")

    @field_validator("descricao", mode="before")
    @classmethod
    def limpar_html(cls, valor: Optional[str]) -> Optional[str]:
        return bleach.clean(valor) if valor else valor

    @field_serializer("preco", mode="plain")
    def arredondar_preco(self, preco: Optional[Decimal]) -> Optional[str]:
        if preco is not None:
            return format(preco.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f")
        return None

    model_config = ConfigDict(extra="forbid", from_attributes=True)