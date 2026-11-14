# COBECO Backend — Catálogo Router (FastAPI)
# Endpoints: Categorias, Fornecedores, Produtos (Autocomplete)


from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.db.database import get_db
from src.adapters.db.models import (
    CategoriaModel,
    FornecedorCategoriaModel,
    FornecedorModel,
    ProdutoModel,
)
from src.domain.repositories import CategoriaRepository, FornecedorRepository, ProdutoRepository

router = APIRouter(tags=["Catálogo"])


# ============================================================
# Schemas
# ============================================================
class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None

    class Config:
        from_attributes = True


class FornecedorResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    categorias: list[CategoriaResponse] = []

    class Config:
        from_attributes = True


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    unidade: str

    class Config:
        from_attributes = True


class FornecedorDisponibilidadeResponse(BaseModel):
    fornecedor: FornecedorResponse
    percentual_disponibilidade: float
    itens_disponiveis: int
    itens_totais: int


# ============================================================
# Repository Implementations
# ============================================================
class CategoriaRepositoryImpl(CategoriaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_todas(self):
        result = await self.session.execute(
            select(CategoriaModel).order_by(CategoriaModel.nome)
        )
        return list(result.scalars().all())

    async def buscar_por_id(self, categoria_id: int):
        result = await self.session.execute(
            select(CategoriaModel).where(CategoriaModel.id == categoria_id)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(CategoriaModel).where(CategoriaModel.id.in_(ids))
        )
        return list(result.scalars().all())


class FornecedorRepositoryImpl(FornecedorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_ativos(self):
        result = await self.session.execute(
            select(FornecedorModel).where(FornecedorModel.ativo == True).order_by(FornecedorModel.nome)
        )
        return list(result.scalars().all())

    async def listar_por_categorias(self, categoria_ids: list[int]):
        # Fornecedores que têm TODAS as categorias selecionadas (interseção)
        # Ou PELO MENOS UMA (união) - conforme RF12/UC03
        # Usando união (pelo menos uma categoria)
        from sqlalchemy import select

        subquery = select(FornecedorCategoriaModel.fornecedor_id).where(
            FornecedorCategoriaModel.categoria_id.in_(categoria_ids)
        ).group_by(FornecedorCategoriaModel.fornecedor_id)

        result = await self.session.execute(
            select(FornecedorModel).where(
                FornecedorModel.id.in_(subquery),
                FornecedorModel.ativo == True,
            ).order_by(FornecedorModel.nome)
        )
        return list(result.scalars().all())

    async def buscar_por_id(self, fornecedor_id: int):
        result = await self.session.execute(
            select(FornecedorModel)
            .options(selectinload(FornecedorModel.categorias))
            .where(FornecedorModel.id == fornecedor_id)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(FornecedorModel).where(FornecedorModel.id.in_(ids))
        )
        return list(result.scalars().all())

    async def calcular_disponibilidade(
        self,
        fornecedor_id: int,
        produto_ids: list[int],
    ):
        from src.adapters.db.models import FornecedorProdutoModel
        result = await self.session.execute(
            select(FornecedorProdutoModel).where(
                FornecedorProdutoModel.fornecedor_id == fornecedor_id,
                FornecedorProdutoModel.produto_id.in_(produto_ids),
                FornecedorProdutoModel.ativo == True,
                FornecedorProdutoModel.estoque > 0,
            )
        )
        produtos_encontrados = list(result.scalars().all())

        itens_disponiveis = len(produtos_encontrados)
        itens_ausentes = len(produto_ids) - itens_disponiveis
        preco_total = sum(p.preco * p.estoque for p in produtos_encontrados)

        return itens_disponiveis, itens_ausentes, preco_total


class ProdutoRepositoryImpl(ProdutoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def buscar_por_id(self, produto_id: int):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id == produto_id, ProdutoModel.ativo == True)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id.in_(ids), ProdutoModel.ativo == True)
        )
        return list(result.scalars().all())

    async def autocomplete(self, query: str, limit: int = 10):
        result = await self.session.execute(
            select(ProdutoModel).where(
                ProdutoModel.nome.ilike(f"%{query}%"),
                ProdutoModel.ativo == True,
            ).limit(limit)
        )
        return list(result.scalars().all())

    async def listar_ativos(self):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.ativo == True).order_by(ProdutoModel.nome)
        )
        return list(result.scalars().all())


def get_categoria_repo(session: AsyncSession = Depends(get_db)) -> CategoriaRepository:
    return CategoriaRepositoryImpl(session)


def get_fornecedor_repo(session: AsyncSession = Depends(get_db)) -> FornecedorRepository:
    return FornecedorRepositoryImpl(session)


def get_produto_repo(session: AsyncSession = Depends(get_db)) -> ProdutoRepository:
    return ProdutoRepositoryImpl(session)


# ============================================================
# Endpoints
# ============================================================
@router.get(
    "/categorias",
    response_model=list[CategoriaResponse],
    summary="UC03/RF12 - Listar Categorias (Pré-filtro)",
)
async def listar_categorias(
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    categorias = await repo.listar_todas()
    return [CategoriaResponse.model_validate(c) for c in categorias]


@router.get(
    "/fornecedores",
    response_model=list[FornecedorResponse],
    summary="UC04/RF13 - Listar Fornecedores (filtrado por categorias)",
)
async def listar_fornecedores(
    categorias: str | None = Query(None, description="IDs de categorias separados por vírgula"),
    repo: FornecedorRepository = Depends(get_fornecedor_repo),
    categoria_repo: CategoriaRepository = Depends(get_categoria_repo),
):
    if categorias:
        categoria_ids = [int(c) for c in categorias.split(",")]
        fornecedores = await repo.listar_por_categorias(categoria_ids)
    else:
        fornecedores = await repo.listar_ativos()

    response = []
    for f in fornecedores:
        # Busca categorias do fornecedor
        from sqlalchemy import select
        cat_result = await repo.session.execute(
            select(CategoriaModel).join(FornecedorCategoriaModel).where(
                FornecedorCategoriaModel.fornecedor_id == f.id
            )
        )
        cats = cat_result.scalars().all()
        response.append(FornecedorResponse(
            id=f.id,
            nome=f.nome,
            cnpj=f.cnpj,
            categorias=[CategoriaResponse.model_validate(c) for c in cats],
        ))
    return response


@router.get(
    "/fornecedores/{fornecedor_id}/disponibilidade",
    response_model=FornecedorDisponibilidadeResponse,
    summary="UC04/UC05 - Calcular Disponibilidade do Fornecedor",
)
async def calcular_disponibilidade_fornecedor(
    fornecedor_id: int,
    produtos: str = Query(..., description="IDs de produtos separados por vírgula"),
    repo: FornecedorRepository = Depends(get_fornecedor_repo),
):
    produto_ids = [int(p) for p in produtos.split(",")]

    itens_disp, itens_aus, preco_total = await repo.calcular_disponibilidade(
        fornecedor_id, produto_ids
    )

    fornecedor = await repo.buscar_por_id(fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    percentual = (itens_disp / len(produto_ids) * 100) if produto_ids else 0

    return FornecedorDisponibilidadeResponse(
        fornecedor=FornecedorResponse.model_validate(fornecedor),
        percentual_disponibilidade=round(percentual, 1),
        itens_disponiveis=itens_disp,
        itens_totais=len(produto_ids),
    )


@router.get(
    "/produtos/autocomplete",
    response_model=list[ProdutoResponse],
    summary="UC02/RF07 - Autocomplete de Produtos",
)
async def autocomplete_produtos(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    produtos = await repo.autocomplete(q, limit)
    return [ProdutoResponse.model_validate(p) for p in produtos]


@router.get(
    "/produtos",
    response_model=list[ProdutoResponse],
    summary="Listar Produtos Ativos",
)
async def listar_produtos(
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    produtos = await repo.listar_ativos()
    return [ProdutoResponse.model_validate(p) for p in produtos]
