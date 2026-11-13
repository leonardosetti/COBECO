# COBECO Backend — Comparação Router (FastAPI)
# Endpoints: POST /v1/comparacao/calcular (RF15, RF16)

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal

from src.domain.usecases import (
    CalcularOrcamentoUseCase, VisualizarResultadosUseCase,
    ComparacaoInput, FornecedoresInsuficientes,
)
from src.domain.repositories import ComparacaoRepository, ListaRepository
from src.adapters.db.models import (
    ListaModel, ItemListaModel, FornecedorModel, ProdutoModel,
    FornecedorProdutoModel, FornecedorCategoriaModel, CategoriaModel
)
from src.adapters.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.adapters.api.auth import get_current_user

router = APIRouter(tags=["Comparação"])


# ============================================================
# Schemas
# ============================================================
class ItemComparacaoResponse(BaseModel):
    produto_id: int
    produto_nome: str
    unidade: str
    quantidade: int
    preco_unitario: Optional[float] = None
    preco_total: Optional[float] = None
    disponivel: bool


class FornecedorComparacaoResponse(BaseModel):
    fornecedor_id: int
    fornecedor_nome: str
    itens_disponiveis: int
    itens_ausentes: int
    preco_total: float
    percentual_disponibilidade: float
    eh_melhor: bool
    itens: List[ItemComparacaoResponse]


class CalcularOrcamentoRequest(BaseModel):
    lista_id: int
    fornecedor_ids: List[int] = Field(..., min_length=2)
    disponibilidade_minima: float = Field(0.0, ge=0.0, le=100.0)


class OrcamentoResponse(BaseModel):
    lista_id: int
    lista_nome: str
    melhor_fornecedor_id: Optional[int] = None
    fornecedores: List[FornecedorComparacaoResponse]


# ============================================================
# Repository Implementation
# ============================================================
class ComparacaoRepositoryImpl(ComparacaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def calcular_orcamento(
        self,
        lista_id: int,
        fornecedor_ids: List[int],
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
                FornecedorModel.ativo == True,
            )
        )
        fornecedores = list(fornecedores_result.scalars().all())
        if len(fornecedores) < 2:
            raise FornecedoresInsuficientes()

        # 4. Para cada fornecedor, busca preços
        fornecedores_comparacao = []

        for fornecedor in fornecedores:
            # Busca preços ativos com estoque
            precos_result = await self.session.execute(
                select(FornecedorProdutoModel).where(
                    FornecedorProdutoModel.fornecedor_id == fornecedor.id,
                    FornecedorProdutoModel.produto_id.in_(produto_ids),
                    FornecedorProdutoModel.ativo == True,
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

                itens_comparacao.append(ItemComparacaoResponse(
                    produto_id=item_lista.produto_id,
                    produto_nome=produto.nome if produto else "Desconhecido",
                    unidade=produto.unidade if produto else "un",
                    quantidade=item_lista.quantidade,
                    preco_unitario=float(preco_unit) if preco_unit else None,
                    preco_total=float(preco_item) if preco_item else None,
                    disponivel=disponivel,
                ))

            percentual = (itens_disponiveis / len(itens_lista) * 100) if itens_lista else 0

            # Filtra por disponibilidade mínima
            if percentual < disponibilidade_minima:
                continue

            fornecedores_comparacao.append(FornecedorComparacaoResponse(
                fornecedor_id=fornecedor.id,
                fornecedor_nome=fornecedor.nome,
                itens_disponiveis=itens_disponiveis,
                itens_ausentes=itens_ausentes,
                preco_total=float(preco_total),
                percentual_disponibilidade=round(percentual, 1),
                eh_melhor=False,  # Será definido após ordenação
                itens=itens_comparacao,
            ))

        # 5. Ordena por preço total ASC (RF15)
        fornecedores_comparacao.sort(key=lambda f: f.preco_total)

        # Marca melhor oferta
        if fornecedores_comparacao:
            fornecedores_comparacao[0].eh_melhor = True
            melhor_id = fornecedores_comparacao[0].fornecedor_id
        else:
            melhor_id = None

        return OrcamentoResponse(
            lista_id=lista.id,
            lista_nome=lista.nome,
            melhor_fornecedor_id=melhor_id,
            fornecedores=fornecedores_comparacao,
        )

    async def buscar_precos_para_comparacao(
        self,
        produto_ids: List[int],
        fornecedor_ids: List[int],
    ):
        result = await self.session.execute(
            select(FornecedorProdutoModel).where(
                FornecedorProdutoModel.fornecedor_id.in_(fornecedor_ids),
                FornecedorProdutoModel.produto_id.in_(produto_ids),
                FornecedorProdutoModel.ativo == True,
            )
        )
        return list(result.scalars().all())


def get_comparacao_repo(session: AsyncSession = Depends(get_db)) -> ComparacaoRepository:
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
    current_user = Depends(get_current_user),
    repo: ComparacaoRepository = Depends(get_comparacao_repo),
):
    usecase = CalcularOrcamentoUseCase(repo)
    try:
        result = await usecase.executar(ComparacaoInput(
            lista_id=request.lista_id,
            fornecedor_ids=request.fornecedor_ids,
            disponibilidade_minima=request.disponibilidade_minima,
        ))
    except FornecedoresInsuficientes:
        raise HTTPException(status_code=400, detail="Selecione pelo menos 2 fornecedores")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result


@router.get(
    "/visualizar/{lista_id}",
    response_model=OrcamentoResponse,
    summary="UC07/RF16 - Visualizar Resultados da Comparação",
)
async def visualizar_resultados(
    lista_id: int,
    fornecedores: str = Query(..., description="IDs de fornecedores separados por vírgula"),
    disponibilidade_minima: float = Query(0.0, ge=0.0, le=100.0),
    current_user = Depends(get_current_user),
    repo: ComparacaoRepository = Depends(get_comparacao_repo),
):
    fornecedor_ids = [int(f) for f in fornecedores.split(",")]

    usecase = CalcularOrcamentoUseCase(repo)
    result = await usecase.executar(ComparacaoInput(
        lista_id=lista_id,
        fornecedor_ids=fornecedor_ids,
        disponibilidade_minima=disponibilidade_minima,
    ))

    return result