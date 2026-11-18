# COBECO Backend — Repository Interfaces (Domain Ports)
# Clean Architecture: Domain define interfaces, Adapters implementam

from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import (
    Categoria,
    Fornecedor,
    FornecedorProduto,
    Lista,
    OrcamentoComparacao,
    Produto,
    Sessao,
    Usuario,
)


# ============================================================
# Usuario Repository
# ============================================================
class UsuarioRepository(ABC):
    @abstractmethod
    async def criar(self, usuario: Usuario) -> Usuario:
        """Cria novo usuário (RF01)"""
        ...

    @abstractmethod
    async def buscar_por_id(self, usuario_id: int) -> Usuario | None: ...

    @abstractmethod
    async def buscar_por_nome_usuario(self, nome_usuario: str) -> Usuario | None:
        """Busca por login (RF02)"""
        ...

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Usuario | None:
        """Verifica unicidade de email (RF01, RF06)"""
        ...

    @abstractmethod
    async def atualizar(self, usuario: Usuario) -> Usuario:
        """Atualiza perfil (RF06)"""
        ...

    @abstractmethod
    async def soft_delete(self, usuario_id: int) -> bool: ...


# ============================================================
# Categoria Repository
# ============================================================
class CategoriaRepository(ABC):
    @abstractmethod
    async def listar_todas(self) -> list[Categoria]:
        """Lista categorias para pré-filtro (RF12, UC03)"""
        ...

    @abstractmethod
    async def buscar_por_id(self, categoria_id: int) -> Categoria | None: ...

    @abstractmethod
    async def buscar_por_ids(self, ids: list[int]) -> list[Categoria]: ...


# ============================================================
# Fornecedor Repository
# ============================================================
class FornecedorRepository(ABC):
    @abstractmethod
    async def listar_ativos(self) -> list[Fornecedor]:
        """Lista fornecedores ativos para seleção (RF13, UC04)"""
        ...

    @abstractmethod
    async def listar_por_categorias(self, categoria_ids: list[int]) -> list[Fornecedor]:
        """Filtra fornecedores por categorias selecionadas (RF12, RF13)"""
        ...

    @abstractmethod
    async def buscar_por_id(self, fornecedor_id: int) -> Fornecedor | None: ...

    @abstractmethod
    async def buscar_por_ids(self, ids: list[int]) -> list[Fornecedor]: ...

    @abstractmethod
    async def calcular_disponibilidade(
        self,
        fornecedor_id: int,
        produto_ids: list[int],
    ) -> tuple[int, int, Decimal]:
        """
        Calcula disponibilidade para um fornecedor dado uma lista de produtos.
        Returns: (itens_disponiveis, itens_ausentes, preco_total)
        """
        ...


# ============================================================
# Produto Repository
# ============================================================
class ProdutoRepository(ABC):
    @abstractmethod
    async def buscar_por_id(self, produto_id: int) -> Produto | None: ...

    @abstractmethod
    async def buscar_por_ids(self, ids: list[int]) -> list[Produto]: ...

    @abstractmethod
    async def autocomplete(self, query: str, limit: int = 10) -> list[Produto]:
        """Autocomplete para criação de lista (RF07, UC02)"""
        ...

    @abstractmethod
    async def listar_ativos(self, limit: int | None = None) -> list[Produto]: ...

    @abstractmethod
    async def count_ativos(self) -> int: ...


# ============================================================
# Lista Repository
# ============================================================
class ListaRepository(ABC):
    @abstractmethod
    async def criar(self, lista: Lista) -> Lista:
        """Salva lista no banco (RF08) - transação com itens"""
        ...

    @abstractmethod
    async def buscar_por_id(self, lista_id: int, usuario_id: int) -> Lista | None: ...

    @abstractmethod
    async def listar_por_usuario(
        self,
        usuario_id: int,
        pagina: int = 1,
        por_pagina: int = 20,
        busca: str | None = None,
    ) -> tuple[Sequence[Lista], int]:
        """Lista paginada do usuário (RF09) — retorna (listas, total)"""
        ...

    @abstractmethod
    async def atualizar(self, lista: Lista) -> Lista:
        """Edita lista salva (RF10)"""
        ...

    @abstractmethod
    async def soft_delete(self, lista_id: int, usuario_id: int, confirmacao_nome: str) -> bool:
        """Exclusão lógica com confirmação (RF11)"""
        ...


# ============================================================
# Comparação Repository (RF15, RF16)
# ============================================================
class ComparacaoRepository(ABC):
    """Camada de comparação (RF15, RF16) — expõe sessão para queries de segurança."""

    session: AsyncSession  # definido na implementação concreta

    @abstractmethod
    async def calcular_orcamento(
        self,
        lista_id: int,
        fornecedor_ids: list[int],
        disponibilidade_minima: float = 0.0,
    ) -> OrcamentoComparacao:
        """
        Calcula orçamento flat comparativo (RF15)
        - Timeout: 10s (config)
        - Cache: 5min (config)
        - Ordena por preço ASC
        """
        ...

    @abstractmethod
    async def calcular_orcamento_itens(
        self,
        itens: list[dict],
        fornecedor_ids: list[int],
        disponibilidade_minima: float = 0.0,
        lista_nome: str = "Lista",
    ) -> OrcamentoComparacao:
        """
        Calcula orçamento a partir de itens em memória (RF15, lista efêmera).
        Não exige lista persistida — suporta visitante (Autenticação Tardia).
        itens: [{"produto_id": int, "quantidade": int}, ...]
        """
        ...

    @abstractmethod
    async def buscar_precos_para_comparacao(
        self,
        produto_ids: list[int],
        fornecedor_ids: list[int],
    ) -> list[FornecedorProduto]:
        """Busca preços ativos para produtos/fornecedores"""
        ...


# ============================================================
# Exportação Repository (RF17)
# ============================================================
class ExportacaoRepository(ABC):
    """Exportação (RF17) — expõe sessão para queries auxiliares."""

    session: AsyncSession  # definido na implementação concreta

    @abstractmethod
    async def gerar_pdf_lista(self, lista_id: int) -> bytes:
        """
        Gera PDF da lista (RF17)
        - Server-side com ReportLab
        - Funciona para visitantes (sem auth)
        - Nome: lista_YYYYMMDD.pdf
        - Formato A4
        - <5s para até 100 itens (RNF11)
        """
        ...

    @abstractmethod
    async def gerar_pdf_vencedora(self, orcamento) -> bytes:
        """
        Gera PDF da LISTA VENCEDORA (RF17)
        - Server-side com ReportLab, A4
        - Exporta APENAS a lista do fornecedor campeão precificada
          (nunca a tabela comparativa)
        - Nome: lista_YYYYMMDD.pdf
        """
        ...


# ============================================================
# Sessao Repository (RF02 - Refresh Tokens)
# ============================================================
class SessaoRepository(ABC):
    @abstractmethod
    async def criar(self, sessao: Sessao) -> Sessao:
        """Cria nova sessão (refresh token)"""
        ...

    @abstractmethod
    async def buscar_por_token_hash(self, token_hash: str) -> Sessao | None:
        """Busca sessão por hash do refresh token"""
        ...

    @abstractmethod
    async def buscar_ativas_por_usuario(self, usuario_id: int) -> list[Sessao]:
        """Lista sessões ativas do usuário"""
        ...

    @abstractmethod
    async def revogar(self, sessao_id: int) -> bool:
        """Revoga sessão (logout)"""
        ...

    @abstractmethod
    async def revogar_todas_do_usuario(self, usuario_id: int) -> int:
        """Revoga todas as sessões do usuário (logout everywhere)"""
        ...

    @abstractmethod
    async def limpar_expiradas(self) -> int:
        """Limpa sessões expiradas (job de manutenção)"""
        ...
