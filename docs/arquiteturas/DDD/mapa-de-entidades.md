# 🗺️ Mapa de Entidades — Sistema de Autoatendimento da Lanchonete

## 📋 Visão Geral

Este documento descreve as entidades principais do sistema, suas responsabilidades e relacionamentos.  
O objetivo é guiar o desenvolvimento do projeto, facilitar a colaboração da equipe e manter a arquitetura do domínio bem definida.

---

## 📦 1. Cliente

Cadastro opcional para identificação do cliente no sistema.

| Atributo     | Tipo             | Descrição                              |
|--------------|------------------|----------------------------------------|
| id           | Integer (PK)     | Identificador único do cliente         |
| nome         | String           | Nome completo do cliente               |
| email        | String           | Email do cliente (único)               |
| telefone     | String           | Telefone para contato                  |
| criado_em    | DateTime         | Data de criação do cadastro            |

**Relacionamentos:**
- Um cliente pode ter vários pedidos.

**Validações e Regras de Negócio:**
- Nome: sanitização de input para evitar injeção de código (XSS).
- Email: deve ser único e ter formato válido.
- Telefone: deve seguir formato numérico válido.
- CPF: deve conter exatamente 11 dígitos numéricos.

---

## 📦 2. Produto

Itens disponíveis no cardápio da lanchonete.

| Atributo     | Tipo             | Descrição                              |
|--------------|------------------|----------------------------------------|
| id           | Integer (PK)     | Identificador único do produto         |
| nome         | String           | Nome do produto                        |
| descricao    | String           | Descrição do produto                   |
| preco        | Integer          | Preço do produto (centavos ou reais)   |

**Relacionamentos:**
- Um produto pode estar em vários itens de pedido.

**Validações e Regras de Negócio:**
- Nome e descrição: sanitização de input para evitar injeção de código.
- Preço: deve ser um valor positivo maior que zero.
- Categoria: deve pertencer ao Enum de categorias predefinidas.

---

## 📦 3. Pedido

Registro de um pedido feito pelo cliente.

| Atributo     | Tipo             | Descrição                              |
|--------------|------------------|----------------------------------------|
| id           | Integer (PK)     | Identificador único do pedido          |
| cliente_id   | Integer (FK)     | Relacionamento com Cliente (opcional)  |
| status       | Enum/String      | Status do pedido ("Em preparo", "Finalizado", etc.) |
| criado_em    | DateTime         | Data de criação do pedido              |

**Relacionamentos:**
- Um pedido pertence a um cliente (opcional).
- Um pedido possui múltiplos itens.

---

## 📦 4. Item do Pedido

Relação entre pedido e produtos, permitindo múltiplos produtos por pedido.

| Atributo         | Tipo             | Descrição                              |
|------------------|------------------|----------------------------------------|
| id               | Integer (PK)     | Identificador único do item            |
| pedido_id        | Integer (FK)     | Referência ao pedido                   |
| produto_id       | Integer (FK)     | Referência ao produto                  |
| quantidade       | Integer          | Quantidade do produto no pedido        |
| preco_unitario   | Integer          | Preço unitário do produto no momento do pedido |

**Relacionamentos:**
- Cada item pertence a um pedido.
- Cada item referencia um produto.

---

## 📦 5. Pagamento (Opcional para escopo inicial)

Registro do pagamento do pedido.

| Atributo          | Tipo             | Descrição                              |
|-------------------|------------------|----------------------------------------|
| id                | Integer (PK)     | Identificador único do pagamento       |
| pedido_id         | Integer (FK)     | Pedido relacionado                     |
| valor_total       | Integer          | Valor total do pagamento               |
| forma_pagamento   | String           | Dinheiro, Cartão, etc.                 |
| status_pagamento  | Enum/String      | Pendente, Confirmado, Cancelado        |
| criado_em         | DateTime         | Data de criação do pagamento           |

**Relacionamentos:**
- Um pagamento está associado a um pedido.

---

## 🔗 Relacionamentos Resumidos

## 🛡️ Notas Técnicas e Boas Práticas Adotadas

- Utilização de Pydantic para validação e sanitização de dados.
- Uso de Enum para categorias de Produto, assegurando valores válidos.
- Tratamento de erros com respostas HTTP padronizadas (400, 404, 409, etc.).
- Proteção contra XSS nas entradas de texto.
- Testes automatizados (pytest) com cobertura de cenários positivos e negativos.
- Adoção de Clean Architecture / Hexagonal Architecture no design do sistema.