# COBECO Backend — EditarListaUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import EditarListaUseCase, CriarListaInput, ListaNaoEncontrada, DomainError
from src.domain.entities import Lista, ItemLista, Produto
from datetime import datetime


@pytest.fixture
def mock_lista_repo():
    repo = AsyncMock()
    repo.buscar_por_id = AsyncMock()
    repo.atualizar = AsyncMock()
    return repo


@pytest.fixture
def mock_produto_repo():
    repo = AsyncMock()
    repo.buscar_por_ids = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_lista_repo, mock_produto_repo):
    return EditarListaUseCase(mock_lista_repo, mock_produto_repo)


@pytest.fixture
def lista_existente():
    return Lista(
        id=1,
        usuario_id=1,
        nome="Lista Original",
        itens=[
            ItemLista(id=1, lista_id=1, produto_id=1, quantidade=2),
            ItemLista(id=2, lista_id=1, produto_id=2, quantidade=1),
        ],
        criado_em=datetime(2026, 11, 10, 10, 0),
        atualizado_em=datetime(2026, 11, 10, 10, 0),
    )


@pytest.fixture
def produtos_exemplo():
    return [
        Produto(id=1, nome="Arroz 5kg", unidade="kg", ativo=True),
        Produto(id=2, nome="Feijão 1kg", unidade="kg", ativo=True),
        Produto(id=3, nome="Óleo 900ml", unidade="L", ativo=True),
    ]


class TestEditarListaUseCase:
    """Testes para EditarListaUseCase (UC13/RF10)"""

    @pytest.mark.asyncio
    async def test_executar_atualizar_nome(
        self, usecase, mock_lista_repo, mock_produto_repo, lista_existente, produtos_exemplo
    ):
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista_existente)
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos_exemplo[:2])
        mock_lista_repo.atualizar = AsyncMock(
            return_value=Lista(
                id=1,
                usuario_id=1,
                nome="Novo Nome",
                itens=[
                    ItemLista(produto_id=1, quantidade=2),
                    ItemLista(produto_id=2, quantidade=1),
                ],
                criado_em=datetime(2026, 11, 10, 10, 0),
                atualizado_em=datetime.now(),
            )
        )

        input_data = CriarListaInput(
            nome="Novo Nome",
            itens=[{"produto_id": 1, "quantidade": 2}, {"produto_id": 2, "quantidade": 1}],
        )
        result = await usecase.executar(lista_id=1, usuario_id=1, input=input_data)

        assert result.nome == "Novo Nome"
        mock_lista_repo.atualizar.assert_called_once()

    @pytest.mark.asyncio
    async def test_executar_adicionar_item(
        self, usecase, mock_lista_repo, mock_produto_repo, lista_existente, produtos_exemplo
    ):
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista_existente)
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=produtos_exemplo)
        mock_lista_repo.atualizar = AsyncMock(
            return_value=Lista(
                id=1,
                usuario_id=1,
                nome="Lista Original",
                itens=[
                    ItemLista(produto_id=1, quantidade=2),
                    ItemLista(produto_id=2, quantidade=1),
                    ItemLista(produto_id=3, quantidade=3),
                ],
                criado_em=datetime(2026, 11, 10, 10, 0),
                atualizado_em=datetime.now(),
            )
        )

        input_data = CriarListaInput(
            nome="Lista Original",
            itens=[
                {"produto_id": 1, "quantidade": 2},
                {"produto_id": 2, "quantidade": 1},
                {"produto_id": 3, "quantidade": 3},
            ],
        )
        result = await usecase.executar(lista_id=1, usuario_id=1, input=input_data)

        assert len(result.itens) == 3
        assert any(item.produto_id == 3 for item in result.itens)

    @pytest.mark.asyncio
    async def test_executar_remover_item(
        self, usecase, mock_lista_repo, mock_produto_repo, lista_existente, produtos_exemplo
    ):
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista_existente)
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=[produtos_exemplo[0]])
        mock_lista_repo.atualizar = AsyncMock(
            return_value=Lista(
                id=1,
                usuario_id=1,
                nome="Lista Original",
                itens=[ItemLista(produto_id=1, quantidade=2)],
                criado_em=datetime(2026, 11, 10, 10, 0),
                atualizado_em=datetime.now(),
            )
        )

        input_data = CriarListaInput(
            nome="Lista Original",
            itens=[{"produto_id": 1, "quantidade": 2}],
        )
        result = await usecase.executar(lista_id=1, usuario_id=1, input=input_data)

        assert len(result.itens) == 1
        assert result.itens[0].produto_id == 1

    @pytest.mark.asyncio
    async def test_executar_lista_nao_encontrada(self, usecase, mock_lista_repo):
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=None)

        input_data = CriarListaInput(nome="Teste", itens=[{"produto_id": 1, "quantidade": 1}])

        with pytest.raises(ListaNaoEncontrada):
            await usecase.executar(lista_id=999, usuario_id=1, input=input_data)

    @pytest.mark.asyncio
    async def test_executar_lista_outro_usuario(self, usecase, mock_lista_repo, lista_existente):
        # Lista pertence ao usuário 2
        lista_outro_usuario = Lista(
            id=1,
            usuario_id=2,
            nome="Lista do Outro",
            itens=[],
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
        )
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=None)  # Não encontra para usuário 1

        input_data = CriarListaInput(nome="Teste", itens=[{"produto_id": 1, "quantidade": 1}])

        with pytest.raises(ListaNaoEncontrada):
            await usecase.executar(lista_id=1, usuario_id=1, input=input_data)

    @pytest.mark.asyncio
    async def test_executar_produto_nao_existe(
        self, usecase, mock_lista_repo, mock_produto_repo, lista_existente
    ):
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista_existente)
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=[])  # Produto não encontrado

        input_data = CriarListaInput(
            nome="Lista",
            itens=[{"produto_id": 999, "quantidade": 1}],
        )

        with pytest.raises(DomainError, match="Um ou mais produtos não existem"):
            await usecase.executar(lista_id=1, usuario_id=1, input=input_data)

    @pytest.mark.asyncio
    async def test_executar_lista_vazia(
        self, usecase, mock_lista_repo, mock_produto_repo, lista_existente
    ):
        """EditarListaUseCase não valida lista vazia (diferente de SalvarListaUseCase).
        Esta validação ocorre no repositório/DB via constraint unique.
        """
        mock_lista_repo.buscar_por_id = AsyncMock(return_value=lista_existente)
        mock_produto_repo.buscar_por_ids = AsyncMock(return_value=[])
        mock_lista_repo.atualizar = AsyncMock(
            return_value=Lista(
                id=1,
                usuario_id=1,
                nome="Lista",
                itens=[],
                criado_em=datetime.now(),
                atualizado_em=datetime.now(),
            )
        )

        input_data = CriarListaInput(nome="Lista", itens=[])
        result = await usecase.executar(lista_id=1, usuario_id=1, input=input_data)

        assert len(result.itens) == 0
