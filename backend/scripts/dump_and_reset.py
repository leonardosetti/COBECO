#!/usr/bin/env python3
"""
COBECO — Dump e Reset de Dados
Faz dump de todas as tabelas e zera o conteúdo para novo seed.
Uso: python scripts/dump_and_reset.py [--dump-only|--reset-only|--both]
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from decimal import Decimal
from typing import Any

# Adiciona backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.adapters.db.database import get_async_session_local, init_db
from src.adapters.db.models import (
    UsuarioModel,
    ListaModel,
    ItemListaModel,
    CategoriaModel,
    FornecedorModel,
    FornecedorCategoriaModel,
    ProdutoModel,
    ProdutoClasseModel,
    FornecedorProdutoModel,
    SessaoModel,
)
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession


TABLES_ORDER = [
    ("sessoes", SessaoModel),
    ("fornecedores_produtos", FornecedorProdutoModel),
    ("itens_lista", ItemListaModel),
    ("listas", ListaModel),
    ("usuarios", UsuarioModel),
    ("fornecedores_categorias", FornecedorCategoriaModel),
    ("produtos", ProdutoModel),
    ("fornecedores", FornecedorModel),
    ("categorias", CategoriaModel),
    ("produto_classes", ProdutoClasseModel),
]


def serialize_value(val: Any) -> Any:
    """Serializa valores para JSON."""
    if isinstance(val, (datetime,)):
        return val.isoformat()
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (int, float, str, bool, type(None))):
        return val
    return str(val)


async def dump_table(session: AsyncSession, table_name: str, model) -> list[dict]:
    """Faz dump de uma tabela."""
    result = await session.execute(select(model))
    rows = result.scalars().all()
    data = []
    for row in rows:
        row_dict = {}
        for col in model.__table__.columns:
            row_dict[col.name] = serialize_value(getattr(row, col.name))
        data.append(row_dict)
    print(f"  {table_name}: {len(data)} registros")
    return data


async def dump_all(output_dir: Path) -> dict:
    """Faz dump de todas as tabelas."""
    print(f"\n=== DUMP INICIADO: {datetime.now().isoformat()} ===")
    async with get_async_session_local()() as session:
        all_data = {}
        for table_name, model in TABLES_ORDER:
            all_data[table_name] = await dump_table(session, table_name, model)

        # Salva arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file = output_dir / f"dump_{timestamp}.json"
        with open(dump_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)

        # Salva também como latest
        latest_file = output_dir / "dump_latest.json"
        with open(latest_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)

        total = sum(len(v) for v in all_data.values())
        print(f"\nTotal: {total} registros em {len(all_data)} tabelas")
        print(f"Salvo em: {dump_file}")
        print(f"Link latest: {latest_file}")

        return all_data


async def reset_all(session: AsyncSession) -> None:
    """Zera todas as tabelas na ordem correta (FK)."""
    print(f"\n=== RESET INICIADO: {datetime.now().isoformat()} ===")
    for table_name, model in TABLES_ORDER:
        result = await session.execute(delete(model))
        print(f"  {table_name}: {result.rowcount} linhas removidas")
    await session.commit()
    print("\nReset concluído. Tabelas vazias, AUTO_INCREMENT mantido.")


async def reset_with_truncate(session: AsyncSession) -> None:
    """Zera tabelas com TRUNCATE (mais rápido, reseta AUTO_INCREMENT)."""
    print(f"\n=== TRUNCATE RESET INICIADO: {datetime.now().isoformat()} ===")
    table_names = [t[0] for t in TABLES_ORDER]

    # Desabilita FK checks
    await session.execute("SET FOREIGN_KEY_CHECKS = 0")

    for table_name in table_names:
        await session.execute(f"TRUNCATE TABLE `{table_name}`")
        print(f"  {table_name}: TRUNCATE executado")

    # Reabilita FK checks
    await session.execute("SET FOREIGN_KEY_CHECKS = 1")
    await session.commit()
    print("\nTruncate concluído. AUTO_INCREMENT resetado para 1.")


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Dump e reset de dados COBECO")
    parser.add_argument(
        "--mode",
        choices=["dump", "reset", "both", "truncate"],
        default="both",
        help="Operação: dump, reset (DELETE), both, ou truncate (TRUNCATE)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent.parent / "dumps",
        help="Diretório para salvar dumps",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    await init_db()

    if args.mode in ("dump", "both"):
        await dump_all(args.output_dir)

    if args.mode in ("reset", "both"):
        async with get_async_session_local()() as session:
            await reset_all(session)

    if args.mode == "truncate":
        async with get_async_session_local()() as session:
            await reset_with_truncate(session)

    print(f"\n=== CONCLUÍDO: {datetime.now().isoformat()} ===")


if __name__ == "__main__":
    asyncio.run(main())