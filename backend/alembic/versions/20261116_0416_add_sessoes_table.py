# COBECO Backend — Add Sessões Table
# Adiciona tabela sessoes para refresh tokens (RF02)

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = '20261116_0416_add_sessoes'
down_revision = '20261113_000001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sessoes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('refresh_token_hash', sa.String(255), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('ip', sa.String(45), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('expira_em', sa.DateTime(), nullable=False),
        sa.Column('revogada_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['usuario_id'], ['usuarios.id'],
            name='fk_sessoes_usuario', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name='pk_sessoes'),
        sa.UniqueConstraint('refresh_token_hash', name='uq_sessoes_refresh_token_hash'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
    )
    op.create_index('ix_sessoes_usuario_expira', 'sessoes', ['usuario_id', 'expira_em'])
    op.create_index('ix_sessoes_token_hash', 'sessoes', ['refresh_token_hash'])


def downgrade() -> None:
    op.drop_table('sessoes')