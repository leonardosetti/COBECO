# COBECO Backend — ListarMinhasListasUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import ListarMinhasListasUseCase
from src.domain.entities import Lista, ItemLista
from datetime import datetime


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.listar_por_usuario = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return ListarMinhasListasUseCase(mock_repo)


@pytest.fixture
def listas_exemplo():
    return [
        Lista(
            id=1,
            usuario_id=1,
            nome="Compras da Semana",
            itens=[
                ItemLista(id=1, lista_id=1, produto_id=1, quantidade=2),
                ItemLista(id=2, lista_id=1, produto_id=2, quantidade=1),
            ],
            criado_em=datetime(2026, 11, 15, 10, 0),
            atualizado_em=datetime(2026, 11, 15, 10, 0),
        ),
        Lista(
            id=2,
            usuario_id=1,
            nome="Lista de Natal",
            itens=[
                ItemLista(id=3, lista_id=2, produto_id=3, quantidade=5),
            ],
            criado_em=datetime(2026, 11, 10, 14, 30),
            atualizado_em=datetime(2026, 11, 10, 14, 30),
        ),
    ]


class TestListarMinhasListasUseCase:
    """Testes para ListarMinhasListasUseCase (UC15/RF09)"""

    @pytest.mark.asyncio
    async def test_executar_pagina_default(self, usecase, mock_repo, listas_exemplo):
        mock_repo.listar_por_usuario = AsyncMock(return_value=(listas_exemplo, 2))

        listas, total = await usecase.executar(usuario_id=1)

        assert len(listas) == 2
        assert total == 2
        assert listas[0].nome == "Compras da Semana"
        assert listas[1].nome == "Lista de Natal"
        mock_repo.listar_por_usuario.assert_called_once_with(1, 1, 20, None)

    @pytest.mark.asyncio
    async def test_executar_pagina_customizada(self, usecase, mock_repo, listas_exemplo):
        mock_repo.listar_por_usuario = AsyncMock(return_value=([listas_exemplo[0]], 2))

        listas, total = await usecase.executar(usuario_id=1, pagina=2, por_pagina=1)

        assert len(listas) == 1
        assert total == 2
        mock_repo.listar_por_usuario.assert_called_once_with(1, 2, 1, None)

    @pytest.mark.asyncio
    async def test_executar_com_busca(self, usecase, mock_repo, listas_exemplo):
        mock_repo.listar_por_usuario = AsyncMock(return_value=([listas_exemplo[0]], 1))

        listas, total = await usecase.executar(usuario_id=1, busca="Semana")

        assert len(listas) == 1
        assert total == 1
        assert listas[0].nome == "Compras da Semana"
        mock_repo.listar_por_usuario.assert_called_once_with(1, 1, 20, "Semana")

    @pytest.mark.asyncio
    async def test_executar_sem_listas(self, usecase, mock_repo):
        mock_repo.listar_por_usuario = AsyncMock(return_value=([], 0))

        listas, total = await usecase.executar(usuario_id=1)

        assert len(listas) == 0
        assert total == 0

    @pytest.mark.asyncio
    async def test_executar_ordem_decrescente_por_criado_em(self, usecase, mock_repo):
        lista_nova = Lista(
            id=3,
            usuario_id=1,
            nome="Lista Nova",
            itens=[],
            criado_em=datetime(2026, 11, 20, 9, 0),
            atualizado_em=datetime(2026, 11, 20, 9, 0),
        )
        lista_velha = Lista(
            id=4,
            usuario_id=1,
            nome="Lista Velha",
            itens=[],
            criado_em=datetime(2026, 11, 1, 8, 0),
            atualizado_em=datetime(2026, 11, 1, 8, 0),
        )
        # O repositório deve retornar ordenado por criado_em DESC
        mock_repo.listar_por_usuario = AsyncMock(return_value=([lista_nova, lista_velha], 2))

        listas, total = await usecase.executar(usuario_id=1)

        assert listas[0].id == 3  # Mais recente primeiro
        assert listas[1].id == 4