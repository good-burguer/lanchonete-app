# FROM python:3.12-slim-bookworm
FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 2) Copia o código
COPY app ./app
# (Alembic: copiar config + scripts de migração)
COPY alembic.ini .
COPY alembic ./alembic
# (opcional) scripts SQL legados, se existirem
COPY migrations ./migrations

EXPOSE 8080

# 3) Sobe a API em prod (sem --reload)
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
