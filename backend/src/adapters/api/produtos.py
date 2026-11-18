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


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    unidade: str

    class Config:
        from_attributes = True


class ProdutosListResponse(BaseModel):
    items: list[ProdutoResponse]
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
        result = await self.session.execute(
            select(ProdutoModel)
            .where(
                ProdutoModel.nome.ilike(f"%{query}%"),
                ProdutoModel.ativo,
            )
            .limit(limit)
        )
        return list(result.scalars().all())


def get_produto_repo(session: AsyncSession = Depends(get_db)) -> ProdutoRepository:
    return ProdutoRepositoryImpl(session)


@router.get(
    "/produtos",
    response_model=ProdutosListResponse,
    summary="Listar Produtos Ativos (raiz da API)",
)
async def listar_produtos(
    limit: int | None = Query(None, ge=1, le=500, description="Limite máximo de produtos retornados"),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    produtos = await repo.listar_ativos(limit=limit)
    total = await repo.count_ativos()
    return ProdutosListResponse(
        items=[ProdutoResponse.model_validate(p) for p in produtos],
        total=total,
    )
