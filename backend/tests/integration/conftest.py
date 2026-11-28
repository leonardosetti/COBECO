# COBECO Backend — Integration Tests Shared Fixtures
# Cada teste: engine dedicado, tabelas criadas se necessário, seed carregado,
# execução em transação com SAVEPOINT/ROLLBACK para isolamento completo.

import os
import asyncio

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-32chars")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://cobeco:cobeco@cobeco-db-stage:5432/cobeco_stage")
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

from src.main import app
from src.adapters.db.database import get_db
from src.adapters.db.models import Base
from src.config import settings

# Seed SQL simplificado para testes (PostgreSQL compatível)
_SEED_SQL = """
TRUNCATE TABLE sessoes, fornecedores_produtos, fornecedores_categorias,
             itens_lista, listas, usuarios, produtos, fornecedores,
             categorias, produto_classes RESTART IDENTITY CASCADE;

INSERT INTO categorias (id, nome, descricao) VALUES
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

INSERT INTO fornecedores (id, nome, cnpj, ativo) VALUES
  (1, 'Carrefour', '99.000.111/0001-22', true),
  (2, 'Extra', '00.111.222/0001-33', true),
  (3, 'Pão de Açúcar', '66.777.888/0001-99', true),
  (4, 'Magazine Luiza', '77.888.999/0001-00', true),
  (5, 'Casas Bahia', '88.999.000/0001-11', true),
  (6, 'Leroy Merlin', '11.222.333/0001-44', true),
  (7, 'Etna', '22.333.444/0001-55', true),
  (8, 'C&A', '33.444.555/0001-66', true),
  (9, 'Renner', '44.555.666/0001-77', true),
  (10, 'Hering', '55.666.777/0001-88', true);

INSERT INTO fornecedores_categorias (fornecedor_id, categoria_id) VALUES
  (1, 1), (1, 2), (1, 3), (1, 5), (1, 11), (1, 4),
  (2, 1), (2, 2), (2, 11),
  (3, 1),
  (4, 11), (4, 4), (4, 6),
  (5, 11), (5, 4), (5, 6),
  (6, 7), (6, 8), (6, 10), (6, 5),
  (7, 5), (7, 6),
  (8, 2), (9, 2), (10, 2);

INSERT INTO produtos (id, nome, unidade, ativo) VALUES
  (1, 'Arroz Tipo 1 5kg', 'un', true),
  (2, 'Feijão Preto 1kg', 'un', true),
  (3, 'Óleo de Soja 900ml', 'un', true),
  (4, 'Café Torrado e Moído 500g', 'un', true),
  (5, 'Açúcar Refinado 1kg', 'un', true),
  (6, 'Leite Integral UHT 1L', 'un', true),
  (7, 'Macarrão Espaguete 500g', 'un', true),
  (8, 'Molho de Tomate 340g', 'un', true),
  (9, 'Farinha de Trigo 1kg', 'un', true),
  (10, 'Ovos Brancos (dúzia)', 'dz', true),
  (11, 'Detergente Neutro 500ml', 'un', true),
  (12, 'Papel Toalha 2 rolos', 'un', true),
  (13, 'Liquidificador 2 Velocidades', 'un', true),
  (14, 'Notebook i5 8GB', 'un', true),
  (15, 'Martelo de Unha 25mm', 'un', true),
  (16, 'Parafuso Philips 5mm (cx)', 'cx', true),
  (17, 'Camiseta Algodão M', 'un', true),
  (18, 'Calça Jeans 40', 'un', true),
  (19, 'Vaso de Barro 20cm', 'un', true),
  (20, 'Cadeira de Escritório', 'un', true);

INSERT INTO produto_classes (id, classe_nome, termos_busca, marcas_referencia, categoria_macro, ativo) VALUES
  (1, 'Arroz', '["arroz", "arroz tipo 1"]', '["Camil", "Tio João"]', 'Mercado', true),
  (2, 'Feijão', '["feijão", "feijão preto"]', '["Camil", "Kicaldo"]', 'Mercado', true),
  (3, 'Óleo', '["óleo", "óleo de soja"]', '["Liza", "Soya"]', 'Mercado', true);

INSERT INTO fornecedores_produtos (fornecedor_id, produto_id, preco, estoque, ativo) VALUES
  (1, 1, 25.51, 9999, true), (1, 2, 8.29, 9999, true), (1, 3, 7.03, 9999, true),
  (1, 4, 17.56, 9999, true), (1, 5, 4.30, 9999, true), (1, 6, 4.90, 9999, true),
  (1, 7, 4.65, 9999, true), (1, 8, 3.88, 9999, true), (1, 9, 5.59, 9999, true),
  (1, 10, 10.06, 9999, true), (1, 11, 2.88, 9999, true), (1, 12, 6.29, 9999, true),
  (1, 13, 124.82, 9999, true), (1, 14, 2834.51, 9999, true), (1, 17, 40.29, 9999, true),
  (1, 18, 117.92, 9999, true),
  (2, 1, 24.78, 9999, true), (2, 2, 7.70, 9999, true), (2, 3, 6.31, 9999, true),
  (2, 5, 4.02, 9999, true), (2, 6, 4.79, 9999, true), (2, 7, 4.59, 9999, true),
  (2, 8, 3.71, 9999, true), (2, 9, 5.11, 9999, true), (2, 10, 8.98, 9999, true),
  (2, 11, 2.62, 9999, true), (2, 12, 5.99, 9999, true), (2, 13, 123.01, 9999, true),
  (2, 17, 36.03, 9999, true),
  (3, 1, 28.93, 9999, true), (3, 2, 9.07, 9999, true), (3, 3, 7.75, 9999, true),
  (3, 4, 20.21, 9999, true), (3, 5, 5.16, 9999, true), (3, 6, 5.94, 9999, true),
  (3, 7, 5.45, 9999, true), (3, 8, 4.33, 9999, true), (3, 9, 6.10, 9999, true),
  (3, 10, 11.23, 9999, true), (3, 11, 3.38, 9999, true), (3, 12, 7.63, 9999, true),
  (4, 13, 120.96, 9999, true), (4, 14, 2733.93, 9999, true), (4, 20, 419.69, 9999, true),
  (5, 13, 138.18, 9999, true), (5, 14, 3133.90, 9999, true), (5, 20, 482.52, 9999, true),
  (6, 15, 31.01, 9999, true), (6, 16, 11.83, 9999, true), (6, 19, 45.80, 9999, true),
  (6, 20, 440.51, 9999, true),
  (7, 19, 49.45, 9999, true), (7, 20, 480.18, 9999, true),
  (8, 17, 37.02, 9999, true), (8, 18, 110.61, 9999, true),
  (9, 17, 39.64, 9999, true), (9, 18, 122.28, 9999, true),
  (10, 17, 42.71, 9999, true);
"""


@pytest.fixture
async def test_app():
    """App FastAPI para testes de integração (engine dedicado por teste).
    Cada teste cria tabelas se necessário, carrega seed, executa em
    transação com SAVEPOINT/ROLLBACK para isolamento."""
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

    # Cria tabelas e extensão se ainda não existirem
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

    # Carrega seed data (tabelas criadas acima, vazias após rollback do teste anterior)
    if _SEED_SQL:
        async with test_engine.begin() as conn:
            for statement in _SEED_SQL.split(";"):
                stmt = statement.strip()
                lines = [line for line in stmt.split("\n") if not line.strip().startswith("--")]
                stmt = "\n".join(lines).strip()
                if stmt:
                    await conn.execute(text(stmt))

    app.state.test_async_session_local = test_async_session_local
    app.state.test_engine = test_engine

    yield app

    await test_engine.dispose()
    await asyncio.sleep(0.1)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def db_transaction(test_app):
    """Cada teste roda em transação com SAVEPOINT/ROLLBACK (isolamento)."""
    async with test_app.state.test_engine.begin() as conn:
        await conn.execute(text("SAVEPOINT test_start"))
        yield
        await conn.execute(text("ROLLBACK TO SAVEPOINT test_start"))


@pytest.fixture
async def client(test_app):
    """Cliente HTTP assíncrono para testes"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user(client):
    """Usuário de teste para autenticação (criado via API, rolback após teste)."""
    payload = {
        "nome_usuario": "testuser",
        "email": "testuser@teste.com",
        "nome": "Test User",
        "senha": "TestSenha@123",
        "confirmar_senha": "TestSenha@123",
        "pergunta_seguranca": "Nome do primeiro animal?",
        "resposta_seguranca": "Rex",
    }
    resp = await client.post("/auth/cadastrar", json=payload)
    assert resp.status_code == 201, f"Falha ao criar usuário de teste: {resp.text}"
    return {
        "username": payload["nome_usuario"],
        "password": payload["senha"],
        "email": payload["email"],
        "nome": payload["nome"],
    }


@pytest.fixture
async def auth_headers(client, test_user):
    """Headers de autenticação (Bearer token) para endpoints protegidos."""
    resp = await client.post(
        "/auth/login",
        json={"nome_usuario": test_user["username"], "senha": test_user["password"]},
    )
    assert resp.status_code == 200, f"Falha ao fazer login: {resp.text}"
    data = resp.json()
    return {"Authorization": f"Bearer {data['access_token']}"}


@pytest.fixture
async def sample_produtos(test_app):
    """Lista de produtos disponíveis (do seed) para testes de lista."""
    async with test_app.state.test_engine.begin() as conn:
        from sqlalchemy import select, text
        result = await conn.execute(text("SELECT id FROM produtos ORDER BY id LIMIT 10"))
        ids = [row[0] for row in result.fetchall()]

    class _Produto:
        def __init__(self, pid):
            self.id = pid

    return [_Produto(pid) for pid in ids]


@pytest.fixture
async def lista_com_itens(client, auth_headers, sample_produtos):
    """Lista criada com itens para testes de comparação."""
    payload = {
        "nome": "Lista de Teste",
        "categorias": [1],
        "itens": [
            {"produto_id": sample_produtos[0].id, "quantidade": 2},
            {"produto_id": sample_produtos[1].id, "quantidade": 1},
        ],
    }
    resp = await client.post("/listas", headers=auth_headers, json=payload)
    assert resp.status_code == 201, f"Falha ao criar lista: {resp.text}"
    return resp.json()


