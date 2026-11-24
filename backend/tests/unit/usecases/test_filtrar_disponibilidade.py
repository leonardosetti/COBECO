# COBECO Backend — FiltrarDisponibilidadeUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import FiltrarDisponibilidadeUseCase
from src.domain.entities import Fornecedor, Categoria, CNPJ


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.buscar_por_ids = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return FiltrarDisponibilidadeUseCase(mock_repo)


@pytest.fixture
def fornecedores_exemplo():
    return [
        Fornecedor(
            id=1,
            nome="Fornecedor A",
            cnpj=CNPJ("12.345.678/0001-95"),
            ativo=True,
            categorias=[Categoria(id=1, nome="Mercado")],
        ),
        Fornecedor(
            id=2,
            nome="Fornecedor B",
            cnpj=CNPJ("98.765.432/0001-10"),
            ativo=True,
            categorias=[Categoria(id=2, nome="Vestuário")],
        ),
        Fornecedor(
            id=3,
            nome="Fornecedor C",
            cnpj=CNPJ("11.222.333/0001-44"),
            ativo=True,
            categorias=[Categoria(id=1, nome="Mercado")],
        ),
    ]


class TestFiltrarDisponibilidadeUseCase:
    """Testes para FiltrarDisponibilidadeUseCase (UC05/RF14)"""

    @pytest.mark.asyncio
    async def test_executar_sem_filtro(self, usecase, mock_repo, fornecedores_exemplo):
        mock_repo.buscar_por_ids = AsyncMock(return_value=fornecedores_exemplo)

        result = await usecase.executar(
            fornecedor_ids=[1, 2, 3],
            produto_ids=[1, 2],
            min_disponibilidade=0.0,
        )

        assert len(result) == 3
        mock_repo.buscar_por_ids.assert_called_once_with([1, 2, 3])

    @pytest.mark.asyncio
    async def test_executar_com_filtro_minimo(self, usecase, mock_repo, fornecedores_exemplo):
        mock_repo.buscar_por_ids = AsyncMock(return_value=fornecedores_exemplo)
        # F:1=100%, F:2=0%, F:3=50% → com min 50% passa F:1 e F:3
        mock_repo.calcular_disponibilidade = AsyncMock(
            side_effect=lambda f_id, p_ids: {
                1: (2, 0, None),
                2: (0, 2, None),
                3: (1, 1, None),
            }[f_id]
        )

        result = await usecase.executar(
            fornecedor_ids=[1, 2, 3],
            produto_ids=[1, 2],
            min_disponibilidade=50.0,
        )

        ids = sorted(f.id for f in result)
        assert ids == [1, 3]

    @pytest.mark.asyncio
    async def test_executar_fornecedores_inexistentes(self, usecase, mock_repo):
        mock_repo.buscar_por_ids = AsyncMock(return_value=[])

        result = await usecase.executar(
            fornecedor_ids=[999],
            produto_ids=[1],
            min_disponibilidade=0.0,
        )

        assert result == []

    @pytest.mark.asyncio
    async def test_executar_lista_vazia(self, usecase, mock_repo):
        mock_repo.buscar_por_ids = AsyncMock(return_value=[])

        result = await usecase.executar(
            fornecedor_ids=[],
            produto_ids=[1],
            min_disponibilidade=0.0,
        )

        assert result == []
