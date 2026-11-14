# COBECO Backend — Initial Schema Migration
# Cria as 8 tabelas PT-BR conforme doc-arch-0001-camada-de-dados-canon.md v3.2

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = '20261113_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ============================================================
    # Tabela: categorias (11 categorias MACRO)
    # ============================================================
    op.create_table(
        'categorias',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_categorias'),
        sa.UniqueConstraint('nome', name='uq_categorias_nome'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_categoria_nome', 'categorias', ['nome'])

    # ============================================================
    # Tabela: fornecedores (10 fornecedores)
    # ============================================================
    op.create_table(
        'fornecedores',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(150), nullable=False),
        sa.Column('cnpj', sa.String(18), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id', name='pk_fornecedores'),
        sa.UniqueConstraint('cnpj', name='uq_fornecedores_cnpj'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_fornecedor_nome', 'fornecedores', ['nome'])
    op.create_index('ix_fornecedor_cnpj', 'fornecedores', ['cnpj'])

    # ============================================================
    # Tabela: fornecedores_categorias (Pivô N:N)
    # ============================================================
    op.create_table(
        'fornecedores_categorias',
        sa.Column('fornecedor_id', sa.Integer(), nullable=False),
        sa.Column('categoria_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['fornecedor_id'], ['fornecedores.id'],
            name='fk_fc_fornecedor', ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['categoria_id'], ['categorias.id'],
            name='fk_fc_categoria', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('fornecedor_id', 'categoria_id', name='pk_fornecedores_categorias'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_fc_fornecedor', 'fornecedores_categorias', ['fornecedor_id'])
    op.create_index('ix_fc_categoria', 'fornecedores_categorias', ['categoria_id'])

    # ============================================================
    # Tabela: produtos (50 produtos agnósticos à categoria)
    # ============================================================
    op.create_table(
        'produtos',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('unidade', sa.String(10), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id', name='pk_produtos'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_produto_nome', 'produtos', ['nome'])

    # ============================================================
    # Tabela: fornecedores_produtos (Preços e Estoque ~300)
    # ============================================================
    op.create_table(
        'fornecedores_produtos',
        sa.Column('fornecedor_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('preco', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('estoque', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.ForeignKeyConstraint(
            ['fornecedor_id'], ['fornecedores.id'],
            name='fk_fp_fornecedor', ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['produto_id'], ['produtos.id'],
            name='fk_fp_produto', ondelete='RESTRICT'
        ),
        sa.PrimaryKeyConstraint('fornecedor_id', 'produto_id', name='pk_fornecedores_produtos'),
        sa.CheckConstraint('preco >= 0', name='ck_fp_preco_positivo'),
        sa.CheckConstraint('estoque >= 0', name='ck_fp_estoque_positivo'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_fp_fornecedor', 'fornecedores_produtos', ['fornecedor_id'])
    op.create_index('ix_fp_produto', 'fornecedores_produtos', ['produto_id'])

    # ============================================================
    # Tabela: usuarios (Auth)
    # ============================================================
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome_usuario', sa.String(30), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('senha_hash', sa.String(255), nullable=False),
        sa.Column('pergunta_seguranca', sa.String(255), nullable=False),
        sa.Column('resposta_seguranca_hash', sa.String(255), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('deletado_em', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_usuarios'),
        sa.UniqueConstraint('nome_usuario', name='uq_usuarios_nome_usuario'),
        sa.UniqueConstraint('email', name='uq_usuarios_email'),
        sa.CheckConstraint("LENGTH(nome_usuario) BETWEEN 3 AND 30", name='ck_usuario_nome_usuario_len'),
        sa.CheckConstraint("LENGTH(nome) BETWEEN 2 AND 100", name='ck_usuario_nome_len'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_usuario_criado_em', 'usuarios', ['criado_em'])

    # ============================================================
    # Tabela: listas (Listas de compras)
    # ============================================================
    op.create_table(
        'listas',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('deletado_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['usuario_id'], ['usuarios.id'],
            name='fk_listas_usuario', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name='pk_listas'),
        sa.CheckConstraint("LENGTH(nome) BETWEEN 1 AND 100", name='ck_lista_nome_len'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_lista_usuario_criado', 'listas', ['usuario_id', 'criado_em'])

    # ============================================================
    # Tabela: itens_lista (Itens de cada lista)
    # ============================================================
    op.create_table(
        'itens_lista',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('lista_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(
            ['lista_id'], ['listas.id'],
            name='fk_itens_lista', ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['produto_id'], ['produtos.id'],
            name='fk_itens_produto', ondelete='RESTRICT'
        ),
        sa.PrimaryKeyConstraint('id', name='pk_itens_lista'),
        sa.CheckConstraint('quantidade BETWEEN 1 AND 9999', name='ck_item_quantidade'),
        sa.UniqueConstraint('lista_id', 'produto_id', name='uq_item_lista_produto'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )


def downgrade() -> None:
    # Drop na ordem inversa (respeita FKs)
    op.drop_table('itens_lista')
    op.drop_table('listas')
    op.drop_table('usuarios')
    op.drop_table('fornecedores_produtos')
    op.drop_table('produtos')
    op.drop_table('fornecedores_categorias')
    op.drop_table('fornecedores')
    op.drop_table('categorias')