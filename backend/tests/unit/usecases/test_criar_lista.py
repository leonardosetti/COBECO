# COBECO Backend — CriarListaUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from src.domain.usecases import (
    CriarListaUseCase, CriarListaInput,
    DomainError
)
from src.domain.entities import Lista, ItemLista, Produto, UnidadeMedida


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.criar = AsyncMock()
    return repo


@pytest.fixture
def mock_produto_repo():
    repo = AsyncMock()
    repo.buscar_por_ids = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo, mock_produto_repo):
    return CriarListaUseCase(mock_repo, mock_produto_repo)


class TestCriarListaUseCase:
    """Testes para CriarListaUseCase (RF07, RF08)"""

    @pytest.mark.asyncio
    async def test_executar_sucesso_lista_com_itens(self, usecase, mock_repo, mock_produto_repo):
        # Produtos existem
        produtos = [
            Produto(id=1, nome="Arroz 5kg", unidade=UnidadeMedida.KG),
            Produto(id=2, nome="Feijão 1kg", unidade=UnidadeMedida.KG),
        ]
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos)

        # Lista criada
        lista_criada = Lista(
            id=1,
            usuario_id=1,
            nome="Compras da Semana",
            itens=[
                ItemLista(id=1, lista_id=1, produto_id=1, quantidade=2),
                ItemLista(id=2, lista_id=1, produto_id=2, quantidade=1),
            ],
        )
        mock_repo.criar = AsyncMock(return_value=lista_criada)

        input_data = CriarListaInput(
            nome="Compras da Semana",
            itens=[
                {"produto_id": 1, "quantidade": 2},
                {"produto_id": 2, "quantidade": 1},
            ],
        )

        result = await usecase.executar(input_data, usuario_id=1)

        assert result.id == 1
        assert result.nome == "Compras da Semana"
        assert result.usuario_id == 1
        assert len(result.itens) == 2
        assert result.itens[0].produto_id == 1
        assert result.itens[0].quantidade == 2
        assert result.itens[1].produto_id == 2
        assert result.itens[1].quantidade == 1

        mock_produto_repo.buscar_por_ids.assert_called_once_with([1, 2])
        mock_repo.criar.assert_called_once()

    @pytest.mark.asyncio
    async def test_executar_produto_inexistente(self, usecase, mock_produto_repo):
        # Apenas um produto existe
        produtos = [Produto(id=1, nome="Arroz", unidade=UnidadeMedida.KG)]
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos)

        input_data = CriarListaInput(
            nome="Lista",
            itens=[
                {"produto_id": 1, "quantidade": 1},
                {"produto_id": 999, "quantidade": 1},  # inexistente
            ],
        )

        with pytest.raises(DomainError, match="Produto.*não encontrado"):
            await usecase.executar(input_data, usuario_id=1)

    @pytest.mark.asyncio
    async def test_executar_lista_sem_itens(self, usecase, mock_produto_repo):
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=[])

        input_data = CriarListaInput(
            nome="Lista Vazia",
            itens=[],
        )

        with pytest.raises(DomainError, match="Lista deve ter pelo menos 1 item"):
            await usecase.executar(input_data, usuario_id=1)

    @pytest.mark.asyncio
    async def test_executar_quantidade_invalida(self, usecase, mock_produto_repo):
        produtos = [Produto(id=1, nome="Arroz", unidade=UnidadeMedida.KG)]
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos)

        input_data = CriarListaInput(
            nome="Lista",
            itens=[{"produto_id": 1, "quantidade": 0}],  # inválido
        )

        with pytest.raises(DomainError, match="Quantidade deve ser entre 1 e 9999"):
            await usecase.executar(input_data, usuario_id=1)

    @pytest.mark.asyncio
    async def test_executor_nome_lista_invalido(self, usecase, mock_produto_repo):
        produtos = [Produto(id=1, nome="Arroz", unidade=UnidadeMedida.KG)]
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos)

        input_data = CriarListaInput(
            nome="",  # inválido
            itens=[{"produto_id": 1, "quantidade": 1}],
        )

        with pytest.raises(DomainError, match="Nome da lista deve ter 1-100 caracteres"):
            await usecase.executar(input_data, usuario_id=1)