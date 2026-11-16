# COBECO Backend — VisualizarPerfilUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import VisualizarPerfilUseCase, DomainError
from src.domain.entities import Usuario, Email, SenhaHash


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.buscar_por_id = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return VisualizarPerfilUseCase(mock_repo)


@pytest.fixture
def usuario_exemplo():
    return Usuario(
        id=1,
        nome_usuario="usuarioteste",
        email=Email("teste@exemplo.com"),
        nome="Usuário Teste",
        senha_hash=SenhaHash("$2b$12$hash"),
        pergunta_seguranca="nome_mae",
        resposta_seguranca_hash=SenhaHash("$2b$12$hash"),
    )


class TestVisualizarPerfilUseCase:
    """Testes para VisualizarPerfilUseCase (UC18/RF05)"""

    @pytest.mark.asyncio
    async def test_executar_usuario_existente(self, usecase, mock_repo, usuario_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)

        result = await usecase.executar(usuario_id=1)

        assert result is usuario_exemplo
        assert result.id == 1
        assert result.nome_usuario == "usuarioteste"
        assert result.email.valor == "teste@exemplo.com"
        assert result.nome == "Usuário Teste"

        mock_repo.buscar_por_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_executar_usuario_nao_encontrado(self, usecase, mock_repo):
        mock_repo.buscar_por_id = AsyncMock(return_value=None)

        with pytest.raises(DomainError, match="Usuário não encontrado"):
            await usecase.executar(usuario_id=999)

    @pytest.mark.asyncio
    async def test_executar_usuario_soft_deleted(self, usecase, mock_repo, usuario_exemplo):
        usuario_exemplo.soft_delete()
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)

        # O use case não verifica soft_delete, apenas retorna o usuário
        result = await usecase.executar(usuario_id=1)
        assert result.deletado_em is not None