"""Add FULLTEXT indices for search optimization (remove LIKE usage)

Revision ID: 0007
Revises: 0006_add_g_ml_units
Create Date: 2026-11-25
"""
from alembic import op
import sqlalchemy as sa

revision = '0007'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. FULLTEXT index em produtos.marca para busca por marca sem LIKE
    try:
        op.execute(
            "ALTER TABLE produtos ADD FULLTEXT INDEX ft_produto_marca (marca)"
        )
    except Exception:
        pass  # Índice pode já existir

    # 2. FULLTEXT index em listas.nome para busca de listas sem LIKE
    try:
        op.execute(
            "ALTER TABLE listas ADD FULLTEXT INDEX ft_lista_nome (nome)"
        )
    except Exception:
        pass

    # 3. Colunas normais (não virtuais) em produto_classes para buscar em JSON via FULLTEXT
    # MySQL 8 não suporta FULLTEXT em colunas virtuais geradas, então usamos colunas normais
    # populadas via UPDATE e mantidas pelo código de aplicação ao salvar produto_classes.
    try:
        op.execute(
            "ALTER TABLE produto_classes ADD COLUMN termos_busca_texto TEXT"
        )
    except Exception:
        pass
    try:
        op.execute(
            "ALTER TABLE produto_classes ADD COLUMN marcas_referencia_texto TEXT"
        )
    except Exception:
        pass

    # 4. Popular as colunas a partir do JSON existente
    op.execute(
        """
        UPDATE produto_classes SET termos_busca_texto = (
            SELECT GROUP_CONCAT(t SEPARATOR ' ') FROM (
                SELECT TRIM(BOTH '"' FROM jt.val) AS t
                FROM JSON_TABLE(termos_busca, '$[*]' COLUMNS (val VARCHAR(200) PATH '$')) AS jt
            ) AS t
        )
        """
    )
    op.execute(
        """
        UPDATE produto_classes SET marcas_referencia_texto = (
            SELECT GROUP_CONCAT(t SEPARATOR ' ') FROM (
                SELECT TRIM(BOTH '"' FROM jt.val) AS t
                FROM JSON_TABLE(marcas_referencia, '$[*]' COLUMNS (val VARCHAR(200) PATH '$')) AS jt
            ) AS t
        )
        """
    )

    # 5. FULLTEXT indices nas colunas de texto
    try:
        op.execute(
            "ALTER TABLE produto_classes ADD FULLTEXT INDEX ft_produto_classes_termos (termos_busca_texto)"
        )
    except Exception:
        pass
    try:
        op.execute(
            "ALTER TABLE produto_classes ADD FULLTEXT INDEX ft_produto_classes_marcas (marcas_referencia_texto)"
        )
    except Exception:
        pass


def downgrade() -> None:
    op.execute("ALTER TABLE produto_classes DROP INDEX IF EXISTS ft_produto_classes_marcas")
    op.execute("ALTER TABLE produto_classes DROP INDEX IF EXISTS ft_produto_classes_termos")
    op.execute("ALTER TABLE produto_classes DROP COLUMN IF EXISTS marcas_referencia_texto")
    op.execute("ALTER TABLE produto_classes DROP COLUMN IF EXISTS termos_busca_texto")
    op.execute("ALTER TABLE listas DROP INDEX IF EXISTS ft_lista_nome")
    op.execute("ALTER TABLE produtos DROP INDEX IF EXISTS ft_produto_marca")
