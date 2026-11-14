# COBECO Backend — Alembic Environment
# Configuração para migrations síncronas com MySQL (pymysql)
# Inclui retry para aguardar DB ficar pronto

import os
import sys
import time
from logging.config import fileConfig
from sqlalchemy import pool, create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import OperationalError
from alembic import context

# Adiciona src ao path para importar models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.db.models import Base
from src.config import settings

# Alembic Config
config = context.config

# Override sqlalchemy.url from settings
# Para migrations, usar driver síncrono (pymysql)
sync_db_url = settings.DATABASE_URL.replace("mysql+asyncmy://", "mysql+pymysql://")
config.set_main_option("sqlalchemy.url", sync_db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata


def create_engine_with_retry(url: str, max_retries: int = 30, retry_interval: int = 2):
    """Cria engine com retry para aguardar DB ficar pronto."""
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(url, poolclass=pool.NullPool)
            # Testa a conexão
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"Database connection sdoc-arch-0006-uc-v1cessful on attempt {attempt + 1}")
            return engine
        except OperationalError as e:
            last_exception = e
            if attempt < max_retries - 1:
                print(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_interval}s...")
                time.sleep(retry_interval)
            else:
                print(f"Database connection failed after {max_retries} attempts")
                raise
    
    raise last_exception


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with sync engine and retry."""
    connectable = create_engine_with_retry(sync_db_url)

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()