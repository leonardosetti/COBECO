# COBECO Backend — Listas Router (FastAPI)
# Endpoints CRUD de listas: POST/GET/PUT/DELETE /v1/listas

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.api.auth import get_current_user
from src.adapters.db.database import get_db
from src.adapters.db.models import ItemListaModel, ListaModel, ProdutoModel
from src.domain.entities import Lista
from src.domain.repositories import ListaRepository, ProdutoRepository
from src.domain.usecases import (
    CriarListaInput,
    EditarListaUseCase,
    ExcluirListaUseCase,
    ListaNaoEncontrada,
    ListarMinhasListasUseCase,
    PromoverListaEfemeraUseCase,
    SalvarListaUseCase,
)

router = APIRouter(tags=["Listas"])


# ============================================================
# Schemas
# ============================================================
class ItemListaRequest(BaseModel):
    produto_id: int = Field(..., gt=0)
    quantidade: int = Field(..., ge=1, le=9999)


class CriarListaRequest(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    itens: list[ItemListaRequest] = Field(..., min_length=1)
    categorias: list[int] = Field(
        default=[],
        description="IDs das categorias selecionadas (RF12/RF08). Validação de negório: ≥1 categoria exigida no salvamento.",
    )


class ListaResponse(BaseModel):
    id: int
    nome: str
    itens: list[dict]
    categorias: list[int] = []
    criado_em: str
    atualizado_em: str

    class Config:
        from_attributes = True


class ListaResumoResponse(BaseModel):
    id: int
    nome: str
    total_itens: int
    categorias: list[int] = []
    criado_em: str


class PaginatedResponse(BaseModel):
    items: list[ListaResumoResponse]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int


# ============================================================
# Repository Implementations
# ============================================================
class ListaRepositoryImpl(ListaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _buscar_model(self, lista_id: int, usuario_id: int) -> ListaModel | None:
        result = await self.session.execute(
            select(ListaModel)
            .options(selectinload(ListaModel.itens))
            .where(
                ListaModel.id == lista_id,
                ListaModel.usuario_id == usuario_id,
                ListaModel.deletado_em.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def criar(self, lista: Lista) -> Lista:
        model = ListaModel(
            usuario_id=lista.usuario_id,
            nome=lista.nome,
            categorias=json.dumps(lista.categorias) if lista.categorias else None,
        )
        self.session.add(model)
        await self.session.flush()

        # Adiciona itens
        for item in lista.itens:
            item_model = ItemListaModel(
                lista_id=model.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
            )
            self.session.add(item_model)

        await self.session.flush()
        # Re-query with itens eager loaded
        result = await self.session.execute(
            select(ListaModel)
            .options(selectinload(ListaModel.itens))
            .where(ListaModel.id == model.id)
        )
        return result.scalar_one().to_domain()

    async def buscar_por_id(self, lista_id: int, usuario_id: int) -> Lista | None:
        model = await self._buscar_model(lista_id, usuario_id)
        return model.to_domain() if model else None

    async def listar_por_usuario(
        self,
        usuario_id: int,
        pagina: int = 1,
        por_pagina: int = 20,
        busca: str | None = None,
    ) -> tuple[list[Lista], int]:
        query = select(ListaModel).where(
            ListaModel.usuario_id == usuario_id,
            ListaModel.deletado_em.is_(None),
        )

        if busca:
            query = query.where(ListaModel.nome.ilike(f"%{busca}%"))

        # Total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        # Paginação
        query = query.order_by(ListaModel.criado_em.desc())
        query = query.offset((pagina - 1) * por_pagina).limit(por_pagina)
        # Eager load dos itens (total_itens) — evita lazy load fora do event loop
        query = query.options(selectinload(ListaModel.itens))

        result = await self.session.execute(query)
        listas = result.scalars().all()

        return [item.to_domain() for item in listas], total or 0

    async def atualizar(self, lista: Lista) -> Lista:
        assert lista.id is not None  # id da entidade persistida
        model = await self._buscar_model(lista.id, lista.usuario_id)
        if not model:
            raise ListaNaoEncontrada
        model.nome = lista.nome
        model.categorias = json.dumps(lista.categorias) if lista.categorias else None
        model.atualizado_em = datetime.now()

        # Remove itens antigos (delete-orphan) antes de inserir os novos
        # (flush intermediário evita violar uq_item_lista_produto)
        model.itens.clear()
        await self.session.flush()

        for item in lista.itens:
            model.itens.append(
                ItemListaModel(
                    lista_id=model.id,
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                )
            )
        await self.session.flush()

        # Recarrega com itens eager-loaded para evitar MissingGreenlet
        # (relacao itens foi modificada; to_domain precisa dela carregada)
        result = await self.session.execute(
            select(ListaModel)
            .options(selectinload(ListaModel.itens))
            .where(ListaModel.id == model.id)
        )
        return result.scalar_one().to_domain()

    async def soft_delete(self, lista_id: int, usuario_id: int, confirmacao_nome: str) -> bool:
        # Busca sem filtro de deletado_em para permitir soft delete
        result = await self.session.execute(
            select(ListaModel).where(
                ListaModel.id == lista_id,
                ListaModel.usuario_id == usuario_id,
            )
        )
        model = result.scalar_one_or_none()
        if model and model.nome == confirmacao_nome:
            model.deletado_em = datetime.now()
            return True
        return False


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
        result = await self.session.execute(marca_sql, {
            "excluded_ids": excluded,
            "query": q,
            "prefix": f"{q}%",
            "limit": remaining
        })
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
                params = {"excluded_ids": tuple(brand_ids) if brand_ids else (0,), "limit": remaining}
                for i, brand in enumerate(related_brands):
                    params[f"brand{i}"] = brand
                result = await self.session.execute(marca_sql, params)
                rows = result.mappings().all()
                produtos.extend(ProdutoModel(**dict(r)) for r in rows)

            if len(produtos) < limit and related_terms:
                remaining = limit - len(produtos)
                term_ids = {p.id for p in produtos}
                simple_terms = [t for t in related_terms if t.replace(" ", "").isalnum() and len(t) >= 2]
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
                    result = await self.session.execute(ft_sql, {
                        "excluded_ids": excluded,
                        "query": ft_query,
                        "limit": remaining
                    })
                    rows = result.mappings().all()
                    produtos.extend(ProdutoModel(**dict(r)) for r in rows)

        return produtos[:limit]

    async def listar_ativos(self):
        result = await self.session.execute(select(ProdutoModel).where(ProdutoModel.ativo))
        return list(result.scalars().all())

    async def count_ativos(self) -> int:
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count()).select_from(ProdutoModel).where(ProdutoModel.ativo)
        )
        return int(result.scalar_one())


def get_lista_repo(session: AsyncSession = Depends(get_db)) -> ListaRepository:
    return ListaRepositoryImpl(session)


def get_produto_repo(session: AsyncSession = Depends(get_db)) -> ProdutoRepository:
    return ProdutoRepositoryImpl(session)


# ============================================================
# Endpoints
# ============================================================
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ListaResponse,
    summary="UC14/RF08 - Salvar Lista (Persistir)",
)
async def salvar_lista(
    request: CriarListaRequest,
    current_user=Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    usecase = SalvarListaUseCase(lista_repo, produto_repo)
    try:
        lista = await usecase.executar(
            current_user.id,
            CriarListaInput(
                nome=request.nome,
                itens=[item.model_dump() for item in request.itens],
                categorias=request.categorias,
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Busca itens com nomes dos produtos para resposta
    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append(
            {
                "produto_id": item.produto_id,
                "produto_nome": produto.nome if produto else "Desconhecido",
                "quantidade": item.quantidade,
            }
        )

    return ListaResponse(
        id=lista.id,  # type: ignore[arg-type]  # id definido no flush do repo
        nome=lista.nome,
        itens=itens_resposta,
        categorias=getattr(lista, "categorias", []),
        criado_em=lista.criado_em.isoformat(),
        atualizado_em=lista.atualizado_em.isoformat(),
    )


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="UC15/RF09 - Listar Minhas Listas",
)
async def listar_minhas_listas(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    busca: str | None = Query(None),
    current_user=Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
):
    usecase = ListarMinhasListasUseCase(lista_repo)
    listas, total = await usecase.executar(current_user.id, pagina, por_pagina, busca)

    items = [
        ListaResumoResponse(
            id=lista.id,  # type: ignore[arg-type]  # id da entidade persistida
            nome=lista.nome,
            total_itens=len(lista.itens),
            categorias=getattr(lista, "categorias", []),
            criado_em=lista.criado_em.isoformat(),
        )
        for lista in listas
    ]

    return PaginatedResponse(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=(total + por_pagina - 1) // por_pagina,
    )


@router.post(
    "/promover-efemera",
    status_code=status.HTTP_201_CREATED,
    response_model=ListaResponse,
    summary="UC17/RF08 - Promover Lista Efêmera",
)
async def promover_lista_efemera(
    lista_memoria: dict,
    current_user=Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    usecase = PromoverListaEfemeraUseCase(lista_repo, produto_repo)
    lista = await usecase.executar(current_user.id, lista_memoria)

    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append(
            {
                "produto_id": item.produto_id,
                "produto_nome": produto.nome if produto else "Desconhecido",
                "quantidade": item.quantidade,
            }
        )

    return ListaResponse(
        id=lista.id,  # type: ignore[arg-type]  # id definido no flush do repo
        nome=lista.nome,
        itens=itens_resposta,
        categorias=getattr(lista, "categorias", []),
        criado_em=lista.criado_em.isoformat(),
        atualizado_em=lista.atualizado_em.isoformat(),
    )


@router.get(
    "/{lista_id}",
    response_model=ListaResponse,
    summary="Buscar Lista por ID",
)
async def buscar_lista(
    lista_id: int,
    current_user=Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    lista = await lista_repo.buscar_por_id(lista_id, current_user.id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append(
            {
                "produto_id": item.produto_id,
                "produto_nome": produto.nome if produto else "Desconhecido",
                "quantidade": item.quantidade,
            }
        )

    return ListaResponse(
        id=lista.id,  # type: ignore[arg-type]  # id definido no flush do repo
        nome=lista.nome,
        itens=itens_resposta,
        categorias=getattr(lista, "categorias", []),
        criado_em=lista.criado_em.isoformat(),
        atualizado_em=lista.atualizado_em.isoformat(),
    )


@router.put(
    "/{lista_id}",
    response_model=ListaResponse,
    summary="UC13/RF10 - Editar Lista Salva",
)
async def editar_lista(
    lista_id: int,
    request: CriarListaRequest,
    current_user=Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    usecase = EditarListaUseCase(lista_repo, produto_repo)
    try:
        lista = await usecase.executar(
            lista_id,
            current_user.id,
            CriarListaInput(
                nome=request.nome,
                itens=[item.model_dump() for item in request.itens],
                categorias=request.categorias,
            ),
        )
    except ListaNaoEncontrada:
        raise HTTPException(status_code=404, detail="Lista não encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append(
            {
                "produto_id": item.produto_id,
                "produto_nome": produto.nome if produto else "Desconhecido",
                "quantidade": item.quantidade,
            }
        )

    return ListaResponse(
        id=lista.id,  # type: ignore[arg-type]  # id definido no flush do repo
        nome=lista.nome,
        itens=itens_resposta,
        categorias=getattr(lista, "categorias", []),
        criado_em=lista.criado_em.isoformat(),
        atualizado_em=lista.atualizado_em.isoformat(),
    )


@router.delete(
    "/{lista_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="UC13/RF11 - Excluir Lista (Soft Delete)",
)
async def excluir_lista(
    lista_id: int,
    confirmacao_nome: str = Query(..., description="Nome da lista para confirmação"),
    current_user=Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
):
    usecase = ExcluirListaUseCase(lista_repo)
    sucesso = await usecase.executar(lista_id, current_user.id, confirmacao_nome)
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail="Nome de confirmação incorreto ou lista não encontrada",
        )
