"""Adiciona coluna categorias na tabela listas (RF08/UC03)

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-17
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'listas',
        sa.Column(
            'categorias',
            sa.String(200),
            nullable=True,
            comment='IDs das categorias selecionadas (RF12/RF08), JSON texto',
        ),
    )


def downgrade() -> None:
    op.drop_column('listas', 'categorias')
