# COBECO Backend — RecuperarSenhaUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.domain.usecases import (
    RecuperarSenhaUseCase, CredenciaisInvalidas
)
from src.domain.entities import Usuario, Email, SenhaHash
from src.config import settings


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.buscar_por_nome_usuario = AsyncMock()
    repo.atualizar = AsyncMock()
    return repo


@pytest.fixture
def hash_senha_fn():
    def fn(senha: str) -> str:
        return f"hashed_{senha}"
    return fn


@pytest.fixture
def rate_limiter_fn():
    async def fn(nome_usuario: str):
        pass
    return fn


@pytest.fixture
def verificar_senha_fn():
    def fn(senha: str, hash_valor: str) -> bool:
        return hash_valor == f"hashed_{senha}"
    return fn


@pytest.fixture
def usecase(mock_repo, hash_senha_fn, verificar_senha_fn, rate_limiter_fn):
    return RecuperarSenhaUseCase(mock_repo, hash_senha_fn, verificar_senha_fn, rate_limiter_fn)


class TestRecuperarSenhaUseCase:
    """Testes para RecuperarSenhaUseCase (UC12/RF4)"""

    @pytest.mark.asyncio
    async def test_solicitar_reset_usuario_existente_modo_email(self, usecase, mock_repo):
        # Configura modo email (padrão)
        original_mode = settings.RECOVERY_MODE
        settings.RECOVERY_MODE = "email"
        
        try:
            usuario = Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
            mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

            token = await usecase.solicitar_reset("usuarioteste")

            # Em modo email, não retorna token (deve enviar por email)
            assert token is None
            mock_repo.buscar_por_nome_usuario.assert_called_once_with("usuarioteste")
        finally:
            settings.RECOVERY_MODE = original_mode

    @pytest.mark.asyncio
    async def test_solicitar_reset_usuario_existente_modo_log(self, usecase, mock_repo):
        # Configura modo log (desenvolvimento)
        original_mode = settings.RECOVERY_MODE
        settings.RECOVERY_MODE = "log"
        
        try:
            usuario = Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
            mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

            token = await usecase.solicitar_reset("usuarioteste")

            # Em modo log, retorna token
            assert token is not None
            assert len(token) > 20  # token_urlsafe(32) gera ~43 chars
            mock_repo.buscar_por_nome_usuario.assert_called_once_with("usuarioteste")
        finally:
            settings.RECOVERY_MODE = original_mode

    @pytest.mark.asyncio
    async def test_solicitar_reset_usuario_inexistente(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=None)

        token = await usecase.solicitar_reset("inexistente")

        # Sempre retorna None para não revelar existência
        assert token is None
        mock_repo.buscar_por_nome_usuario.assert_called_once_with("inexistente")

    @pytest.mark.asyncio
    async def test_confirmar_reset_modo_log_token_valido(self, usecase, mock_repo):
        original_mode = settings.RECOVERY_MODE
        settings.RECOVERY_MODE = "log"
        
        try:
            usuario = Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
            mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)
            mock_repo.atualizar = AsyncMock(return_value=usuario)

            # Em modo log, aceita qualquer token (dev)
            result = await usecase.confirmar_reset(
                "usuarioteste",
                "qualquer_token",
                "NovaSenha@456",
            )

            assert result.id == 1
            # hash_senha_fn returns string, not SenhaHash object
            assert result.senha_hash == "hashed_NovaSenha@456"
            mock_repo.atualizar.assert_called_once()
        finally:
            settings.RECOVERY_MODE = original_mode

    @pytest.mark.asyncio
    async def test_confirmar_reset_modo_email_resposta_correta(self, usecase, mock_repo):
        original_mode = settings.RECOVERY_MODE
        settings.RECOVERY_MODE = "email"
        
        try:
            usuario = Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
            mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)
            mock_repo.atualizar = AsyncMock(return_value=usuario)

            result = await usecase.confirmar_reset(
                "usuarioteste",
                "Maria",  # resposta de segurança
                "NovaSenha@456",
            )

            assert result.id == 1
            # hash_senha_fn returns string, not SenhaHash object
            assert result.senha_hash == "hashed_NovaSenha@456"
        finally:
            settings.RECOVERY_MODE = original_mode

    @pytest.mark.asyncio
    async def test_confirmar_reset_resposta_incorreta(self, usecase, mock_repo):
        original_mode = settings.RECOVERY_MODE
        settings.RECOVERY_MODE = "email"
        
        try:
            usuario = Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
            mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=usuario)

            with pytest.raises(CredenciaisInvalidas):
                await usecase.confirmar_reset(
                    "usuarioteste",
                    "Resposta Errada",
                    "NovaSenha@456",
                )
        finally:
            settings.RECOVERY_MODE = original_mode

    @pytest.mark.asyncio
    async def test_confirmar_reset_usuario_inexistente(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=None)

        with pytest.raises(CredenciaisInvalidas):
            await usecase.confirmar_reset(
                "inexistente",
                "qualquer_coisa",
                "NovaSenha@456",
            )