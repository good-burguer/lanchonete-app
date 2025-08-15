from pydantic import BaseModel

class CategoriaProdutoResponseSchema(BaseModel):
    id: int
    nome: str