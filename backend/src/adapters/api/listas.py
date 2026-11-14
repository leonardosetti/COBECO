# COBECO Backend — Listas Router (FastAPI)
# Endpoints CRUD de listas: POST/GET/PUT/DELETE /v1/listas

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.api.auth import get_current_user
from src.adapters.db.database import get_db
from src.adapters.db.models import ItemListaModel, ListaModel, ProdutoModel
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


class ListaResponse(BaseModel):
    id: int
    nome: str
    itens: list[dict]
    criado_em: str
    atualizado_em: str

    class Config:
        from_attributes = True


class ListaResumoResponse(BaseModel):
    id: int
    nome: str
    total_itens: int
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

    async def criar(self, lista) -> ListaModel:
        model = ListaModel(
            usuario_id=lista.usuario_id,
            nome=lista.nome,
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
        return result.scalar_one()

    async def buscar_por_id(self, lista_id: int, usuario_id: int):
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

    async def listar_por_usuario(
        self,
        usuario_id: int,
        pagina: int = 1,
        por_pagina: int = 20,
        busca: str | None = None,
    ):
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

        return listas, total

    async def atualizar(self, lista) -> ListaModel:
        model = await self.buscar_por_id(lista.id, lista.usuario_id)
        if model:
            model.nome = lista.nome
            model.atualizado_em = datetime.now()

            # Remove itens antigos (delete-orphan) antes de inserir os novos
            # (flush intermediário evita violar uq_item_lista_produto)
            model.itens.clear()
            await self.session.flush()

            for item in lista.itens:
                model.itens.append(ItemListaModel(
                    lista_id=model.id,
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                ))
            await self.session.flush()

        return model

    async def soft_delete(self, lista_id: int, usuario_id: int, confirmacao_nome: str) -> bool:
        model = await self.buscar_por_id(lista_id, usuario_id)
        if model and model.nome == confirmacao_nome:
            model.deletado_em = datetime.now()
            return True
        return False


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
            select(ProdutoModel).where(ProdutoModel.ativo == True)
        )
        return list(result.scalars().all())


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
    current_user = Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    usecase = SalvarListaUseCase(lista_repo, produto_repo)
    try:
        lista = await usecase.executar(current_user.id, CriarListaInput(
            nome=request.nome,
            itens=[item.model_dump() for item in request.itens],
        ))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Busca itens com nomes dos produtos para resposta
    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append({
            "produto_id": item.produto_id,
            "produto_nome": produto.nome if produto else "Desconhecido",
            "quantidade": item.quantidade,
        })

    return ListaResponse(
        id=lista.id,
        nome=lista.nome,
        itens=itens_resposta,
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
    current_user = Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
):
    usecase = ListarMinhasListasUseCase(lista_repo)
    listas, total = await usecase.executar(current_user.id, pagina, por_pagina, busca)

    items = [
        ListaResumoResponse(
            id=l.id,
            nome=l.nome,
            total_itens=len(l.itens),
            criado_em=l.criado_em.isoformat(),
        )
        for l in listas
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
    current_user = Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    usecase = PromoverListaEfemeraUseCase(lista_repo, produto_repo)
    lista = await usecase.executar(current_user.id, lista_memoria)

    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append({
            "produto_id": item.produto_id,
            "produto_nome": produto.nome if produto else "Desconhecido",
            "quantidade": item.quantidade,
        })

    return ListaResponse(
        id=lista.id,
        nome=lista.nome,
        itens=itens_resposta,
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
    current_user = Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    lista = await lista_repo.buscar_por_id(lista_id, current_user.id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append({
            "produto_id": item.produto_id,
            "produto_nome": produto.nome if produto else "Desconhecido",
            "quantidade": item.quantidade,
        })

    return ListaResponse(
        id=lista.id,
        nome=lista.nome,
        itens=itens_resposta,
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
    current_user = Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
    produto_repo: ProdutoRepository = Depends(get_produto_repo),
):
    usecase = EditarListaUseCase(lista_repo, produto_repo)
    try:
        lista = await usecase.executar(lista_id, current_user.id, CriarListaInput(
            nome=request.nome,
            itens=[item.model_dump() for item in request.itens],
        ))
    except ListaNaoEncontrada:
        raise HTTPException(status_code=404, detail="Lista não encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    itens_resposta = []
    for item in lista.itens:
        produto = await produto_repo.buscar_por_id(item.produto_id)
        itens_resposta.append({
            "produto_id": item.produto_id,
            "produto_nome": produto.nome if produto else "Desconhecido",
            "quantidade": item.quantidade,
        })

    return ListaResponse(
        id=lista.id,
        nome=lista.nome,
        itens=itens_resposta,
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
    current_user = Depends(get_current_user),
    lista_repo: ListaRepository = Depends(get_lista_repo),
):
    usecase = ExcluirListaUseCase(lista_repo)
    sucesso = await usecase.executar(lista_id, current_user.id, confirmacao_nome)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Nome de confirmação incorreto ou lista não encontrada")
