# COBECO Backend — Catálogo Router (FastAPI)
# Endpoints: Categorias, Fornecedores, Produtos (Autocomplete)


from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.db.database import get_db
from src.adapters.db.models import (
    CategoriaModel,
    FornecedorCategoriaModel,
    FornecedorModel,
    FornecedorProdutoModel,
    ProdutoModel,
)
from src.domain.repositories import (
    CategoriaRepository,
    FornecedorRepository,
    ProdutoRepository,
)

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
    marca: str | None = None
    unidade: str

    class Config:
        from_attributes = True


class FornecedorDisponibilidadeResponse(BaseModel):
    fornecedor: FornecedorResponse
    percentual_disponibilidade: float
    itens_disponiveis: int
    itens_totais: int


# Mapeamento de grandes áreas para categorias macro (RF27/RF28).
# Nomes batem EXATAMENTE com as 25 categorias do seed realístico (banco stage/dev).
# Expandido à medida que o catálogo cresce; migrar para coluna/tabela no DB quando houver >20 áreas.
AREAS_GRANDES: dict[str, list[str]] = {
    "Supermercado": [
        "Mercearia", "Bebidas", "Limpeza", "Higiene",
        "Padaria", "Frios e Laticínios", "Açougue", "Hortifruti"
    ],
    "Informática e Eletrônicos": [
        "Eletrônicos", "Informática", "Eletrodomésticos", "Móveis"
    ],
    "Livros e Papelaria": [
        "Livros", "Papelaria"
    ],
    "Construção e Ferragens": [
        "Ferramentas", "Materiais Construção", "Jardinagem", "Iluminação"
    ],
    "Pet": [
        "Pet Alimentos", "Pet Acessórios"
    ],
    "Automotivo": [
        "Peças Automotivas", "Pneus e Rodas"
    ],
    "Moda": [
        "Vestuário Masculino", "Vestuário Feminino", "Calçados"
    ],
}


class AreaGrandeResponse(BaseModel):
    id: int
    nome: str
    categorias: list[CategoriaResponse] = []

    class Config:
        from_attributes = True


# ============================================================
# Repository Implementations
# ============================================================
class CategoriaRepositoryImpl(CategoriaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_todas(self):
        result = await self.session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))
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
            select(FornecedorModel).where(FornecedorModel.ativo).order_by(FornecedorModel.nome)
        )
        return list(result.scalars().all())

    async def listar_por_categorias(self, categoria_ids: list[int]):
        # Fornecedores que têm TODAS as categorias selecionadas (interseção)
        # Ou PELO MENOS UMA (união) - conforme RF12/UC03
        # Usando união (pelo menos uma categoria)
        from sqlalchemy import select

        subquery = (
            select(FornecedorCategoriaModel.fornecedor_id)
            .where(FornecedorCategoriaModel.categoria_id.in_(categoria_ids))
            .group_by(FornecedorCategoriaModel.fornecedor_id)
        )

        result = await self.session.execute(
            select(FornecedorModel)
            .where(
                FornecedorModel.id.in_(subquery),
                FornecedorModel.ativo,
            )
            .order_by(FornecedorModel.nome)
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
                FornecedorProdutoModel.ativo,
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
            select(ProdutoModel).where(ProdutoModel.id == produto_id, ProdutoModel.ativo)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id.in_(ids), ProdutoModel.ativo)
        )
        return list(result.scalars().all())

    async def autocomplete(self, query: str, limit: int = 10, categoria_ids: list[int] | None = None):
        """Busca textual via tsvector + índice GIN (português).

        Retorna resultados ordenados por relevância (ts_rank_cd).
        Todas as buscas usam índices GIN sobre colunas tsvector — nenhuma busca por LIKE/ILIKE.
        Se categoria_ids fornecido, filtra produtos apenas dessas categorias.
        """
        from sqlalchemy import text

        q = query.strip()
        if not q:
            return []

        # Sanitiza termo para plainto_tsquery (remove caracteres que quebram a sintaxe)
        q_sanitized = "".join(ch for ch in q if ch.isalnum() or ch.isspace()).strip()
        if not q_sanitized:
            return []

        # Cláusula WHERE adicional para filtro de categoria
        cat_where = ""
        cat_params = {}
        if categoria_ids:
            cat_where = " AND categoria_id IN :categoria_ids"
            cat_params = {"categoria_ids": tuple(categoria_ids)}

        # Busca textual combinada: nome_tsv e marca_tsv com tsvector
        sql = text(f"""
            SELECT id, nome, marca, unidade, ativo, criado_em,
                   ts_rank_cd(nome_tsv, query) AS relevancia_nome,
                   ts_rank_cd(marca_tsv, query) AS relevancia_marca
            FROM produtos,
                 plainto_tsquery('portuguese', :query) AS query
            WHERE ativo = true
              AND (nome_tsv @@ query OR marca_tsv @@ query)
              {cat_where}
            ORDER BY
                (COALESCE(ts_rank_cd(nome_tsv, query), 0) +
                 COALESCE(ts_rank_cd(marca_tsv, query), 0)) DESC
            LIMIT :limit
        """)
        params = {"query": q_sanitized, "limit": limit, **cat_params}
        result = await self.session.execute(sql, params)
        rows = result.mappings().all()
        produtos = [
            ProdutoModel(**{k: v for k, v in dict(r).items() if k not in ("relevancia_nome", "relevancia_marca")})
            for r in rows
        ]
        for p, r in zip(produtos, rows):
            rn = float(r["relevancia_nome"] or 0)
            rm = float(r["relevancia_marca"] or 0)
            p.relevancia = rn + rm

        return produtos[:limit]

    async def listar_ativos(self):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.ativo).order_by(ProdutoModel.nome)
        )
        return list(result.scalars().all())

    async def count_ativos(self) -> int:
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count()).select_from(ProdutoModel).where(ProdutoModel.ativo)
        )
        return int(result.scalar_one())

    async def listar_por_categorias(self, categoria_ids: list[int]):
        """Produtos das categorias selecionadas (RF19).
        
        Filtra produtos pela sua categoria principal (produtos.categoria_id)
        e garante que estejam disponíveis em pelo menos um fornecedor ativo.
        """
        if not categoria_ids:
            return []
        
        # Subquery: fornecedores ativos com estoque > 0
        sub_fornecedores = (
            select(FornecedorProdutoModel.fornecedor_id)
            .distinct()
            .where(
                FornecedorProdutoModel.ativo == True,
                FornecedorProdutoModel.estoque > 0,
            )
        )
        
        result = await self.session.execute(
            select(ProdutoModel)
            .where(
                ProdutoModel.ativo == True,
                ProdutoModel.categoria_id.in_(categoria_ids),
                # Garante que existe pelo menos um fornecedor ativo com estoque
                ProdutoModel.id.in_(
                    select(FornecedorProdutoModel.produto_id)
                    .where(
                        FornecedorProdutoModel.fornecedor_id.in_(sub_fornecedores),
                        FornecedorProdutoModel.ativo == True,
                        FornecedorProdutoModel.estoque > 0,
                    )
                )
            )
            .order_by(ProdutoModel.nome)
        )
        return list(result.scalars().all())


def get_categoria_repo(session: AsyncSession = Depends(get_db)) -> CategoriaRepository:
    return CategoriaRepositoryImpl(session)


def get_fornecedor_repo(
    session: AsyncSession = Depends(get_db),
) -> FornecedorRepository:
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
    areas: str | None = Query(
        None, description="IDs de grandes áreas separados por vírgula (filtro multi-seleção, RF27)"
    ),
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    categorias = await repo.listar_todas()
    if areas:
        try:
            area_ids = [int(a) for a in areas.split(",") if a.strip()]
            nomes_area = list(AREAS_GRANDES.keys())
            nomes_categorias_permitidas: set[str] = set()
            for aid in area_ids:
                if 1 <= aid <= len(nomes_area):
                    nomes_categorias_permitidas.update(AREAS_GRANDES[nomes_area[aid - 1]])
            if nomes_categorias_permitidas:
                categorias = [c for c in categorias if (c.nome or "").strip() in nomes_categorias_permitidas]
            else:
                categorias = []
        except ValueError:
            pass
    return [CategoriaResponse.model_validate(c) for c in categorias]


@router.get(
    "/areas-grandes",
    response_model=list[AreaGrandeResponse],
    summary="RF28 - Listar grandes áreas com suas categorias macro",
)
async def listar_areas_grandes(
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    todas = await repo.listar_todas()
    mapa_nome = {(c.nome or "").strip(): c for c in todas}
    resultado = []
    for idx, (nome_area, nomes_cats) in enumerate(AREAS_GRANDES.items(), start=1):
        cats_resp = []
        for nm in nomes_cats:
            c = mapa_nome.get(nm)
            if c:
                cats_resp.append(CategoriaResponse.model_validate(c))
        resultado.append(AreaGrandeResponse(id=idx, nome=nome_area, categorias=cats_resp))
    return resultado


@router.get(
    "/fornecedores",
    response_model=list[FornecedorResponse],
    summary="UC04/RF13 - Listar Fornecedores (filtrado por categorias)",
)
async def listar_fornecedores(
    categorias: str | None = Query(None, description="IDs de categorias separados por vírgula"),
    repo: FornecedorRepositoryImpl = Depends(get_fornecedor_repo),
    categoria_repo: CategoriaRepository = Depends(get_categoria_repo),
):
    if categorias:
        categoria_ids = [int(c) for c in categorias.split(",")]
        fornecedores = await repo.listar_por_categorias(categoria_ids)
    else:
        fornecedores = await repo.listar_ativos()

    response = []
    for fornecedor in fornecedores:
        # Busca categorias do fornecedor
        from sqlalchemy import select

        cat_result = await repo.session.execute(
            select(CategoriaModel)
            .join(FornecedorCategoriaModel)
            .where(FornecedorCategoriaModel.fornecedor_id == fornecedor.id)
        )
        cats = cat_result.scalars().all()
        response.append(
            FornecedorResponse(
                id=fornecedor.id or 0,
                nome=fornecedor.nome,
                cnpj=fornecedor.cnpj,
                categorias=[CategoriaResponse.model_validate(c) for c in cats],
            )
        )
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


class FornecedorDisponibilidadeLoteItem(BaseModel):
    fornecedor_id: int
    percentual_disponibilidade: float
    itens_disponiveis: int
    itens_totais: int


@router.get(
    "/fornecedores/disponibilidade-lote",
    response_model=list[FornecedorDisponibilidadeLoteItem],
    summary="UC04/UC05 - Disponibilidade em lote de fornecedores para uma lista de produtos",
)
async def calcular_disponibilidade_lote(
    produtos: str = Query(..., description="IDs de produtos separados por vírgula"),
    fornecedores: str | None = Query(
        None, description="IDs de fornecedores separados por vírgula (opcional: todos os ativos)"
    ),
    repo: FornecedorRepository = Depends(get_fornecedor_repo),
):
    produto_ids = [int(p) for p in produtos.split(",")]
    if not produto_ids:
        return []

    if fornecedores:
        fornecedor_ids = [int(f) for f in fornecedores.split(",")]
    else:
        todos = await repo.listar_ativos()
        fornecedor_ids = [f.id for f in todos]

    resultado: list[FornecedorDisponibilidadeLoteItem] = []
    for fornecedor_id in fornecedor_ids:
        itens_disp, itens_aus, _preco = await repo.calcular_disponibilidade(
            fornecedor_id, produto_ids
        )
        percentual = (itens_disp / len(produto_ids) * 100) if produto_ids else 0
        resultado.append(
            FornecedorDisponibilidadeLoteItem(
                fornecedor_id=fornecedor_id,
                percentual_disponibilidade=round(percentual, 1),
                itens_disponiveis=itens_disp,
                itens_totais=len(produto_ids),
            )
        )
    return resultado


@router.get(
    "/produtos/autocomplete",
    response_model=list[ProdutoResponse],
    summary="UC02/RF07 - Autocomplete de Produtos (com filtro opcional de categorias)",
)
async def autocomplete_produtos(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50),
    categorias: str | None = Query(None, description="IDs de categorias separados por vírgula (filtro opcional)"),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    categoria_ids = [int(c) for c in categorias.split(",")] if categorias else None
    produtos = await repo.autocomplete(q, limit, categoria_ids)
    return [ProdutoResponse.model_validate(p) for p in produtos]


@router.get(
    "/produtos",
    response_model=list[ProdutoResponse],
    summary="Listar Produtos Ativos (filtrado por categorias selecionadas, RF19)",
)
async def listar_produtos(
    categorias: str | None = Query(
        None, description="IDs de categorias separados por vírgula (filtra produtos por categoria)"
    ),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    if categorias:
        categoria_ids = [int(c) for c in categorias.split(",")]
        produtos = await repo.listar_por_categorias(categoria_ids)
    else:
        produtos = await repo.listar_ativos()
    return [ProdutoResponse.model_validate(p) for p in produtos]
