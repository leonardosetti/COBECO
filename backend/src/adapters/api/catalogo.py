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


# Gatilhos de busca semântica para categorias (RF20).
# Mapeia termo do usuário -> nomes de categorias relacionadas.
# Expandido à medida que o catálogo cresce; migrar para coluna de sinônimos no DB quando houver >20 categorias.
CATEGORIA_GATILHOS: dict[str, list[str]] = {
    "vestuário": ["roupas", "camiseta", "camisa", "calça", "calçado", "sapato", "moda", "roupa"],
    "livros": ["livro", "revista", "leitura", "didático", "literatura"],
    "jardinagem": ["pá", "rastelo", "jardim", "plantas", "vasos", "adubo", "jardim"],
    "ferramentas": ["martelo", "serrote", "chave de fenda", "alicate", "furadeira", "pá", "rastelo"],
    "informática": ["computador", "notebook", "periférico", "impressora", "processador", "placa de vídeo"],
    "mercado": ["arroz", "feijão", "supermercado", "mercearia", "alimento"],
    "eletrodomésticos": ["geladeira", "fogão", "máquina de lavar", "micro-ondas"],
    "móveis": ["sofá", "cadeira", "mesa", "armário", "cama"],
    "automotivos": ["pneu", "óleo", "bateria", "carro", "moto"],
    "materiais de construção": ["cimento", "tijolo", "tinta", "canos", "construção"],
    "decoração": ["quadro", "tapete", "vaso", "luminaire", "enfeite"],
}


class CategoriaBuscaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None
    match_por: str = "nome"  # "nome" | "sinonimo"

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

    async def buscar_por_termo(self, termo: str):
        """Busca semântica de categorias por nome ou sinônimos (RF20)."""
        from sqlalchemy import select, func

        t = (termo or "").strip().lower()
        if not t:
            return []

        categorias_por_nome: dict[int, CategoriaModel] = {}
        categorias_por_sinonimo: dict[int, CategoriaModel] = {}

        todas = await self.session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))
        for cat in todas.scalars().all():
            nome = (cat.nome or "").lower()
            if t in nome or nome in t:
                categorias_por_nome[cat.id] = cat
                continue
            gatilhos = CATEGORIA_GATILHOS.get(nome, [])
            if t in gatilhos or any(g.startswith(t) or t.startswith(g) for g in gatilhos if g):
                categorias_por_sinonimo[cat.id] = cat

        mescladas = {**categorias_por_sinonimo, **categorias_por_nome}
        return list(mescladas.values())


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

    async def autocomplete(self, query: str, limit: int = 10):
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
        for p, r in zip(produtos, rows):
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
        for p, r in zip(produtos[len(produtos) - len(rows):], rows):
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
                    for p, r in zip(novos, rows):
                        p.relevancia = float(r["relevancia"])
                    produtos.extend(novos)

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
        """Produtos vendidos por fornecedores das categorias selecionadas (união, RF19)."""
        if not categoria_ids:
            return []
        sub_fornecedores = (
            select(FornecedorCategoriaModel.fornecedor_id)
            .where(FornecedorCategoriaModel.categoria_id.in_(categoria_ids))
        )
        result = await self.session.execute(
            select(ProdutoModel)
            .distinct()
            .join(
                FornecedorProdutoModel,
                FornecedorProdutoModel.produto_id == ProdutoModel.id,
            )
            .where(
                ProdutoModel.ativo,
                FornecedorProdutoModel.ativo,
                FornecedorProdutoModel.fornecedor_id.in_(sub_fornecedores),
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
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    categorias = await repo.listar_todas()
    return [CategoriaResponse.model_validate(c) for c in categorias]


@router.get(
    "/categorias/busca",
    response_model=list[CategoriaBuscaResponse],
    summary="RF20 - Busca semântica de categorias (nome + sinônimos)",
)
async def buscar_categorias(
    q: str = Query(..., min_length=1, description="Termo de busca semântica (ex.: roupas, pá, rastelo)"),
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    categorias = await repo.buscar_por_termo(q)
    resultados = []
    t = (q or "").strip().lower()
    for c in categorias:
        nome = (c.nome or "").lower()
        match_por = "nome" if (t in nome or nome in t) else "sinonimo"
        resultados.append(
            CategoriaBuscaResponse(
                id=c.id,
                nome=c.nome,
                descricao=c.descricao,
                match_por=match_por,
            )
        )
    return resultados


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
