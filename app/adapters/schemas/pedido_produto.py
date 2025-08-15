from pydantic import BaseModel

class PedidoProdutoCreateSchema(BaseModel):
    pedido_id: int
    produto_id: int

class PedidoProdutoResponseSchema(PedidoProdutoCreateSchema):
    pedido_id: int
    produto_id: int

    class Config:
        allow_population_by_field_name = True
    
class ProdutoPedidoResponseSchema(BaseModel):
    produto_id: int

    class Config:
        allow_population_by_field_name = True