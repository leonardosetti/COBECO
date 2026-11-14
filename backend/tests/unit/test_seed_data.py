"""Testes da fonte canônica e do gerador de seed do COBECO."""

from __future__ import annotations

import unicodedata
from collections import Counter

import pytest

from scripts.generate_seed import render_sql
from scripts.seed_data import build_dataset, is_valid_cnpj, make_cnpj, normalize_text


@pytest.mark.parametrize(
    ("profile", "expected"),
    [
        (
            "baseline",
            {
                "categorias": 11,
                "fornecedores": 10,
                "produtos": 50,
                "precos": 300,
                "relacoes": 25,
            },
        ),
        (
            "expanded",
            {
                "categorias": 26,
                "fornecedores": 60,
                "produtos": 2_600,
                "precos": 31_200,
                "relacoes": 312,
            },
        ),
    ],
)
def test_perfis_possuem_contagens_exatas(profile, expected):
    assert build_dataset(profile).counts == expected


def test_normalizacao_usa_nfc_e_colapsa_espacos():
    value = "  Café\tTorra do\n Pão  "
    normalized = normalize_text(value)

    assert normalized == "Café Torra do Pão"
    assert normalized == unicodedata.normalize("NFC", normalized)
    assert normalize_text("produto\x00inválido") == "produtoinválido"


def test_cnpj_ficticio_tem_formato_e_digitos_validos():
    cnpj = make_cnpj("11222333")

    assert cnpj == "11.222.333/0001-81"
    assert is_valid_cnpj(cnpj)
    assert not is_valid_cnpj("11.222.333/0001-45")
    assert not is_valid_cnpj("00.000.000/0000-00")


def test_invariantes_e_associacoes_do_perfil_expandido():
    dataset = build_dataset("expanded")
    offers_per_product = Counter(offer.product_id for offer in dataset.offers)
    suppliers_per_category = Counter(category_id for _, category_id in dataset.supplier_categories)

    assert set(offers_per_product.values()) == {12}
    assert set(suppliers_per_category.values()) == {12}
    assert all(supplier.categories for supplier in dataset.suppliers)
    assert len({supplier.cnpj for supplier in dataset.suppliers}) == dataset.counts["fornecedores"]
    assert len({product.name for product in dataset.products}) == dataset.counts["produtos"]


def test_baseline_oferece_seis_precos_por_produto():
    dataset = build_dataset("baseline")
    offers_per_product = Counter(offer.product_id for offer in dataset.offers)

    assert set(offers_per_product.values()) == {6}
    assert len(offers_per_product) == dataset.counts["produtos"]


def test_geracao_sql_e_deterministica():
    first = render_sql(build_dataset("expanded"))
    second = render_sql(build_dataset("expanded"))

    assert first == second
    assert "INSERT INTO `categorias`" in first
    assert "INSERT INTO `fornecedores_produtos`" in first
    assert "31.200 preços" in first
    assert "DELETE FROM `produtos`;" in first
