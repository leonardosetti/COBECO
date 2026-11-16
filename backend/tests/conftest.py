# COBECO Backend — conftest global de testes
# Paridade com o ambiente do CI (.github/workflows config-ci-0001): Settings
# exige SECRET_KEY >= 32 chars; sem isso, a coleta dos testes falha fora do CI.
import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-32chars")
os.environ.setdefault("DATABASE_URL", "mysql+asyncmy://test:test@localhost:3306/cobeco_test")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("RECOVERY_MODE", "log")
