
# Guia de Estudos Personalizado — Projeto da Lanchonete

## Objetivo do Guia
Te dar uma referência rápida e prática, conectando teoria + exemplos dos repositórios, para usar como base no desenvolvimento do seu projeto.

## 1. Estrutura Hexagonal

| Conceito | Aplicação |
|----------|-----------|
| Centro do Hexágono (Domínio) | app/core/models/ + app/core/use_cases/ |
| Portas de Entrada | FastAPI: app/api/endpoints/ |
| Portas de Saída | Banco: app/adapters/db/ <br> Serviços externos: app/adapters/external_services/ |
| Adaptadores de Teste | Testes mocks em tests/bdd/steps/ ou tests/unit/ |

**Exemplo:**  
Veja no ts-hexagon-architecture como core/entities contém as entidades principais e adapters cuidam de integração.

## 2. Modularização

| Módulo | Diretório |
|--------|-----------|
| Pedidos | app/core/models/pedido.py + app/api/endpoints/pedido.py |
| Produtos | app/core/models/produto.py + app/api/endpoints/produto.py |
| Pagamentos | app/core/models/pagamento.py + app/adapters/external_services/gateway_pagamento.py |

**Dica:**  
No repositório FIAP_POS, repare como cada feature tem sua própria pasta.

## 3. Testabilidade + BDD

| Tipo de Teste | Local |
|---------------|--------|
| Unitários | tests/unit/ |
| Integração | tests/integration/ |
| BDD | tests/bdd/features/ + tests/bdd/steps/ |

**Exemplo de Feature BDD:**

Funcionalidade: Finalização de Pedido
Cenário: Cliente finaliza pedido com sucesso
Dado que o cliente selecionou produtos no cardápio
Quando ele confirma o pedido e efetua o pagamento
Então o sistema registra o pedido como 'Em preparação'

## 4. Documentação Viva

FastAPI gera Swagger automaticamente a partir de app/api/schemas/.

No main.py, inclua:

from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Autoatendimento da Lanchonete",
    description="Documentação automática com Swagger e Redoc",
    version="1.0.0",
)

Acesse via: http://localhost:8000/docs

## 5. Escalabilidade e Desempenho

| Ação | Implementação |
|------|---------------|
| Health Check | Endpoint em app/api/endpoints/health.py |
| Cache (opcional) | Use Redis, adaptador em app/adapters/external_services/cache.py |
| Containerização | Dockerfile + docker-compose.yml |

## Dicas Extras

- Sempre que criar um novo módulo, lembre-se: Models → Use Cases → Endpoints → Testes
- No requirements.txt, inclua:
  fastapi
  uvicorn
  pytest
  pytest-bdd
  sqlalchemy
  pydantic
- Use .env para segredos sensíveis.

## Conclusão

Este guia vai te acompanhar como referência na hora do desenvolvimento.
