# 🍔 Sistema de Autoatendimento - Lanchonete

Bem-vindo ao repositório oficial do projeto de autoatendimento para lanchonete!

Este projeto faz parte do Tech Challenge da pós-graduação em Arquitetura de Sistemas (FIAP) e aplica os conceitos de arquitetura hexagonal, modularização, testabilidade com BDD e documentação viva com FastAPI.

---

## ⚙️ Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (precisa estar em execução no Mac)
- [Minikube](https://minikube.sigs.k8s.io/docs/) (recomendado para cluster local)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Git](https://git-scm.com/)
- [k6](https://k6.io/) (opcional, para testes de carga: `brew install k6` no Mac)

## Pré-requisitos para usuários Windows

Este projeto utiliza scripts Bash (`setup.sh`) e comandos Unix.  
Se você está usando Windows, é necessário rodar o script em um ambiente compatível, como:

- **WSL (Windows Subsystem for Linux)** – Recomendado para Windows 10/11.
- **Git Bash** – Disponível ao instalar o [Git for Windows](https://gitforwindows.org/).
- **Terminal do Minikube** – Se estiver usando Minikube no Windows.

> **Atenção:** O script não funcionará no prompt de comando (cmd) ou PowerShell puro do Windows.

Siga as instruções do ambiente escolhido antes de executar o `setup.sh`.

---

## 📂 Estrutura do Projeto

```
project_root/
├── .docker/           # Configuração dos containers
├── app/               # Código principal da aplicação
├── k8s/               # Manifestos Kubernetes (Deployment, Service, HPA, ConfigMap, Secret, test.js, check-minikube.sh)
├── tests/             # Testes unitários, integração e BDD
├── docs/              # Documentação técnica do projeto
├── setup.sh           # Script automatizado para setup local com Kubernetes
└── README.md          # Este arquivo
```

---

## 🧭 Fluxo do Projeto

1. Cliente acessa a API FastAPI de autoatendimento
2. Consulta de cardápio com possibilidade de cache
3. Montagem do pedido e escolha de produtos
4. Realização do pagamento
5. Registro do pedido e atualização de status
6. Monitoramento e health-check da aplicação

---

## 📐 Desenho da Arquitetura

- **Kubernetes (Minikube)**: Orquestração dos containers (testado localmente com Minikube, mas compatível com outros clusters)
- **HPA**: Escalabilidade automática dos pods conforme demanda
- **ConfigMap/Secret**: Boas práticas de segurança para variáveis sensíveis
- **Deployment/Service**: Exposição e gerenciamento dos pods
- **Banco de Dados**: PostgreSQL rodando em container separado

> ---

## 📚 Documentação de Arquitetura

A documentação detalhada da arquitetura Clean Architecture do projeto está disponível em:

- [`docs/arquiteturas/Clean-Architecture/clean-architecture.md`](docs/arquiteturas/Clean-Architecture/clean-architecture.md)

### Diagrama Clean Architecture

![Clean Architecture](docs/arquiteturas/Clean-Architecture/Clean-Architecture.png)

---

## 🔗 APIs e Documentação

- **Swagger/OpenAPI:**  
  Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

- **Collection Postman:**  
  [Download da Collection](docs/collection/lanchonete.postman_collection.json)  
  *(Adicione o arquivo JSON da collection do Postman na pasta docs/collection)*

---

## ▶️ Guia Completo de Execução

### 1. Clone o repositório

```bash
git clone https://github.com/danilocasabona/sistema-autoatendimento-lanchonete
cd sistema-autoatendimento-lanchonete
```

### 2. Instale e inicie o Minikube (se necessário)

O script `setup.sh` já verifica e instala automaticamente o Minikube (e o Homebrew no macOS, se necessário).

```bash
# No macOS, o script instala o Homebrew e o Minikube se necessário.
# No Linux, instala o Minikube automaticamente.
```

### 3. (Opcional) Use imagens locais no Minikube

Se quiser buildar as imagens localmente (sem Docker Hub), execute:

```bash
eval $(minikube docker-env)
docker build -t dcasabona/lanchonete-app:latest -f .docker/bin/webserver/Dockerfile .
docker build -t dcasabona/custom-postgres:latest -f .docker/bin/postgresql/Dockerfile .
```

### 4. Execute o script de setup Kubernetes

```bash
chmod +x setup.sh
./setup.sh
```

O script irá:
- Instalar e iniciar o Minikube (se necessário)
- Aplicar todos os manifestos Kubernetes (pasta `k8s/`)
- Esperar os pods ficarem prontos
- Fazer port-forward para http://localhost:8000
- Testar automaticamente o endpoint principal e o Swagger

### 5. Teste de carga com k6

Já existe um arquivo de teste em `k8s/test.js`. Para rodar um teste de carga real e acionar o autoscaling, utilize o comando abaixo (por exemplo, com 20 usuários virtuais por 2 minutos):

```bash
k6 run --vus 20 --duration 2m k8s/test.js
```

Acompanhe o autoscaling:

```bash
kubectl get hpa -w
kubectl get pods -w
```

### 6. Acesse a documentação da API

Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para ver o Swagger.

> Para interromper o port-forward, use o comando exibido ao final do script (`kill <PID>`).

---

## 🏁 Como mostrar que está rodando no Minikube

Para demonstrar que o ambiente está rodando no Minikube, execute:

```bash
chmod +x k8s/check-minikube.sh
./k8s/check-minikube.sh
```

Esse script mostra:
- Status do Minikube
- Pods ativos no cluster
- Contexto atual do kubectl
- IP do Minikube

---

## 🗂️ Ordem de Execução das APIs

1. **Consultar cardápio:** `GET /produtos`
2. **Cadastro de clientes:** `POST /clientes`
3. **Criar pedido:** `POST /pedidos`
4. **Realizar pagamento manualmente:** `POST /pagamento`
5. **Consultar status do pedido:** `GET /pedidos/{id}`
6. **Realizar pagamento via webhook:** `POST /webhook/update-payment`
7. **Atualizar manualmente status do pedido:** `PUT /pedidos/{id}`

*(Consulte exemplos reais no Swagger ou na Collection do Postman)*

---

## 🔒 Segurança e Boas Práticas

- Variáveis sensíveis estão em arquivos Secret (não versionar em produção)
- ConfigMap para configs não sensíveis
- HPA configurado para escalabilidade automática
- Deployments e Services para todos os componentes

---

## ✅ Checklist de Entrega

- [x] Manifestos Kubernetes (Deployment, Service, HPA, ConfigMap, Secret) no repositório
- [x] Documentação da arquitetura e infraestrutura
- [x] Collection Postman ou link do Swagger
- [x] Guia completo de execução
- [x] Boas práticas de segurança e arquitetura

---

## ℹ️ Observação importante sobre o metrics-server

Para que o autoscaling (HPA) funcione corretamente, é necessário que o **metrics-server** esteja instalado e rodando no cluster Kubernetes.

O script `setup.sh` já verifica e instala automaticamente o metrics-server caso não esteja presente, tanto no Minikube quanto em outros clusters.  
**Além disso, o script também aplica automaticamente a configuração `--kubelet-insecure-tls` no metrics-server, necessária para clusters locais (Minikube), garantindo que o HPA funcione corretamente sem necessidade de ajustes manuais.**

Se o HPA não mostrar métricas, aguarde alguns minutos após o deploy ou confira se o metrics-server está rodando com:

```bash
kubectl get deployment metrics-server -n kube-system
```
E, se necessário, consulte os logs do metrics-server para identificar possíveis problemas.

---

## 📝 Contribuição

Este projeto faz parte de um desafio educacional e está aberto para melhorias e contribuições pessoais para aprendizado!

## 📫 Contato

The Code Crafters  
[Repositório do Projeto no GitHub](https://github.com/danilocasabona/sistema-autoatendimento-lanchonete)

---

> "Construindo sistemas com propósito: escaláveis, testáveis e preparados para o futuro."