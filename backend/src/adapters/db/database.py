# COBECO Backend — Database Adapter (SQLAlchemy Async + MySQL)
# Camada de infraestrutura: configuração de engine, session, base
# Engine criada lazy para evitar problemas no alembic

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

# ============================================================
# Base Declarativa — Modelos ORM
# ============================================================
class Base(DeclarativeBase):
    """Base para todos os modelos SQLAlchemy"""
    pass


# ============================================================
# Engine & Session Factory (Lazy Initialization)
# ============================================================
_engine: Optional[AsyncEngine] = None
_async_session_local: Optional[async_sessionmaker] = None


def get_engine() -> AsyncEngine:
    """Retorna engine assíncrona (cria na primeira chamada)"""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=False,
            pool_recycle=3600,
        )
    return _engine


def get_async_session_local() -> async_sessionmaker:
    """Retorna factory de sessão assíncrona (cria na primeira chamada)"""
    global _async_session_local
    if _async_session_local is None:
        _async_session_local = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
    return _async_session_local


# ============================================================
# Dependency Injection — Session por Request
# ============================================================
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency para obter sessão DB por request"""
    async with get_async_session_local()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ============================================================
# Init / Close — Lifecycle
# ============================================================
async def init_db() -> None:
    """Inicializa banco de dados (cria tabelas se não existirem)"""
    # Em produção, usar Alembic migrations
    # Aqui apenas para desenvolvimento/testes
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Fecha conexões do pool"""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


# ============================================================
# Transaction Helper — Para UseCases
# ============================================================
@asynccontextmanager
async def transaction() -> AsyncGenerator[AsyncSession, None]:
    """Context manager para transações explícitas (Clean Architecture)"""
    async with get_async_session_local()() as session:
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


# ============================================================
# Health Check DB
# ============================================================
async def check_db_connection() -> bool:
    """Verifica se conexão com DB está ativa"""
    try:
        async with get_async_session_local()() as session:
            await session.execute("SELECT 1")
        return True
    except Exception:
        return False