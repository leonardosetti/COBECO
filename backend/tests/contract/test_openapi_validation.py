# COBECO Backend — Contract Tests (OpenAPI Validation)
# Validação de contrato: requests/responses vs /openapi.json

import pytest
from httpx import AsyncClient


class TestOpenAPIContract:
    """Testes básicos de contrato OpenAPI"""

    @pytest.mark.asyncio
    async def test_openapi_json_accessible(self, client):
        """Verifica se /openapi.json está acessível e retorna JSON válido"""
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        spec = response.json()
        assert spec["openapi"] == "3.1.0"
        assert spec["info"]["title"] == "COBECO MVP"
        assert spec["info"]["version"] == "0.1.0"

    @pytest.mark.asyncio
    async def test_openapi_has_required_paths(self, client):
        """Verifica se endpoints críticos estão documentados no OpenAPI"""
        response = await client.get("/openapi.json")
        spec = response.json()
        paths = spec.get("paths", {})
        
        # Endpoints críticos que devem existir
        critical_paths = [
            "/health",
            "/auth/cadastrar",
            "/auth/login",
            "/auth/logout",
            "/auth/refresh",
            "/auth/recuperar-senha/solicitar",
            "/auth/recuperar-senha/confirmar",
            "/auth/perfil",
            "/listas",
            "/listas/promover-efemera",
            "/catalogo/categorias",
            "/catalogo/fornecedores",
            "/catalogo/produtos/autocomplete",
            "/catalogo/produtos",
            "/produtos",
            "/comparacao/calcular",
            "/comparacao/calcular-efemera",
            "/export/pdf",
            "/export/pdf/vencedora",
            "/perfil/health",
        ]
        
        for path in critical_paths:
            # Verifica se o path template existe no schema (com parâmetros)
            found = False
            for schema_path in paths.keys():
                if self._path_matches(path, schema_path):
                    found = True
                    break
            assert found, f"Endpoint {path} não documentado no OpenAPI spec"

    @pytest.mark.asyncio
    async def test_openapi_has_security_scheme(self, client):
        """Verifica se o esquema de segurança OAuth2 está definido"""
        response = await client.get("/openapi.json")
        spec = response.json()
        
        security_schemes = spec.get("components", {}).get("securitySchemes", {})
        assert "OAuth2PasswordBearer" in security_schemes
        assert security_schemes["OAuth2PasswordBearer"]["type"] == "oauth2"
        assert "password" in security_schemes["OAuth2PasswordBearer"]["flows"]
        assert security_schemes["OAuth2PasswordBearer"]["flows"]["password"]["tokenUrl"] == "/v1/auth/login"

    @pytest.mark.asyncio
    async def test_openapi_has_error_schema(self, client):
        """Verifica se o schema de erro HTTPValidationError está definido"""
        response = await client.get("/openapi.json")
        spec = response.json()
        
        schemas = spec.get("components", {}).get("schemas", {})
        assert "HTTPValidationError" in schemas
        assert "ValidationError" in schemas

    def _path_matches(self, route_path, schema_path):
        """Verifica se route_path corresponde a schema_path (com params)"""
        import re
        
        # Converte schema_path para regex
        pattern = schema_path
        pattern = pattern.replace("{lista_id}", r"[^/]+")
        pattern = pattern.replace("{fornecedor_id}", r"[^/]+")
        pattern = pattern.replace("{id}", r"[^/]+")
        pattern = "^" + pattern + "$"
        
        return bool(re.match(pattern, route_path))


class TestOpenAPISchemaValidation:
    """Testes de validação do schema OpenAPI gerado"""

    @pytest.mark.asyncio
    async def test_openapi_spec_valid_json(self, client):
        """Verifica se o spec é JSON válido e bem formado"""
        response = await client.get("/openapi.json")
        spec = response.json()
        
        # Campos obrigatórios do OpenAPI 3.1.0
        assert "openapi" in spec
        assert "info" in spec
        assert "paths" in spec
        assert "components" in spec

    @pytest.mark.asyncio
    async def test_openapi_info_section(self, client):
        """Verifica seção info do OpenAPI"""
        response = await client.get("/openapi.json")
        spec = response.json()
        info = spec["info"]
        
        assert info["title"] == "COBECO MVP"
        assert info["version"] == "0.1.0"
        assert "description" in info

    @pytest.mark.asyncio
    async def test_openapi_servers_section(self, client):
        """Verifica seção servers do OpenAPI"""
        response = await client.get("/openapi.json")
        spec = response.json()
        servers = spec.get("servers", [])
        
        assert len(servers) >= 1
        assert servers[0]["url"] == "/v1"