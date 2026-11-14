# COBECO Backend — Integration Tests: Auth Flow
# Testes de integração para fluxo completo de autenticação

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy import text
from pathlib import Path

from src.main import app
from src.adapters.db.database import get_db, init_db, close_db
from src.adapters.db.models import Base
from src.config import settings


# ============================================================
# Fixtures
# ============================================================
@pytest.fixture(scope="function")
async def test_app():
    """App FastAPI para testes de integração"""
    # Cria engine e session factory específicos para testes (no event loop do teste)
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
    
    # Inicializa tabelas
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Carrega seed data
    seed_path = Path("/app/seed.sql")
    if seed_path.exists():
        seed_sql = seed_path.read_text()
        async with test_engine.begin() as conn:
            # Split by semicolon and execute each non-empty, non-comment statement
            for statement in seed_sql.split(';'):
                stmt = statement.strip()
                # Remove comment lines
                lines = [line for line in stmt.split('\n') if not line.strip().startswith('--')]
                stmt = '\n'.join(lines).strip()
                if stmt:
                    await conn.execute(text(stmt))
    
    # Store test session factory on app state for other fixtures
    app.state.test_async_session_local = test_async_session_local
    app.state.test_engine = test_engine
    
    yield app
    
    # Cleanup — não derruba o schema: o banco é compartilhado com a app local
    # (dados são limpos pelo seed.sql na próxima execução)
    await test_engine.dispose()
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


@pytest.fixture(autouse=True)
async def setup_user(client):
    """Cria usuário base (testuser) usado pelos fixtures de auth"""
    await client.post("/auth/cadastrar", json={
        "nome_usuario": "testuser",
        "email": "test@teste.com",
        "nome": "Test User",
        "senha": "Senha@123",
        "confirmar_senha": "Senha@123",
        "pergunta_seguranca": "Pet name?",
        "resposta_seguranca": "Fluffy"
    })
    yield


@pytest.fixture
async def auth_headers(client):
    """Faz login e retorna headers de autorização"""
    login_resp = await client.post("/auth/login", json={
        "nome_usuario": "testuser",
        "senha": "Senha@123"
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def db_session(test_app):
    """Sessão DB para setup/teardown direto"""
    async with test_app.state.test_async_session_local() as session:
        yield session


# ============================================================
# Testes: Cadastro (UC09/RF01)
# ============================================================
class TestCadastroUsuario:
    """UC09 — Cadastrar Usuário"""

    @pytest.mark.asyncio
    async def test_cadastrar_usuario_sucesso(self, client):
        """HP1: Cadastro com dados válidos retorna 201"""
        payload = {
            "nome_usuario": "joaosilva",
            "email": "joao@teste.com",
            "nome": "João Silva",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "Nome do primeiro animal?",
            "resposta_seguranca": "Rex"
        }
        
        response = await client.post("/auth/cadastrar", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert "usuario_id" in data
        assert data["message"] == "Conta criada com sucesso"

    @pytest.mark.asyncio
    async def test_cadastrar_usuario_duplicado_nome_usuario(self, client):
        """E1: nome_usuario já existe retorna 400 com mensagem genérica"""
        payload = {
            "nome_usuario": "maria",
            "email": "maria1@teste.com",
            "nome": "Maria Santos",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "Cor favorita?",
            "resposta_seguranca": "Azul"
        }
        
        # Primeiro cadastro
        await client.post("/auth/cadastrar", json=payload)
        
        # Segundo cadastro com mesmo nome_usuario
        payload["email"] = "maria2@teste.com"
        response = await client.post("/auth/cadastrar", json=payload)
        
        assert response.status_code == 400
        assert "Credenciais inválidas" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_cadastrar_usuario_senha_fraca(self, client):
        """E2: Senha fraca retorna 422 (validação Pydantic)"""
        payload = {
            "nome_usuario": "pedro",
            "email": "pedro@teste.com",
            "nome": "Pedro Oliveira",
            "senha": "123",  # Muito curta, sem maiúscula, sem especial
            "confirmar_senha": "123",
            "pergunta_seguranca": "Cidade natal?",
            "resposta_seguranca": "SP"
        }
        
        response = await client.post("/auth/cadastrar", json=payload)
        
        assert response.status_code == 422  # Pydantic validation error

    @pytest.mark.asyncio
    async def test_cadastrar_usuario_senhas_diferentes(self, client):
        """E4: Confirmação diferente retorna 400"""
        payload = {
            "nome_usuario": "ana",
            "email": "ana@teste.com",
            "nome": "Ana Costa",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@456",  # Diferente
            "pergunta_seguranca": "Time do coração?",
            "resposta_seguranca": "Corinthians"
        }
        
        response = await client.post("/auth/cadastrar", json=payload)
        
        assert response.status_code == 400
        assert "não coincidem" in response.json()["detail"].lower()


# ============================================================
# Testes: Login (UC10/RF02)
# ============================================================
class TestLogin:
    """UC10 — Realizar Login"""

    @pytest.mark.asyncio
    async def test_login_sucesso(self, client):
        """HP1: Login com credenciais válidas retorna tokens"""
        response = await client.post("/auth/login", json={
            "nome_usuario": "testuser",
            "senha": "Senha@123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 900  # 15 min * 60
        
        # Verifica cookie httpOnly
        assert "refresh_token" in response.cookies

    @pytest.mark.asyncio
    async def test_login_credenciais_invalidas(self, client):
        """E2: Credenciais inválidas retorna 401 genérico"""
        response = await client.post("/auth/login", json={
            "nome_usuario": "testuser",
            "senha": "SenhaErrada@123"
        })
        
        assert response.status_code == 401
        assert "Credenciais inválidas" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_usuario_inexistente(self, client):
        """E2: Usuário inexistente retorna 401 genérico (não revela existência)"""
        response = await client.post("/auth/login", json={
            "nome_usuario": "naoexiste",
            "senha": "Senha@123"
        })
        
        assert response.status_code == 401
        assert "Credenciais inválidas" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_rate_limiting(self, client):
        """E1: 6 tentativas falhas → lockout 15min (429)"""
        # Faz 5 tentativas (ainda permite)
        for i in range(5):
            response = await client.post("/auth/login", json={
                "nome_usuario": "testuser",
                "senha": f"Errada{i}"
            })
            assert response.status_code == 401
        
        # 6ª tentativa → 429
        response = await client.post("/auth/login", json={
            "nome_usuario": "testuser",
            "senha": "Errada6"
        })
        
        assert response.status_code == 429
        assert "Tente novamente em" in response.json()["detail"]


# ============================================================
# Testes: Logout (UC11/RF03)
# ============================================================
class TestLogout:
    """UC11 — Realizar Logout"""

    @pytest.mark.asyncio
    async def test_logout_invalida_cookie(self, client):
        """HP1: Logout remove cookie refresh_token"""
        # Login primeiro
        login_resp = await client.post("/auth/login", json={
            "nome_usuario": "testuser",
            "senha": "Senha@123"
        })
        assert login_resp.status_code == 200
        
        # Logout
        response = await client.post("/auth/logout", cookies=login_resp.cookies)
        
        assert response.status_code == 204
        # Cookie deve ser deletado
        assert "refresh_token" not in response.cookies or response.cookies.get("refresh_token") == ""


# ============================================================
# Testes: Recuperar Senha (UC12/RF04)
# ============================================================
class TestRecuperarSenha:
    """UC12 — Recuperar Senha"""

    @pytest.mark.asyncio
    async def test_recuperar_senha_modo_log(self, client):
        """HP2: Modo log retorna token no stdout (não na resposta)"""
        response = await client.post("/auth/recuperar-senha/solicitar", json={
            "nome_usuario": "testuser"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "logado no servidor" in data["message"]
        # Token NÃO vem na resposta (segurança)

    @pytest.mark.asyncio
    async def test_recuperar_senha_usuario_inexistente(self, client):
        """E1: Usuário inexistente retorna sucesso genérico (não revela existência)"""
        response = await client.post("/auth/recuperar-senha/solicitar", json={
            "nome_usuario": "naoexiste"
        })
        
        assert response.status_code == 200
        # Mesma mensagem de sucesso


# ============================================================
# Testes: Perfil (UC18/RF05, UC16/RF06)
# ============================================================
class TestPerfil:
    """UC18 — Visualizar Perfil | UC16 — Gerenciar Perfil"""

    @pytest.mark.asyncio
    async def test_visualizar_perfil(self, client, auth_headers):
        """UC18: Visualizar perfil retorna dados do usuário"""
        response = await client.get("/auth/perfil", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome_usuario"] == "testuser"
        assert data["email"] == "test@teste.com"
        assert data["nome"] == "Test User"
        assert "criado_em" in data

    @pytest.mark.asyncio
    async def test_atualizar_perfil_nome(self, client, auth_headers):
        """UC16: Atualizar nome do perfil"""
        response = await client.put("/auth/perfil", headers=auth_headers, json={
            "nome": "Test User Atualizado"
        })
        
        assert response.status_code == 200
        assert response.json()["nome"] == "Test User Atualizado"

    @pytest.mark.asyncio
    async def test_atualizar_perfil_email_duplicado(self, client, auth_headers):
        """E1: Email duplicado retorna 400"""
        # Cria outro usuário
        await client.post("/auth/cadastrar", json={
            "nome_usuario": "outrouser",
            "email": "outro@teste.com",
            "nome": "Outro User",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "Pet name?",
            "resposta_seguranca": "Dog"
        })
        
        # Tenta atualizar email para o do outro usuário
        response = await client.put("/auth/perfil", headers=auth_headers, json={
            "email": "outro@teste.com"
        })
        
        assert response.status_code == 400
        assert "já cadastrado" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_alterar_senha_sucesso(self, client, auth_headers):
        """UC16: Alterar senha com senha atual correta"""
        response = await client.put("/auth/perfil", headers=auth_headers, json={
            "senha_atual": "Senha@123",
            "nova_senha": "NovaSenha@456",
            "confirmar_nova_senha": "NovaSenha@456"
        })
        
        assert response.status_code == 200
        
        # Verifica que nova senha funciona
        login_resp = await client.post("/auth/login", json={
            "nome_usuario": "testuser",
            "senha": "NovaSenha@456"
        })
        assert login_resp.status_code == 200

    @pytest.mark.asyncio
    async def test_alterar_senha_atual_incorreta(self, client, auth_headers):
        """E2: Senha atual incorreta retorna 400"""
        response = await client.put("/auth/perfil", headers=auth_headers, json={
            "senha_atual": "SenhaErrada",
            "nova_senha": "NovaSenha@456",
            "confirmar_nova_senha": "NovaSenha@456"
        })
        
        assert response.status_code == 400
        assert "incorreta" in response.json()["detail"]


# ============================================================
# Testes: Proteção de Rotas
# ============================================================
class TestAuthProtection:
    """Verifica que rotas protegidas exigem autenticação"""

    @pytest.mark.asyncio
    async def test_rotas_protegidas_sem_token(self, client):
        """Rotas /auth/perfil, /listas, etc exigem token"""
        protected_routes = [
            ("GET", "/auth/perfil"),
            ("GET", "/listas"),
            ("POST", "/listas"),
            ("POST", "/comparacao/calcular"),
        ]
        
        for method, route in protected_routes:
            response = await client.request(method, route)
            assert response.status_code == 401, f"{method} {route} should require auth"

    @pytest.mark.asyncio
    async def test_token_expirado(self, client):
        """Token expirado retorna 401"""
        from jose import jwt
        from datetime import datetime, timedelta, timezone
        
        # Cria token expirado
        expired_token = jwt.encode(
            {"sub": "999", "exp": datetime.now(timezone.utc) - timedelta(hours=1), "type": "access"},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        response = await client.get(
            "/auth/perfil",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
        assert "expirado" in response.json()["detail"]


# ============================================================
# Testes: Listas (UC14/RF08, UC15/RF09, UC13/RF10, RF11)
# ============================================================
class TestListas:
    """Testes de integração para CRUD de listas"""

    @pytest.fixture
    async def sample_products(self, db_session):
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

    @pytest.mark.asyncio
    async def test_salvar_lista_sucesso(self, client, auth_headers, sample_products):
        """UC14/RF08: Salvar lista com itens válidos"""
        payload = {
            "nome": "Compras da Semana",
            "itens": [
                {"produto_id": sample_products[0].id, "quantidade": 2},
                {"produto_id": sample_products[1].id, "quantidade": 1},
            ]
        }
        
        response = await client.post("/listas", headers=auth_headers, json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Compras da Semana"
        assert len(data["itens"]) == 2
        assert "id" in data

    @pytest.mark.asyncio
    async def test_listar_minhas_listas_paginado(self, client, auth_headers, sample_products):
        """UC15/RF09: Listar listas com paginação"""
        # Cria 3 listas
        for i in range(3):
            await client.post("/listas", headers=auth_headers, json={
                "nome": f"Lista {i}",
                "itens": [{"produto_id": sample_products[0].id, "quantidade": 1}]
            })
        
        # Lista primeira página
        response = await client.get("/listas?pagina=1&por_pagina=2", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["pagina"] == 1
        assert data["por_pagina"] == 2
        assert data["total"] == 3
        assert data["total_paginas"] == 2

    @pytest.mark.asyncio
    async def test_buscar_lista_por_id(self, client, auth_headers, sample_products):
        """Buscar lista específica por ID"""
        create_resp = await client.post("/listas", headers=auth_headers, json={
            "nome": "Lista Específica",
            "itens": [{"produto_id": sample_products[0].id, "quantidade": 3}]
        })
        lista_id = create_resp.json()["id"]
        
        response = await client.get(f"/listas/{lista_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == lista_id
        assert data["nome"] == "Lista Específica"

    @pytest.mark.asyncio
    async def test_editar_lista(self, client, auth_headers, sample_products):
        """UC13/RF10: Editar lista salva"""
        create_resp = await client.post("/listas", headers=auth_headers, json={
            "nome": "Lista Original",
            "itens": [{"produto_id": sample_products[0].id, "quantidade": 1}]
        })
        lista_id = create_resp.json()["id"]
        
        response = await client.put(f"/listas/{lista_id}", headers=auth_headers, json={
            "nome": "Lista Editada",
            "itens": [
                {"produto_id": sample_products[0].id, "quantidade": 5},
                {"produto_id": sample_products[1].id, "quantidade": 2}
            ]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Lista Editada"
        assert len(data["itens"]) == 2

    @pytest.mark.asyncio
    async def test_excluir_lista_soft_delete(self, client, auth_headers, sample_products):
        """UC13/RF11: Excluir lista (soft delete com confirmação)"""
        create_resp = await client.post("/listas", headers=auth_headers, json={
            "nome": "Para Excluir",
            "itens": [{"produto_id": sample_products[0].id, "quantidade": 1}]
        })
        lista_id = create_resp.json()["id"]
        
        # Confirmação correta
        response = await client.delete(
            f"/listas/{lista_id}?confirmacao_nome=Para Excluir",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Lista não deve mais aparecer na listagem
        list_resp = await client.get("/listas", headers=auth_headers)
        ids = [l["id"] for l in list_resp.json()["items"]]
        assert lista_id not in ids

    @pytest.mark.asyncio
    async def test_excluir_lista_confirmacao_incorreta(self, client, auth_headers, sample_products):
        """Confirmação incorreta retorna 400"""
        create_resp = await client.post("/listas", headers=auth_headers, json={
            "nome": "Nome Correto",
            "itens": [{"produto_id": sample_products[0].id, "quantidade": 1}]
        })
        lista_id = create_resp.json()["id"]
        
        response = await client.delete(
            f"/listas/{lista_id}?confirmacao_nome=Nome Errado",
            headers=auth_headers
        )
        
        assert response.status_code == 400


# ============================================================
# Testes: Catálogo (UC02, UC03, UC04, UC05)
# ============================================================
class TestCatalogo:
    """Testes de integração para catálogo"""

    @pytest.mark.asyncio
    async def test_listar_categorias(self, client):
        """UC03/RF12: Listar categorias para pré-filtro"""
        response = await client.get("/catalogo/categorias")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 11  # Seed tem 11 categorias
        assert all("id" in c and "nome" in c for c in data)

    @pytest.mark.asyncio
    async def test_listar_fornecedores_filtrado_por_categoria(self, client):
        """UC04/RF13: Fornecedores filtrados por categoria"""
        response = await client.get("/catalogo/fornecedores?categorias=1")  # Mercado
        
        assert response.status_code == 200
        data = response.json()
        # Pão de Açúcar, Carrefour, Extra têm categoria Mercado
        assert len(data) >= 3

    @pytest.mark.asyncio
    async def test_autocomplete_produtos(self, client):
        """UC02/RF07: Autocomplete de produtos (debounce simulado)"""
        response = await client.get("/catalogo/produtos/autocomplete?q=Arroz&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any("Arroz" in p["nome"] for p in data)

    @pytest.mark.asyncio
    async def test_calcular_disponibilidade_fornecedor(self, client):
        """UC04/UC05: Disponibilidade de fornecedor para lista de produtos"""
        # Precisa de produtos existentes
        response = await client.get("/catalogo/fornecedores/1/disponibilidade?produtos=1,2,3")
        
        assert response.status_code == 200
        data = response.json()
        assert "fornecedor" in data
        assert "percentual_disponibilidade" in data
        assert "itens_disponiveis" in data
        assert "itens_totais" in data


# ============================================================
# Testes: Comparação (UC06/RF15, UC07/RF16)
# ============================================================
class TestComparacao:
    """Testes de integração para comparação de preços"""

    @pytest.fixture
    async def lista_com_itens(self, client, auth_headers, db_session):
        """Cria lista com itens para comparação"""
        from src.adapters.db.models import ProdutoModel
        
        # Garante produtos
        produtos = []
        for nome in ["Arroz 5kg", "Feijão 1kg", "Óleo 900ml"]:
            p = ProdutoModel(nome=nome, unidade="un", ativo=True)
            db_session.add(p)
            produtos.append(p)
        await db_session.commit()
        for p in produtos:
            await db_session.refresh(p)
        
        # Cria lista
        response = await client.post("/listas", headers=auth_headers, json={
            "nome": "Para Comparar",
            "itens": [
                {"produto_id": produtos[0].id, "quantidade": 2},
                {"produto_id": produtos[1].id, "quantidade": 1},
                {"produto_id": produtos[2].id, "quantidade": 1},
            ]
        })
        return response.json()

    @pytest.mark.asyncio
    async def test_calcular_orcamento_sucesso(self, client, auth_headers, lista_com_itens):
        """UC06/RF15: Calcular orçamento retorna tabela flat ordenada por preço"""
        response = await client.post("/comparacao/calcular", headers=auth_headers, json={
            "lista_id": lista_com_itens["id"],
            "fornecedor_ids": [1, 6, 9],  # Leroy Merlin, Pão de Açúcar, Carrefour
            "disponibilidade_minima": 0
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["lista_id"] == lista_com_itens["id"]
        assert len(data["fornecedores"]) >= 2
        
        # Verifica ordenação por preço ASC
        precos = [f["preco_total"] for f in data["fornecedores"]]
        assert precos == sorted(precos), "Fornecedores devem estar ordenados por preço ASC"
        
        # Verifica destaque melhor oferta
        melhor = [f for f in data["fornecedores"] if f["eh_melhor"]]
        assert len(melhor) == 1
        assert melhor[0]["fornecedor_id"] == data["melhor_fornecedor_id"]

    @pytest.mark.asyncio
    async def test_calcular_orcamento_fornecedores_insuficientes(self, client, auth_headers, lista_com_itens):
        """Menos de 2 fornecedores retorna 400"""
        response = await client.post("/comparacao/calcular", headers=auth_headers, json={
            "lista_id": lista_com_itens["id"],
            "fornecedor_ids": [1],  # Apenas 1
            "disponibilidade_minima": 0
        })
        
        assert response.status_code == 400
        assert "pelo menos 2" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_filtro_disponibilidade_minima(self, client, auth_headers, lista_com_itens):
        """UC05/RF14: Filtro por disponibilidade mínima"""
        response = await client.post("/comparacao/calcular", headers=auth_headers, json={
            "lista_id": lista_com_itens["id"],
            "fornecedor_ids": [1, 2, 6, 7, 9, 10],
            "disponibilidade_minima": 50  # 50%
        })
        
        assert response.status_code == 200
        data = response.json()
        # Todos fornecedores retornados devem ter >= 50% disponibilidade
        for f in data["fornecedores"]:
            assert f["percentual_disponibilidade"] >= 50


# ============================================================
# Testes: Exportação PDF (UC08/RF17)
# ============================================================
class TestExportacaoPDF:
    """Testes de integração para exportação PDF"""

    @pytest.mark.asyncio
    async def test_exportar_pdf_lista(self, client, auth_headers, db_session):
        """UC08/RF17: Exportar lista em PDF (ReportLab)"""
        from src.adapters.db.models import ProdutoModel
        
        # Cria produtos e lista
        produtos = []
        for nome in ["Arroz 5kg", "Feijão 1kg"]:
            p = ProdutoModel(nome=nome, unidade="un", ativo=True)
            db_session.add(p)
            produtos.append(p)
        await db_session.commit()
        for p in produtos:
            await db_session.refresh(p)
        
        list_resp = await client.post("/listas", headers=auth_headers, json={
            "nome": "Lista para PDF",
            "itens": [
                {"produto_id": produtos[0].id, "quantidade": 2},
                {"produto_id": produtos[1].id, "quantidade": 1},
            ]
        })
        lista_id = list_resp.json()["id"]
        
        # Exporta PDF
        response = await client.post(f"/export/pdf?lista_id={lista_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers["content-disposition"]
        assert "lista_" in response.headers["content-disposition"]
        assert ".pdf" in response.headers["content-disposition"]
        
        # Verifica que é PDF válido (começa com %PDF)
        content = response.content
        assert content.startswith(b"%PDF")


# ============================================================
# Configuração pytest-asyncio
# ============================================================
pytest_plugins = ("pytest_asyncio",)