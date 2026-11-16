# COBECO Backend — ExcluirListaUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import ExcluirListaUseCase, ListaNaoEncontrada
from src.domain.entities import Lista
from datetime import datetime


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.soft_delete = AsyncMock()
    repo.buscar_por_id = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return ExcluirListaUseCase(mock_repo)


@pytest.fixture
def lista_exemplo():
    return Lista(
        id=1,
        usuario_id=1,
        nome="Lista para Excluir",
        itens=[],
        criado_em=datetime(2026, 11, 10, 10, 0),
        atualizado_em=datetime(2026, 11, 10, 10, 0),
    )


class TestExcluirListaUseCase:
    """Testes para ExcluirListaUseCase (UC13/RF11)"""

    @pytest.mark.asyncio
    async def test_executar_sucesso(self, usecase, mock_repo, lista_exemplo):
        # O use case delega para o repo.soft_delete que modifica o modelo
        # Simulamos o comportamento real: repo.buscar_por_id retorna a lista,
        # e soft_delete retorna True
        mock_repo.buscar_por_id = AsyncMock(return_value=lista_exemplo)
        mock_repo.soft_delete = AsyncMock(return_value=True)

        result = await usecase.executar(lista_id=1, usuario_id=1, confirmacao_nome="Lista para Excluir")

        assert result is True
        mock_repo.soft_delete.assert_called_once_with(1, 1, "Lista para Excluir")

    @pytest.mark.asyncio
    async def test_executar_confirmacao_incorreta(self, usecase, mock_repo, lista_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=lista_exemplo)
        mock_repo.soft_delete = AsyncMock(return_value=False)

        result = await usecase.executar(lista_id=1, usuario_id=1, confirmacao_nome="Nome Errado")

        assert result is False
        assert lista_exemplo.deletado_em is None

    @pytest.mark.asyncio
    async def test_executar_lista_nao_encontrada(self, usecase, mock_repo):
        mock_repo.buscar_por_id = AsyncMock(return_value=None)
        mock_repo.soft_delete = AsyncMock(return_value=False)

        result = await usecase.executar(lista_id=999, usuario_id=1, confirmacao_nome="Inexistente")

        assert result is False

    @pytest.mark.asyncio
    async def test_executar_lista_outro_usuario(self, usecase, mock_repo):
        mock_repo.buscar_por_id = AsyncMock(return_value=None)
        mock_repo.soft_delete = AsyncMock(return_value=False)

        result = await usecase.executar(lista_id=1, usuario_id=999, confirmacao_nome="Nome")

        assert result is False

    @pytest.mark.asyncio
    async def test_executar_lista_ja_excluida(self, usecase, mock_repo, lista_exemplo):
        lista_exemplo.soft_delete("Lista para Excluir")
        mock_repo.buscar_por_id = AsyncMock(return_value=lista_exemplo)
        mock_repo.soft_delete = AsyncMock(return_value=False)

        result = await usecase.executar(lista_id=1, usuario_id=1, confirmacao_nome="Lista para Excluir")

        assert result is False