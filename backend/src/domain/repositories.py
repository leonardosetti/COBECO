# COBECO Backend — Repository Interfaces (Domain Ports)
# Clean Architecture: Domain define interfaces, Adapters implementam

from abc import ABC, abstractmethod
from typing import Optional, List, Sequence
from decimal import Decimal
from src.domain.entities import (
    Usuario, Categoria, Fornecedor, Produto,
    FornecedorProduto, Lista, ItemLista,
    OrcamentoComparacao, FornecedorComparacao, ItemComparacao
)
from src.config import settings


# ============================================================
# Usuario Repository
# ============================================================
class UsuarioRepository(ABC):
    @abstractmethod
    async def criar(self, usuario: Usuario) -> Usuario:
        """Cria novo usuário (RF01)"""
        ...

    @abstractmethod
    async def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        ...

    @abstractmethod
    async def buscar_por_nome_usuario(self, nome_usuario: str) -> Optional[Usuario]:
        """Busca por login (RF02)"""
        ...

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Verifica unicidade de email (RF01, RF06)"""
        ...

    @abstractmethod
    async def atualizar(self, usuario: Usuario) -> Usuario:
        """Atualiza perfil (RF06)"""
        ...

    @abstractmethod
    async def soft_delete(self, usuario_id: int) -> bool:
        ...


# ============================================================
# Categoria Repository
# ============================================================
class CategoriaRepository(ABC):
    @abstractmethod
    async def listar_todas(self) -> List[Categoria]:
        """Lista categorias para pré-filtro (RF12, UC03)"""
        ...

    @abstractmethod
    async def buscar_por_id(self, categoria_id: int) -> Optional[Categoria]:
        ...

    @abstractmethod
    async def buscar_por_ids(self, ids: List[int]) -> List[Categoria]:
        ...


# ============================================================
# Fornecedor Repository
# ============================================================
class FornecedorRepository(ABC):
    @abstractmethod
    async def listar_ativos(self) -> List[Fornecedor]:
        """Lista fornecedores ativos para seleção (RF13, UC04)"""
        ...

    @abstractmethod
    async def listar_por_categorias(self, categoria_ids: List[int]) -> List[Fornecedor]:
        """Filtra fornecedores por categorias selecionadas (RF12, RF13)"""
        ...

    @abstractmethod
    async def buscar_por_id(self, fornecedor_id: int) -> Optional[Fornecedor]:
        ...

    @abstractmethod
    async def buscar_por_ids(self, ids: List[int]) -> List[Fornecedor]:
        ...

    @abstractmethod
    async def calcular_disponibilidade(
        self,
        fornecedor_id: int,
        produto_ids: List[int],
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
    async def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        ...

    @abstractmethod
    async def buscar_por_ids(self, ids: List[int]) -> List[Produto]:
        ...

    @abstractmethod
    async def autocomplete(self, query: str, limit: int = 10) -> List[Produto]:
        """Autocomplete para criação de lista (RF07, UC02)"""
        ...

    @abstractmethod
    async def listar_ativos(self) -> List[Produto]:
        ...


# ============================================================
# Lista Repository
# ============================================================
class ListaRepository(ABC):
    @abstractmethod
    async def criar(self, lista: Lista) -> Lista:
        """Salva lista no banco (RF08) - transação com itens"""
        ...

    @abstractmethod
    async def buscar_por_id(self, lista_id: int, usuario_id: int) -> Optional[Lista]:
        ...

    @abstractmethod
    async def listar_por_usuario(
        self,
        usuario_id: int,
        pagina: int = 1,
        por_pagina: int = 20,
        busca: Optional[str] = None,
    ) -> Sequence[Lista]:
        """Lista paginada do usuário (RF09)"""
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
    @abstractmethod
    async def calcular_orcamento(
        self,
        lista_id: int,
        fornecedor_ids: List[int],
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
    async def buscar_precos_para_comparacao(
        self,
        produto_ids: List[int],
        fornecedor_ids: List[int],
    ) -> List[FornecedorProduto]:
        """Busca preços ativos para produtos/fornecedores"""
        ...


# ============================================================
# Exportação Repository (RF17)
# ============================================================
class ExportacaoRepository(ABC):
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