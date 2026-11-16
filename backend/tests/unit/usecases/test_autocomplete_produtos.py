# COBECO Backend — AutocompleteProdutosUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import AutocompleteProdutosUseCase
from src.domain.entities import Produto, UnidadeMedida


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.autocomplete = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return AutocompleteProdutosUseCase(mock_repo)


@pytest.fixture
def produtos_exemplo():
    return [
        Produto(id=1, nome="Arroz Tipo 1 5kg", unidade=UnidadeMedida.KG, ativo=True),
        Produto(id=2, nome="Arroz Integral 1kg", unidade=UnidadeMedida.KG, ativo=True),
        Produto(id=3, nome="Feijão Preto 1kg", unidade=UnidadeMedida.KG, ativo=True),
    ]


class TestAutocompleteProdutosUseCase:
    """Testes para AutocompleteProdutosUseCase (UC02/RF07)"""

    @pytest.mark.asyncio
    async def test_executar_busca_valida(self, usecase, mock_repo, produtos_exemplo):
        mock_repo.autocomplete = AsyncMock(return_value=produtos_exemplo[:2])

        result = await usecase.executar(query="arroz", limit=10)

        assert len(result) == 2
        assert result[0].nome == "Arroz Tipo 1 5kg"
        assert result[1].nome == "Arroz Integral 1kg"
        mock_repo.autocomplete.assert_called_once_with("arroz", 10)

    @pytest.mark.asyncio
    async def test_executar_busca_curta_retorna_vazio(self, usecase, mock_repo):
        result = await usecase.executar(query="a", limit=10)

        assert result == []
        mock_repo.autocomplete.assert_not_called()

    @pytest.mark.asyncio
    async def test_executar_busca_vazia_retorna_vazio(self, usecase, mock_repo):
        result = await usecase.executar(query="", limit=10)

        assert result == []
        mock_repo.autocomplete.assert_not_called()

    @pytest.mark.asyncio
    async def test_executar_limite_customizado(self, usecase, mock_repo, produtos_exemplo):
        mock_repo.autocomplete = AsyncMock(return_value=produtos_exemplo)

        result = await usecase.executar(query="arroz", limit=5)

        assert len(result) == 3
        mock_repo.autocomplete.assert_called_once_with("arroz", 5)

    @pytest.mark.asyncio
    async def test_executar_sem_resultados(self, usecase, mock_repo):
        mock_repo.autocomplete = AsyncMock(return_value=[])

        result = await usecase.executar(query="xyz123", limit=10)

        assert result == []

    @pytest.mark.asyncio
    async def test_executar_case_insensitive(self, usecase, mock_repo, produtos_exemplo):
        mock_repo.autocomplete = AsyncMock(return_value=produtos_exemplo[:1])

        result = await usecase.executar(query="ARROZ", limit=10)

        assert len(result) == 1
        # O case-insensitive é responsabilidade do repositório (ilike)