# COBECO Backend — Listas Integration Tests
# Testes de integração para CRUD de Listas e Itens (RF07-RF11)
# Usa fixtures compartilhadas de tests/integration/conftest.py

import pytest


class TestListasIntegration:
    """Testes de integração para /listas"""

    @pytest.mark.asyncio
    async def test_criar_lista_com_itens(self, client, auth_headers, sample_produtos):
        """RF7, RF8 - Criar lista com itens em transação"""
        produtos = sample_produtos[:2]
        lista_data = {
            "nome": "Compras da Semana",
            "itens": [
                {"produto_id": produtos[0].id, "quantidade": 2},
                {"produto_id": produtos[1].id, "quantidade": 1},
            ],
            "categorias": [1],
        }

        response = await client.post(
            "/listas",
            json=lista_data,
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Compras da Semana"
        assert "id" in data
        assert len(data["itens"]) == 2
        assert data["itens"][0]["quantidade"] == 2
        assert data["itens"][1]["quantidade"] == 1

    @pytest.mark.asyncio
    async def test_criar_lista_sem_itens_falha(self, client, auth_headers):
        """Lista deve ter pelo menos 1 item"""
        response = await client.post(
            "/listas",
            json={"nome": "Lista Vazia", "itens": [], "categorias": [1]},
            headers=auth_headers,
        )
        assert response.status_code == 422
        assert (
            "list should have at least 1 item" in str(response.json()).lower()
            or "pelo menos 1 item" in str(response.json()).lower()
        )

    @pytest.mark.asyncio
    async def test_criar_lista_produto_inexistente(self, client, auth_headers):
        response = await client.post(
            "/listas",
            json={
                "nome": "Lista",
                "itens": [{"produto_id": 99999, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert "produto" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_listar_minhas_listas_paginacao(self, client, auth_headers, sample_produtos):
        """RF9 - Listar listas do usuário com paginação"""
        # Cria 3 listas
        for i in range(3):
            await client.post(
                "/listas",
                json={
                    "nome": f"Lista {i}",
                    "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                    "categorias": [1],
                },
                headers=auth_headers,
            )

        # Página 1, 2 por página
        response = await client.get(
            "/listas?pagina=1&por_pagina=2",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["pagina"] == 1
        assert data["por_pagina"] == 2
        assert data["total"] >= 3

        # Página 2
        response = await client.get(
            "/listas?pagina=2&por_pagina=2",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1

    @pytest.mark.asyncio
    async def test_buscar_lista_por_id(self, client, auth_headers, sample_produtos):
        """Buscar lista específica com itens"""
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Lista para Buscar",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 3}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        response = await client.get(
            f"/listas/{lista_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == lista_id
        assert data["nome"] == "Lista para Buscar"
        assert len(data["itens"]) == 1
        assert data["itens"][0]["quantidade"] == 3

    @pytest.mark.asyncio
    async def test_buscar_lista_outro_usuario_44(self, client, auth_headers, sample_produtos):
        """Usuário não pode acessar lista de outro usuário"""
        # Cria lista com user atual
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Minha Lista",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        # Cria outro usuário
        import uuid

        unique_suffix = uuid.uuid4().hex[:8]
        other_user = {
            "nome_usuario": f"outrouser{unique_suffix}",
            "email": f"outro{unique_suffix}@teste.com",
            "nome": "Outro",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "pergunta_seguranca": "nome_mae",
            "resposta_seguranca": "Maria",
        }
        await client.post("/auth/cadastrar", json=other_user)
        login_resp = await client.post(
            "/auth/login", json={"nome_usuario": other_user["nome_usuario"], "senha": "Senha@123"}
        )
        other_auth = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}

        # Tenta acessar lista do primeiro usuário
        response = await client.get(f"/listas/{lista_id}", headers=other_auth)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_atualizar_lista_nome(self, client, auth_headers, sample_produtos):
        """RF10 - Editar lista salva"""
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Nome Original",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        response = await client.put(
            f"/listas/{lista_id}",
            json={
                "nome": "Nome Atualizado",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["nome"] == "Nome Atualizado"

    @pytest.mark.asyncio
    async def test_atualizar_lista_nome_vazio_falha(self, client, auth_headers, sample_produtos):
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Original",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        response = await client.put(
            f"/listas/{lista_id}",
            json={
                "nome": "",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_excluir_lista_com_confirmacao(self, client, auth_headers, sample_produtos):
        """RF11 - Exclusão lógica com confirmação de nome"""
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Para Excluir",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        # Exclui sem confirmação - deve falhar
        response = await client.delete(
            f"/listas/{lista_id}?confirmacao_nome=Nome Errado",
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert "confirmação" in response.json()["detail"].lower()

        # Exclui com confirmação correta
        response = await client.delete(
            f"/listas/{lista_id}?confirmacao_nome=Para Excluir",
            headers=auth_headers,
        )
        assert response.status_code == 204

        # Lista não aparece mais
        list_resp = await client.get("/listas", headers=auth_headers)
        ids = [item["id"] for item in list_resp.json()["items"]]
        assert lista_id not in ids


class TestItensListaIntegration:
    """Testes para itens dentro de listas (RF07-RF11)"""

    @pytest.mark.asyncio
    async def test_adicionar_item_lista_existente(self, client, auth_headers, sample_produtos):
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Lista para Itens",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        # Adiciona item via PUT na lista
        response = await client.put(
            f"/listas/{lista_id}",
            json={
                "nome": "Lista para Itens",
                "itens": [
                    {"produto_id": sample_produtos[0].id, "quantidade": 1},
                    {"produto_id": sample_produtos[1].id, "quantidade": 2},
                ],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["itens"]) == 2
        # Verifica se quantidade do primeiro item foi mantida/atualizada
        item_quantities = {item["produto_id"]: item["quantidade"] for item in data["itens"]}
        assert item_quantities[sample_produtos[0].id] == 1
        assert item_quantities[sample_produtos[1].id] == 2

    @pytest.mark.asyncio
    async def test_remover_item_lista(self, client, auth_headers, sample_produtos):
        create_resp = await client.post(
            "/listas",
            json={
                "nome": "Lista com Item",
                "itens": [
                    {"produto_id": sample_produtos[0].id, "quantidade": 1},
                    {"produto_id": sample_produtos[1].id, "quantidade": 1},
                ],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        lista_id = create_resp.json()["id"]

        # Remove um item enviando lista sem ele
        response = await client.put(
            f"/listas/{lista_id}",
            json={
                "nome": "Lista Atualizada",
                "itens": [{"produto_id": sample_produtos[0].id, "quantidade": 1}],
                "categorias": [1],
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["itens"]) == 1
        assert data["itens"][0]["produto_id"] == sample_produtos[0].id
