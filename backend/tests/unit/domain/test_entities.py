# COBECO Backend — Domain Entities Unit Tests
# Testes para Entidades: Usuario, Categoria, Fornecedor, Produto, Lista, ItemLista, etc.

import pytest
from datetime import datetime
from decimal import Decimal
from src.domain.entities import (
    Usuario, Categoria, Fornecedor, Produto,
    FornecedorProduto, Lista, ItemLista,
    ItemComparacao, FornecedorComparacao, OrcamentoComparacao,
    Sessao, Email, CNPJ, SenhaHash, UnidadeMedida
)


class TestUsuario:
    """Testes para Entidade Usuario"""

    def test_usuario_criacao_valida(self):
        usuario = Usuario(
            id=1,
            nome_usuario="usuario_teste",
            email=Email("teste@exemplo.com"),
            nome="Usuário Teste",
            senha_hash=SenhaHash("$2b$12$hash"),
            pergunta_seguranca="nome_mae",
            resposta_seguranca_hash=SenhaHash("$2b$12$hash"),
        )
        assert usuario.id == 1
        assert usuario.nome_usuario == "usuario_teste"
        assert usuario.email.valor == "teste@exemplo.com"
        assert usuario.esta_ativo() is True

    def test_usuario_nome_usuario_muito_curto(self):
        with pytest.raises(ValueError, match="nome_usuario deve ter 3-30 caracteres"):
            Usuario(nome_usuario="ab", email=Email("a@b.com"), nome="Nome")

    def test_usuario_nome_usuario_muito_longo(self):
        with pytest.raises(ValueError, match="nome_usuario deve ter 3-30 caracteres"):
            Usuario(nome_usuario="a" * 31, email=Email("a@b.com"), nome="Nome")

    def test_usuario_nome_usuario_nao_alfanumerico(self):
        with pytest.raises(ValueError, match="nome_usuario deve ser alfanumérico"):
            Usuario(nome_usuario="usuario-teste", email=Email("a@b.com"), nome="Nome")

    def test_usuario_nome_muito_curto(self):
        with pytest.raises(ValueError, match="nome deve ter 2-10 caracteres"):
            Usuario(nome_usuario="usuario", email=Email("a@b.com"), nome="A")

    def test_usuario_nome_muito_longo(self):
        with pytest.raises(ValueError, match="nome deve ter 2-10 caracteres"):
            Usuario(nome_usuario="usuario", email=Email("a@b.com"), nome="A" * 11)

    def test_usuario_soft_delete(self):
        usuario = Usuario(nome_usuario="usuario", email=Email("a@b.com"), nome="Nome")
        assert usuario.esta_ativo() is True
        usuario.soft_delete()
        assert usuario.esta_ativo() is False
        assert usuario.deletado_em is not None


class TestCategoria:
    """Testes para Entidade Categoria"""

    def test_categoria_criacao_valida(self):
        categoria = Categoria(id=1, nome="Supermercados", descricao="Grandes redes")
        assert categoria.nome == "Supermercados"
        assert categoria.descricao == "Grandes redes"

    def test_categoria_nome_obrigatorio(self):
        with pytest.raises(ValueError, match="nome da categoria é obrigatório"):
            Categoria(nome="")

    def test_categoria_nome_apenas_espacos(self):
        with pytest.raises(ValueError, match="nome da categoria é obrigatório"):
            Categoria(nome="   ")


class TestFornecedor:
    """Testes para Entidade Fornecedor"""

    def test_fornecedor_criacao_valida(self):
        fornecedor = Fornecedor(
            id=1,
            nome="Supermercado ABC",
            cnpj=CNPJ("12.345.678/0001-95"),
            ativo=True,
        )
        assert fornecedor.nome == "Supermercado ABC"
        assert fornecedor.cnpj.valor == "12.345.678/0001-95"
        assert fornecedor.ativo is True

    def test_fornecedor_nome_obrigatorio(self):
        with pytest.raises(ValueError, match="nome do fornecedor é obrigatório"):
            Fornecedor(nome="", cnpj=CNPJ("12345678000195"))

    def test_fornecedor_categorias_inicializa_vazio(self):
        fornecedor = Fornecedor(nome="Teste", cnpj=CNPJ("12345678000195"))
        assert fornecedor.categorias == []


class TestProduto:
    """Testes para Entidade Produto"""

    def test_produto_criacao_valida(self):
        produto = Produto(
            id=1,
            nome="Arroz Tipo 1 5kg",
            unidade=UnidadeMedida.KG,
            ativo=True,
        )
        assert produto.nome == "Arroz Tipo 1 5kg"
        assert produto.unidade == UnidadeMedida.KG

    def test_produto_nome_obrigatorio(self):
        with pytest.raises(ValueError, match="nome do produto é obrigatório"):
            Produto(nome="")

    def test_produto_unidade_default(self):
        produto = Produto(nome="Teste")
        assert produto.unidade == UnidadeMedida.UN


class TestFornecedorProduto:
    """Testes para Entidade FornecedorProduto (Preços e Estoque)"""

    def test_fornecedor_produto_criacao_valida(self):
        fp = FornecedorProduto(
            fornecedor_id=1,
            produto_id=1,
            preco=Decimal("12.90"),
            estoque=10,
            ativo=True,
        )
        assert fp.preco == Decimal("12.90")
        assert fp.estoque == 10

    def test_fornecedor_produto_preco_negativo(self):
        with pytest.raises(ValueError, match="preco não pode ser negativo"):
            FornecedorProduto(fornecedor_id=1, produto_id=1, preco=Decimal("-1.00"))

    def test_fornecedor_produto_estoque_negativo(self):
        with pytest.raises(ValueError, match="estoque não pode ser negativo"):
            FornecedorProduto(fornecedor_id=1, produto_id=1, preco=Decimal("10.00"), estoque=-1)


class TestLista:
    """Testes para Entidade Lista"""

    def test_lista_criacao_valida(self):
        lista = Lista(
            id=1,
            usuario_id=1,
            nome="Compras da Semana",
        )
        assert lista.nome == "Compras da Semana"
        assert lista.usuario_id == 1
        assert lista.esta_ativa() is True

    def test_lista_nome_obrigatorio(self):
        with pytest.raises(ValueError, match="nome da lista deve ter 1-10 caracteres"):
            Lista(usuario_id=1, nome="")

    def test_lista_nome_muito_longo(self):
        with pytest.raises(ValueError, match="nome da lista deve ter 1-10 caracteres"):
            Lista(usuario_id=1, nome="A" * 11)

    def test_lista_soft_delete_com_confirmacao(self):
        lista = Lista(usuario_id=1, nome="Teste")
        lista.soft_delete("Teste")
        assert lista.esta_ativa() is False

    def test_lista_soft_delete_confirmacao_incorreta(self):
        lista = Lista(usuario_id=1, nome="Teste")
        with pytest.raises(ValueError, match="Confirmação de nome incorreta"):
            lista.soft_delete("Nome Errado")


class TestItemLista:
    """Testes para Entidade ItemLista"""

    def test_item_lista_criacao_valida(self):
        item = ItemLista(
            id=1,
            lista_id=1,
            produto_id=1,
            quantidade=5,
        )
        assert item.quantidade == 5

    def test_item_lista_quantidade_minima(self):
        with pytest.raises(ValueError, match="quantidade deve ser entre 1 e 9999"):
            ItemLista(lista_id=1, produto_id=1, quantidade=0)

    def test_item_lista_quantidade_maxima(self):
        with pytest.raises(ValueError, match="quantidade deve ser entre 1 e 9999"):
            ItemLista(lista_id=1, produto_id=1, quantidade=1000)


class TestEntidadesComparacao:
    """Testes para Entidades de Comparação (RF15, RF16)"""

    def test_item_comparacao_criacao(self):
        item = ItemComparacao(
            produto_id=1,
            produto_nome="Arroz 5kg",
            unidade="kg",
            quantidade=2,
            preco_unitario=Decimal("12.50"),
            preco_total=Decimal("25.00"),
            disponivel=True,
        )
        assert item.preco_total == Decimal("25.00")

    def test_fornecedor_comparacao_criacao(self):
        forn = FornecedorComparacao(
            fornecedor_id=1,
            fornecedor_nome="Supermercado ABC",
            itens_disponiveis=8,
            itens_ausentes=2,
            preco_total=Decimal("150.00"),
            percentual_disponibilidade=80.0,
        )
        assert forn.percentual_disponibilidade == 80.0

    def test_orcamento_comparacao_ordenacao(self):
        orcamento = OrcamentoComparacao(
            lista_id=1,
            lista_nome="Lista Teste",
            fornecedores=[
                FornecedorComparacao(fornecedor_id=2, fornecedor_nome="B", preco_total=Decimal("200.00")),
                FornecedorComparacao(fornecedor_id=1, fornecedor_nome="A", preco_total=Decimal("100.00")),
                FornecedorComparacao(fornecedor_id=3, fornecedor_nome="C", preco_total=Decimal("150.00")),
            ],
        )
        orcamento.ordenar_por_preco()
        assert orcamento.fornecedores[0].fornecedor_id == 1
        assert orcamento.fornecedores[1].fornecedor_id == 3
        assert orcamento.fornecedores[2].fornecedor_id == 2
        assert orcamento.melhor_fornecedor_id == 1

    def test_orcamento_comparacao_vazio(self):
        orcamento = OrcamentoComparacao(lista_id=1, lista_nome="Vazia")
        orcamento.ordenar_por_preco()
        assert orcamento.melhor_fornecedor_id is None


class TestSessao:
    """Testes para Entidade Sessao (Refresh Tokens)"""

    def test_sessao_criacao_valida(self):
        sessao = Sessao(
            id=1,
            usuario_id=1,
            refresh_token_hash="hash123",
            expira_em=datetime.now().replace(year=227),
        )
        assert sessao.esta_ativa() is True

    def test_sessao_expirada(self):
        sessao = Sessao(
            id=1,
            usuario_id=1,
            refresh_token_hash="hash123",
            expira_em=datetime(220, 1, 1),
        )
        assert sessao.esta_ativa() is False

    def test_sessao_revogada(self):
        sessao = Sessao(
            id=1,
            usuario_id=1,
            refresh_token_hash="hash123",
            expira_em=datetime.now().replace(year=227),
            revogada_em=datetime.now(),
        )
        assert sessao.esta_ativa() is False

    def test_sessao_revogar(self):
        sessao = Sessao(
            id=1,
            usuario_id=1,
            refresh_token_hash="hash123",
            expira_em=datetime.now().replace(year=227),
        )
        assert sessao.revogada_em is None
        sessao.revogar()
        assert sessao.revogada_em is not None
        assert sessao.esta_ativa() is False