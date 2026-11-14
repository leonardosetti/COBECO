# COBECO Backend — LoginUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from datetime import timedelta
from src.domain.usecases import (
    LoginUseCase, LoginInput, LoginOutput,
    CredenciaisInvalidas, RateLimitExcedido
)
from src.domain.entities import Usuario, Email, SenhaHash


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.buscar_por_nome_usuario = AsyncMock()
    return repo


@pytest.fixture
def verificar_senha_fn():
    def fn(senha: str, hash: str) -> bool:
        return hash == f"hashed_{senha}"
    return fn


@pytest.fixture
def criar_token_fn():
    def fn(sub: str, expires_delta: timedelta, token_type: str = "access") -> str:
        return f"{token_type}_token_for_{sub}"
    return fn


@pytest.fixture
def rate_limiter_fn():
    async def fn(nome_usuario: str):
        pass  # No rate limiting in tests
    return fn


@pytest.fixture
def usecase(mock_repo, verificar_senha_fn, criar_token_fn, rate_limiter_fn):
    return LoginUseCase(mock_repo, verificar_senha_fn, criar_token_fn, rate_limiter_fn)


class TestLoginUseCase:
    """Testes para LoginUseCase (UC10/RF2)"""

    @pytest.mark.asyncio
    async def test_executar_sucesso(self, usecase, mock_repo, criar_token_fn):
        usuario = Usuario(
            id=1,
            nome_usuario="usuario_teste",
            email=Email("teste@exemplo.com"),
            nome="Usuário Teste",
            senha_hash=SenhaHash("hashed_Senha@123"),
            pergunta_seguranca="nome_mae",
            resposta_seguranca_hash=SenhaHash("hashed_Maria"),
        )
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

        input_data = LoginInput(
            nome_usuario="usuario_teste",
            senha="Senha@123",
        )

        result = await usecase.executar(input_data)

        assert isinstance(result, LoginOutput)
        assert result.access_token == "access_token_for_1"
        assert result.refresh_token == "refresh_token_for_1"
        assert result.token_type == "bearer"
        assert result.expires_in == 90  # 15 min * 60
        assert result.usuario_id == 1

    @pytest.mark.asyncio
    async def test_executar_usuario_nao_encontrado(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=None)

        input_data = LoginInput(
            nome_usuario="inexistente",
            senha="Senha@123",
        )

        with pytest.raises(CredenciaisInvalidas):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_usuario_inativo(self, usecase, mock_repo):
        usuario = Usuario(
            id=1,
            nome_usuario="usuario_teste",
            email=Email("teste@exemplo.com"),
            nome="Usuário Teste",
            senha_hash=SenhaHash("hashed_Senha@123"),
        )
        usuario.soft_delete()  # Marca como inativo
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

        input_data = LoginInput(
            nome_usuario="usuario_teste",
            senha="Senha@123",
        )

        with pytest.raises(CredenciaisInvalidas):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_senha_incorreta(self, usecase, mock_repo):
        usuario = Usuario(
            id=1,
            nome_usuario="usuario_teste",
            email=Email("teste@exemplo.com"),
            nome="Usuário Teste",
            senha_hash=SenhaHash("hashed_Senha@123"),
        )
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

        input_data = LoginInput(
            nome_usuario="usuario_teste",
            senha="SenhaErrada@123",
        )

        with pytest.raises(CredenciaisInvalidas):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_rate_limit_excedido(self, usecase, mock_repo, rate_limiter_fn):
        async def rate_limiter_block(nome_usuario: str):
            raise RateLimitExcedido(15)

        usecase_blocked = LoginUseCase(
            mock_repo,
            lambda s, h: True,
            lambda sub, exp, tp="access": "token",
            rate_limiter_block,
        )

        input_data = LoginInput(
            nome_usuario="usuario_teste",
            senha="Senha@123",
        )

        with pytest.raises(RateLimitExcedido, match="15"):
            await usecase_blocked.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_tokens_tipos_corretos(self, usecase, mock_repo):
        usuario = Usuario(
            id=42,
            nome_usuario="usuario_teste",
            email=Email("teste@exemplo.com"),
            nome="Usuário Teste",
            senha_hash=SenhaHash("hashed_Senha@123"),
        )
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

        input_data = LoginInput(
            nome_usuario="usuario_teste",
            senha="Senha@123",
        )

        result = await usecase.executar(input_data)

        assert result.access_token.startswith("access_token_for_")
        assert result.refresh_token.startswith("refresh_token_for_")
        assert "42" in result.access_token
        assert "42" in result.refresh_token