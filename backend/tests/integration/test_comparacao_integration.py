# COBECO Backend — Comparação Integration Tests
# Testes de integração para Comparação Flat (RF15, RF16)

import pytest
from decimal import Decimal
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_user(client):
    """Cria usuário autenticado com lista e itens"""
    user_data = {
        "nome_usuario": "testuser_comp",
        "email": "comp@teste.com",
        "nome": "User Comparacao",
        "senha": "Senha@123",
        "confirmar_senha": "Senha@123",
        "pergunta_seguranca": "nome_mae",
        "resposta_seguranca": "Maria Silva",
    }
    await client.post("/v1/auth/cadastrar", json=user_data)

    login_data = {"nome_usuario": "testuser_comp", "senha": "Senha@123"}
    response = await client.post("/v1/auth/login", json=login_data)
    tokens = response.json()

    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
async def lista_com_itens(client, auth_user):
    """Cria lista com alguns itens para comparação"""
    # Pega alguns produtos do seed
    prod_resp = await client.get("/v1/produtos?limit=3")
    produtos = prod_resp.json()["items"]

    lista_data = {
        "nome": "Lista para Comparação",
        "itens": [
            {"produto_id": produtos[0]["id"], "quantidade": 2},
            {"produto_id": produtos[1]["id"], "quantidade": 1},
            {"produto_id": produtos[2]["id"], "quantidade": 3},
        ],
    }
    response = await client.post("/v1/listas", json=lista_data, headers=auth_user)
    assert response.status_code == 201
    return response.json()


class TestComparacaoIntegration:
    """Testes de integração para /comparacao"""

    @pytest.mark.asyncio
    async def test_comparacao_flat_ordenacao_preco_asc(self, client, auth_user, lista_com_itens):
        """RF15 - Tabela flat comparativa ordenada por preço total ASC"""
        lista_id = lista_com_itens["id"]

        # Busca fornecedores ativos
        forn_resp = await client.get("/v1/fornecedores", headers=auth_user)
        fornecedores = forn_resp.json()
        forn_ids = [f["id"] for f in fornecedores[:5]]

        response = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )

        assert response.status_code == 200
        data = response.json()

        # Estrutura da resposta
        assert data["lista_id"] == lista_id
        assert data["lista_nome"] == "Lista para Comparação"
        assert "fornecedores" in data
        assert "melhor_fornecedor_id" in data
        assert "calculado_em" in data

        fornecedores_resp = data["fornecedores"]
        assert len(fornecedores_resp) > 0

        # Verifica ordenação por preço total ASC (RF15)
        precos = [Decimal(str(f["preco_total"])) for f in fornecedores_resp]
        assert precos == sorted(precos), "Fornecedores devem estar ordenados por preço ASC"

        # Melhor fornecedor é o primeiro
        assert data["melhor_fornecedor_id"] == fornecedores_resp[0]["fornecedor_id"]

        # Verifica estrutura de cada fornecedor
        for f in fornecedores_resp:
            assert "fornecedor_id" in f
            assert "fornecedor_nome" in f
            assert "itens_disponiveis" in f
            assert "itens_ausentes" in f
            assert "percentual_disponibilidade" in f
            assert "preco_total" in f
            assert "itens" in f
            assert isinstance(f["itens"], list)

            # Verifica itens
            for item in f["itens"]:
                assert "produto_id" in item
                assert "produto_nome" in item
                assert "unidade" in item
                assert "quantidade" in item
                assert "preco_unitario" in item
                assert "preco_total" in item
                assert "disponivel" in item

    @pytest.mark.asyncio
    async def test_comparacao_slider_disponibilidade_filtra_fornecedores(
        self, client, auth_user, lista_com_itens
    ):
        """RF16 - Slider de disponibilidade filtra fornecedores"""
        lista_id = lista_com_itens["id"]

        forn_resp = await client.get("/v1/fornecedores", headers=auth_user)
        fornecedores = forn_resp.json()
        forn_ids = [f["id"] for f in fornecedores[:5]]

        # Disponibilidade mínima 0% (todos)
        response_0 = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )
        data_0 = response_0.json()
        count_0 = len(data_0["fornecedores"])

        # Disponibilidade mínima 100% (apenas quem tem todos os itens)
        response_100 = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 100.0,
            },
            headers=auth_user,
        )
        data_100 = response_100.json()
        count_10 = len(data_100["fornecedores"])

        # 100% deve retornar menos ou igual fornecedores
        assert count_10 <= count_0

        # Todos fornecedores retornados com 100% devem ter 100% disponibilidade
        for f in data_100["fornecedores"]:
            assert f["percentual_disponibilidade"] == 100.0
            assert f["itens_ausentes"] == 0

    @pytest.mark.asyncio
    async def test_comparacao_lista_inexistente(self, client, auth_user):
        forn_resp = await client.get("/v1/fornecedores", headers=auth_user)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]

        response = await client.post(
            "/comparacao",
            json={
                "lista_id": 99999,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_comparacao_lista_sem_itens(self, client, auth_user):
        # Cria lista vazia
        lista_resp = await client.post(
            "/v1/listas",
            json={"nome": "Lista Vazia", "itens": []},
            headers=auth_user,
        )
        # Deve falhar na criação (validação)
        assert lista_resp.status_code == 400

    @pytest.mark.asyncio
    async def test_comparacao_sem_fornecedores(self, client, auth_user, lista_com_itens):
        response = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_com_itens["id"],
                "fornecedor_ids": [],
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["fornecedores"] == []
        assert data["melhor_fornecedor_id"] is None

    @pytest.mark.asyncio
    async def test_comparacao_fornecedor_inexistente(self, client, auth_user, lista_com_itens):
        response = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_com_itens["id"],
                "fornecedor_ids": [99999],
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )
        # Deve ignorar fornecedores inexistentes ou retornar vazio
        assert response.status_code == 200
        data = response.json()
        assert data["fornecedores"] == []


class TestComparacaoFlatEstrutura:
    """Testes para validar estrutura da tabela flat (RF15, RF16)"""

    @pytest.mark.asyncio
    async def test_item_comparacao_campos_obrigatorios(self, client, auth_user, lista_com_itens):
        lista_id = lista_com_itens["id"]
        forn_resp = await client.get("/v1/fornecedores", headers=auth_user)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]

        response = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )
        data = response.json()

        for f in data["fornecedores"]:
            for item in f["itens"]:
                # Campos obrigatórios do ItemComparacao
                assert "produto_id" in item
                assert "produto_nome" in item
                assert "unidade" in item
                assert "quantidade" in item
                assert "preco_unitario" in item
                assert "preco_total" in item
                assert "disponivel" in item
                assert isinstance(item["disponivel"], bool)

    @pytest.mark.asyncio
    async def test_fornecedor_comparacao_campos_obrigatorios(
        self, client, auth_user, lista_com_itens
    ):
        lista_id = lista_com_itens["id"]
        forn_resp = await client.get("/v1/fornecedores", headers=auth_user)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]

        response = await client.post(
            "/comparacao",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_user,
        )
        data = response.json()

        for f in data["fornecedores"]:
            assert "fornecedor_id" in f
            assert "fornecedor_nome" in f
            assert "itens_disponiveis" in f
            assert "itens_ausentes" in f
            assert "percentual_disponibilidade" in f
            assert "preco_total" in f
            assert "itens" in f
            assert isinstance(f["percentual_disponibilidade"], (int, float))
            assert 0 <= f["percentual_disponibilidade"] <= 100
