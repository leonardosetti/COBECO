"""Add marca column and FULLTEXT index to produtos

Revision ID: 0003
Revises: 0001
Create Date: 2026-11-19
"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add marca column (nullable initially for backfill)
    op.add_column(
        'produtos',
        sa.Column('marca', sa.String(100), nullable=True)
    )

    # 2. Create index on marca for exact/prefix lookups
    op.create_index('ix_produto_marca', 'produtos', ['marca'])

    # 3. Add FULLTEXT index on nome for semantic search (MySQL 8+)
    # Using raw SQL for MySQL-specific FULLTEXT syntax
    op.execute(
        "ALTER TABLE produtos ADD FULLTEXT INDEX ft_produto_nome (nome)"
    )


def downgrade() -> None:
    # Drop FULLTEXT index
    op.execute("ALTER TABLE produtos DROP INDEX ft_produto_nome")

    # Drop marca index
    op.drop_index('ix_produto_marca', table_name='produtos')

    # Drop marca column
    op.drop_column('produtos', 'marca')