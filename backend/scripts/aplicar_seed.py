#!/usr/bin/env python3
"""
COBECO — Aplicar arquivo SQL de seed em uma base PostgreSQL.
Divide o arquivo por ';' e executa statement a statement via asyncpg.

Uso:
  DATABASE_URL=postgresql+asyncpg://... python scripts/aplicar_seed.py seed_from_csv.sql
"""

import asyncio
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def aplicar(database_url: str, sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    # Remove comentários de linha (-- ...) para não quebrar o split por ';'
    linhas_limpas = []
    for linha in sql.splitlines():
        idx = linha.find("--")
        if idx != -1:
            linha = linha[:idx]
        linhas_limpas.append(linha)
    sql_sem_comentario = "\n".join(linhas_limpas)
    statements = [s.strip() for s in sql_sem_comentario.split(";") if s.strip()]

    engine = create_async_engine(database_url)
    async with engine.begin() as conn:
        for stmt in statements:
            stmt_limpo = " ".join(parte for parte in stmt.split() if parte)
            if not stmt_limpo:
                continue
            await conn.execute(text(stmt_limpo))
            print(f"OK: {stmt_limpo[:70]}...")
    await engine.dispose()
    print(f"\nSeed aplicado em {sql_path.name}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python scripts/aplicar_seed.py <arquivo.sql>")
        sys.exit(1)
    sql_path = Path(sys.argv[1])
    import os
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL não definida")
        sys.exit(1)
    asyncio.run(aplicar(database_url, sql_path))


if __name__ == "__main__":
    main()