"""Gera o seed SQL determinístico realista para COBECO MVP v3.2.

Uso:
  python scripts/script-seed-0005-generate-realistic-seed.py --profile realistico --output /tmp/seed-realistico.sql
  python scripts/script-seed-0005-generate-realistic-seed.py --profile expandido
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any, TypeVar


def _carregar_seed_data() -> Any:
    caminho = Path(__file__).resolve().parent / "script-seed-0004-realistic-seed-data.py"
    spec = importlib.util.spec_from_file_location("realistic_seed_data", caminho)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


_seed_data = _carregar_seed_data()
Profile = _seed_data.Profile
SeedDataset = _seed_data.SeedDataset
build_dataset = _seed_data.build_dataset


Row = tuple[str, ...]
T = TypeVar("T")


def _sql_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("'", "''")
    return f"'{escaped}'"


def _format_count(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def _chunks(values: Sequence[T], size: int) -> Iterable[Sequence[T]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _insert_statements(
    table: str,
    columns: tuple[str, ...],
    rows: Sequence[Row],
    chunk_size: int = 500,
) -> list[str]:
    statements: list[str] = []
    column_sql = ", ".join(f"`{column}`" for column in columns)
    for chunk in _chunks(rows, chunk_size):
        values = ",\n".join(f"  ({', '.join(row)})" for row in chunk)
        statements.append(f"INSERT INTO `{table}` ({column_sql}) VALUES\n{values};")
    return statements


def render_sql(dataset: SeedDataset) -> str:
    counts = dataset.counts
    statements = [
        "-- COBECO — Seed SQL realista e determinístico (MySQL 8 InnoDB)",
        f"-- Perfil: {dataset.profile}",
        (
            "-- Volume: "
            f"{counts['categorias']} categorias, {counts['fornecedores']} fornecedores, "
            f"{counts['produtos']} produtos, {_format_count(counts['precos'])} preços, "
            f"{counts['relacoes']} relações N:N"
        ),
        "-- Fonte: backend/scripts/script-seed-0004-realistic-seed-data.py",
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
        statements.append(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1;")

    # Categorias
    statements.extend(["", "-- Categorias"])
    statements.extend(
        _insert_statements(
            "categorias",
            ("id", "nome", "descricao"),
            tuple(
                (str(c.id), _sql_string(c.name), _sql_string(c.description))
                for c in dataset.categories
            ),
        )
    )

    # Fornecedores
    statements.extend(["", "-- Fornecedores"])
    statements.extend(
        _insert_statements(
            "fornecedores",
            ("id", "nome", "cnpj", "ativo"),
            tuple(
                (str(s.id), _sql_string(s.name), _sql_string(s.cnpj), "TRUE")
                for s in dataset.suppliers
            ),
        )
    )

    # Fornecedores por categoria (N:N)
    statements.extend(["", "-- Fornecedores por categoria (N:N)"])
    statements.extend(
        _insert_statements(
            "fornecedores_categorias",
            ("fornecedor_id", "categoria_id"),
            tuple(
                (str(sid), str(cid)) for sid, cid in dataset.supplier_categories
            ),
        )
    )

    # Produtos
    statements.extend(["", "-- Produtos"])
    statements.extend(
        _insert_statements(
            "produtos",
            ("id", "nome", "marca", "unidade", "ativo"),
            tuple(
                (
                    str(p.id),
                    _sql_string(p.name),
                    _sql_string(p.marca or ""),
                    _sql_string(p.unit),
                    "TRUE",
                )
                for p in dataset.products
            ),
        )
    )

    # Preços e estoque por fornecedor/produto
    statements.extend(["", "-- Preços e estoque por fornecedor/produto"])
    statements.extend(
        _insert_statements(
            "fornecedores_produtos",
            ("fornecedor_id", "produto_id", "preco", "estoque", "ativo"),
            tuple(
                (
                    str(o.supplier_id),
                    str(o.product_id),
                    format(o.price, ".2f"),
                    str(o.stock),
                    "TRUE",
                )
                for o in dataset.offers
            ),
        )
    )

    statements.extend(
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
    return "\n".join(statements)


def generate_sql(profile: Profile) -> str:
    return render_sql(build_dataset(profile))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gera o seed SQL realista do COBECO")
    parser.add_argument(
        "--profile",
        choices=("realistico", "expandido"),
        default="realistico",
        help="perfil de seed (padrão: realistico)",
    )
    parser.add_argument("--output", type=Path, help="arquivo de saída; omitir envia para stdout")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    sql = generate_sql(args.profile)
    if args.output is None:
        sys.stdout.write(sql)
    else:
        with args.output.open("w", encoding="utf-8", newline="\n") as file:
            file.write(sql)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
