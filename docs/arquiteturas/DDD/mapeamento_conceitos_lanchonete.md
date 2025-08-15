
# Mapeamento de Aplicação dos Conceitos — Tech Challenge Lanchonete

## 1. Fluxo do Cliente (Usuário Final)

1️⃣ Cliente acessa o sistema de autoatendimento da lanchonete (API FastAPI)

**Conceito aplicado:**
- Adaptador de entrada: app/api/endpoints/pedido.py
- Documentação Viva: FastAPI Swagger automático

## 2. Consulta ao Cardápio

2️⃣ Sistema busca itens disponíveis no banco de dados

**Conceito aplicado:**
- Adaptador de saída: app/adapters/db/repositories.py
- Cache (opcional para performance): Redis em app/adapters/external_services/cache.py
- Escalabilidade: Otimização da consulta com cache

## 3. Montagem do Pedido

3️⃣ Cliente seleciona produtos e cria o pedido

**Conceito aplicado:**
- Domínio do Pedido: app/core/models/pedido.py
- Caso de uso: app/core/use_cases/criar_pedido.py
- Testabilidade: Teste unitário + BDD no fluxo tests/bdd/features/criar_pedido.feature

## 4. Pagamento

4️⃣ Cliente finaliza o pedido e efetua pagamento

**Conceito aplicado:**
- Adaptador de saída externo: app/adapters/external_services/gateway_pagamento.py
- Serviço de domínio: Validação de pagamentos em app/core/services/calculo_desconto.py
- Teste de integração: tests/integration/test_api.py

## 5. Registro do Pedido

5️⃣ Sistema registra o pedido como "Em preparação"

**Conceito aplicado:**
- Persistência: Banco de dados via app/adapters/db/repositories.py
- Eventual integração futura: Envio para sistema de cozinha
- Testes de aceitação: tests/bdd/features/finalizar_pedido.feature

## 6. Monitoramento & Saúde da Aplicação

6️⃣ Monitoramento da saúde do sistema e logs

**Conceito aplicado:**
- Health check: Endpoint em app/api/endpoints/health.py
- Observabilidade: Monitoramento com Prometheus + Grafana (opcional)

## Conexão com Conceitos de Arquitetura

| Ponto de Fluxo | Conceito de Arquitetura |
|----------------|--------------------------|
| API de atendimento | Porta de entrada (Adaptador HTTP) |
| Banco de dados | Adaptador de saída |
| Business logic (Pedido, Pagamento) | Centro do hexágono |
| Serviços externos | Adaptadores externos |
| Testes BDD e unitários | Testabilidade + Modularização |
| Documentação Swagger | Documentação Viva |
| Cache / Performance | Escalabilidade e Performance |
| Docker e .env | Escalabilidade futura e portabilidade |

## Conclusão

Você agora tem um roteiro claro de como cada conceito teórico se encaixa perfeitamente no projeto da lanchonete. Não apenas para este desafio, mas para qualquer sistema que você venha a desenhar no futuro.
