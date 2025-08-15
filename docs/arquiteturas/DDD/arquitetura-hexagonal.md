# Arquitetura Hexagonal – Projeto Lanchonete

## Visão Geral

A arquitetura hexagonal (ou Ports and Adapters) organiza a aplicação separando regras de negócio de implementações técnicas. Essa abordagem promove isolamento, testabilidade e flexibilidade.

---

## Camadas e Responsabilidades

### 1. **Domínio (Domain)**
- **Local:** `app/domain/produto/`
- **Responsabilidade:** Regras de negócio e abstrações (interfaces/ports).
- **Exemplo:** `ProdutoRepositoryPort` define contratos para persistência de produtos.

### 2. **Use Cases (Application Layer)**
- **Local:** `app/use_cases/produto/`
- **Responsabilidade:** Coordena as regras de negócio e fluxo da aplicação.
- **Exemplos:**
  - `CriarProdutoUseCase`
  - `BuscarProdutoUseCase`
  - `ListarProdutosUseCase`

### 3. **Adaptadores de Entrada (Driven Adapters / Interfaces de Entrada)**
- **Local:** `app/api/`
- **Responsabilidade:** Controladores que recebem requisições HTTP (FastAPI).
- **Exemplo:** `produto.py` define as rotas da API REST.

### 4. **Adaptadores de Saída (Driven Adapters / Interfaces de Saída)**
- **Local:** `app/adapters/out/`
- **Responsabilidade:** Implementação concreta das interfaces de repositório.
- **Exemplo:** `produto_repository.py` implementa `ProdutoRepositoryPort`.

### 5. **Schemas (DTOs / Presenters)**
- **Local:** `app/core/schemas/`
- **Responsabilidade:** Entrada e saída de dados da API.
- **Exemplo:** `ProdutoCreate`, `ProdutoResponse`.

### 6. **Enums**
- **Local:** `app/core/enums/`
- **Responsabilidade:** Padronização de valores fixos.
- **Exemplo:** `CategoriaEnum`.

---

## Rotas Implementadas

- `POST /produtos/` → Criar Produto
- `GET /produtos/{produto_id}` → Buscar Produto por ID
- `GET /produtos/` → Listar Produtos
- `DELETE /produtos/{produto_id}` → Deletar Produto
- `PUT /produtos/{produto_id}` → Atualizar Produto
- `GET /produtos/categoria/{categoria}` → Listar Produtos por Categoria

---

## Diagrama de Fluxo de Informações

```plaintext
        [ HTTP Request ]
               │
               ▼
        [ app/api/produto.py ]
               │
               ▼
     [ Use Case: Criar/Buscar/Listar Produto ]
               │
               ▼
 [ app/domain/produto/ProdutoRepositoryPort ] <─┐
               │                                │
               ▼                                │
 [ app/adapters/out/produto_repository.py ] ────┘
               │
               ▼
         [ Banco de Dados ]
```

---

## Observações

- O uso do método `.executar()` foi padronizado nos use cases.
- Os repositórios são injetados nas factories definidas no controller (`get_criar_produto_use_case`, etc.).
- O Swagger exibe os nomes como "Listar Produtos" com base na docstring (`summary="..."`) passada na definição da rota.
