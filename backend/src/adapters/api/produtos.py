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
    relevancia: float | None = None  # Score de relevância da busca Full-Text (MAIOR = mais relevante)

    class Config:
        from_attributes = True


class ProdutosListResponse(BaseModel):
    items: list[ProdutoRootResponse]
    total: int


class ProdutoBuscaResponse(BaseModel):
    """Resultado de busca Full-Text com score de relevância (ordem: mais relevante primeiro)."""
    id: int
    nome: str
    marca: str | None = None
    unidade: str
    relevancia: float  # Score do MATCH/AGAINST (BOOLEAN MODE) — ordenação por relevância

    class Config:
        from_attributes = True


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

    async def autocomplete(self, query: str, limit: int = 10):  # noqa: PLR0912
        """Busca híbrida Full-Text Search: FULLTEXT (nome) + marca (FULLTEXT) + expansão semântica via produto_classes (FULLTEXT).

        Retorna resultados ordenados por relevância (score do MATCH/AGAINST, BOOLEAN MODE).
        Todas as buscas usam índices FULLTEXT do MySQL — nenhuma busca por LIKE.
        """
        from sqlalchemy import text

        q = query.strip()
        if not q:
            return []

        # Sanitiza termo para BOOLEAN MODE (escapa caracteres especiais)
        q_sanitized = "".join(ch for ch in q if ch.isalnum() or ch.isspace()).strip()
        if not q_sanitized:
            return []

        # 1. FULLTEXT search no nome (MySQL MATCH AGAINST) — ordenado por relevância
        fulltext_sql = text("""
            SELECT id, nome, marca, unidade, ativo, criado_em,
                   MATCH(nome) AGAINST(:query IN BOOLEAN MODE) AS relevancia
            FROM produtos
            WHERE ativo = TRUE
              AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)
            ORDER BY relevancia DESC
            LIMIT :limit
        """)
        result = await self.session.execute(fulltext_sql, {"query": f"+{q_sanitized}*", "limit": limit})
        rows = result.mappings().all()
        produtos = [ProdutoModel(**{k: v for k, v in dict(r).items() if k != "relevancia"}) for r in rows]
        for p, r in zip(produtos, rows, strict=False):
            p.relevancia = float(r["relevancia"])

        if len(produtos) >= limit:
            return produtos[:limit]

        # 2. FULLTEXT search em marca (MySQL MATCH AGAINST)
        remaining = limit - len(produtos)
        marca_ids = {p.id for p in produtos}
        marca_sql = text("""
            SELECT id, nome, marca, unidade, ativo, criado_em,
                   MATCH(marca) AGAINST(:query IN BOOLEAN MODE) AS relevancia
            FROM produtos
            WHERE ativo = TRUE
              AND id NOT IN :excluded_ids
              AND MATCH(marca) AGAINST(:query IN BOOLEAN MODE)
            ORDER BY relevancia DESC
            LIMIT :limit
        """)
        excluded = tuple(marca_ids) if marca_ids else (0,)
        result = await self.session.execute(
            marca_sql, {"excluded_ids": excluded, "query": f"+{q_sanitized}*", "limit": remaining}
        )
        rows = result.mappings().all()
        produtos.extend(ProdutoModel(**{k: v for k, v in dict(r).items() if k != "relevancia"}) for r in rows)
        for p, r in zip(produtos[len(produtos) - len(rows):], rows, strict=False):
            p.relevancia = float(r["relevancia"])

        if len(produtos) >= limit:
            return produtos[:limit]

        # 3. Expansão semântica via produto_classes (FULLTEXT nas colunas geradas)
        remaining = limit - len(produtos)
        if remaining > 0:
            classe_sql = text("""
                SELECT termos_busca, marcas_referencia
                FROM produto_classes
                WHERE ativo = TRUE
                  AND (
                    MATCH(termos_busca_texto) AGAINST(:query IN BOOLEAN MODE)
                    OR MATCH(marcas_referencia_texto) AGAINST(:query IN BOOLEAN MODE)
                  )
            """)
            result = await self.session.execute(classe_sql, {"query": f"+{q_sanitized}*"})
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
                        SELECT id, nome, marca, unidade, ativo, criado_em,
                               MATCH(nome) AGAINST(:query IN BOOLEAN MODE) AS relevancia
                        FROM produtos
                        WHERE ativo = TRUE
                          AND id NOT IN :excluded_ids
                          AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)
                        ORDER BY relevancia DESC
                        LIMIT :limit
                    """)
                    excluded = tuple(term_ids) if term_ids else (0,)
                    result = await self.session.execute(
                        ft_sql, {"excluded_ids": excluded, "query": ft_query, "limit": remaining}
                    )
                    rows = result.mappings().all()
                    novos = [ProdutoModel(**{k: v for k, v in dict(r).items() if k != "relevancia"}) for r in rows]
                    for p, r in zip(novos, rows, strict=False):
                        p.relevancia = float(r["relevancia"])
                    produtos.extend(novos)

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
