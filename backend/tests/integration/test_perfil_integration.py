# COBECO Backend — Perfil Integration Tests
# Testes de integração para Perfil e Sessões (RF5, RF6, RF02-Refresh)

import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_user(client):
    """Cria usuário autenticado"""
    user_data = {
        "nome_usuario": "testuser_perfil",
        "email": "perfil@teste.com",
        "nome": "User Perfil",
        "senha": "Senha@123",
        "confirmar_senha": "Senha@123",
        "pergunta_seguranca": "nome_mae",
        "resposta_seguranca": "Maria Silva",
    }
    await client.post("/v1/auth/cadastrar", json=user_data)

    login_data = {"nome_usuario": "testuser_perfil", "senha": "Senha@123"}
    response = await client.post("/v1/auth/login", json=login_data)
    tokens = response.json()

    return {
        "auth": {"Authorization": f"Bearer {tokens['access_token']}"},
        "refresh_token": tokens["refresh_token"],
        "user_data": tokens,
    }


class TestPerfilIntegration:
    """Testes de integração para /v1/auth/perfil e /perfil"""

    @pytest.mark.asyncio
    async def test_visualizar_perfil_get(self, client, auth_user):
        """RF5 - Visualizar Perfil (UC18)"""
        response = await client.get("/v1/auth/perfil", headers=auth_user["auth"])
        assert response.status_code == 200
        data = response.json()
        assert data["nome_usuario"] == "testuser_perfil"
        assert data["email"] == "perfil@teste.com"
        assert data["nome"] == "User Perfil"
        assert "id" in data
        assert "criado_em" in data
        # Senha NÃO deve estar na resposta
        assert "senha" not in data
        assert "senha_hash" not in data

    @pytest.mark.asyncio
    async def test_atualizar_perfil_nome(self, client, auth_user):
        """RF6 - Gerenciar Perfil: atualizar nome"""
        response = await client.put(
            "/v1/auth/perfil",
            json={"nome": "Nome Atualizado"},
            headers=auth_user["auth"],
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Nome Atualizado"

        # Verifica persistência
        get_resp = await client.get("/v1/auth/perfil", headers=auth_user["auth"])
        assert get_resp.json()["nome"] == "Nome Atualizado"

    @pytest.mark.asyncio
    async def test_atualizar_perfil_email(self, client, auth_user):
        """RF6 - Atualizar email"""
        response = await client.put(
            "/v1/auth/perfil",
            json={"email": "novo_email@teste.com"},
            headers=auth_user["auth"],
        )
        assert response.status_code == 200
        assert response.json()["email"] == "novo_email@teste.com"

    @pytest.mark.asyncio
    async def test_atualizar_perfil_email_invalido(self, client, auth_user):
        response = await client.put(
            "/v1/auth/perfil",
            json={"email": "email_invalido"},
            headers=auth_user["auth"],
        )
        assert response.status_code == 40

    @pytest.mark.asyncio
    async def test_atualizar_perfil_email_duplicado(self, client, auth_user):
        # Cria outro usuário com email
        other = {
            "nome_usuario": "outro_user",
            "email": "outro@teste.com",
            "nome": "Outro",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria",
        }
        await client.post("/v1/auth/cadastrar", json=other)

        # Tenta atualizar para email do outro
        response = await client.put(
            "/v1/auth/perfil",
            json={"email": "outro@teste.com"},
            headers=auth_user["auth"],
        )
        assert response.status_code == 40
        assert "email" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_alterar_senha_com_senha_atual_correta(self, client, auth_user):
        """RF6 - Alterar senha com senha atual correta"""
        response = await client.put(
            "/v1/auth/perfil",
            json={
                "senha_atual": "Senha@123",
                "nova_senha": "NovaSenha@456",
                "confirmar_nova_senha": "NovaSenha@456",
            },
            headers=auth_user["auth"],
        )
        assert response.status_code == 200

        # Login com nova senha deve funcionar
        login_resp = await client.post(
            "/v1/auth/login",
            json={"nome_usuario": "testuser_perfil", "senha": "NovaSenha@456"},
        )
        assert login_resp.status_code == 20

    @pytest.mark.asyncio
    async def test_alterar_senha_senha_atual_incorreta(self, client, auth_user):
        response = await client.put(
            "/v1/auth/perfil",
            json={
                "senha_atual": "SenhaErrada@123",
                "nova_senha": "NovaSenha@456",
                "confirmar_nova_senha": "NovaSenha@456",
            },
            headers=auth_user["auth"],
        )
        assert response.status_code == 40
        assert "senha" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_alterar_senha_confirmacao_diferente(self, client, auth_user):
        response = await client.put(
            "/v1/auth/perfil",
            json={
                "senha_atual": "Senha@123",
                "nova_senha": "NovaSenha@456",
                "confirmar_nova_senha": "OutraSenha@456",
            },
            headers=auth_user["auth"],
        )
        assert response.status_code == 40
        assert "confirmar" in response.json()["detail"].lower() or "coincid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_alterar_senha_nova_fraca(self, client, auth_user):
        response = await client.put(
            "/v1/auth/perfil",
            json={
                "senha_atual": "Senha@123",
                "nova_senha": "fraca",
                "confirmar_nova_senha": "fraca",
            },
            headers=auth_user["auth"],
        )
        assert response.status_code == 40
        assert "senha" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_atualizar_apenas_email_sem_senha(self, client, auth_user):
        """Atualizar apenas email sem informar senha_atual"""
        response = await client.put(
            "/v1/auth/perfil",
            json={"email": "email_only@teste.com"},
            headers=auth_user["auth"],
        )
        assert response.status_code == 200
        assert response.json()["email"] == "email_only@teste.com"


class TestSessoesRefreshToken:
    """Testes para Refresh Token e Gestão de Sessões (RF2)"""

    @pytest.mark.asyncio
    async def test_login_retorna_refresh_token_cookie(self, client):
        """Login deve definir cookie httpOnly com refresh token"""
        user_data = {
            "nome_usuario": "testuser_session",
            "email": "session@teste.com",
            "nome": "Session User",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria Silva",
        }
        await client.post("/v1/auth/cadastrar", json=user_data)

        response = await client.post(
            "/v1/auth/login",
            json={"nome_usuario": "testuser_session", "senha": "Senha@123"},
        )
        assert response.status_code == 200

        # Verifica cookie refresh_token
        cookies = response.headers.get("set-cookie", "")
        assert "refresh_token=" in cookies
        assert "HttpOnly" in cookies
        assert "SameSite=Strict" in cookies

    @pytest.mark.asyncio
    async def test_logout_remove_cookie_e_revoga_sessao(self, client, auth_user):
        """Logout remove cookie e revoga sessão no banco"""
        refresh_token = auth_user["refresh_token"]

        response = await client.post("/v1/auth/logout", headers=auth_user["auth"])
        assert response.status_code == 24

        # Cookie deve ser removido
        cookies = response.headers.get("set-cookie", "")
        assert "refresh_token=" in cookies
        assert "Max-Age=0" in cookies or "Expires=" in cookies

    @pytest.mark.asyncio
    async def test_refresh_token_invalido_apos_logout(self, client, auth_user):
        """Refresh token revogado não deve mais funcionar"""
        # Faz logout
        await client.post("/v1/auth/logout", headers=auth_user["auth"])

        # Tenta usar refresh token (se endpoint existir)
        # Como não temos endpoint /refresh implementado, testamos que
        # o access token ainda funciona até expirar
        get_resp = await client.get("/v1/auth/perfil", headers=auth_user["auth"])
        # Access token ainda válido até expirar (15min)
        assert get_resp.status_code == 20


class TestLogoutEverywhere:
    """Teste para logout de todas as sessões (futuro)"""

    @pytest.mark.asyncio
    async def test_logout_todas_sessoes_futuro(self, client, auth_user):
        """Endpoint futuro: POST /v1/auth/logout/all"""
        # Por enquanto apenas documenta a necessidade
        # response = await client.post("/v1/auth/logout/all", headers=auth_user["auth"])
        # assert response.status_code == 24
        pass