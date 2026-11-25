"""Seed do protótipo alta fidelidade (doc-prototype-0003 v3.2).

Gera o SQL determinístico que popula o banco com EXATAMENTE os dados do
frontend (DOC-03): 11 categorias, 10 fornecedores, 20 produtos, CATALOGO
(fornecedor -> produtos) e preços calculados pela mesma regra do protótipo
(preco = base * FATOR[f] * (1 + sin(f*997 + p*131)*0.03)).

O estoque é fixado em 9999 (o protótipo não modela estoque; todo item do
CATALOGO está disponível).
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

# ---------------------------------------------------------------------------
# Dados do protótipo DOC-03 (fonte canônica do frontend)
# ---------------------------------------------------------------------------
CATEGORIAS = [
    (1, "Mercado", "Supermercados, mercearias e atacados"),
    (2, "Vestuário", "Roupas, calçados e acessórios"),
    (3, "Automotivos", "Peças, acessórios e serviços automotivos"),
    (4, "Informática", "Computadores, periféricos e eletrônicos"),
    (5, "Decoração", "Itens de decoração e artigos para casa"),
    (6, "Móveis", "Móveis residenciais e corporativos"),
    (7, "Materiais de Construção e Ferragens", "Materiais de construção, ferramentas e ferragens"),
    (8, "Ferramentas", "Ferramentas manuais, elétricas e de medição"),
    (9, "Livros", "Livros, revistas e publicações"),
    (10, "Jardinagem", "Plantas, ferramentas e artigos de jardim"),
    (11, "Eletrodomésticos", "Eletrodomésticos de linha branca e marrom"),
]

# (id, nome, cnpj, [categorias]) — IDs do protótipo DOC-03
FORNECEDORES = [
    (1, "Carrefour", "99.000.111/0001-22", [1, 2, 3, 5, 11, 4]),
    (2, "Extra", "00.111.222/0001-33", [1, 2, 9, 11]),
    (3, "Pão de Açúcar", "66.777.888/0001-99", [1]),
    (4, "Magazine Luiza", "77.888.999/0001-00", [11, 4, 6]),
    (5, "Casas Bahia", "88.999.000/0001-11", [11, 4, 6]),
    (6, "Leroy Merlin", "11.222.333/0001-44", [7, 8, 10, 5]),
    (7, "Etna", "22.333.444/0001-55", [5, 6]),
    (8, "C&A", "33.444.555/0001-66", [2]),
    (9, "Renner", "44.555.666/0001-77", [2]),
    (10, "Hering", "55.666.777/0001-88", [2]),
]

# (id, nome, un, base)
PRODUTOS = [
    (1, "Arroz Tipo 1 5kg", "un", 25.90),
    (2, "Feijão Preto 1kg", "un", 8.20),
    (3, "Óleo de Soja 900ml", "un", 6.90),
    (4, "Café Torrado e Moído 500g", "un", 17.50),
    (5, "Açúcar Refinado 1kg", "un", 4.40),
    (6, "Leite Integral UHT 1L", "un", 5.10),
    (7, "Macarrão Espaguete 500g", "un", 4.80),
    (8, "Molho de Tomate 340g", "un", 3.90),
    (9, "Farinha de Trigo 1kg", "un", 5.50),
    (10, "Ovos Brancos (dúzia)", "dz", 9.90),
    (11, "Detergente Neutro 500ml", "un", 2.90),
    (12, "Papel Toalha 2 rolos", "un", 6.50),
    (13, "Liquidificador 2 Velocidades", "un", 129.90),
    (14, "Notebook i5 8GB", "un", 2899.00),
    (15, "Martelo de Unha 25mm", "un", 32.90),
    (16, "Parafuso Philips 5mm (cx)", "cx", 12.50),
    (17, "Camiseta Algodão M", "un", 39.90),
    (18, "Calça Jeans 40", "un", 119.90),
    (19, "Vaso de Barro 20cm", "un", 45.90),
    (20, "Cadeira de Escritório", "un", 449.90),
]

# fornecedor_id -> [produto_ids]
CATALOGO = {
    1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18],
    2: [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17],
    3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    4: [13, 14, 20],
    5: [13, 14, 20],
    6: [15, 16, 19, 20],
    7: [19, 20],
    8: [17, 18],
    9: [17, 18],
    10: [17],
}

FATOR = {1: 0.99, 2: 0.93, 3: 1.14, 4: 0.96, 5: 1.05, 6: 0.97, 7: 1.10, 8: 0.95, 9: 1.00, 10: 1.04}

STOCK = 9999


def _sql_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("'", "''")
    return f"'{escaped}'"


def preco(fid: int, pid: int, base: float) -> str:
    """Replica exata do preco() do protótipo (JS), arredondando .5 para cima."""
    jit = math.sin(fid * 997 + pid * 131) * 0.03
    val = base * FATOR[fid] * (1 + jit)
    cents = Decimal(str(val * 100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return f"{cents / Decimal(100):.2f}"


def render_sql() -> str:
    lines = [
        "-- COBECO — Seed do protótipo alta fidelidade (doc-prototype-0003 v3.2)",
        "-- Fonte: frontend (DOC-03) — 11 categorias, 10 fornecedores, 20 produtos",
        "-- Geração determinística a partir de backend/scripts/script-seed-0003-prototype-seed-v1.0.py",
        "",
        "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
        "-- Limpeza idempotente dos dados mockados",
        "DELETE FROM `sessoes`;",
        "DELETE FROM `fornecedores_produtos`;",
        "DELETE FROM `fornecedores_categorias`;",
        "DELETE FROM `itens_lista`;",
        "DELETE FROM `listas`;",
        "DELETE FROM `usuarios`;",
        "DELETE FROM `produtos`;",
        "DELETE FROM `fornecedores`;",
        "DELETE FROM `categorias`;",
        "",
    ]
    for table in ("sessoes", "usuarios", "listas", "itens_lista", "categorias", "fornecedores", "produtos"):
        lines.append(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1;")

    lines.extend(["", "-- Categorias (11 macro — protótipo DOC-03)"])
    values = ",\n".join(
        f"  ({cid}, {_sql_string(nome)}, {_sql_string(desc)})" for cid, nome, desc in CATEGORIAS
    )
    lines.append(f"INSERT INTO `categorias` (`id`, `nome`, `descricao`) VALUES\n{values};")

    lines.extend(["", "-- Fornecedores (10 — IDs do protótipo DOC-03)"])
    values = ",\n".join(
        f"  ({fid}, {_sql_string(nome)}, {_sql_string(cnpj)}, TRUE)"
        for fid, nome, cnpj, _ in FORNECEDORES
    )
    lines.append(f"INSERT INTO `fornecedores` (`id`, `nome`, `cnpj`, `ativo`) VALUES\n{values};")

    lines.extend(["", "-- Fornecedores por categoria (N:N)"])
    rows = []
    for fid, nome, cnpj, cats in FORNECEDORES:
        for cid in cats:
            rows.append(f"  ({fid}, {cid})")
    lines.append(f"INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES\n" + ",\n".join(rows) + ";")

    lines.extend(["", "-- Produtos (20 — protótipo DOC-03)"])
    values = ",\n".join(
        f"  ({pid}, {_sql_string(nome)}, {_sql_string(un)}, TRUE)" for pid, nome, un, _ in PRODUTOS
    )
    lines.append(f"INSERT INTO `produtos` (`id`, `nome`, `unidade`, `ativo`) VALUES\n{values};")

    lines.extend(["", "-- Preços e estoque (regra do protótipo: base * FATOR[f] * (1 + sin*0.03))"])
    offer_rows = []
    for fid, nome, cnpj, cats in FORNECEDORES:
        for pid in CATALOGO[fid]:
            base = dict((p[0], p[3]) for p in PRODUTOS)[pid]
            price = preco(fid, pid, base)
            offer_rows.append(f"  ({fid}, {pid}, {price}, {STOCK}, TRUE)")
    lines.append(
        "INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES\n"
        + ",\n".join(offer_rows)
        + ";"
    )

    lines.extend(
        [
            "",
            "SET FOREIGN_KEY_CHECKS = 1;",
            "",
            "-- Verificação do volume persistido",
            "SELECT 'categorias' AS tabela, COUNT(*) AS quantidade FROM `categorias`",
            "UNION ALL SELECT 'fornecedores', COUNT(*) FROM `fornecedores`",
            "UNION ALL SELECT 'produtos', COUNT(*) FROM `produtos` WHERE `ativo` = TRUE",
            "UNION ALL SELECT 'precos', COUNT(*) FROM `fornecedores_produtos` WHERE `ativo` = TRUE",
            "UNION ALL SELECT 'relacoes', COUNT(*) FROM `fornecedores_categorias`;",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    output = Path(__file__).resolve().parent.parent / "config-seed-0001-seed-v1.0.sql"
    output.write_text(render_sql(), encoding="utf-8", newline="\n")
    print(f"SQL escrito em {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
