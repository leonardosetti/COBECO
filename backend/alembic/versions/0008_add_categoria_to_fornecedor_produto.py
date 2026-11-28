"""Add categoria_id to fornecedores_produtos for proper product categorization

Revision ID: 0008
Revises: 0007
Create Date: 2026-11-27
"""
from alembic import op
import sqlalchemy as sa

revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add categoria_id to fornecedores_produtos
    op.add_column(
        'fornecedores_produtos',
        sa.Column('categoria_id', sa.Integer, nullable=True)
    )
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_fornecedores_produtos_categoria',
        'fornecedores_produtos',
        'categorias',
        ['categoria_id'],
        ['id']
    )
    
    # Create index for performance
    op.create_index(
        'ix_fornecedores_produtos_categoria',
        'fornecedores_produtos',
        ['categoria_id']
    )
    
    # Create composite index for listar_por_categorias query
    op.create_index(
        'ix_fornecedores_produtos_fornecedor_categoria',
        'fornecedores_produtos',
        ['fornecedor_id', 'categoria_id']
    )


def downgrade() -> None:
    op.drop_index('ix_fornecedores_produtos_fornecedor_categoria', table_name='fornecedores_produtos')
    op.drop_index('ix_fornecedores_produtos_categoria', table_name='fornecedores_produtos')
    op.drop_constraint('fk_fornecedores_produtos_categoria', 'fornecedores_produtos', type_='foreignkey')
    op.drop_column('fornecedores_produtos', 'categoria_id')
