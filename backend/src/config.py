# COBECO Backend — Configuração Centralizada (Pydantic Settings)
# Single source of truth para todas as variáveis de ambiente

from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas via .env"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ============================================================
    # Application
    # ============================================================
    APP_NAME: str = "COBECO MVP"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ============================================================
    # Database — MySQL 8 InnoDB (RNF03, RNF12)
    # ============================================================
    DATABASE_URL: str = Field(
        default="mysql+asyncmy://cobeco:cobeco@localhost:3306/cobeco",
        description="URL de conexão MySQL (async via asyncmy)",
    )
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ============================================================
    # Authentication — JWT (RF01-RF06)
    # ============================================================
    SECRET_KEY: str = Field(
        default="",
        description="Chave secreta para JWT (gere com: openssl rand -hex 32)",
        min_length=32,
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Rate Limiting (RF02, RNF10)
    RATE_LIMIT_REQUESTS: int = 6
    RATE_LIMIT_WINDOW_MINUTES: int = 15

    # Password Policy (RF01)
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPER: bool = True
    PASSWORD_REQUIRE_LOWER: bool = True
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    BCRYPT_ROUNDS: int = 12

    # Recovery Mode (RF04)
    RECOVERY_MODE: str = Field(
        default="log",
        description="Modo de recuperação de senha: 'log' (stdout) ou 'email'",
        pattern="^(log|email)$",
    )

    # ============================================================
    # CORS (se necessário para desenvolvimento)
    # ============================================================
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:8080", "http://127.0.0.1:8080"],
        description="Origens permitidas para CORS",
    )

    # ============================================================
    # PDF Export (RF17) — ReportLab
    # ============================================================
    PDF_FONT_DIR: str = "/usr/share/fonts/truetype/dejavu"
    PDF_DEFAULT_FONT: str = "DejaVuSans"

    # ============================================================
    # Seed Data (RNF08)
    # ============================================================
    SEED_CATEGORIES_COUNT: int = 11
    SEED_SUPPLIERS_COUNT: int = 10
    SEED_PRODUCTS_COUNT: int = 50
    SEED_PRICES_COUNT: int = 300

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if not v or v == "gere_com_openssl_rand_hex_32":
            import secrets
            return secrets.token_hex(32)
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("mysql"):
            raise ValueError("DATABASE_URL deve usar mysql+pymysql://")
        return v


@lru_cache
def get_settings() -> Settings:
    """Singleton de configurações (cacheado via lru_cache)"""
    return Settings()


settings = get_settings()