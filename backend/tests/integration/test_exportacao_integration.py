# COBECO Backend — Exportação Integration Tests
# Testes de integração para Exportação PDF (RF17)

import pytest
import io
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_user(client):
    """Cria usuário autenticado"""
    user_data = {
        "nome_usuario": "testuser_export",
        "email": "export@teste.com",
        "nome": "User Export",
        "senha": "Senha@123",
        "confirmar_senha": "Senha@123",
        "pergunta_seguranca": "nome_mae",
        "resposta_seguranca": "Maria Silva",
    }
    await client.post("/v1/auth/cadastrar", json=user_data)

    login_data = {"nome_usuario": "testuser_export", "senha": "Senha@123"}
    response = await client.post("/v1/auth/login", json=login_data)
    tokens = response.json()

    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
async def lista_com_itens(client, auth_user):
    """Cria lista com itens para exportação"""
    prod_resp = await client.get("/v1/produtos?limit=5")
    produtos = prod_resp.json()["items"]

    lista_data = {
        "nome": "Lista para Exportar PDF",
        "itens": [
            {"produto_id": produtos[0]["id"], "quantidade": 2},
            {"produto_id": produtos[1]["id"], "quantidade": 1},
            {"produto_id": produtos[2]["id"], "quantidade": 3},
        ],
    }
    response = await client.post("/v1/listas", json=lista_data, headers=auth_user)
    assert response.status_code == 21
    return response.json()


class TestExportacaoIntegration:
    """Testes de integração para /export (RF17)"""

    @pytest.mark.asyncio
    async def test_exportar_pdf_lista_autenticado(self, client, auth_user, lista_com_itens):
        """RF17 - Exportar lista em PDF (autenticado)"""
        lista_id = lista_com_itens["id"]

        response = await client.get(
            f"/export/lista/{lista_id}/pdf",
            headers=auth_user,
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        
        # Verifica header Content-Disposition
        content_disp = response.headers.get("content-disposition", "")
        assert "attachment" in content_disp
        assert f"lista_{lista_id}" in content_disp or "lista_" in content_disp
        assert ".pdf" in content_disp

        # Verifica que é um PDF válido (header %PDF)
        content = response.content
        assert content.startswith(b"%PDF-")

    @pytest.mark.asyncio
    async def test_exportar_pdf_lista_visitante_sem_auth(self, client, lista_com_itens):
        """RF17 - PDF deve funcionar para visitantes (sem auth)"""
        lista_id = lista_com_itens["id"]

        response = await client.get(f"/export/lista/{lista_id}/pdf")

        # Deve funcionar sem autenticação (público)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content.startswith(b"%PDF-")

    @pytest.mark.asyncio
    async def test_exportar_pdf_lista_inexistente(self, client):
        response = await client.get("/export/lista/99999/pdf")
        assert response.status_code == 44

    @pytest.mark.asyncio
    async def test_pdf_conteudo_basico(self, client, auth_user, lista_com_itens):
        """Verifica se PDF contém informações básicas da lista"""
        lista_id = lista_com_itens["id"]

        response = await client.get(
            f"/export/lista/{lista_id}/pdf",
            headers=auth_user,
        )

        # Como não podemos parsear PDF facilmente sem lib extra,
        # verificamos apenas que é um PDF válido e tamanho razoável
        assert response.status_code == 200
        assert len(response.content) > 100  # PDF mínimo ~1KB
        assert response.content.startswith(b"%PDF-")

    @pytest.mark.asyncio
    async def test_nome_arquivo_formato(self, client, auth_user, lista_com_itens):
        """Nome do arquivo: lista_YYYYMMDD.pdf"""
        lista_id = lista_com_itens["id"]

        response = await client.get(
            f"/export/lista/{lista_id}/pdf",
            headers=auth_user,
        )

        content_disp = response.headers.get("content-disposition", "")
        # Formato: attachment; filename="lista_YYYYMMDD.pdf"
        assert "attachment" in content_disp
        assert "filename=" in content_disp
        assert ".pdf\"" in content_disp or ".pdf'" in content_disp


class TestExportacaoFormatos:
    """Testes para formatos de exportação (RF17)"""

    @pytest.mark.asyncio
    async def test_pdf_formato_a4(self, client, auth_user, lista_com_itens):
        """PDF deve ser formato A4 (verificação indireta via tamanho)"""
        lista_id = lista_com_itens["id"]

        response = await client.get(
            f"/export/lista/{lista_id}/pdf",
            headers=auth_user,
        )

        # PDF A4 com conteúdo razoável deve ter tamanho > 2KB
        assert len(response.content) > 200

    @pytest.mark.asyncio
    async def test_pdf_tempo_geracao_rnf11(self, client, auth_user, lista_com_itens):
        """RNF11 - <5s para até 10 itens"""
        import time
        
        lista_id = lista_com_itens["id"]
        
        start = time.time()
        response = await client.get(
            f"/export/lista/{lista_id}/pdf",
            headers=auth_user,
        )
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0, f"Geração de PDF levou {elapsed:.2f}s, esperado <5s (RNF11)"

    @pytest.mark.asyncio
    async def test_pdf_com_lista_grande_10_itens(self, client, auth_user):
        """Teste de stress: lista com 10 itens (RNF11)"""
        # Cria lista com muitos itens (usa produtos do seed)
        prod_resp = await client.get("/v1/produtos?limit=20")
        produtos = prod_resp.json()["items"]
        
        itens = []
        for i, prod in enumerate(produtos):
            itens.append({"produto_id": prod["id"], "quantidade": (i % 5) + 1})
            if len(itens) >= 20:
                break
        
        # Repete para chegar a ~10 itens
        itens_10 = itens * 5
        
        lista_data = {"nome": "Lista Grande 10 Itens", "itens": itens_100}
        create_resp = await client.post("/v1/listas", json=lista_data, headers=auth_user)
        assert create_resp.status_code == 21
        lista_id = create_resp.json()["id"]

        import time
        start = time.time()
        response = await client.get(f"/export/lista/{lista_id}/pdf", headers=auth_user)
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0, f"PDF 10 itens levou {elapsed:.2f}s (RNF11: <5s)"

    @pytest.mark.asyncio
    async def test_pdf_visitante_mesmo_conteudo(self, client, lista_com_itens):
        """Visitante e usuário autenticado devem gerar mesmo PDF"""
        lista_id = lista_com_itens["id"]

        # Autenticado
        user_data = {
            "nome_usuario": "testuser_export2",
            "email": "export2@teste.com",
            "nome": "User 2",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria Silva",
        }
        await client.post("/v1/auth/cadastrar", json=user_data)
        login = await client.post("/v1/auth/login", json={"nome_usuario": "testuser_export2", "senha": "Senha@123"})
        auth2 = {"Authorization": f"Bearer {login.json()['access_token']}"}

        resp_auth = await client.get(f"/export/lista/{lista_id}/pdf", headers=auth2)
        resp_anon = await client.get(f"/export/lista/{lista_id}/pdf")

        # Ambos devem ser PDFs válidos
        assert resp_auth.status_code == 20
        assert resp_anon.status_code == 20
        # Conteúdo deve ser idêntico (mesma lista)
        assert resp_auth.content == resp_anon.content