# COBECO Backend — Contract Tests Fixtures
# Fixtures para testes de contrato OpenAPI (sem banco de dados)

import os
import pytest
from httpx import AsyncClient, ASGITransport

# Configurações de ambiente (devem vir antes dos imports do src)
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-32chars")
os.environ.setdefault("DATABASE_URL", "mysql+asyncmy://test:test@localhost:3306/cobeco_test")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("RECOVERY_MODE", "log")
os.environ.setdefault("DEBUG", "true")

from src.main import app


@pytest.fixture
def test_app():
    """App FastAPI para testes de contrato (sem DB)"""
    yield app


@pytest.fixture
async def client(test_app):
    """Cliente HTTP assíncrono para testes de contrato"""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def clear_rate_limiter():
    """Limpa rate limiters entre testes (estado é global no módulo auth)"""
    from src.adapters.api.auth import _tentativas_login, _tentativas_recovery

    _tentativas_login.clear()
    _tentativas_recovery.clear()
    yield
    _tentativas_login.clear()
    _tentativas_recovery.clear()


pytest_plugins = ("pytest_asyncio",)