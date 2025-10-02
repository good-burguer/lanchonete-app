import os
import re
import sqlalchemy as sa
from alembic import context

# 👇 Tenta importar o metadata da app; se não der, usa None
try:
    # ajuste conforme onde está seu declarative Base
    # exemplos comuns:
    # from app.db import Base
    # from app.models import Base
    from app.db import Base  # <-- ajuste se necessário
    target_metadata = Base.metadata
except Exception:
    target_metadata = None  # ainda funciona; apenas não faz autogenerate

config = context.config

def _with_sslmode(url: str) -> str:
    # acrescenta sslmode=require se não houver "sslmode=" na querystring
    if "sslmode=" in url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}sslmode=require"

def _build_db_url() -> str:
    """
    Tenta importar um helper do projeto; se não existir, retorna string vazia.
    """
    try:
        # ajuste este import se você já tiver um helper no projeto
        from app.settings import build_db_url as _b
        return _b()
    except Exception:
        return ""

def _get_db_url() -> str:
    """
    Resolve a URL do banco na seguinte ordem de prioridade:
      1) ALEMBIC_DATABASE_URL (útil para CI/CD e execuções direcionadas)
      2) DATABASE_URL (padrão comum em PaaS)
      3) _build_db_url() do projeto
      4) sqlalchemy.url definido no alembic.ini
    Sempre normaliza para conter `sslmode=require` salvo se já houver `sslmode=` na query.
    """
    def _mask(u: str) -> str:
        try:
            return re.sub(r"://([^:/@]+):([^@]+)@", r"://\1:***@", u)
        except Exception:
            return u

    # 1) ALEMBIC_DATABASE_URL
    env_alembic = os.getenv("ALEMBIC_DATABASE_URL", "").strip()
    if env_alembic:
        print(f"[alembic] Using DB URL source=env(ALEMBIC_DATABASE_URL): {_mask(env_alembic)}")
        return _with_sslmode(env_alembic)

    # 2) DATABASE_URL
    env_database = os.getenv("DATABASE_URL", "").strip()
    if env_database:
        print(f"[alembic] Using DB URL source=env(DATABASE_URL): {_mask(env_database)}")
        return _with_sslmode(env_database)

    # 3) _build_db_url() do projeto
    try:
        built_url = _build_db_url()
        if built_url:
            print(f"[alembic] Using DB URL source=build_url: {_mask(built_url)}")
            return _with_sslmode(built_url)
    except Exception as e:
        # Mantém silêncio para não poluir saída, mas deixa um hint mínimo
        print(f"[alembic] _build_db_url() falhou: {type(e).__name__}")

    # 4) sqlalchemy.url do alembic.ini
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url:
        print(f"[alembic] Using DB URL source=ini: {_mask(ini_url)}")
        return _with_sslmode(ini_url)

    raise RuntimeError(
        "Nenhuma URL de banco encontrada. Defina ALEMBIC_DATABASE_URL ou DATABASE_URL, "
        "implemente _build_db_url() corretamente, ou configure sqlalchemy.url no alembic.ini."
    )

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = _get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = sa.create_engine(_get_db_url())

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
