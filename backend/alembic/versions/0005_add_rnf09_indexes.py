"""Add performance indexes for RNF09 (API Performance Audit)

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-20
"""
from alembic import op
import sqlalchemy as sa

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # listas: (usuario_id, criado_em, deletado_em) — supports listar_por_usuario with soft delete filter
    # Keeps existing ix_lista_usuario_criado (usuario_id, criado_em)
    op.create_index(
        'ix_lista_usuario_criado_deletado',
        'listas',
        ['usuario_id', 'criado_em', 'deletado_em']
    )

    # itens_lista: (lista_id, produto_id) — explicit composite for item lookup
    # (covered by uq_item_lista_produto unique constraint, but explicit for clarity)
    op.create_index(
        'ix_itens_lista_lista_produto',
        'itens_lista',
        ['lista_id', 'produto_id']
    )

    # fornecedores_produtos: (fornecedor_id, produto_id, ativo, estoque)
    # Supports calcular_disponibilidade and buscar_precos_para_comparacao
    op.create_index(
        'ix_fp_fornecedor_produto_ativo_estoque',
        'fornecedores_produtos',
        ['fornecedor_id', 'produto_id', 'ativo', 'estoque']
    )

    # sessoes: (usuario_id, revogada_em, expira_em)
    # Supports buscar_ativas_por_usuario (filters revogada_em IS NULL)
    # Keeps existing ix_sessao_usuario_expira (usuario_id, expira_em)
    op.create_index(
        'ix_sessao_usuario_revogada_expira',
        'sessoes',
        ['usuario_id', 'revogada_em', 'expira_em']
    )


def downgrade() -> None:
    op.drop_index('ix_sessao_usuario_revogada_expira', table_name='sessoes')
    op.drop_index('ix_fp_fornecedor_produto_ativo_estoque', table_name='fornecedores_produtos')
    op.drop_index('ix_itens_lista_lista_produto', table_name='itens_lista')
    op.drop_index('ix_lista_usuario_criado_deletado', table_name='listas')