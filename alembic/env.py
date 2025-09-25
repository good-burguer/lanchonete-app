from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
import os
import sys
import re

# Ensure the app package is importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import Base and models so Alembic "sees" all tables via metadata
from app.infrastructure.db.database import Base, _build_db_url  # <- Base do seu projeto, usando _build_db_url()
from app.models import *  # noqa: F401,F403  (garante que modelos sejam carregados)

# Alembic Config: acesso ao arquivo .ini
config = context.config

# Logging do Alembic (se definido no .ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados usados para autogenerate
target_metadata = Base.metadata


def _with_sslmode(url: str) -> str:
    """
    Normaliza a URL para garantir `sslmode=require` de forma correta.
    Casos tratados:
      - Já tem ?sslmode=... (ok) → mantém
      - Já tem &sslmode=... após '?' (ok) → mantém
      - Malformado no PATH (ex.: .../db&sslmode=require ou .../db?sslmode=require sem query válida) → move para a query corretamente
      - Não tem sslmode → adiciona à query (? ou & conforme existir)
    """
    if not url:
        return url
    from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

    u = urlparse(url, allow_fragments=False)
    path = u.path
    query = u.query or ""

    # Caso malformado: sslmode foi pendurado no PATH (sem '?')
    # Exemplos: "/goodburger&sslmode=require" ou "/goodburger?sslmode=require" (mas query não foi parseada)
    if ("&sslmode=" in path or "?sslmode=" in path) and not query:
        # remove qualquer sufixo pendurado no path e inicia query com sslmode=require
        base_path = path.split("&sslmode=")[0].split("?sslmode=")[0]
        path = base_path
        query = "sslmode=require"

    # Parse da query atual (se houver) e normalização
    qs = dict(parse_qsl(query, keep_blank_values=True))
    if "sslmode" not in qs:
        qs["sslmode"] = "require"

    new_query = urlencode(qs)
    return urlunparse((u.scheme, u.netloc, path, u.params, new_query, u.fragment))


def _get_db_url() -> str:
    """
    Resolve a URL do banco priorizando a variável de ambiente DATABASE_URL.
    Se não existir, tenta usar build_url() do projeto.
    Se ainda não existir, usa o valor do alembic.ini (sqlalchemy.url).
    """
    env_url = os.getenv("DATABASE_URL", "").strip()
    if env_url:
        try:
            safe = re.sub(r'://([^:/@]+):([^@]+)@', r'://\1:***@', env_url)
            print(f"[alembic] Using DB URL source=env: {safe}")
        except Exception:
            pass
        return _with_sslmode(env_url)

    try:
        built_url = _build_db_url()
        if built_url:
            try:
                safe = re.sub(r'://([^:/@]+):([^@]+)@', r'://\1:***@', built_url)
                print(f"[alembic] Using DB URL source=build_url: {safe}")
            except Exception:
                pass
            return _with_sslmode(built_url)
    except Exception:
        pass

    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url:
        try:
            safe = re.sub(r'://([^:/@]+):([^@]+)@', r'://\1:***@', ini_url)
            print(f"[alembic] Using DB URL source=ini: {safe}")
        except Exception:
            pass
        return _with_sslmode(ini_url)

    raise RuntimeError(
        "DATABASE_URL não definida, _build_db_url() falhou ou retornou vazio, e 'sqlalchemy.url' vazio no alembic.ini. "
        "Defina DATABASE_URL, implemente _build_db_url() corretamente, ou preencha sqlalchemy.url."
    )

def run_migrations_offline() -> None:
    """Executa migrações em modo 'offline' (sem engine real)."""
    url = _get_db_url()
    url = _with_sslmode(url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações em modo 'online' (com conexão real)."""
    resolved_url = _with_sslmode(_get_db_url())
    connectable = engine_from_config(
        {**config.get_section(config.config_ini_section, {}), "sqlalchemy.url": resolved_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
