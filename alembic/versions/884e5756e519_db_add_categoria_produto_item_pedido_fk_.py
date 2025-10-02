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
    
    # 2) Backfill de dados e FK produto.categoria -> categoria_produto.id (robusto)
    # 2.1) garantir que existe ao menos uma categoria "Lanches" e obter seu id
    op.execute("""
    WITH ins AS (
      INSERT INTO categoria_produto (nome)
      VALUES ('Lanches')
      ON CONFLICT (nome) DO UPDATE SET nome = EXCLUDED.nome
      RETURNING id
    )
    SELECT 1;
    """)
  
    # 2.2) normalizar valores inválidos de produto.categoria (NULL, 0, inexistente) para a categoria "Lanches"
    op.execute("""
    WITH cat AS (
      SELECT id FROM categoria_produto WHERE nome = 'Lanches' LIMIT 1
    )
    UPDATE produto p
    SET categoria = (SELECT id FROM cat)
    WHERE
      categoria IS NULL
      OR categoria = 0
      OR NOT EXISTS (
        SELECT 1 FROM categoria_produto c WHERE c.id = p.categoria
      );
    """)
  
    # 2.3) criar a FK de forma segura:
    #  - se ainda não existir
    #  - adicionar como NOT VALID para não bloquear por dados legados entre o passo 2.2 e este
    #  - validar em seguida
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
          REFERENCES categoria_produto(id)
          NOT VALID;
        ALTER TABLE produto VALIDATE CONSTRAINT produto_categoria_fkey;
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