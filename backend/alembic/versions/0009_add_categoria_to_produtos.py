"""Add categoria_id to produtos for proper product categorization

Revision ID: 0009
Revises: 0008
Create Date: 2026-11-27
"""
from alembic import op
import sqlalchemy as sa

revision = '0009'
down_revision = '0008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add categoria_id to produtos
    op.add_column(
        'produtos',
        sa.Column('categoria_id', sa.Integer, nullable=True)
    )
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_produtos_categoria',
        'produtos',
        'categorias',
        ['categoria_id'],
        ['id']
    )
    
    # Create index for performance
    op.create_index(
        'ix_produtos_categoria',
        'produtos',
        ['categoria_id']
    )


def downgrade() -> None:
    op.drop_index('ix_produtos_categoria', table_name='produtos')
    op.drop_constraint('fk_produtos_categoria', 'produtos', type_='foreignkey')
    op.drop_column('produtos', 'categoria_id')
