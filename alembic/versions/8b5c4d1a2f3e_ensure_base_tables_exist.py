"""ensure base tables exist (idempotent)

Revision ID: 8b5c4d1a2f3e
Revises: 3f13625e81b2
Create Date: 2025-09-25 00:00:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text

# revision identifiers, used by Alembic.
revision: str = "8b5c4d1a2f3e"
down_revision: Union[str, None] = "3f13625e81b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_table(bind, name: str, schema: str = "public") -> bool:
    return name in inspect(bind).get_table_names(schema=schema)


def _table_empty(bind, name: str) -> bool:
    try:
        return bind.execute(text(f"SELECT COUNT(*) FROM {name}")).scalar() == 0
    except Exception:
        return True


def upgrade() -> None:
    bind = op.get_bind()

    # ---------- cliente ----------
    if not _has_table(bind, "cliente"):
        op.create_table(
            "cliente",
            sa.Column("cliente_id", sa.Integer(), nullable=False),
            sa.Column("nome", sa.String(length=255), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("telefone", sa.String(length=11), nullable=True),
            sa.Column("cpf", sa.String(length=11), nullable=False),
            sa.PrimaryKeyConstraint("cliente_id"),
            sa.UniqueConstraint("cpf"),
        )
        op.create_index(op.f("ix_cliente_cliente_id"), "cliente", ["cliente_id"], unique=False)
        op.create_index(op.f("ix_cliente_email"), "cliente", ["email"], unique=True)

    # ---------- funcionario ----------
    if not _has_table(bind, "funcionario"):
        op.create_table(
            "funcionario",
            sa.Column("funcionario_id", sa.Integer(), nullable=False),
            sa.Column("nome", sa.String(length=255), nullable=False),
            sa.Column("senha", sa.String(length=110), nullable=False),
            sa.Column("cargo", sa.String(length=255), nullable=False),
            sa.PrimaryKeyConstraint("funcionario_id"),
        )
        op.create_index(op.f("ix_funcionario_funcionario_id"), "funcionario", ["funcionario_id"], unique=False)

    # ---------- pedido_status ----------
    if not _has_table(bind, "pedido_status"):
        op.create_table(
            "pedido_status",
            sa.Column("pedido_status_id", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(length=50), nullable=False),
            sa.PrimaryKeyConstraint("pedido_status_id"),
        )
        op.create_index(op.f("ix_pedido_status_pedido_status_id"), "pedido_status", ["pedido_status_id"], unique=False)
    if _table_empty(bind, "pedido_status"):
        op.execute(
            """
            INSERT INTO pedido_status(status) VALUES
            ('Recebido'),
            ('Em prepação'),
            ('Pronto'),
            ('Finalizado'),
            ('Em processo de pagamento')
            """
        )

    # ---------- produto_tipo ----------
    if not _has_table(bind, "produto_tipo"):
        op.create_table(
            "produto_tipo",
            sa.Column("produto_tipo_id", sa.Integer(), nullable=False),
            sa.Column("nome", sa.String(length=255), nullable=False),
            sa.PrimaryKeyConstraint("produto_tipo_id"),
        )
        op.create_index(op.f("ix_produto_tipo_produto_tipo_id"), "produto_tipo", ["produto_tipo_id"], unique=False)
    if _table_empty(bind, "produto_tipo"):
        op.execute(
            """
            INSERT INTO produto_tipo(nome) VALUES
            ('Lanche'),
            ('Acompanhamento'),
            ('Bebida'),
            ('Sobremesa')
            """
        )

    # ---------- produto ----------
    if not _has_table(bind, "produto"):
        op.create_table(
            "produto",
            sa.Column("produto_id", sa.Integer(), nullable=False),
            sa.Column("nome", sa.String(length=255), nullable=False),
            sa.Column("descricao", sa.String(length=255), nullable=False),
            sa.Column("preco", sa.DECIMAL(precision=10, scale=2), nullable=False),
            sa.Column("categoria", sa.Integer(), nullable=False),
            sa.Column("imagem", sa.String(length=255), nullable=True),
            sa.Column("cliente", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(["cliente"], ["cliente.cliente_id"]),
            sa.PrimaryKeyConstraint("produto_id"),
        )
        op.create_index(op.f("ix_produto_produto_id"), "produto", ["produto_id"], unique=False)

    # ---------- pedido ----------
    if not _has_table(bind, "pedido"):
        op.create_table(
            "pedido",
            sa.Column("pedido_id", sa.Integer(), nullable=False),
            sa.Column("cliente", sa.Integer(), nullable=True),
            sa.Column("produto_1", sa.Integer(), nullable=True),
            sa.Column("produto_2", sa.Integer(), nullable=True),
            sa.Column("produto_3", sa.Integer(), nullable=True),
            sa.Column("produto_4", sa.Integer(), nullable=True),
            sa.Column("status", sa.Integer(), nullable=True),
            sa.Column("data_criacao", sa.Time(), nullable=False),
            sa.Column("data_finalizacao", sa.Time(), nullable=True),
            sa.ForeignKeyConstraint(["cliente"], ["cliente.cliente_id"]),
            sa.ForeignKeyConstraint(["produto_1"], ["produto.produto_id"]),
            sa.ForeignKeyConstraint(["produto_2"], ["produto.produto_id"]),
            sa.ForeignKeyConstraint(["produto_3"], ["produto.produto_id"]),
            sa.ForeignKeyConstraint(["produto_4"], ["produto.produto_id"]),
            sa.ForeignKeyConstraint(["status"], ["pedido_status.pedido_status_id"]),
            sa.PrimaryKeyConstraint("pedido_id"),
        )

    # ---------- pagamento ----------
    if not _has_table(bind, "pagamento"):
        op.create_table(
            "pagamento",
            sa.Column("pedido", sa.Integer(), nullable=False),
            sa.Column("codigo_pagamento", sa.String(length=255), nullable=False),
            sa.Column("status", sa.String(length=100), nullable=True),
            sa.ForeignKeyConstraint(["pedido"], ["pedido.pedido_id"]),
            sa.PrimaryKeyConstraint("pedido", "codigo_pagamento"),
        )


def downgrade() -> None:
    # Mantemos o downgrade simples: só apagamos o que esta revisão criou.
    bind = op.get_bind()
    for name in ["pagamento", "pedido", "produto", "produto_tipo", "pedido_status", "funcionario"]:
        if _has_table(bind, name):
            op.drop_table(name)