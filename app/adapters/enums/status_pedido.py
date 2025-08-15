from enum import Enum

class StatusPedidoEnum(str, Enum):
    Recebido = 1
    Iniciado = 2
    Pronto = 3
    Finalizado = 4
