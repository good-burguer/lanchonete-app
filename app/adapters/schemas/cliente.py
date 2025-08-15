from pydantic import BaseModel, EmailStr, constr, ConfigDict, field_validator
from typing import Optional

class ClienteCreateSchema(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    telefone: Optional[constr(min_length=10, max_length=11, pattern=r'^\d{10,11}$')] = None  # Ex: 11912345678
    cpf: constr(min_length=11, max_length=11, pattern=r'^\d{11}$')

    @field_validator("nome")
    def nome_nao_pode_conter_tags(cls, v):
        if "<" in v or ">" in v:
            raise ValueError("Nome não pode conter caracteres inválidos como '<' ou '>'.")
        return v

class ClienteResponseSchema(BaseModel):
    cliente_id: int
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    cpf: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ClienteUpdateSchema(BaseModel):
    nome: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None
    telefone: Optional[constr(min_length=10, max_length=15)] = None
    cpf: Optional[constr(min_length=11, max_length=11, pattern=r'^\d{11}$')] = None

    @field_validator("nome")
    def nome_nao_pode_conter_tags(cls, v):
        if v and ("<" in v or ">" in v):
            raise ValueError("Nome não pode conter caracteres inválidos como '<' ou '>'.")
        return v