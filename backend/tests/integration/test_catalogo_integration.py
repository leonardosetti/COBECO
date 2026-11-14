# COBECO Backend — Catálogo Integration Tests
# Testes de integração para Catálogo: Categorias, Fornecedores, Produtos, Autocomplete (RF12, RF13)

import pytest
from httpx import AsyncClient
from src.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class TestCatalogoIntegration:
    """Testes de integração para /v1/catalogo"""

    @pytest.mark.asyncio
    async def test_listar_categorias(self, client):
        """RF12 - Listar categorias para pré-filtro (UC03)"""
        response = await client.get("/v1/categorias")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 11  # Seed tem 11 categorias
        
        # Verifica estrutura
        cat = data[0]
        assert "id" in cat
        assert "nome" in cat
        assert "descricao" in cat

    @pytest.mark.asyncio
    async def test_buscar_categoria_por_id(self, client):
        response = await client.get("/v1/categorias/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "nome" in data

    @pytest.mark.asyncio
    async def test_listar_fornecedores_ativos(self, client):
        """RF13 - Listar fornecedores ativos para seleção (UC04)"""
        response = await client.get("/v1/fornecedores")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 10  # Seed tem 10 fornecedores
        
        forn = data[0]
        assert "id" in forn
        assert "nome" in forn
        assert "cnpj" in forn
        assert "ativo" in forn
        assert forn["ativo"] is True

    @pytest.mark.asyncio
    async def test_listar_fornecedores_por_categorias(self, client):
        """RF12, RF13 - Filtrar fornecedores por categorias selecionadas"""
        # Busca categorias existentes
        cat_resp = await client.get("/v1/categorias")
        categorias = cat_resp.json()
        cat_ids = [c["id"] for c in categorias[:2]]

        response = await client.get(
            f"/v1/fornecedores?categoria_ids={cat_ids[0]},{cat_ids[1]}"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Todos fornecedores retornados devem ter pelo menos uma das categorias
        for forn in data:
            forn_cat_ids = [c["id"] for c in forn.get("categorias", [])]
            assert any(cid in cat_ids for cid in forn_cat_ids)

    @pytest.mark.asyncio
    async def test_autocomplete_produtos(self, client):
        """RF07, UC02 - Autocomplete para criação de lista"""
        # Busca por termo parcial
        response = await client.get("/v1/produtos/autocomplete?q=Arroz&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        
        if data:
            prod = data[0]
            assert "id" in prod
            assert "nome" in prod
            assert "unidade" in prod
            # Termo buscado deve estar no nome
            assert "arroz" in prod["nome"].lower()

    @pytest.mark.asyncio
    async def test_autocomplete_limite_resultados(self, client):
        response = await client.get("/v1/produtos/autocomplete?q=a&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3

    @pytest.mark.asyncio
    async def test_autocomplete_query_vazia(self, client):
        response = await client.get("/v1/produtos/autocomplete?q=")
        # Query vazia pode retornar lista vazia ou todos (comportamento definido)
        assert response.status_code in (200, 400)

    @pytest.mark.asyncio
    async def test_listar_produtos_ativos(self, client):
        response = await client.get("/v1/produtos")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert data["total"] >= 50  # Seed tem 50 produtos

    @pytest.mark.asyncio
    async def test_buscar_produto_por_id(self, client):
        # Pega primeiro produto da lista
        list_resp = await client.get("/v1/produtos?limit=1")
        first_prod = list_resp.json()["items"][0]
        
        response = await client.get(f"/v1/produtos/{first_prod['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == first_prod["id"]
        assert data["nome"] == first_prod["nome"]
        assert "unidade" in data


class TestCatalogoPrefiltroComparacao:
    """Testes para pré-filtro por categorias na comparação (RF12, UC03)"""

    @pytest.mark.asyncio
    async def test_fornecedores_com_categorias_para_comparacao(self, client):
        """Fornecedores retornados devem incluir categorias para UI de pré-filtro"""
        response = await client.get("/v1/fornecedores")
        assert response.status_code == 200
        data = response.json()
        
        for forn in data:
            assert "categorias" in forn
            assert isinstance(forn["categorias"], list)
            for cat in forn["categorias"]:
                assert "id" in cat
                assert "nome" in cat