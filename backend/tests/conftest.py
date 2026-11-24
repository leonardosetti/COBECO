# COBECO Backend — conftest global de testes
# Configuração mínima para testes unitários
# Testes de integração (test_auth_flow.py) definem suas próprias fixtures

import os

import pytest

# Configurações de ambiente (devem vir antes dos imports do src)
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-32chars")
os.environ.setdefault("DATABASE_URL", "mysql+asyncmy://test:test@localhost:3306/cobeco_test")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("RECOVERY_MODE", "log")


# ============================================================
# Fixtures para testes unitários
# ============================================================

@pytest.fixture(autouse=True)
def clear_rate_limiter():
    """Limpa rate limiters entre testes (estado é global no módulo auth)"""
    from src.adapters.api.auth import _tentativas_login, _tentativas_recovery

    _tentativas_login.clear()
    _tentativas_recovery.clear()
    yield
    _tentativas_login.clear()
    _tentativas_recovery.clear()


# ============================================================
# Configuração pytest-asyncio
# ============================================================

pytest_plugins = ("pytest_asyncio",)