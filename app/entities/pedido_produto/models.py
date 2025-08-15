class PedidoProduto():
    id: int
    pedido_id: int
    produto_id: int

    def __init__(self, pedido_id: int, produto_id: int):
        self.pedido_id = pedido_id
        self.produto_id = produto_id

    model_config = {
        "from_attributes": True
    }