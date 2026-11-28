"""Add pgvector, tsvector columns and search indexes.

Revision ID: 0010
Revises: 0009
Create Date: 2026-11-28
"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = '0010'
down_revision = '0009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Extensão pgvector
    op.execute("CREATE EXTENSION IF NOT EXISTS pgvector")

    # 2. Colunas tsvector (texto) — mantidas por trigger
    op.add_column(
        'produtos',
        sa.Column('nome_tsv', sa.Text(), nullable=True),
    )
    op.add_column(
        'produtos',
        sa.Column('marca_tsv', sa.Text(), nullable=True),
    )
    op.add_column(
        'produtos',
        sa.Column('embedding', Vector(384), nullable=True),
    )

    op.add_column(
        'produto_classes',
        sa.Column('termos_busca_tsv', sa.Text(), nullable=True),
    )
    op.add_column(
        'produto_classes',
        sa.Column('marcas_referencia_tsv', sa.Text(), nullable=True),
    )
    op.add_column(
        'produto_classes',
        sa.Column('embedding', Vector(384), nullable=True),
    )

    # 3. Índices GIN para tsvector
    op.create_index(
        'ix_produto_nome_tsv', 'produtos', ['nome_tsv'],
        postgresql_using='gin',
    )
    op.create_index(
        'ix_produto_marca_tsv', 'produtos', ['marca_tsv'],
        postgresql_using='gin',
    )
    op.create_index(
        'ix_produto_classes_termos_tsv', 'produto_classes', ['termos_busca_tsv'],
        postgresql_using='gin',
    )
    op.create_index(
        'ix_produto_classes_marcas_tsv', 'produto_classes', ['marcas_referencia_tsv'],
        postgresql_using='gin',
    )

    # 4. Índices vetoriais (HNSW, cosseno)
    op.create_index(
        'ix_produto_embedding', 'produtos', ['embedding'],
        postgresql_using='hnsw',
        postgresql_with={'m': 16, 'ef_construction': 64},
        postgresql_opclass={'embedding': 'vector_cosine_ops'},
    )
    op.create_index(
        'ix_produto_classes_embedding', 'produto_classes', ['embedding'],
        postgresql_using='hnsw',
        postgresql_with={'m': 16, 'ef_construction': 64},
        postgresql_opclass={'embedding': 'vector_cosine_ops'},
    )

    # 5. Triggers para manter tsvector sincronizado com texto fonte
    op.execute("""
        CREATE OR REPLACE FUNCTION atualizar_produto_nome_tsv()
        RETURNS trigger AS $$
        BEGIN
            NEW.nome_tsv := to_tsvector('portuguese', COALESCE(NEW.nome, ''));
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_produto_nome_tsv
        BEFORE INSERT OR UPDATE OF nome ON produtos
        FOR EACH ROW EXECUTE FUNCTION atualizar_produto_nome_tsv();
    """)
    op.execute("""
        CREATE OR REPLACE FUNCTION atualizar_produto_marca_tsv()
        RETURNS trigger AS $$
        BEGIN
            NEW.marca_tsv := to_tsvector('portuguese', COALESCE(NEW.marca, ''));
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_produto_marca_tsv
        BEFORE INSERT OR UPDATE OF marca ON produtos
        FOR EACH ROW EXECUTE FUNCTION atualizar_produto_marca_tsv();
    """)
    op.execute("""
        CREATE OR REPLACE FUNCTION atualizar_produto_classes_termos_tsv()
        RETURNS trigger AS $$
        BEGIN
            NEW.termos_busca_tsv := to_tsvector('portuguese', COALESCE(NEW.termos_busca::text, ''));
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_produto_classes_termos_tsv
        BEFORE INSERT OR UPDATE OF termos_busca ON produto_classes
        FOR EACH ROW EXECUTE FUNCTION atualizar_produto_classes_termos_tsv();
    """)

    # 6. Backfill tsvector para dados existentes
    op.execute("UPDATE produtos SET nome_tsv = to_tsvector('portuguese', COALESCE(nome, '')) WHERE nome_tsv IS NULL")
    op.execute("UPDATE produtos SET marca_tsv = to_tsvector('portuguese', COALESCE(marca, '')) WHERE marca_tsv IS NULL")
    op.execute("UPDATE produto_classes SET termos_busca_tsv = to_tsvector('portuguese', COALESCE(termos_busca::text, '')) WHERE termos_busca_tsv IS NULL")
    op.execute("UPDATE produto_classes SET marcas_referencia_tsv = to_tsvector('portuguese', COALESCE(marcas_referencia::text, '')) WHERE marcas_referencia_tsv IS NULL")


def downgrade() -> None:
    # 6. Remover triggers e funções
    op.execute("DROP TRIGGER IF EXISTS trg_produto_classes_termos_tsv ON produto_classes")
    op.execute("DROP FUNCTION IF EXISTS atualizar_produto_classes_termos_tsv()")
    op.execute("DROP TRIGGER IF EXISTS trg_produto_marca_tsv ON produtos")
    op.execute("DROP FUNCTION IF EXISTS atualizar_produto_marca_tsv()")
    op.execute("DROP TRIGGER IF EXISTS trg_produto_nome_tsv ON produtos")
    op.execute("DROP FUNCTION IF EXISTS atualizar_produto_nome_tsv()")

    # 5. Remover índices vetoriais e GIN
    op.drop_index('ix_produto_classes_embedding', table_name='produto_classes')
    op.drop_index('ix_produto_embedding', table_name='produtos')
    op.drop_index('ix_produto_classes_marcas_tsv', table_name='produto_classes')
    op.drop_index('ix_produto_classes_termos_tsv', table_name='produto_classes')
    op.drop_index('ix_produto_marca_tsv', table_name='produtos')
    op.drop_index('ix_produto_nome_tsv', table_name='produtos')

    # 4. Remover colunas
    op.drop_column('produto_classes', 'embedding')
    op.drop_column('produto_classes', 'marcas_referencia_tsv')
    op.drop_column('produto_classes', 'termos_busca_tsv')
    op.drop_column('produtos', 'embedding')
    op.drop_column('produtos', 'marca_tsv')
    op.drop_column('produtos', 'nome_tsv')

    # 3. Remover extensão pgvector (se não houver dependências)
    op.execute("DROP EXTENSION IF EXISTS pgvector")
