from pydantic import EmailStr

class Cliente():

    def __init__(self, nome: str, email: EmailStr, telefone: str, cpf: str):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cpf = cpf

    model_config = {
        "from_attributes": True
    }