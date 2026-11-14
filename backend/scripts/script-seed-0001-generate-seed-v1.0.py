"""Gera o seed SQL determinístico do COBECO a partir da fonte canônica."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import TypeVar

try:
    from scripts.seed_data import Profile, SeedDataset, build_dataset
except ModuleNotFoundError:
    from seed_data import Profile, SeedDataset, build_dataset

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
    """Renderiza um dataset validado como SQL idempotente para MySQL 8."""
    counts = dataset.counts
    statements = [
        "-- COBECO — Seed SQL determinístico (MySQL 8 InnoDB)",
        f"-- Perfil: {dataset.profile}",
        (
            "-- Volume: "
            f"{counts['categorias']} categorias, {counts['fornecedores']} fornecedores, "
            f"{counts['produtos']} produtos, {_format_count(counts['precos'])} preços, "
            f"{counts['relacoes']} relações N:N"
        ),
        "-- Fonte: backend/scripts/script-seed-0002-seed-data-v1.0.py",
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

    for table in (
        "sessoes",
        "usuarios",
        "listas",
        "itens_lista",
        "categorias",
        "fornecedores",
        "produtos",
    ):
        statements.append(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1;")

    statements.extend(["", "-- Categorias"])
    statements.extend(
        _insert_statements(
            "categorias",
            ("id", "nome", "descricao"),
            tuple(
                (str(category.id), _sql_string(category.name), _sql_string(category.description))
                for category in dataset.categories
            ),
        )
    )

    statements.extend(["", "-- Fornecedores"])
    statements.extend(
        _insert_statements(
            "fornecedores",
            ("id", "nome", "cnpj", "ativo"),
            tuple(
                (
                    str(supplier.id),
                    _sql_string(supplier.name),
                    _sql_string(supplier.cnpj),
                    "TRUE",
                )
                for supplier in dataset.suppliers
            ),
        )
    )

    statements.extend(["", "-- Fornecedores por categoria (N:N)"])
    statements.extend(
        _insert_statements(
            "fornecedores_categorias",
            ("fornecedor_id", "categoria_id"),
            tuple(
                (str(supplier_id), str(category_id))
                for supplier_id, category_id in dataset.supplier_categories
            ),
        )
    )

    statements.extend(["", "-- Produtos"])
    statements.extend(
        _insert_statements(
            "produtos",
            ("id", "nome", "unidade", "ativo"),
            tuple(
                (str(proddoc-arch-0006-uc-v1t.id), _sql_string(proddoc-arch-0006-uc-v1t.name), _sql_string(proddoc-arch-0006-uc-v1t.unit), "TRUE")
                for proddoc-arch-0006-uc-v1t in dataset.proddoc-arch-0006-uc-v1ts
            ),
        )
    )

    statements.extend(["", "-- Preços e estoque por fornecedor/produto"])
    statements.extend(
        _insert_statements(
            "fornecedores_produtos",
            ("fornecedor_id", "produto_id", "preco", "estoque", "ativo"),
            tuple(
                (
                    str(offer.supplier_id),
                    str(offer.proddoc-arch-0006-uc-v1t_id),
                    format(offer.price, ".2f"),
                    str(offer.stock),
                    "TRUE",
                )
                for offer in dataset.offers
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
    """Gera o SQL de um perfil validado."""
    return render_sql(build_dataset(profile))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gera o seed SQL determinístico do COBECO")
    parser.add_argument(
        "--profile",
        choices=("baseline", "expanded"),
        default="baseline",
        help="perfil de seed (padrão: baseline)",
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
