#!/usr/bin/env python3
"""
Validação rápida da busca semântica híbrida (tsvector + pgvector).

Executa contra PostgreSQL local na porta 5435 (banco de teste cobeco_test).
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from src.adapters.db.models import Base, ProdutoModel
from src.services.embedding import get_embedding_service


async def main():
    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

        # Carrega serviço de embeddings e gera vetor para consulta
        emb_service = get_embedding_service()
        query_embedding = emb_service.gerar("arroz tipo 1")
        print(f"Embedding gerado: {len(query_embedding)} dims")

        # Busca semântica via pgvector
        emb_str = "[" + ",".join(f"{v:.6f}" for v in query_embedding) + "]"
        result = await conn.execute(
            text("""
                SELECT id, nome, marca,
                       (embedding <=> :q::vector) AS distancia
                FROM produtos
                WHERE embedding IS NOT NULL
                ORDER BY distancia ASC
                LIMIT 5
            """),
            {"q": emb_str},
        )
        rows = result.mappings().all()
        print("\nResultados busca semântica (arroz tipo 1):")
        for r in rows:
            print(f"  id={r['id']} nome={r['nome']} distancia={r['distancia']:.4f}")

        # Verifica se produtos têm embedding preenchido
        result = await conn.execute(
            text("SELECT count(*) as total, count(embedding) as com_embedding FROM produtos")
        )
        row = result.fetchone()
        print(f"\nProdutos: total={row.total}, com_embedding={row.com_embedding}")

    await engine.dispose()
    print("\nValidação concluída com sucesso.")


if __name__ == "__main__":
    asyncio.run(main())
