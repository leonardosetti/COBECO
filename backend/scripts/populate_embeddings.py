#!/usr/bin/env python3
"""
COBECO — População de embeddings (backfill).

Gera embeddings para produtos e produto_classes existentes que ainda não
tenham vetor preenchido. Usa o EmbeddingService FOSS (sentence-transformers).

Uso:
  DATABASE_URL=postgresql+asyncpg://... python scripts/populate_embeddings.py
"""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.adapters.db.models import ProdutoModel, ProdutoClasseModel
from src.services.embedding import get_embedding_service


async def popular() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL não definida")
        sys.exit(1)

    engine = create_async_engine(database_url)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    embedding_service = get_embedding_service()

    async with session_factory() as session:
        # Produtos sem embedding
        result = await session.execute(
            select(ProdutoModel).where(ProdutoModel.embedding.is_(None))
        )
        produtos = result.scalars().all()
        for p in produtos:
            texto = f"{p.nome or ''} {p.marca or ''}".strip()
            if texto:
                p.embedding = embedding_service.gerar(texto)
                print(f"Produto {p.id}: embedding gerado ({texto[:40]}...)")

        # Produto classes sem embedding
        result = await session.execute(
            select(ProdutoClasseModel).where(ProdutoClasseModel.embedding.is_(None))
        )
        classes = result.scalars().all()
        for c in classes:
            texto = f"{c.classe_nome or ''} {' '.join(c.termos_busca or [])}".strip()
            if texto:
                c.embedding = embedding_service.gerar(texto)
                print(f"ProdutoClasse {c.id}: embedding gerado ({texto[:40]}...)")

        await session.commit()

    await engine.dispose()
    print("\nPopulação de embeddings concluída.")


def main() -> None:
    asyncio.run(popular())


if __name__ == "__main__":
    main()
