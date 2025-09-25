from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import json
import boto3
from functools import lru_cache
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, quote_plus

# Prefer DATABASE_URL if provided (e.g., for local dev/overrides)
DEFAULT_DB_URL = os.getenv("DATABASE_URL")

@lru_cache(maxsize=1)
def _read_secret():
    """Read DB credentials from AWS Secrets Manager once (IRSA provides creds).
    Returns a dict like: {username, password, host, dbname, port}
    If DB_SECRET_NAME isn't set or fetching fails, returns None.
    """
    secret_name = os.getenv("DB_SECRET_NAME", "")
    region = os.getenv("AWS_REGION", "us-east-1")
    if not secret_name:
        return None
    try:
        sm = boto3.client("secretsmanager", region_name=region)
        sec = sm.get_secret_value(SecretId=secret_name)
        return json.loads(sec["SecretString"])  # may raise if missing
    except Exception:
        # Fallback handled by caller; avoid crashing app startup
        return None

def _add_sslmode(url: str) -> str:
    """Ensure sslmode=require is present and well-formed in the DB URL."""
    if not url:
        return url
    u = urlparse(url)
    # Build/normalize query dict
    qs = dict(parse_qsl(u.query, keep_blank_values=True))
    if "sslmode" not in qs:
        qs["sslmode"] = "require"
    new_query = urlencode(qs)
    return urlunparse((u.scheme, u.netloc, u.path, u.params, new_query, u.fragment))

def _build_db_url():
    # 1) If DATABASE_URL is set, respect it (useful for local dev/tests)
    if DEFAULT_DB_URL:
        return DEFAULT_DB_URL

    # 2) Try Secrets Manager (IRSA in EKS)
    s = _read_secret()
    if s:
        user = quote_plus(s["username"])
        pw = quote_plus(s["password"])
        host = s["host"]
        db = s.get("dbname", "postgres")
        port = s.get("port", 5432)
        raw = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"
        # If this is an RDS endpoint, force sslmode=require into the URL itself
        if "rds.amazonaws.com" in host:
            return _add_sslmode(raw)
        return raw

    # 3) Last resort: docker-compose local default
    return "postgresql+psycopg2://postgres:postgres@db:5432/lanchonete"

DATABASE_URL = _build_db_url()

if "rds.amazonaws.com" in DATABASE_URL:
    DATABASE_URL = _add_sslmode(DATABASE_URL)

# Add sane defaults for connection pooling; require SSL when talking to RDS
connect_args = {"sslmode": "require"} if "rds.amazonaws.com" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()