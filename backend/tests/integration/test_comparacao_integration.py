# COBECO Backend — Comparação Integration Tests
# Testes de integração para Comparação Flat (RF15, RF16)
# Usa fixtures compartilhadas de tests/integration/conftest.py

import pytest
from decimal import Decimal


class TestComparacaoIntegration:
    """Testes de integração para /v1/comparacao"""

    @pytest.mark.asyncio
    async def test_comparacao_flat_ordenacao_preco_asc(self, client, auth_headers, lista_com_itens):
        """RF15 - Tabela flat comparativa ordenada por preço total ASC"""
        lista_id = lista_com_itens["id"]

        # Busca fornecedores ativos
        forn_resp = await client.get("/catalogo/fornecedores", headers=auth_headers)
        fornecedores = forn_resp.json()
        forn_ids = [f["id"] for f in fornecedores[:5]]

        response = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Estrutura da resposta
        assert data["lista_id"] == lista_id
        assert data["lista_nome"] == "Lista para Testes"
        assert "fornecedores" in data
        assert "melhor_fornecedor_id" in data

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
        self, client, auth_headers, lista_com_itens
    ):
        """RF16 - Slider de disponibilidade filtra fornecedores"""
        lista_id = lista_com_itens["id"]

        forn_resp = await client.get("/catalogo/fornecedores", headers=auth_headers)
        fornecedores = forn_resp.json()
        forn_ids = [f["id"] for f in fornecedores[:5]]

        # Disponibilidade mínima 0% (todos)
        response_0 = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
        )
        data_0 = response_0.json()
        count_0 = len(data_0["fornecedores"])

        # Disponibilidade mínima 100% (apenas quem tem todos os itens)
        response_100 = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 100.0,
            },
            headers=auth_headers,
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
    async def test_comparacao_lista_inexistente(self, client, auth_headers):
        forn_resp = await client.get("/catalogo/fornecedores", headers=auth_headers)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]

        response = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": 99999,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_comparacao_lista_sem_itens(self, client, auth_headers):
        # Cria lista vazia - deve falhar na criação (validação Pydantic min_length=1)
        response = await client.post(
            "/listas",
            json={"nome": "Lista Vazia", "itens": [], "categorias": [1]},
            headers=auth_headers,
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_comparacao_sem_fornecedores(self, client, auth_headers, lista_com_itens):
        response = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_com_itens["id"],
                "fornecedor_ids": [],
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
        )
        # Pydantic validação min_length=2
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_comparacao_fornecedor_inexistente(self, client, auth_headers, lista_com_itens):
        # Fornecedores inexistentes com min_length=2 retorna 400 (validação Pydantic)
        response = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_com_itens["id"],
                "fornecedor_ids": [99999, 99998],
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
        )
        # Pydantic valida min_length=2 mas não valida existência dos IDs
        # Se nenhum fornecedor válido, retorna 200 com lista vazia
        # Mas o endpoint pode retornar 400 se a query não encontrar nada
        assert response.status_code in (200, 400)
        if response.status_code == 200:
            data = response.json()
            assert data["fornecedores"] == []


class TestComparacaoFlatEstrutura:
    """Testes para validar estrutura da tabela flat (RF15, RF16)"""

    @pytest.mark.asyncio
    async def test_item_comparacao_campos_obrigatorios(self, client, auth_headers, lista_com_itens):
        lista_id = lista_com_itens["id"]
        forn_resp = await client.get("/catalogo/fornecedores", headers=auth_headers)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]

        response = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
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
        self, client, auth_headers, lista_com_itens
    ):
        lista_id = lista_com_itens["id"]
        forn_resp = await client.get("/catalogo/fornecedores", headers=auth_headers)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]

        response = await client.post(
            "/comparacao/calcular",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
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
