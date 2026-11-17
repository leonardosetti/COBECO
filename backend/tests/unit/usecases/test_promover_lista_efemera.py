# COBECO Backend — PromoverListaEfemeraUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.domain.usecases import (
    PromoverListaEfemeraUseCase,
    SalvarListaUseCase,
    CriarListaInput,
    DomainError,
)
from src.domain.entities import Lista, ItemLista, Produto
from datetime import datetime


@pytest.fixture
def mock_lista_repo():
    repo = AsyncMock()
    repo.criar = AsyncMock()
    return repo


@pytest.fixture
def mock_produto_repo():
    repo = AsyncMock()
    repo.buscar_por_ids = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_lista_repo, mock_produto_repo):
    return PromoverListaEfemeraUseCase(mock_lista_repo, mock_produto_repo)


@pytest.fixture
def lista_efemera():
    return {
        "nome": "Lista Efêmera",
        "itens": [
            {"produto_id": 1, "quantidade": 2},
            {"produto_id": 2, "quantidade": 1},
        ],
    }


@pytest.fixture
def produtos_exemplo():
    return [
        Produto(id=1, nome="Arroz 5kg", unidade="kg", ativo=True),
        Produto(id=2, nome="Feijão 1kg", unidade="kg", ativo=True),
    ]


class TestPromoverListaEfemeraUseCase:
    """Testes para PromoverListaEfemeraUseCase (UC17/RF08)"""

    @pytest.mark.asyncio
    async def test_executar_sucesso(
        self, usecase, mock_lista_repo, mock_produto_repo, lista_efemera, produtos_exemplo
    ):
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos_exemplo)
        mock_lista_repo.criar = AsyncMock(
            return_value=Lista(
                id=1,
                usuario_id=1,
                nome="Lista Efêmera",
                itens=[
                    ItemLista(produto_id=1, quantidade=2),
                    ItemLista(produto_id=2, quantidade=1),
                ],
                criado_em=datetime.now(),
                atualizado_em=datetime.now(),
            )
        )

        result = await usecase.executar(usuario_id=1, lista_memoria=lista_efemera)

        assert result.id == 1
        assert result.nome == "Lista Efêmera"
        assert len(result.itens) == 2
        mock_produto_repo.buscar_por_ids.assert_called_once_with([1, 2])
        mock_lista_repo.criar.assert_called_once()

    @pytest.mark.asyncio
    async def test_executar_produto_nao_existe(self, usecase, mock_produto_repo, lista_efemera):
        mock_produto_repo.buscar_por_ids = AsyncMock(
            return_value=[Produto(id=1, nome="Arroz 5kg", unidade="kg", ativo=True)]
        )

        with pytest.raises(DomainError, match="Um ou mais produtos não existem"):
            await usecase.executar(usuario_id=1, lista_memoria=lista_efemera)

    @pytest.mark.asyncio
    async def test_executar_lista_vazia(self, usecase, mock_produto_repo):
        lista_vazia = {"nome": "Vazia", "itens": []}
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=[])

        with pytest.raises(ValueError, match="Lista deve ter pelo menos 1 item"):
            await usecase.executar(usuario_id=1, lista_memoria=lista_vazia)

    @pytest.mark.asyncio
    async def test_executar_nome_invalido(self, usecase, mock_produto_repo, produtos_exemplo):
        lista_nome_longo = {"nome": "A" * 101, "itens": [{"produto_id": 1, "quantidade": 1}]}
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos_exemplo[:1])

        with pytest.raises(ValueError, match="nome da lista deve ter 1-100 caracteres"):
            await usecase.executar(usuario_id=1, lista_memoria=lista_nome_longo)
