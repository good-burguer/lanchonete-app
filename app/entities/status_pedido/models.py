class StatusPedido:
    def __init__(self, descricao: str):
        self.descricao = descricao

    model_config = {
        "from_attributes": True
    }