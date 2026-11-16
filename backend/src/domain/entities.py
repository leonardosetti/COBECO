# COBECO Backend — Domain Entities (Clean Architecture)
# Entidades puras de domínio — sem dependências de framework/ORM
# Baseadas em doc-arch-0001-camada-de-dados-canon.md v3.2 (8 tabelas PT-BR)

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum


# ============================================================
# Value Objects
# ============================================================
@dataclass(frozen=True)
class Email:
    """Value Object para Email com validação"""

    valor: str

    def __post_init__(self) -> None:
        if "@" not in self.valor or "." not in self.valor.split("@")[-1]:
            raise ValueError("Email inválido")
        object.__setattr__(self, "valor", self.valor.lower().strip())


@dataclass(frozen=True)
class CNPJ:
    """Value Object para CNPJ formatado"""

    valor: str

    def __post_init__(self) -> None:
        # Remove formatação para validação
        limpo = "".join(c for c in self.valor if c.isdigit())
        if len(limpo) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        object.__setattr__(self, "valor", self.valor)


@dataclass(frozen=True)
class SenhaHash:
    """Value Object para senha hasheada (bcrypt)"""

    valor: str


# ============================================================
# Enums
# ============================================================
class UnidadeMedida(str, Enum):
    UN = "un"
    KG = "kg"
    L = "L"
    M = "m"


# ============================================================
# Entidades de Domínio
# ============================================================


@dataclass
class Usuario:
    """Entidade Usuário — Tabela: usuarios"""

    id: int | None = None
    nome_usuario: str = ""
    email: Email = field(default_factory=lambda: Email(""))
    nome: str = ""
    senha_hash: SenhaHash = field(default_factory=lambda: SenhaHash(""))
    pergunta_seguranca: str = ""
    resposta_seguranca_hash: SenhaHash = field(default_factory=lambda: SenhaHash(""))
    criado_em: datetime = field(default_factory=datetime.now)
    atualizado_em: datetime = field(default_factory=datetime.now)
    deletado_em: datetime | None = None

    # Regras de negócio
    def __post_init__(self) -> None:
        if not 3 <= len(self.nome_usuario) <= 30:
            raise ValueError("nome_usuario deve ter 3-30 caracteres")
        if not self.nome_usuario.isalnum():
            raise ValueError("nome_usuario deve ser alfanumérico")
        if not 2 <= len(self.nome) <= 100:
            raise ValueError("nome deve ter 2-100 caracteres")

    def esta_ativo(self) -> bool:
        return self.deletado_em is None

    def soft_delete(self) -> None:
        self.deletado_em = datetime.now()
        self.atualizado_em = datetime.now()


@dataclass
class Categoria:
    """Entidade Categoria — Tabela: categorias (categorias MACRO de fornecedores)"""

    id: int | None = None
    nome: str = ""
    descricao: str | None = None

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise ValueError("nome da categoria é obrigatório")


@dataclass
class Fornecedor:
    """Entidade Fornecedor — Tabela: fornecedores"""

    id: int | None = None
    nome: str = ""
    cnpj: CNPJ = field(default_factory=lambda: CNPJ(""))
    ativo: bool = True
    criado_em: datetime = field(default_factory=datetime.now)
    categorias: list["Categoria"] = field(default_factory=list)  # N:N via fornecedores_categorias

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise ValueError("nome do fornecedor é obrigatório")


@dataclass
class Produto:
    """Entidade Produto — Tabela: produtos (agnóstico à categoria)"""

    id: int | None = None
    nome: str = ""
    unidade: UnidadeMedida = UnidadeMedida.UN
    ativo: bool = True
    criado_em: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise ValueError("nome do produto é obrigatório")


@dataclass
class FornecedorProduto:
    """Entidade de Relacionamento — Tabela: fornecedores_produtos (preços e estoque)"""

    fornecedor_id: int
    produto_id: int
    preco: Decimal
    estoque: int = 0
    ativo: bool = True

    def __post_init__(self) -> None:
        if self.preco < 0:
            raise ValueError("preco não pode ser negativo")
        if self.estoque < 0:
            raise ValueError("estoque não pode ser negativo")


@dataclass
class Lista:
    """Entidade Lista — Tabela: listas"""

    id: int | None = None
    usuario_id: int = 0
    nome: str = ""
    criado_em: datetime = field(default_factory=datetime.now)
    atualizado_em: datetime = field(default_factory=datetime.now)
    deletado_em: datetime | None = None
    itens: list["ItemLista"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 1 <= len(self.nome) <= 100:
            raise ValueError("nome da lista deve ter 1-100 caracteres")

    def esta_ativa(self) -> bool:
        return self.deletado_em is None

    def soft_delete(self, confirmacao_nome: str) -> None:
        if confirmacao_nome != self.nome:
            raise ValueError("Confirmação de nome incorreta")
        self.deletado_em = datetime.now()
        self.atualizado_em = datetime.now()


@dataclass
class ItemLista:
    """Entidade ItemLista — Tabela: itens_lista"""

    id: int | None = None
    lista_id: int = 0
    produto_id: int = 0
    quantidade: int = 1
    criado_em: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not 1 <= self.quantidade <= 9999:
            raise ValueError("quantidade deve ser entre 1 e 9999")


# ============================================================
# Entidades para Comparação (RF15, RF16)
# ============================================================


@dataclass
class ItemComparacao:
    """Item na tabela flat de comparação"""

    produto_id: int
    produto_nome: str
    unidade: str
    quantidade: int
    preco_unitario: Decimal | None = None
    preco_total: Decimal | None = None
    disponivel: bool = False


@dataclass
class FornecedorComparacao:
    """Fornecedor na tabela flat de comparação"""

    fornecedor_id: int
    fornecedor_nome: str
    itens_disponiveis: int = 0
    itens_ausentes: int = 0
    preco_total: Decimal = Decimal("0")
    percentual_disponibilidade: float = 0.0
    itens: list[ItemComparacao] = field(default_factory=list)


@dataclass
class OrcamentoComparacao:
    """Resultado completo da comparação (RF15, RF16)"""

    lista_id: int
    lista_nome: str
    fornecedores: list[FornecedorComparacao] = field(default_factory=list)
    melhor_fornecedor_id: int | None = None
    calculado_em: datetime = field(default_factory=datetime.now)

    def ordenar_por_preco(self) -> None:
        """Ordena fornecedores por preço total ASC (RF15)"""
        self.fornecedores.sort(key=lambda f: f.preco_total)
        if self.fornecedores:
            self.melhor_fornecedor_id = self.fornecedores[0].fornecedor_id


# ============================================================
# Entidade: Sessao (Refresh Tokens / Session Management)
# ============================================================


@dataclass
class Sessao:
    """Entidade Sessao — Tabela: sessoes (refresh tokens)"""

    id: int | None = None
    usuario_id: int = 0
    refresh_token_hash: str = ""
    user_agent: str | None = None
    ip: str | None = None
    criado_em: datetime = field(default_factory=datetime.now)
    expira_em: datetime = field(default_factory=datetime.now)
    revogada_em: datetime | None = None

    def esta_ativa(self) -> bool:
        return self.revogada_em is None and datetime.now() < self.expira_em

    def revogar(self) -> None:
        self.revogada_em = datetime.now()
