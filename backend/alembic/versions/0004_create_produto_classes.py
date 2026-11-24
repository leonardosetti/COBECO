"""Create produto_classes table for semantic brand->class mapping

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-19
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'produto_classes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('classe_nome', sa.String(100), nullable=False),
        sa.Column('termos_busca', sa.JSON(), nullable=False),           # ['pomarola', 'molho tomate', 'elefante']
        sa.Column('marcas_referencia', sa.JSON(), nullable=False),     # ['Pomarola', 'Elefante', 'Qualitá']
        sa.Column('categoria_macro', sa.String(100), nullable=True),   # 'Mercearia', 'Alimentos'
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id', name='pk_produto_classes'),
        sa.UniqueConstraint('classe_nome', name='uq_produto_classes_nome'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_produto_classes_ativo', 'produto_classes', ['ativo'])
    op.create_index('ix_produto_classes_categoria_macro', 'produto_classes', ['categoria_macro'])

    # GIN index on JSON arrays for fast containment queries (MySQL 8.0.17+)
    op.execute(
        "ALTER TABLE produto_classes ADD INDEX ix_produto_classes_termos_busca ((CAST(termos_busca AS CHAR(500))))"
    )
    op.execute(
        "ALTER TABLE produto_classes ADD INDEX ix_produto_classes_marcas_ref ((CAST(marcas_referencia AS CHAR(500))))"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE produto_classes DROP INDEX ix_produto_classes_marcas_ref")
    op.execute("ALTER TABLE produto_classes DROP INDEX ix_produto_classes_termos_busca")
    op.drop_index('ix_produto_classes_categoria_macro', table_name='produto_classes')
    op.drop_index('ix_produto_classes_ativo', table_name='produto_classes')
    op.drop_table('produto_classes')