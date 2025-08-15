from fastapi import status, HTTPException
from app.use_cases.cliente.cliente_use_case import ClienteUseCase

class ClienteController:
    
    def criar_cliente(cliente_data, gateway):
        """ cadastrar cliente para realizar o pedido """
        
        try:
            return ClienteUseCase(gateway).criar_cliente(cliente_data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def buscar_cliente_por_cpf(cpf: str, gateway):
        """ buscar dados do cliente pelo cpf """
        
        try:
            return ClienteUseCase(gateway).buscar_cliente_por_cpf(cpf)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def buscar_cliente(cliente_id: int, gateway):
        """ buscar dados do cliente pelo id """
        
        try:
            return ClienteUseCase(gateway).buscar_cliente_por_id(cliente_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def listar_clientes(gateway):
        """ listar todos clientes cadastrados """
        
        try:
            return ClienteUseCase(gateway).listar_clientes()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def atualizar_cliente(cliente_id: int, cliente_data, gateway):
        """ atualizar dados do cliente pelo id """
        
        try:
            return ClienteUseCase(gateway).atualizar_cliente(cliente_id=cliente_id, clienteRequest=cliente_data)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    def deletar_cliente(cliente_id: int, gateway):
        """ excluir cliente """
        
        try:
            return ClienteUseCase(gateway).deletar_cliente(cliente_id=cliente_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
