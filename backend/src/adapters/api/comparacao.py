# COBECO Backend — Comparação Router (FastAPI)
# Endpoints: POST /v1/comparacao/calcular (RF15, RF16)
# RF15: cache 5min + timeout 10s no cálculo de orçamento

import asyncio
import time
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.auth import get_current_user
from src.adapters.db.database import get_db
from src.adapters.db.models import (
    FornecedorModel,
    FornecedorProdutoModel,
    ItemListaModel,
    ListaModel,
    ProdutoModel,
)
from src.domain.repositories import ComparacaoRepository
from src.domain.usecases import (
    CalcularOrcamentoUseCase,
    ComparacaoInput,
    FornecedoresInsuficientes,
)

router = APIRouter(tags=["Comparação"])

# ============================================================
# Cache de orçamento (RF15: cache 5min)
# ============================================================
_ORCAMENTO_CACHE: dict[str, tuple[float, object]] = {}
_CACHE_TTL_SECONDS = 300  # 5 minutos


def _cache_key(lista_id: int, fornecedor_ids: list[int], disponibilidade_minima: float) -> str:
    fids = ",".join(map(str, sorted(fornecedor_ids)))
    return f"{lista_id}:{fids}:{disponibilidade_minima}"


def _cache_get(key: str):
    entry = _ORCAMENTO_CACHE.get(key)
    if not entry:
        return None
    ts, value = entry
    if time.time() - ts > _CACHE_TTL_SECONDS:
        _ORCAMENTO_CACHE.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: object) -> None:
    _ORCAMENTO_CACHE[key] = (time.time(), value)


# ============================================================
# Schemas
# ============================================================
class ItemComparacaoResponse(BaseModel):
    produto_id: int
    produto_nome: str
    unidade: str
    quantidade: int
    preco_unitario: float | None = None
    preco_total: float | None = None
    disponivel: bool


class FornecedorComparacaoResponse(BaseModel):
    fornecedor_id: int
    fornecedor_nome: str
    itens_disponiveis: int
    itens_ausentes: int
    preco_total: float
    percentual_disponibilidade: float
    eh_melhor: bool
    itens: list[ItemComparacaoResponse]


class CalcularOrcamentoRequest(BaseModel):
    lista_id: int
    fornecedor_ids: list[int] = Field(..., min_length=2)
    disponibilidade_minima: float = Field(0.0, ge=0.0, le=100.0)


class ItemEfemeroRequest(BaseModel):
    produto_id: int = Field(..., gt=0)
    quantidade: int = Field(..., ge=1, le=9999)


class CalcularOrcamentoEfemeroRequest(BaseModel):
    itens: list[ItemEfemeroRequest] = Field(..., min_length=1)
    fornecedor_ids: list[int] = Field(..., min_length=2)
    disponibilidade_minima: float = Field(0.0, ge=0.0, le=100.0)
    lista_nome: str = Field("Lista", max_length=100)


class OrcamentoResponse(BaseModel):
    lista_id: int
    lista_nome: str
    melhor_fornecedor_id: int | None = None
    fornecedores: list[FornecedorComparacaoResponse]


# ============================================================
# Repository Implementation
# ============================================================
class ComparacaoRepositoryImpl(ComparacaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def calcular_orcamento(
        self,
        lista_id: int,
        fornecedor_ids: list[int],
        disponibilidade_minima: float = 0.0,
    ):
        # 1. Busca lista e itens
        lista_result = await self.session.execute(
            select(ListaModel).where(ListaModel.id == lista_id, ListaModel.deletado_em.is_(None))
        )
        lista = lista_result.scalar_one_or_none()
        if not lista:
            raise HTTPException(status_code=404, detail="Lista não encontrada")

        itens_result = await self.session.execute(
            select(ItemListaModel).where(ItemListaModel.lista_id == lista_id)
        )
        itens_lista = list(itens_result.scalars().all())
        if not itens_lista:
            raise HTTPException(status_code=400, detail="Lista vazia")

        return await self.calcular_orcamento_itens(
            [{"produto_id": i.produto_id, "quantidade": i.quantidade} for i in itens_lista],
            fornecedor_ids,
            disponibilidade_minima,
            lista_nome=lista.nome,
            lista_id=lista.id,
        )

    async def calcular_orcamento_itens(  # noqa: PLR0912
        self,
        itens: list[dict],
        fornecedor_ids: list[int],
        disponibilidade_minima: float = 0.0,
        lista_nome: str = "Lista",
        lista_id: int = 0,
    ):
        """Núcleo do cálculo (RF15/RF16) — recebe itens em memória (lista efêmera
        ou persistida). Regra da Melhor Oferta: maior cobertura; empate → menor total."""

        # RF15: cache 5min — para lista efémera (lista_id=0), inclui os itens
        # na chave para não colidir entre visitantes diferentes
        if lista_id == 0:
            itens_key = ",".join(
                f"{i['produto_id']}:{i['quantidade']}"
                for i in sorted(itens, key=lambda x: x["produto_id"])
            )
            key = f"ephemeral:{itens_key}:{','.join(map(str, sorted(fornecedor_ids)))}:{disponibilidade_minima}"
        else:
            key = _cache_key(lista_id, fornecedor_ids, disponibilidade_minima)
        cached = _cache_get(key)
        if cached is not None:
            return cached

        class _Item:  # duck-type de ItemListaModel para o loop abaixo
            def __init__(self, produto_id: int, quantidade: int):
                self.produto_id = produto_id
                self.quantidade = quantidade

        itens_lista = [_Item(int(i["produto_id"]), int(i["quantidade"])) for i in itens]
        if not itens_lista:
            raise HTTPException(status_code=400, detail="Lista vazia")

        produto_ids = [item.produto_id for item in itens_lista]

        # 2. Busca produtos (para nomes/unidades)
        produtos_result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id.in_(produto_ids))
        )
        produtos_map = {p.id: p for p in produtos_result.scalars().all()}

        # 3. Busca fornecedores
        fornecedores_result = await self.session.execute(
            select(FornecedorModel).where(
                FornecedorModel.id.in_(fornecedor_ids),
                FornecedorModel.ativo,
            )
        )
        fornecedores = list(fornecedores_result.scalars().all())
        if len(fornecedores) < 2:
            raise FornecedoresInsuficientes

        # 4. Para cada fornecedor, busca preços
        fornecedores_comparacao = []

        for fornecedor in fornecedores:
            # Busca preços ativos com estoque
            precos_result = await self.session.execute(
                select(FornecedorProdutoModel).where(
                    FornecedorProdutoModel.fornecedor_id == fornecedor.id,
                    FornecedorProdutoModel.produto_id.in_(produto_ids),
                    FornecedorProdutoModel.ativo,
                    FornecedorProdutoModel.estoque > 0,
                )
            )
            precos = list(precos_result.scalars().all())
            precos_map = {p.produto_id: p for p in precos}

            # Monta itens da comparação
            itens_comparacao = []
            itens_disponiveis = 0
            itens_ausentes = 0
            preco_total = Decimal("0")

            for item_lista in itens_lista:
                produto = produtos_map.get(item_lista.produto_id)
                preco_fp = precos_map.get(item_lista.produto_id)

                if preco_fp and preco_fp.estoque >= item_lista.quantidade:
                    preco_unit = preco_fp.preco
                    preco_item = preco_unit * item_lista.quantidade
                    disponivel = True
                    itens_disponiveis += 1
                else:
                    preco_unit = None
                    preco_item = None
                    disponivel = False
                    itens_ausentes += 1

                if preco_item:
                    preco_total += preco_item

                itens_comparacao.append(
                    ItemComparacaoResponse(
                        produto_id=item_lista.produto_id,
                        produto_nome=produto.nome if produto else "Desconhecido",
                        unidade=produto.unidade if produto else "un",
                        quantidade=item_lista.quantidade,
                        preco_unitario=float(preco_unit) if preco_unit else None,
                        preco_total=float(preco_item) if preco_item else None,
                        disponivel=disponivel,
                    )
                )

            percentual = (itens_disponiveis / len(itens_lista) * 100) if itens_lista else 0

            # Filtra por disponibilidade mínima
            if percentual < disponibilidade_minima:
                continue

            fornecedores_comparacao.append(
                FornecedorComparacaoResponse(
                    fornecedor_id=fornecedor.id,
                    fornecedor_nome=fornecedor.nome,
                    itens_disponiveis=itens_disponiveis,
                    itens_ausentes=itens_ausentes,
                    preco_total=float(preco_total),
                    percentual_disponibilidade=round(percentual, 1),
                    eh_melhor=False,  # Será definido após ordenação
                    itens=itens_comparacao,
                )
            )

        # 5. Ordena exibição por preço total ASC (RF15)
        fornecedores_comparacao.sort(key=lambda f: f.preco_total)

        # Melhor Oferta (RF16): maior % cobertura; empate → menor custo total
        if fornecedores_comparacao:
            melhor = max(
                fornecedores_comparacao,
                key=lambda f: (f.percentual_disponibilidade, -f.preco_total),
            )
            melhor.eh_melhor = True
            melhor_id = melhor.fornecedor_id
        else:
            melhor_id = None

        result = OrcamentoResponse(
            lista_id=lista_id,
            lista_nome=lista_nome,
            melhor_fornecedor_id=melhor_id,
            fornecedores=fornecedores_comparacao,
        )
        _cache_set(key, result)
        return result

    async def buscar_precos_para_comparacao(
        self,
        produto_ids: list[int],
        fornecedor_ids: list[int],
    ):
        result = await self.session.execute(
            select(FornecedorProdutoModel).where(
                FornecedorProdutoModel.fornecedor_id.in_(fornecedor_ids),
                FornecedorProdutoModel.produto_id.in_(produto_ids),
                FornecedorProdutoModel.ativo,
            )
        )
        return list(result.scalars().all())


def get_comparacao_repo(
    session: AsyncSession = Depends(get_db),
) -> ComparacaoRepository:
    return ComparacaoRepositoryImpl(session)


# ============================================================
# Endpoints
# ============================================================
@router.post(
    "/calcular",
    response_model=OrcamentoResponse,
    summary="UC06/RF15 - Calcular Orçamento (Tabela Flat)",
)
async def calcular_orcamento(
    request: CalcularOrcamentoRequest,
    current_user=Depends(get_current_user),
    repo: ComparacaoRepository = Depends(get_comparacao_repo),
):
    # Segurança: lista só pode ser comparada pelo seu proprietário
    lista_result = await repo.session.execute(
        select(ListaModel).where(
            ListaModel.id == request.lista_id,
            ListaModel.usuario_id == current_user.id,
            ListaModel.deletado_em.is_(None),
        )
    )
    if lista_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    usecase = CalcularOrcamentoUseCase(repo)
    try:
        # RF15: timeout 10s no cálculo de orçamento
        result = await asyncio.wait_for(
            usecase.executar(
                ComparacaoInput(
                    lista_id=request.lista_id,
                    fornecedor_ids=request.fornecedor_ids,
                    disponibilidade_minima=request.disponibilidade_minima,
                )
            ),
            timeout=10.0,
        )
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Cálculo de orçamento excedeu o tempo limite (10s)")
    except FornecedoresInsuficientes:
        raise HTTPException(status_code=400, detail="Selecione pelo menos 2 fornecedores")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result


@router.post(
    "/calcular-efemera",
    response_model=OrcamentoResponse,
    summary="UC06/RF15 - Calcular Orçamento (Lista Efêmera — sem login)",
)
async def calcular_orcamento_efemera(
    request: CalcularOrcamentoEfemeroRequest,
    repo: ComparacaoRepository = Depends(get_comparacao_repo),
):
    """Autenticação Tardia (SPECS §7): visitante compara sem login, itens em memória."""
    try:
        # RF15: timeout 10s no cálculo de orçamento
        return await asyncio.wait_for(
            repo.calcular_orcamento_itens(
                [item.model_dump() for item in request.itens],
                request.fornecedor_ids,
                request.disponibilidade_minima,
                lista_nome=request.lista_nome,
            ),
            timeout=10.0,
        )
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Cálculo de orçamento excedeu o tempo limite (10s)")
    except FornecedoresInsuficientes:
        raise HTTPException(status_code=400, detail="Selecione pelo menos 2 fornecedores")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/visualizar/{lista_id}",
    response_model=OrcamentoResponse,
    summary="UC07/RF16 - Visualizar Resultados da Comparação",
)
async def visualizar_resultados(
    lista_id: int,
    fornecedores: str = Query(..., description="IDs de fornecedores separados por vírgula"),
    disponibilidade_minima: float = Query(0.0, ge=0.0, le=100.0),
    current_user=Depends(get_current_user),
    repo: ComparacaoRepository = Depends(get_comparacao_repo),
):
    # Segurança: lista só pode ser visualizada pelo seu proprietário
    lista_result = await repo.session.execute(
        select(ListaModel).where(
            ListaModel.id == lista_id,
            ListaModel.usuario_id == current_user.id,
            ListaModel.deletado_em.is_(None),
        )
    )
    if lista_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    fornecedor_ids = [int(f) for f in fornecedores.split(",")]

    usecase = CalcularOrcamentoUseCase(repo)
    result = await usecase.executar(
        ComparacaoInput(
            lista_id=lista_id,
            fornecedor_ids=fornecedor_ids,
            disponibilidade_minima=disponibilidade_minima,
        )
    )

    return result
