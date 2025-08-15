# Arquitetura Clean Architecture – Projeto Lanchonete

## Visão Geral

A arquitetura Clean Architecture (Arquitetura Limpa) organiza a aplicação separando regras de negócio de implementações técnicas. Essa abordagem promove isolamento, testabilidade e flexibilidade.

---

## Camadas e Responsabilidades

### 1. **Adaptadores (adapters)**
- **Local:** `app/adapters/`
- **Responsabilidade:** Adaptar dados para entrada e saída de dados da API.

### 2. **API (api)**
- **Local:** `app/api/`
- **Responsabilidade:** Recebe requisições HTTP (FastAPI).
- **Exemplo:** `produto.py` define as rotas da API REST.

### 3. **Controller (controllers)**
- **Local:** `app/controllers/`
- **Responsabilidade:** Intermediário entre as requisições externas e os casos de uso da aplicação.
- **Exemplo:** `produto_controller.py` faz o intermediário entre a requisição e o caso de uso.

### 4. **gateways (Gateways)**
- **Local:** `app/gateways/`
- **Responsabilidade:** Acesso e comunicação com o banco de dados.
- **Exemplo:** `pagamento_gateway.py` Acesso ao banco de dados.

### 5. **Use Cases (Application Layer)**
- **Local:** `app/use_cases/pagamento/`
- **Responsabilidade:** Coordena as regras de negócio e fluxo da aplicação.
- **Exemplos:**
  - `PagamentoUseCase`

### 6. **Entidade (entities)**
- **Local:** `app/entities/`
- **Responsabilidade:** Regras de negócio e abstrações (interfaces/entidades).
- **Exemplo:** `pagamento/entities` define interface para persistência de pagamento.

### 7. **Enums**
- **Local:** `app/adapters/enums/`
- **Responsabilidade:** Padronização de valores fixos.
- **Exemplo:** `CategoriaEnum`.

---

## Diagrama de Fluxo de Informações

```plaintext
        [ HTTP Request ]
               │
               ▼
        [ API: app/api/produto.py ]
               │
               ▼
        [ Controller: app/controllers/produto_controller.py ] <─> [ app/gateways/produto_gateway.py ] <─> [ Banco de Dados ]
               │
               ▼
        [ Use Case: app/use_cases/produto_use_case/produto_use_case.py ]
               │
               ▼
        [ Entidade: app/entities/produto/entities.py ] 
               
         
```

---

## Observações

- O Swagger exibe os nomes como "Listar Produtos" com base na docstring (`summary="..."`) passada na definição da rota.
