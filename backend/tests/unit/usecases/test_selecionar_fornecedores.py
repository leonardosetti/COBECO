# COBECO Backend — SelecionarFornecedoresUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import SelecionarFornecedoresUseCase
from src.domain.entities import Fornecedor, Categoria, CNPJ


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.listar_por_categorias = AsyncMock()
    repo.buscar_por_ids = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return SelecionarFornecedoresUseCase(mock_repo)


@pytest.fixture
def categorias_exemplo():
    return [
        Categoria(id=1, nome="Mercado", descricao="Supermercados"),
        Categoria(id=2, nome="Vestuário", descricao="Roupas"),
    ]


@pytest.fixture
def fornecedores_exemplo():
    return [
        Fornecedor(
            id=1,
            nome="Supermercado ABC",
            cnpj=CNPJ("12.345.678/0001-95"),
            ativo=True,
            categorias=[Categoria(id=1, nome="Mercado")],
        ),
        Fornecedor(
            id=2,
            nome="Loja de Roupas XYZ",
            cnpj=CNPJ("98.765.432/0001-10"),
            ativo=True,
            categorias=[Categoria(id=2, nome="Vestuário")],
        ),
    ]


class TestSelecionarFornecedoresUseCase:
    """Testes para SelecionarFornecedoresUseCase (UC04/RF13)"""

    @pytest.mark.asyncio
    async def test_listar_por_categorias(self, usecase, mock_repo, fornecedores_exemplo):
        mock_repo.listar_por_categorias = AsyncMock(return_value=fornecedores_exemplo)

        result = await usecase.listar_por_categorias(categoria_ids=[1, 2])

        assert len(result) == 2
        assert result[0].nome == "Supermercado ABC"
        assert result[1].nome == "Loja de Roupas XYZ"
        mock_repo.listar_por_categorias.assert_called_once_with([1, 2])

    @pytest.mark.asyncio
    async def test_listar_por_categoria_unica(self, usecase, mock_repo, fornecedores_exemplo):
        mock_repo.listar_por_categorias = AsyncMock(return_value=[fornecedores_exemplo[0]])

        result = await usecase.listar_por_categorias(categoria_ids=[1])

        assert len(result) == 1
        assert result[0].nome == "Supermercado ABC"

    @pytest.mark.asyncio
    async def test_listar_sem_categorias(self, usecase, mock_repo):
        mock_repo.listar_por_categorias = AsyncMock(return_value=[])

        result = await usecase.listar_por_categorias(categoria_ids=[])

        assert result == []

    @pytest.mark.asyncio
    async def test_buscar_disponibilidade(self, usecase, mock_repo):
        mock_repo.calcular_disponibilidade = AsyncMock(
            side_effect=lambda f_id, p_ids: (1, 1, None) if f_id == 1 else (0, 2, None)
        )

        result = await usecase.buscar_disponibilidade(
            fornecedor_ids=[1, 2], produto_ids=[1, 2]
        )

        assert result == {1: 50.0, 2: 0.0}
        assert mock_repo.calcular_disponibilidade.call_count == 2
