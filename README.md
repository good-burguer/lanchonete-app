# Lanchonete – App
Aplicação (ex.: FastAPI) implantada no EKS via Helm.

## Estrutura
- `app/` código da aplicação
- `charts/app/` chart Helm
- `migrations/` migrações (Alembic)

## CI (depois)
- VARS: `AWS_REGION`, `AWS_ACCOUNT_ID`, `EKS_CLUSTER`
- SECRET: `AWS_ROLE_APP`
