# COBECO Backend — Produtos Router (raiz da API)
# Endpoint GET /v1/produtos usado pelos testes de integração e pelo frontend.
# Reusa o ProdutoRepository do catálogo para evitar duplicar lógica de domínio.

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.adapters.db.database import get_db
from src.adapters.db.models import ProdutoModel
from src.domain.repositories import ProdutoRepository
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Produtos"])


class ProdutoRootResponse(BaseModel):
    id: int
    nome: str
    marca: str | None = None
    unidade: str

    class Config:
        from_attributes = True


class ProdutosListResponse(BaseModel):
    items: list[ProdutoRootResponse]
    total: int


class ProdutoRepositoryImpl(ProdutoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_ativos(self, limit: int | None = None):
        query = select(ProdutoModel).where(ProdutoModel.ativo).order_by(ProdutoModel.nome)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_ativos(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(ProdutoModel).where(ProdutoModel.ativo)
        )
        return int(result.scalar_one())

    async def buscar_por_id(self, produto_id: int):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id == produto_id, ProdutoModel.ativo)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id.in_(ids), ProdutoModel.ativo)
        )
        return list(result.scalars().all())

    async def autocomplete(self, query: str, limit: int = 10):
        """Busca híbrida: FULLTEXT (nome) + marca exata + expansão semântica via produto_classes."""
        from sqlalchemy import text

        q = query.strip()
        if not q:
            return []

        # 1. FULLTEXT search no nome (MySQL MATCH AGAINST)
        fulltext_sql = text("""
            SELECT id, nome, marca, unidade, ativo, criado_em
            FROM produtos
            WHERE ativo = TRUE
              AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)
            LIMIT :limit
        """)
        result = await self.session.execute(fulltext_sql, {"query": f"+{q}*", "limit": limit})
        rows = result.mappings().all()
        produtos = [ProdutoModel(**dict(r)) for r in rows]

        if len(produtos) >= limit:
            return produtos[:limit]

        # 2. Match exato/prefixo em marca (case-insensitive)
        remaining = limit - len(produtos)
        marca_ids = {p.id for p in produtos}
        marca_sql = text("""
            SELECT id, nome, marca, unidade, ativo, criado_em
            FROM produtos
            WHERE ativo = TRUE
              AND id NOT IN :excluded_ids
              AND (marca = :query OR marca LIKE :prefix)
            LIMIT :limit
        """)
        excluded = tuple(marca_ids) if marca_ids else (0,)
        result = await self.session.execute(
            marca_sql, {"excluded_ids": excluded, "query": q, "prefix": f"{q}%", "limit": remaining}
        )
        rows = result.mappings().all()
        produtos.extend(ProdutoModel(**dict(r)) for r in rows)

        if len(produtos) >= limit:
            return produtos[:limit]

        # 3. Expansão semântica via produto_classes
        remaining = limit - len(produtos)
        if remaining > 0:
            classe_sql = text("""
                SELECT termos_busca, marcas_referencia
                FROM produto_classes
                WHERE ativo = TRUE
                  AND (
                    CAST(termos_busca AS CHAR) LIKE :query_like
                    OR CAST(marcas_referencia AS CHAR) LIKE :query_like
                  )
            """)
            result = await self.session.execute(classe_sql, {"query_like": f"%{q.lower()}%"})
            classe_rows = result.mappings().all()

            import json

            related_terms = set()
            related_brands = set()
            for row in classe_rows:
                related_terms.update(json.loads(row["termos_busca"]))
                related_brands.update(json.loads(row["marcas_referencia"]))

            if related_brands:
                brand_ids = {p.id for p in produtos}
                brand_placeholders = ", ".join([f":brand{i}" for i in range(len(related_brands))])
                marca_sql = text(f"""
                    SELECT id, nome, marca, unidade, ativo, criado_em
                    FROM produtos
                    WHERE ativo = TRUE
                      AND id NOT IN :excluded_ids
                      AND (marca IN ({brand_placeholders}))
                    LIMIT :limit
                """)
                params = {
                    "excluded_ids": tuple(brand_ids) if brand_ids else (0,),
                    "limit": remaining,
                }
                for i, brand in enumerate(related_brands):
                    params[f"brand{i}"] = brand
                result = await self.session.execute(marca_sql, params)
                rows = result.mappings().all()
                produtos.extend(ProdutoModel(**dict(r)) for r in rows)

            if len(produtos) < limit and related_terms:
                remaining = limit - len(produtos)
                term_ids = {p.id for p in produtos}
                simple_terms = [
                    t for t in related_terms if t.replace(" ", "").isalnum() and len(t) >= 2
                ]
                if simple_terms:
                    ft_query = " ".join(f"+{t}*" for t in simple_terms[:5])
                    ft_sql = text("""
                        SELECT id, nome, marca, unidade, ativo, criado_em
                        FROM produtos
                        WHERE ativo = TRUE
                          AND id NOT IN :excluded_ids
                          AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)
                        LIMIT :limit
                    """)
                    excluded = tuple(term_ids) if term_ids else (0,)
                    result = await self.session.execute(
                        ft_sql, {"excluded_ids": excluded, "query": ft_query, "limit": remaining}
                    )
                    rows = result.mappings().all()
                    produtos.extend(ProdutoModel(**dict(r)) for r in rows)

        return produtos[:limit]


def get_produto_repo(session: AsyncSession = Depends(get_db)) -> ProdutoRepository:
    return ProdutoRepositoryImpl(session)


@router.get(
    "/produtos",
    response_model=ProdutosListResponse,
    summary="Listar Produtos Ativos (raiz da API)",
)
async def listar_produtos(
    limit: int | None = Query(
        None, ge=1, le=500, description="Limite máximo de produtos retornados"
    ),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    produtos = await repo.listar_ativos(limit=limit)
    total = await repo.count_ativos()
    return ProdutosListResponse(
        items=[ProdutoRootResponse.model_validate(p) for p in produtos],
        total=total,
    )
