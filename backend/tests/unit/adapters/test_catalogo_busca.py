# COBECO Backend — Catálogo: produtos por categoria (RF19)
# Testes de unidade com sessão mockada (sem banco).

import pytest
from unittest.mock import AsyncMock, Mock

from src.adapters.api.catalogo import (
    ProdutoRepositoryImpl,
)
from src.adapters.db.models import CategoriaModel, ProdutoModel


def _result(rows):
    res = AsyncMock()
    scal = Mock()
    scal.all = Mock(return_value=rows)
    res.scalars = Mock(return_value=scal)
    return res


def _cat(id_, nome, descricao="d"):
    c = CategoriaModel(id=id_, nome=nome, descricao=descricao)
    return c


def _prod(id_, nome):
    p = ProdutoModel(id=id_, nome=nome, unidade="un")
    return p


class TestProdutosPorCategoria:
    """RF19 — produtos disponibilizados apenas para categorias selecionadas."""

    @pytest.fixture
    def repo(self):
        session = AsyncMock()
        return ProdutoRepositoryImpl(session), session

    @pytest.mark.asyncio
    async def test_filtra_produtos_por_categorias(self, repo):
        repo_impl, session = repo
        session.execute = AsyncMock(return_value=_result([
            _prod(10, "Camiseta"), _prod(11, "Calça"),
        ]))
        resultado = await repo_impl.listar_por_categorias([1, 2])
        assert [p.id for p in resultado] == [10, 11]
        session.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_sem_categorias_retorna_vazio(self, repo):
        repo_impl, session = repo
        resultado = await repo_impl.listar_por_categorias([])
        assert resultado == []
        session.execute.assert_not_awaited()