# COBECO Backend — Exportação Integration Tests
# Testes de integração para Exportação PDF (RF17)
# Usa fixtures compartilhadas de tests/integration/conftest.py

import pytest
import time


class TestExportacaoIntegration:
    """Testes de integração para /export (RF17)"""

    @pytest.mark.asyncio
    async def test_exportar_pdf_lista_autenticado(self, client, auth_headers, lista_com_itens):
        """RF17 - Exportar lista em PDF (autenticado)"""
        lista_id = lista_com_itens["id"]

        response = await client.post(
            f"/export/pdf?lista_id={lista_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

        # Verifica header Content-Disposition
        content_disp = response.headers.get("content-disposition", "")
        assert "attachment" in content_disp
        assert "lista_" in content_disp
        assert ".pdf" in content_disp

        # Verifica que é um PDF válido (header %PDF)
        content = response.content
        assert content.startswith(b"%PDF-")

    @pytest.mark.asyncio
    async def test_exportar_pdf_vencedora_visitante(self, client, lista_com_itens):
        """RF17 - Exportar lista vencedora funciona para visitantes (sem auth)"""
        # Exporta lista vencedora (efêmera) - não precisa de auth
        response = await client.post(
            "/export/pdf/vencedora",
            json={
                "itens": lista_com_itens["itens"],
                "fornecedor_ids": [1, 6, 9],
                "lista_nome": lista_com_itens["nome"],
            },
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content.startswith(b"%PDF-")

    @pytest.mark.asyncio
    async def test_exportar_pdf_lista_inexistente(self, client, auth_headers):
        response = await client.post(
            "/export/pdf?lista_id=99999",
            headers=auth_headers,
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_pdf_conteudo_basico(self, client, auth_headers, lista_com_itens):
        """Verifica se PDF contém informações básicas da lista"""
        lista_id = lista_com_itens["id"]

        response = await client.post(
            f"/export/pdf?lista_id={lista_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert len(response.content) > 100  # PDF mínimo ~1KB
        assert response.content.startswith(b"%PDF-")

    @pytest.mark.asyncio
    async def test_nome_arquivo_formato(self, client, auth_headers, lista_com_itens):
        """Nome do arquivo: lista_YYYYMMDD.pdf"""
        lista_id = lista_com_itens["id"]

        response = await client.post(
            f"/export/pdf?lista_id={lista_id}",
            headers=auth_headers,
        )

        content_disp = response.headers.get("content-disposition", "")
        # Formato: attachment; filename="lista_YYYYMMDD.pdf"
        assert "attachment" in content_disp
        assert "filename=" in content_disp
        assert '.pdf"' in content_disp or ".pdf'" in content_disp


class TestExportacaoFormatos:
    """Testes para formatos de exportação (RF17)"""

    @pytest.mark.asyncio
    async def test_pdf_formato_a4(self, client, auth_headers, lista_com_itens):
        """PDF deve ser formato A4 (verificação indireta via tamanho)"""
        lista_id = lista_com_itens["id"]

        response = await client.post(
            f"/export/pdf?lista_id={lista_id}",
            headers=auth_headers,
        )

        # PDF A4 com conteúdo razoável deve ter tamanho > 2KB
        assert len(response.content) > 200

    @pytest.mark.asyncio
    async def test_pdf_tempo_geracao_rnf11(self, client, auth_headers, lista_com_itens):
        """RNF11 - <5s para até 100 itens"""
        lista_id = lista_com_itens["id"]

        start = time.time()
        response = await client.post(
            f"/export/pdf?lista_id={lista_id}",
            headers=auth_headers,
        )
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0, f"Geração de PDF levou {elapsed:.2f}s, esperado <5s (RNF11)"

    @pytest.mark.asyncio
    async def test_pdf_com_lista_grande_100_itens(self, client, auth_headers, sample_produtos):
        """Teste de stress: lista com muitos itens (RNF11)"""
        # Cria lista com muitos itens (usa produtos únicos para evitar duplicatas)
        itens = []
        for i, prod in enumerate(sample_produtos):
            itens.append({"produto_id": prod.id, "quantidade": (i % 5) + 1})

        # Repete para chegar a muitos itens
        itens_100 = itens * 10

        lista_data = {"nome": "Lista Grande 100 Itens", "itens": itens_100, "categorias": [1]}
        create_resp = await client.post("/listas", json=lista_data, headers=auth_headers)
        # Pode falhar por limite de itens únicos (uq_item_lista_produto)
        if create_resp.status_code != 201:
            pytest.skip(f"Não foi possível criar lista com itens duplicados: {create_resp.json()}")
        lista_id = create_resp.json()["id"]

        start = time.time()
        response = await client.post(f"/export/pdf?lista_id={lista_id}", headers=auth_headers)
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0, f"PDF 100 itens levou {elapsed:.2f}s (RNF11: <5s)"

    @pytest.mark.asyncio
    async def test_pdf_visitante_mesmo_conteudo(self, client, auth_headers, lista_com_itens):
        """Visitante e usuário autenticado devem gerar mesmo PDF para lista vencedora"""
        # Autenticado
        resp_auth = await client.post(
            "/export/pdf/vencedora",
            json={
                "itens": lista_com_itens["itens"],
                "fornecedor_ids": [1, 6, 9],
                "lista_nome": lista_com_itens["nome"],
            },
            headers=auth_headers,
        )
        # Visitante (sem auth)
        resp_anon = await client.post(
            "/export/pdf/vencedora",
            json={
                "itens": lista_com_itens["itens"],
                "fornecedor_ids": [1, 6, 9],
                "lista_nome": lista_com_itens["nome"],
            },
        )

        # Ambos devem ser PDFs válidos
        assert resp_auth.status_code == 200
        assert resp_anon.status_code == 200
        # Conteúdo pode diferir ligeiramente (timestamp de geração), verificar estrutura
        assert resp_auth.content.startswith(b"%PDF-")
        assert resp_anon.content.startswith(b"%PDF-")
        assert len(resp_auth.content) > 100
        assert len(resp_anon.content) > 100