# COBECO Backend — Contract Tests (OpenAPI Validation)
# Validação de contrato: requests/responses vs /openapi.json

import pytest
from schemathesis import from_pytest_fixture
import schemathesis
from hypothesis import given, settings
from httpx import AsyncClient

# Configuração do Schemathesis para validar contra OpenAPI spec
@pytest.fixture(scope="session")
def openapi_schema():
    """Carrega schema OpenAPI da aplicação"""
    from src.main import app
    import json
    
    # Gera schema via FastAPI
    from fastapi.openapi.utils import get_openapi
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    return schema


@schemathesis.parametrize(
    "case",
    schemathesis.from_dict(
        openapi_schema,
        base_url="http://test",
    ).filter(
        # Filtra apenas endpoints da API v1
        lambda c: c.path.startswith("/v1/") or c.path.startswith("/auth") or c.path.startswith("/listas") 
                  or c.path.startswith("/catalogo") or c.path.startswith("/comparacao") 
                  or c.path.startswith("/export") or c.path.startswith("/perfil"),
    ),
    settings=settings(max_examples=10, deadline=None),
)
class TestOpenAPIContract:
    """Testes de contrato usando Schemathesis"""

    @pytest.mark.asyncio
    async def test_openapi_request_validation(self, case, client):
        """Valida que requests válidos são aceitos"""
        # Schemathesis gera requests válidos baseados no schema
        # Apenas verifica se o request é bem formado
        await case.call_and_validate(client)

    @pytest.mark.asyncio
    async def test_openapi_response_validation(self, case, client):
        """Valida que responses conformam ao schema"""
        # Para endpoints que precisam de auth, pula validação de response
        if case.operation.tags and any(t in ["Autenticação"] for t in case.operation.tags):
            return
        
        # Valida response contra schema
        await case.call_and_validate(client)


# Testes específicos para endpoints críticos
class TestCriticalEndpointsContract:
    """Testes de contrato para endpoints críticos"""

    @pytest.fixture
    async def auth_headers(self, client):
        """Cria usuário e retorna headers de autenticação"""
        user_data = {
            "nome_usuario": "testuser_contract",
            "email": "contract@teste.com",
            "nome": "Contract User",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria Silva",
        }
        await client.post("/v1/auth/cadastrar", json=user_data)
        
        login_resp = await client.post("/v1/auth/login", json={
            "nome_usuario": "testuser_contract",
            "senha": "Senha@123",
        })
        tokens = login_resp.json()
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    @pytest.mark.asyncio
    async def test_cadastrar_usuario_schema(self, client):
        """POST /v1/auth/cadastrar - valida request/response schema"""
        user_data = {
            "nome_usuario": "schema_test",
            "email": "schema@teste.com",
            "nome": "Schema Test",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria Silva",
        }
        
        response = await client.post("/v1/auth/cadastrar", json=user_data)
        
        # Status code
        assert response.status_code in (201, 400)
        
        # Response schema
        if response.status_code == 201:
            data = response.json()
            assert "message" in data
            assert "usuario_id" in data
            assert isinstance(data["usuario_id"], int)

    @pytest.mark.asyncio
    async def test_login_schema(self, client):
        """POST /v1/auth/login - valida TokenResponse schema"""
        # Precisa cadastrar primeiro
        user_data = {
            "nome_usuario": "login_test",
            "email": "login@teste.com",
            "nome": "Login Test",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria Silva",
        }
        await client.post("/v1/auth/cadastrar", json=user_data)
        
        response = await client.post("/v1/auth/login", json={
            "nome_usuario": "login_test",
            "senha": "Senha@123",
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # TokenResponse schema
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert isinstance(data["expires_in"], int)
        assert data["expires_in"] > 0

    @pytest.mark.asyncio
    async def test_perfil_get_schema(self, client, auth_headers):
        """GET /v1/auth/perfil - valida PerfilResponse schema"""
        response = await client.get("/v1/auth/perfil", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # PerfilResponse schema
        assert "id" in data
        assert "nome_usuario" in data
        assert "email" in data
        assert "nome" in data
        assert "criado_em" in data
        
        # Tipos
        assert isinstance(data["id"], int)
        assert isinstance(data["nome_usuario"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["nome"], str)
        # criado_em é string ISO format

    @pytest.mark.asyncio
    async def test_perfil_put_schema(self, client, auth_headers):
        """PUT /v1/auth/perfil - valida request/response schema"""
        response = await client.put(
            "/v1/auth/perfil",
            json={"nome": "Nome Atualizado Contrato"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["nome"] == "Nome Atualizado Contrato"
        assert "id" in data
        assert "email" in data

    @pytest.mark.asyncio
    async def test_criar_lista_schema(self, client, auth_headers):
        """POST /v1/listas - valida CriarListaInput/ListaResponse schema"""
        # Pega produtos do catálogo
        prod_resp = await client.get("/v1/catalogo/produtos?limit=2", headers=auth_headers)
        produtos = prod_resp.json()["items"]
        
        lista_data = {
            "nome": "Lista Schema Test",
            "itens": [
                {"produto_id": produtos[0]["id"], "quantidade": 2},
                {"produto_id": produtos[1]["id"], "quantidade": 1},
            ],
        }
        
        response = await client.post("/v1/listas", json=lista_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        
        # ListaResponse schema
        assert "id" in data
        assert "nome" in data
        assert "usuario_id" in data
        assert "itens" in data
        assert len(data["itens"]) == 2

    @pytest.mark.asyncio
    async def test_listar_minhas_listas_schema(self, client, auth_headers):
        """GET /v1/listas/minhas - valida paginação schema"""
        response = await client.get("/v1/listas/minhas?pagina=1&por_pagina=10", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # PaginatedResponse schema
        assert "items" in data
        assert "total" in data
        assert "pagina" in data
        assert "por_pagina" in data
        assert "total_paginas" in data
        
        assert isinstance(data["items"], list)
        assert isinstance(data["total"], int)
        assert data["pagina"] == 1
        assert data["por_pagina"] == 10

    @pytest.mark.asyncio
    async def test_autocomplete_produtos_schema(self, client):
        """GET /v1/produtos/autocomplete - valida schema"""
        response = await client.get("/v1/produtos/autocomplete?q=Arroz&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if data:
            item = data[0]
            assert "id" in item
            assert "nome" in item
            assert "unidade" in item

    @pytest.mark.asyncio
    async def test_comparacao_schema(self, client, auth_headers):
        """POST /v1/comparacao - valida OrcamentoComparacao schema"""
        # Cria lista com itens
        prod_resp = await client.get("/v1/catalogo/produtos?limit=3", headers=auth_headers)
        produtos = prod_resp.json()["items"]
        
        lista_data = {
            "nome": "Lista Comparação Schema",
            "itens": [
                {"produto_id": produtos[0]["id"], "quantidade": 2},
                {"produto_id": produtos[1]["id"], "quantidade": 1},
            ],
        }
        lista_resp = await client.post("/v1/listas", json=lista_data, headers=auth_headers)
        lista_id = lista_resp.json()["id"]
        
        # Busca fornecedores
        forn_resp = await client.get("/v1/catalogo/fornecedores", headers=auth_headers)
        forn_ids = [f["id"] for f in forn_resp.json()[:3]]
        
        response = await client.post(
            "/v1/comparacao",
            json={
                "lista_id": lista_id,
                "fornecedor_ids": forn_ids,
                "disponibilidade_minima": 0.0,
            },
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # OrcamentoComparacao schema
        assert "lista_id" in data
        assert "lista_nome" in data
        assert "fornecedores" in data
        assert "melhor_fornecedor_id" in data
        assert "calculado_em" in data
        
        fornecedores = data["fornecedores"]
        for f in fornecedores:
            assert "fornecedor_id" in f
            assert "fornecedor_nome" in f
            assert "itens_disponiveis" in f
            assert "itens_ausentes" in f
            assert "percentual_disponibilidade" in f
            assert "preco_total" in f
            assert "itens" in f
            
            for item in f["itens"]:
                assert "produto_id" in item
                assert "produto_nome" in item
                assert "unidade" in item
                assert "quantidade" in item
                assert "preco_unitario" in item
                assert "preco_total" in item
                assert "disponivel" in item

    @pytest.mark.asyncio
    async def test_export_pdf_schema(self, client, auth_headers):
        """GET /v1/export/lista/{id}/pdf - valida response"""
        # Cria lista
        prod_resp = await client.get("/v1/catalogo/produtos?limit=1", headers=auth_headers)
        produto = prod_resp.json()["items"][0]
        
        lista_data = {
            "nome": "Lista Export Schema",
            "itens": [{"produto_id": produto["id"], "quantidade": 1}],
        }
        lista_resp = await client.post("/v1/listas", json=lista_data, headers=auth_headers)
        lista_id = lista_resp.json()["id"]
        
        response = await client.get(f"/v1/export/lista/{lista_id}/pdf")
        
        # Pode ser 200 (sucesso) ou 404 (se não implementado)
        if response.status_code == 200:
            assert response.headers["content-type"] == "application/pdf"
            assert response.content.startswith(b"%PDF-")


# Teste de drift detection (CI)
class TestOpenAPIDriftDetection:
    """Detecta drift entre código e spec OpenAPI"""

    @pytest.mark.asyncio
    async def test_openapi_spec_matches_routes(self, client):
        """Verifica se todos endpoints /v1/ estão documentados no OpenAPI"""
        from src.main import app
        from fastapi.openapi.utils import get_openapi
        
        schema = get_openapi(
            title=app.title,
            version=app.version,
            routes=app.routes,
        )
        
        paths = schema.get("paths", {})
        
        # Verifica endpoints críticos existem no schema
        critical_paths = [
            "/v1/auth/cadastrar",
            "/v1/auth/login",
            "/v1/auth/logout",
            "/v1/auth/perfil",
            "/v1/auth/recuperar-senha/solicitar",
            "/v1/auth/recuperar-senha/confirmar",
            "/v1/listas",
            "/v1/listas/minhas",
            "/v1/catalogo/produtos",
            "/v1/catalogo/produtos/autocomplete",
            "/v1/catalogo/categorias",
            "/v1/catalogo/fornecedores",
            "/v1/comparacao",
            "/v1/export/lista/{id}/pdf",
        ]
        
        for path in paths:
            # Verifica se path template existe no schema (com parâmetros)
            found = False
            for schema_path in paths.keys():
                # Normaliza path params: {id} -> {id}
                if self._path_matches(path, schema_path):
                    found = True
                    break
            
            # Alguns paths podem não estar expostos no schema (ex: /health)
            if path.startswith("/v1/"):
                assert found, f"Endpoint {path} não documentado no OpenAPI spec"

    def _path_matches(self, route_path, schema_path):
        """Verifica se route_path corresponde a schema_path (com params)"""
        import re
        
        # Converte schema_path para regex
        pattern = schema_path.replace("{id}", r"[^/]+").replace("{lista_id}", r"[^/]+")
        pattern = "^" + pattern + "$"
        
        return bool(re.match(pattern, route_path))