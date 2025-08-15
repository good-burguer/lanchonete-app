from decimal import Decimal

class Produto:
    def __init__(self, nome: str, descricao: str, preco: Decimal, categoria: str):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    model_config = {
        "from_attributes": True
    }