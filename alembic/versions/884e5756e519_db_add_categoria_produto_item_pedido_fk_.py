"""db: add categoria_produto & item_pedido + FK em produto

Cria as tabelas faltantes e a FK que os endpoints esperam.
Idempotente: só cria se não existir; insere seed com ON CONFLICT DO NOTHING.
"""

from alembic import op
import sqlalchemy as sa

# Ajuste aqui a partir do seu head atual, que hoje é o merge 95a435bd8835
revision = "884e5756e519"
down_revision = "95a435bd8835"
branch_labels = None
depends_on = None

def upgrade():
    # 1) categoria_produto
    op.execute("""
    CREATE TABLE IF NOT EXISTS categoria_produto (
      id   SERIAL PRIMARY KEY,
      nome VARCHAR(255) NOT NULL UNIQUE
    );
    """)

    # 4) seed mínimo de categorias (idempotente)
    op.execute("""
    INSERT INTO categoria_produto (nome)
    VALUES ('Lanches'), ('Bebidas'), ('Sobremesas')
    ON CONFLICT (nome) DO NOTHING;
    """)
    
    # 2) FK produto.categoria -> categoria_produto.id (se ainda não existir)
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'produto_categoria_fkey'
      ) THEN
        ALTER TABLE produto
          ADD CONSTRAINT produto_categoria_fkey
          FOREIGN KEY (categoria)
          REFERENCES categoria_produto(id);
      END IF;
    END$$;
    """)

    # 3) item_pedido
    op.execute("""
    CREATE TABLE IF NOT EXISTS item_pedido (
      id         SERIAL PRIMARY KEY,
      pedido     INTEGER NOT NULL REFERENCES pedido(pedido_id) ON DELETE CASCADE,
      produto    INTEGER NOT NULL REFERENCES produto(produto_id),
      quantidade INTEGER NOT NULL DEFAULT 1,
      preco_unit NUMERIC(10,2) NOT NULL
    );
    """)

def downgrade():
    # Remover FK se existir
    op.execute("""
    DO $$
    BEGIN
      IF EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'produto_categoria_fkey'
      ) THEN
        ALTER TABLE produto DROP CONSTRAINT produto_categoria_fkey;
      END IF;
    END$$;
    """)
    # Dropar tabelas (se existirem)
    op.execute("DROP TABLE IF EXISTS item_pedido;")
    op.execute("DROP TABLE IF EXISTS categoria_produto;")