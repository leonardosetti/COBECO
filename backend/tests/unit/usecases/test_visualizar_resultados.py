# COBECO Backend — VisualizarResultadosUseCase Unit Tests

import pytest
from decimal import Decimal
from datetime import datetime
from src.domain.usecases import VisualizarResultadosUseCase
from src.domain.entities import (
    OrcamentoComparacao,
    FornecedorComparacao,
    ItemComparacao,
)


@pytest.fixture
def usecase():
    return VisualizarResultadosUseCase()


@pytest.fixture
def orcamento_exemplo():
    forn1 = FornecedorComparacao(
        fornecedor_id=1,
        fornecedor_nome="Fornecedor A",
        itens_disponiveis=2,
        itens_ausentes=0,
        percentual_disponibilidade=100.0,
        preco_total=Decimal("28.00"),
        itens=[
            ItemComparacao(
                produto_id=1,
                produto_nome="Arroz 5kg",
                unidade="kg",
                quantidade=2,
                preco_unitario=Decimal("10.00"),
                preco_total=Decimal("20.00"),
                disponivel=True,
            ),
            ItemComparacao(
                produto_id=2,
                produto_nome="Feijão 1kg",
                unidade="kg",
                quantidade=1,
                preco_unitario=Decimal("8.00"),
                preco_total=Decimal("8.00"),
                disponivel=True,
            ),
        ],
    )
    forn2 = FornecedorComparacao(
        fornecedor_id=2,
        fornecedor_nome="Fornecedor B",
        itens_disponiveis=1,
        itens_ausentes=1,
        percentual_disponibilidade=50.0,
        preco_total=Decimal("24.00"),
        itens=[
            ItemComparacao(
                produto_id=1,
                produto_nome="Arroz 5kg",
                unidade="kg",
                quantidade=2,
                preco_unitario=Decimal("12.00"),
                preco_total=Decimal("24.00"),
                disponivel=True,
            ),
            ItemComparacao(
                produto_id=2,
                produto_nome="Feijão 1kg",
                unidade="kg",
                quantidade=1,
                preco_unitario=None,
                preco_total=None,
                disponivel=False,
            ),
        ],
    )

    return OrcamentoComparacao(
        lista_id=1,
        lista_nome="Compras da Semana",
        fornecedores=[forn2, forn1],  # Já ordenado por preço
        melhor_fornecedor_id=2,
        calculado_em=datetime.now(),
    )


class TestVisualizarResultadosUseCase:
    """Testes para VisualizarResultadosUseCase (UC07/RF16)"""

    def test_formatar_para_tabela_basico(self, usecase, orcamento_exemplo):
        result = usecase.formatar_para_tabela(orcamento_exemplo)

        assert result["lista_id"] == 1
        assert result["lista_nome"] == "Compras da Semana"
        assert result["melhor_fornecedor_id"] == 2
        assert len(result["fornecedores"]) == 2

    def test_formatar_melhor_fornecedor_marcado(self, usecase, orcamento_exemplo):
        result = usecase.formatar_para_tabela(orcamento_exemplo)

        forn_melhor = next(f for f in result["fornecedores"] if f["fornecedor_id"] == 2)
        assert forn_melhor["eh_melhor"] is True

        forn_outro = next(f for f in result["fornecedores"] if f["fornecedor_id"] == 1)
        assert forn_outro["eh_melhor"] is False

    def test_formatar_itens_com_precos(self, usecase, orcamento_exemplo):
        result = usecase.formatar_para_tabela(orcamento_exemplo)

        forn1 = next(f for f in result["fornecedores"] if f["fornecedor_id"] == 1)
        item1 = next(i for i in forn1["itens"] if i["produto_id"] == 1)

        assert item1["preco_unitario"] == 10.00
        assert item1["preco_total"] == 20.00
        assert item1["disponivel"] is True
        assert item1["produto_nome"] == "Arroz 5kg"

    def test_formatar_itens_indisponiveis(self, usecase, orcamento_exemplo):
        result = usecase.formatar_para_tabela(orcamento_exemplo)

        forn2 = next(f for f in result["fornecedores"] if f["fornecedor_id"] == 2)
        item_indisponivel = next(i for i in forn2["itens"] if i["produto_id"] == 2)

        assert item_indisponivel["preco_unitario"] is None
        assert item_indisponivel["preco_total"] is None
        assert item_indisponivel["disponivel"] is False

    def test_formatar_ordenacao_mantida(self, usecase, orcamento_exemplo):
        result = usecase.formatar_para_tabela(orcamento_exemplo)

        # Deve manter a ordem do orcamento (já ordenado por preço)
        assert result["fornecedores"][0]["fornecedor_id"] == 2  # Melhor preço
        assert result["fornecedores"][1]["fornecedor_id"] == 1

    def test_formatar_valores_numericos(self, usecase, orcamento_exemplo):
        result = usecase.formatar_para_tabela(orcamento_exemplo)

        # Verifica conversão Decimal -> float
        assert isinstance(result["fornecedores"][0]["preco_total"], float)
        assert isinstance(result["fornecedores"][0]["itens"][0]["preco_unitario"], float)
        assert isinstance(result["fornecedores"][0]["percentual_disponibilidade"], float)
