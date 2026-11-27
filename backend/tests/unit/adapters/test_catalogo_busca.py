# COBECO Backend — Catálogo: busca semântica de categorias e produtos por categoria (RF19, RF20)
# Testes de unidade com sessão mockada (sem banco).

import pytest
from unittest.mock import AsyncMock, Mock

from src.adapters.api.catalogo import (
    CategoriaRepositoryImpl,
    ProdutoRepositoryImpl,
    CATEGORIA_GATILHOS,
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


class TestCategoriaBuscaSemantica:
    """RF20 — busca de categorias por nome ou sinônimos."""

    @pytest.fixture
    def repo(self):
        session = AsyncMock()
        return CategoriaRepositoryImpl(session), session

    @pytest.mark.asyncio
    async def test_termo_por_sinonimo_roupas(self, repo):
        repo_impl, session = repo
        session.execute = AsyncMock(return_value=_result([
            _cat(1, "Vestuário"), _cat(2, "Mercado"), _cat(3, "Jardinagem"),
        ]))
        resultado = await repo_impl.buscar_por_termo("roupas")
        ids = {c.id for c in resultado}
        assert ids == {1}, f"esperado Vestuário, obteve {ids}"

    @pytest.mark.asyncio
    async def test_termo_por_sinonimo_pa_rastelo(self, repo):
        repo_impl, session = repo
        session.execute = AsyncMock(return_value=_result([
            _cat(1, "Vestuário"), _cat(2, "Jardinagem"), _cat(3, "Ferramentas"),
        ]))
        resultado = await repo_impl.buscar_por_termo("pá")
        ids = {c.id for c in resultado}
        assert ids == {2, 3}, f"esperado Jardinagem+Ferramentas, obteve {ids}"

        session.execute = AsyncMock(return_value=_result([
            _cat(2, "Jardinagem"), _cat(3, "Ferramentas"),
        ]))
        resultado = await repo_impl.buscar_por_termo("rastelo")
        ids = {c.id for c in resultado}
        assert ids == {2, 3}

    @pytest.mark.asyncio
    async def test_termo_por_nome_categoria(self, repo):
        repo_impl, session = repo
        session.execute = AsyncMock(return_value=_result([
            _cat(1, "Vestuário"), _cat(2, "Livros"),
        ]))
        resultado = await repo_impl.buscar_por_termo("liv")
        ids = {c.id for c in resultado}
        assert ids == {2}

    @pytest.mark.asyncio
    async def test_terpo_vazio_retorna_vazio(self, repo):
        repo_impl, session = repo
        resultado = await repo_impl.buscar_por_termo("")
        assert resultado == []
        session.execute.assert_not_awaited()

    def test_gatilhos_cobrem_exemplos_requisitados(self):
        # roupas/camiseta -> Vestuário ; pá/rastelo -> Jardinagem e Ferramentas
        # Chaves genéricas estão em GENERIC_CATEGORIA_GATILHOS com prefixo '_'
        from src.adapters.api.catalogo import GENERIC_CATEGORIA_GATILHOS
        assert "roupas" in GENERIC_CATEGORIA_GATILHOS["_vestuário"]
        assert "camiseta" in GENERIC_CATEGORIA_GATILHOS["_vestuário"]
        assert "pá" in CATEGORIA_GATILHOS["jardinagem"] and "pá" in CATEGORIA_GATILHOS["ferramentas"]
        assert "rastelo" in CATEGORIA_GATILHOS["jardinagem"] and "rastelo" in CATEGORIA_GATILHOS["ferramentas"]


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
