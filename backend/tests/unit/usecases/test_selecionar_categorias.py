# COBECO Backend — SelecionarCategoriasUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import SelecionarCategoriasUseCase
from src.domain.entities import Categoria


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.listar_todas = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return SelecionarCategoriasUseCase(mock_repo)


@pytest.fixture
def categorias_exemplo():
    return [
        Categoria(id=1, nome="Mercado", descricao="Supermercados e atacados"),
        Categoria(id=2, nome="Vestuário", descricao="Roupas e calçados"),
        Categoria(id=3, nome="Informática", descricao="Eletrônicos e periféricos"),
    ]


class TestSelecionarCategoriasUseCase:
    """Testes para SelecionarCategoriasUseCase (UC03/RF12)"""

    @pytest.mark.asyncio
    async def test_listar_todas(self, usecase, mock_repo, categorias_exemplo):
        mock_repo.listar_todas = AsyncMock(return_value=categorias_exemplo)

        result = await usecase.listar_todas()

        assert len(result) == 3
        assert result[0].nome == "Mercado"
        assert result[1].nome == "Vestuário"
        assert result[2].nome == "Informática"
        mock_repo.listar_todas.assert_called_once()

    @pytest.mark.asyncio
    async def test_listar_todas_vazio(self, usecase, mock_repo):
        mock_repo.listar_todas = AsyncMock(return_value=[])

        result = await usecase.listar_todas()

        assert result == []

    @pytest.mark.asyncio
    async def test_filtrar_fornecedores_placeholder(self, usecase, mock_repo):
        # O método filtrar_fornecedores é um placeholder
        result = await usecase.filtrar_fornecedores(categoria_ids=[1, 2])
        assert result == []