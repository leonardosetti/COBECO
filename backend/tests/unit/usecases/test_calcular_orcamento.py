# COBECO Backend — CalcularOrcamentoUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from src.domain.usecases import (
    CalcularOrcamentoUseCase, ComparacaoInput,
    DomainError
)
from src.domain.entities import (
    Lista, ItemLista, Produto, UnidadeMedida,
    FornecedorProduto, Fornecedor, OrcamentoComparacao,
    FornecedorComparacao, ItemComparacao
)


@pytest.fixture
def mock_comparacao_repo():
    repo = AsyncMock()
    repo.buscar_precos_para_comparacao = AsyncMock()
    return repo


@pytest.fixture
def mock_lista_repo():
    repo = AsyncMock()
    repo.buscar_por_id = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_comparacao_repo, mock_lista_repo):
    return CalcularOrcamentoUseCase(mock_comparacao_repo, mock_lista_repo)


class TestCalcularOrcamentoUseCase:
    """Testes para CalcularOrcamentoUseCase (RF15, RF16)"""

    @pytest.mark.asyncio
    async def test_executar_sucesso_comparacao_completa(
        self, usecase, mock_lista_repo, mock_comparacao_repo
    ):
        # Lista existe com itens
        lista = Lista(
            id=1,
            usuario_id=1,
            nome="Compras da Semana",
            itens=[
                ItemLista(id=1, lista_id=1, produto_id=1, quantidade=2),
                ItemLista(id=2, lista_id=1, produto_id=2, quantidade=1),
            ],
        )
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista)

        # Preços disponíveis para 2 fornecedores
        precos = [
            # Fornecedor 1: tem ambos produtos
            FornecedorProduto(fornecedor_id=1, produto_id=1, preco=Decimal("10.00"), estoque=10, ativo=True),
            FornecedorProduto(fornecedor_id=1, produto_id=2, preco=Decimal("8.00"), estoque=5, ativo=True),
            # Fornecedor 2: tem apenas produto 1
            FornecedorProduto(fornecedor_id=2, produto_id=1, preco=Decimal("12.00"), estoque=20, ativo=True),
            # Fornecedor 3: tem ambos mas mais caro
            FornecedorProduto(fornecedor_id=3, produto_id=1, preco=Decimal("11.00"), estoque=15, ativo=True),
            FornecedorProduto(fornecedor_id=3, produto_id=2, preco=Decimal("9.00"), estoque=8, ativo=True),
        ]
        mock_comparacao_repo.buscar_precos_para_comparacao = AsyncMock(return_value=precos)

        input_data = ComparacaoInput(
            lista_id=1,
            fornecedor_ids=[1, 2, 3],
            disponibilidade_minima=0.0,
        )

        result = await usecase.executar(input_data)

        assert isinstance(result, OrcamentoComparacao)
        assert result.lista_id == 1
        assert result.lista_nome == "Compras da Semana"
        assert len(result.fornecedores) == 3

        # Verifica ordenação por preço ASC (RF15)
        # Forn 1: (10*2) + (8*1) = 28.00 - 100% disp
        # Forn 3: (11*2) + (9*1) = 31.00 - 100% disp
        # Forn 2: (12*2) + (0*1) = 24.00 - 50% disp (falta produto 2)
        assert result.fornecedores[0].fornecedor_id == 2  # menor preço total (mesmo com 50%)
        assert result.fornecedores[1].fornecedor_id == 1
        assert result.fornecedores[2].fornecedor_id == 3
        assert result.melhor_fornecedor_id == 2

        # Verifica cálculos
        forn1 = next(f for f in result.fornecedores if f.fornecedor_id == 1)
        assert forn1.itens_disponiveis == 2
        assert forn1.itens_ausentes == 0
        assert forn1.percentual_disponibilidade == 100.0
        assert forn1.preco_total == Decimal("28.00")

        forn2 = next(f for f in result.fornecedores if f.fornecedor_id == 2)
        assert forn2.itens_disponiveis == 1
        assert forn2.itens_ausentes == 1
        assert forn2.percentual_disponibilidade == 50.0
        assert forn2.preco_total == Decimal("24.00")  # apenas produto 1: 12*2

    @pytest.mark.asyncio
    async def test_executar_filtro_disponibilidade_minima(
        self, usecase, mock_lista_repo, mock_comparacao_repo
    ):
        lista = Lista(
            id=1,
            usuario_id=1,
            nome="Lista",
            itens=[
                ItemLista(id=1, lista_id=1, produto_id=1, quantidade=1),
                ItemLista(id=2, lista_id=1, produto_id=2, quantidade=1),
            ],
        )
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista)

        precos = [
            FornecedorProduto(fornecedor_id=1, produto_id=1, preco=Decimal("10.00"), estoque=10, ativo=True),
            FornecedorProduto(fornecedor_id=1, produto_id=2, preco=Decimal("8.00"), estoque=5, ativo=True),
            FornecedorProduto(fornecedor_id=2, produto_id=1, preco=Decimal("12.00"), estoque=20, ativo=True),
            # Fornecedor 2 NÃO tem produto 2
        ]
        mock_comparacao_repo.buscar_precos_para_comparacao = AsyncMock(return_value=precos)

        # Exige 100% disponibilidade
        input_data = ComparacaoInput(
            lista_id=1,
            fornecedor_ids=[1, 2],
            disponibilidade_minima=100.0,
        )

        result = await usecase.executar(input_data)

        # Apenas fornecedor 1 tem 100% disponibilidade
        assert len(result.fornecedores) == 1
        assert result.fornecedores[0].fornecedor_id == 1
        assert result.melhor_fornecedor_id == 1

    @pytest.mark.asyncio
    async def test_executar_lista_nao_encontrada(self, usecase, mock_lista_repo):
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=None)

        input_data = ComparacaoInput(lista_id=999, fornecedor_ids=[1])

        with pytest.raises(DomainError, match="Lista não encontrada"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_lista_sem_itens(self, usecase, mock_lista_repo):
        lista = Lista(id=1, usuario_id=1, nome="Vazia", itens=[])
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista)

        input_data = ComparacaoInput(lista_id=1, fornecedor_ids=[1])

        with pytest.raises(DomainError, match="Lista deve ter pelo menos 1 item"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_sem_precos_disponiveis(self, usecase, mock_lista_repo, mock_comparacao_repo):
        lista = Lista(
            id=1,
            usuario_id=1,
            nome="Lista",
            itens=[ItemLista(id=1, lista_id=1, produto_id=1, quantidade=1)],
        )
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista)
        mock_comparacao_repo.buscar_precos_para_comparacao = AsyncMock(return_value=[])

        input_data = ComparacaoInput(lista_id=1, fornecedor_ids=[1])

        result = await usecase.executar(input_data)

        assert len(result.fornecedores) == 0
        assert result.melhor_fornecedor_id is None

    @pytest.mark.asyncio
    async def test_executar_fornecedor_sem_estoque(self, usecase, mock_lista_repo, mock_comparacao_repo):
        lista = Lista(
            id=1,
            usuario_id=1,
            nome="Lista",
            itens=[ItemLista(id=1, lista_id=1, produto_id=1, quantidade=5)],
        )
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista)

        # Fornecedor tem produto mas estoque = 0
        precos = [
            FornecedorProduto(fornecedor_id=1, produto_id=1, preco=Decimal("10.00"), estoque=0, ativo=True),
        ]
        mock_comparacao_repo.buscar_precos_para_comparacao = AsyncMock(return_value=precos)

        input_data = ComparacaoInput(lista_id=1, fornecedor_ids=[1])

        result = await usecase.executar(input_data)

        # Produto indisponível por estoque zero
        assert len(result.fornecedores) == 1
        forn = result.fornecedores[0]
        assert forn.itens_disponiveis == 0
        assert forn.itens_ausentes == 1
        assert forn.percentual_disponibilidade == 0.0