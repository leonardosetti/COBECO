# COBECO Backend — Integration Tests Shared Fixtures
# Fixtures compartilhadas para todos os testes de integração

import os

# Define env vars ANTES de importar src.config (get_settings é lru_cache —
# a primeira chamada congela os valores; sem isso, DEBUG fica False e
# openapi_url=None, quebrando testes de contrato quando rodados juntos).
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-32chars")
os.environ.setdefault("DATABASE_URL", "mysql+asyncmy://test:test@localhost:3306/cobeco_test")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("RECOVERY_MODE", "log")
os.environ.setdefault("DEBUG", "true")

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from pathlib import Path

from src.main import app
from src.adapters.db.database import get_db
from src.adapters.db.models import Base
from src.config import settings

# Seed SQL simplificado para testes (evita parsing complexo do seed.sql completo)
_SEED_SQL = """
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM `sessoes`;
DELETE FROM `fornecedores_produtos`;
DELETE FROM `fornecedores_categorias`;
DELETE FROM `itens_lista`;
DELETE FROM `listas`;
DELETE FROM `usuarios`;
DELETE FROM `produtos`;
DELETE FROM `fornecedores`;
DELETE FROM `categorias`;
DELETE FROM `produto_classes`;

ALTER TABLE `sessoes` AUTO_INCREMENT = 1;
ALTER TABLE `usuarios` AUTO_INCREMENT = 1;
ALTER TABLE `listas` AUTO_INCREMENT = 1;
ALTER TABLE `itens_lista` AUTO_INCREMENT = 1;
ALTER TABLE `categorias` AUTO_INCREMENT = 1;
ALTER TABLE `fornecedores` AUTO_INCREMENT = 1;
ALTER TABLE `produtos` AUTO_INCREMENT = 1;
ALTER TABLE `produto_classes` AUTO_INCREMENT = 1;

INSERT INTO `categorias` (`id`, `nome`, `descricao`) VALUES
  (1, 'Mercado', 'Supermercados, mercearias e atacados'),
  (2, 'Vestuário', 'Roupas, calçados e acessórios'),
  (3, 'Automotivos', 'Peças, acessórios e serviços automotivos'),
  (4, 'Informática', 'Computadores, periféricos e eletrônicos'),
  (5, 'Decoração', 'Itens de decoração e artigos para casa'),
  (6, 'Móveis', 'Móveis residenciais e corporativos'),
  (7, 'Materiais de Construção e Ferragens', 'Materiais de construção, ferramentas e ferragens'),
  (8, 'Ferramentas', 'Ferramentas manuais, elétricas e de medição'),
  (9, 'Livros', 'Livros, revistas e publicações'),
  (10, 'Jardinagem', 'Plantas, ferramentas e artigos de jardim'),
  (11, 'Eletrodomésticos', 'Eletrodomésticos de linha branca e marrom');

INSERT INTO `fornecedores` (`id`, `nome`, `cnpj`, `ativo`) VALUES
  (1, 'Carrefour', '99.000.111/0001-22', TRUE),
  (2, 'Extra', '00.111.222/0001-33', TRUE),
  (3, 'Pão de Açúcar', '66.777.888/0001-99', TRUE),
  (4, 'Magazine Luiza', '77.888.999/0001-00', TRUE),
  (5, 'Casas Bahia', '88.999.000/0001-11', TRUE),
  (6, 'Leroy Merlin', '11.222.333/0001-44', TRUE),
  (7, 'Etna', '22.333.444/0001-55', TRUE),
  (8, 'C&A', '33.444.555/0001-66', TRUE),
  (9, 'Renner', '44.555.666/0001-77', TRUE),
  (10, 'Hering', '55.666.777/0001-88', TRUE);

INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
  (1, 1), (1, 2), (1, 3), (1, 5), (1, 11), (1, 4),
  (2, 1), (2, 2), (2, 11),
  (3, 1),
  (4, 11), (4, 4), (4, 6),
  (5, 11), (5, 4), (5, 6),
  (6, 7), (6, 8), (6, 10), (6, 5),
  (7, 5), (7, 6),
  (8, 2), (9, 2), (10, 2);

INSERT INTO `produtos` (`id`, `nome`, `unidade`, `ativo`) VALUES
  (1, 'Arroz Tipo 1 5kg', 'un', TRUE),
  (2, 'Feijão Preto 1kg', 'un', TRUE),
  (3, 'Óleo de Soja 900ml', 'un', TRUE),
  (4, 'Café Torrado e Moído 500g', 'un', TRUE),
  (5, 'Açúcar Refinado 1kg', 'un', TRUE),
  (6, 'Leite Integral UHT 1L', 'un', TRUE),
  (7, 'Macarrão Espaguete 500g', 'un', TRUE),
  (8, 'Molho de Tomate 340g', 'un', TRUE),
  (9, 'Farinha de Trigo 1kg', 'un', TRUE),
  (10, 'Ovos Brancos (dúzia)', 'dz', TRUE),
  (11, 'Detergente Neutro 500ml', 'un', TRUE),
  (12, 'Papel Toalha 2 rolos', 'un', TRUE),
  (13, 'Liquidificador 2 Velocidades', 'un', TRUE),
  (14, 'Notebook i5 8GB', 'un', TRUE),
  (15, 'Martelo de Unha 25mm', 'un', TRUE),
  (16, 'Parafuso Philips 5mm (cx)', 'cx', TRUE),
  (17, 'Camiseta Algodão M', 'un', TRUE),
  (18, 'Calça Jeans 40', 'un', TRUE),
  (19, 'Vaso de Barro 20cm', 'un', TRUE),
  (20, 'Cadeira de Escritório', 'un', TRUE);

INSERT INTO `produto_classes` (`id`, `classe_nome`, `termos_busca`, `marcas_referencia`, `categoria_macro`, `ativo`) VALUES
  (1, 'Arroz', '["arroz", "arroz tipo 1"]', '["Camil", "Tio João"]', 'Mercado', TRUE),
  (2, 'Feijão', '["feijão", "feijão preto"]', '["Camil", "Kicaldo"]', 'Mercado', TRUE),
  (3, 'Óleo', '["óleo", "óleo de soja"]', '["Liza", "Soya"]', 'Mercado', TRUE);

-- Create FULLTEXT index for autocomplete (idempotent)
DROP INDEX `ix_produto_nome_fulltext` ON `produtos`;
ALTER TABLE `produtos` ADD FULLTEXT INDEX `ix_produto_nome_fulltext` (`nome`);

INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
  (1, 1, 25.51, 9999, TRUE), (1, 2, 8.29, 9999, TRUE), (1, 3, 7.03, 9999, TRUE),
  (1, 4, 17.56, 9999, TRUE), (1, 5, 4.30, 9999, TRUE), (1, 6, 4.90, 9999, TRUE),
  (1, 7, 4.65, 9999, TRUE), (1, 8, 3.88, 9999, TRUE), (1, 9, 5.59, 9999, TRUE),
  (1, 10, 10.06, 9999, TRUE), (1, 11, 2.88, 9999, TRUE), (1, 12, 6.29, 9999, TRUE),
  (1, 13, 124.82, 9999, TRUE), (1, 14, 2834.51, 9999, TRUE), (1, 17, 40.29, 9999, TRUE),
  (1, 18, 117.92, 9999, TRUE),
  (2, 1, 24.78, 9999, TRUE), (2, 2, 7.70, 9999, TRUE), (2, 3, 6.31, 9999, TRUE),
  (2, 5, 4.02, 9999, TRUE), (2, 6, 4.79, 9999, TRUE), (2, 7, 4.59, 9999, TRUE),
  (2, 8, 3.71, 9999, TRUE), (2, 9, 5.11, 9999, TRUE), (2, 10, 8.98, 9999, TRUE),
  (2, 11, 2.62, 9999, TRUE), (2, 12, 5.99, 9999, TRUE), (2, 13, 123.01, 9999, TRUE),
  (2, 17, 36.03, 9999, TRUE),
  (3, 1, 28.93, 9999, TRUE), (3, 2, 9.07, 9999, TRUE), (3, 3, 7.75, 9999, TRUE),
  (3, 4, 20.21, 9999, TRUE), (3, 5, 5.16, 9999, TRUE), (3, 6, 5.94, 9999, TRUE),
  (3, 7, 5.45, 9999, TRUE), (3, 8, 4.33, 9999, TRUE), (3, 9, 6.10, 9999, TRUE),
  (3, 10, 11.23, 9999, TRUE), (3, 11, 3.38, 9999, TRUE), (3, 12, 7.63, 9999, TRUE),
  (4, 13, 120.96, 9999, TRUE), (4, 14, 2733.93, 9999, TRUE), (4, 20, 419.69, 9999, TRUE),
  (5, 13, 138.18, 9999, TRUE), (5, 14, 3133.90, 9999, TRUE), (5, 20, 482.52, 9999, TRUE),
  (6, 15, 31.01, 9999, TRUE), (6, 16, 11.83, 9999, TRUE), (6, 19, 45.80, 9999, TRUE),
  (6, 20, 440.51, 9999, TRUE),
  (7, 19, 49.45, 9999, TRUE), (7, 20, 480.18, 9999, TRUE),
  (8, 17, 37.02, 9999, TRUE), (8, 18, 110.61, 9999, TRUE),
  (9, 17, 39.64, 9999, TRUE), (9, 18, 122.28, 9999, TRUE),
  (10, 17, 42.71, 9999, TRUE);

SET FOREIGN_KEY_CHECKS = 1;
"""


# ============================================================
# Fixtures base para testes de integração
# ============================================================


@pytest.fixture
async def test_app():
    """App FastAPI para testes de integração"""
    test_engine: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=False,
        pool_recycle=3600,
    )
    test_async_session_local = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async def override_get_db():
        async with test_async_session_local() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db

    # Tabelas já criadas pelo Alembic (alembic upgrade head roda antes dos testes no CI).
    # create_all() removido para evitar "Duplicate key name" em índices já existentes
    # (ex: ix_produto_classes_categoria_macro da migration 0004).

    # Carrega seed data (conteúdo lido no nível do módulo)
    if _SEED_SQL:
        async with test_engine.begin() as conn:
            for statement in _SEED_SQL.split(";"):
                stmt = statement.strip()
                lines = [line for line in stmt.split("\n") if not line.strip().startswith("--")]
                stmt = "\n".join(lines).strip()
                if stmt:
                    await conn.execute(text(stmt))

    # Store test session factory on app state for other fixtures
    app.state.test_async_session_local = test_async_session_local
    app.state.test_engine = test_engine

    yield app

    # Cleanup — truncate all tables and reset auto_increment to ensure clean state for next test
    import asyncio
    from sqlalchemy import create_engine
    from sqlalchemy import text as sql_text

    sync_engine = create_engine(
        settings.DATABASE_URL.replace("asyncmy", "pymysql"),
        pool_pre_ping=True,
    )
    with sync_engine.begin() as conn:
        # Disable foreign key checks, truncate tables in FK order, reset auto_increment, re-enable
        conn.execute(sql_text("SET FOREIGN_KEY_CHECKS = 0"))
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(sql_text(f"TRUNCATE TABLE `{table.name}`"))
            conn.execute(sql_text(f"ALTER TABLE `{table.name}` AUTO_INCREMENT = 1"))
        conn.execute(sql_text("SET FOREIGN_KEY_CHECKS = 1"))
    sync_engine.dispose()
    await test_engine.dispose()
    await asyncio.sleep(0.1)  # Brief pause to ensure connections close
    app.dependency_overrides.clear()


@pytest.fixture
async def client(test_app):
    """Cliente HTTP assíncrono para testes"""
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


@pytest.fixture
async def test_user(client):
    """Cria usuário único para cada teste e retorna credenciais"""
    import uuid

    unique_suffix = uuid.uuid4().hex[:8]
    username = f"testuser{unique_suffix}"
    email = f"test{unique_suffix}@teste.com"
    resp = await client.post(
        "/auth/cadastrar",
        json={
            "nome_usuario": username,
            "email": email,
            "nome": "Test User",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "Pet name?",
            "resposta_seguranca": "Fluffy",
        },
    )
    return {"username": username, "email": email, "password": "Senha@123", "nome": "Test User"}


@pytest.fixture
async def auth_headers(client, test_user):
    """Faz login e retorna headers de autorização"""
    login_resp = await client.post(
        "/auth/login", json={"nome_usuario": test_user["username"], "senha": test_user["password"]}
    )
    if login_resp.status_code != 200:
        raise RuntimeError(f"Login failed: {login_resp.json()}")
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def db_session(test_app):
    """Sessão DB para setup/teardown direto"""
    async with test_app.state.test_async_session_local() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest.fixture
async def sample_produtos(db_session):
    """Cria produtos de teste"""
    from src.adapters.db.models import ProdutoModel

    produtos = [
        ProdutoModel(nome="Arroz 5kg", unidade="un", ativo=True),
        ProdutoModel(nome="Feijão 1kg", unidade="un", ativo=True),
        ProdutoModel(nome="Óleo 900ml", unidade="un", ativo=True),
    ]
    for p in produtos:
        db_session.add(p)
    await db_session.commit()
    for p in produtos:
        await db_session.refresh(p)
    return produtos


@pytest.fixture
async def lista_com_itens(client, auth_headers, sample_produtos):
    """Cria lista com itens para comparação/exportação"""
    response = await client.post(
        "/listas",
        headers=auth_headers,
        json={
            "nome": "Lista para Testes",
            "itens": [
                {"produto_id": sample_produtos[0].id, "quantidade": 2},
                {"produto_id": sample_produtos[1].id, "quantidade": 1},
                {"produto_id": sample_produtos[2].id, "quantidade": 3},
            ],
            "categorias": [1],
        },
    )
    assert response.status_code == 201
    return response.json()


# ============================================================
# Configuração pytest-asyncio
# ============================================================

pytest_plugins = ("pytest_asyncio",)
