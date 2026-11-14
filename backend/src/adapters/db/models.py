# COBECO Backend — SQLAlchemy Models (Adapters/DB)
# Mapeamento ORM para as 8 tabelas PT-BR (CAMADADEDADOS.md v3.2)
# Clean Architecture: Adapters não vazam para Domain

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.database import Base


# ============================================================
# Tabela: usuarios
# ============================================================
class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_usuario: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    pergunta_seguranca: Mapped[str] = mapped_column(String(255), nullable=False)
    resposta_seguranca_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deletado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relacionamentos
    listas: Mapped[list["ListaModel"]] = relationship(
        "ListaModel", back_populates="usuario", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("LENGTH(nome_usuario) BETWEEN 3 AND 30", name="ck_usuario_nome_usuario_len"),
        CheckConstraint("LENGTH(nome) BETWEEN 2 AND 100", name="ck_usuario_nome_len"),
        Index("ix_usuario_criado_em", "criado_em"),
    )

    def to_domain(self) -> "Usuario":
        from src.domain.entities import Email, SenhaHash, Usuario
        return Usuario(
            id=self.id,
            nome_usuario=self.nome_usuario,
            email=Email(self.email),
            nome=self.nome,
            senha_hash=SenhaHash(self.senha_hash),
            pergunta_seguranca=self.pergunta_seguranca,
            resposta_seguranca_hash=SenhaHash(self.resposta_seguranca_hash),
            criado_em=self.criado_em,
            atualizado_em=self.atualizado_em,
            deletado_em=self.deletado_em,
        )


# ============================================================
# Tabela: listas
# ============================================================
class ListaModel(Base):
    __tablename__ = "listas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deletado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relacionamentos
    usuario: Mapped["UsuarioModel"] = relationship("UsuarioModel", back_populates="listas")
    itens: Mapped[list["ItemListaModel"]] = relationship(
        "ItemListaModel", back_populates="lista", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("LENGTH(nome) BETWEEN 1 AND 100", name="ck_lista_nome_len"),
        Index("ix_lista_usuario_criado", "usuario_id", "criado_em"),
    )

    def to_domain(self) -> "Lista":
        from src.domain.entities import Lista
        return Lista(
            id=self.id,
            usuario_id=self.usuario_id,
            nome=self.nome,
            criado_em=self.criado_em,
            atualizado_em=self.atualizado_em,
            deletado_em=self.deletado_em,
            itens=[item.to_domain() for item in self.itens],
        )


# ============================================================
# Tabela: itens_lista
# ============================================================
class ItemListaModel(Base):
    __tablename__ = "itens_lista"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lista_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("listas.id", ondelete="CASCADE"), nullable=False, index=True
    )
    produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relacionamentos
    lista: Mapped["ListaModel"] = relationship("ListaModel", back_populates="itens")
    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel")

    # Constraints
    __table_args__ = (
        CheckConstraint("quantidade BETWEEN 1 AND 9999", name="ck_item_quantidade"),
        UniqueConstraint("lista_id", "produto_id", name="uq_item_lista_produto"),
    )

    def to_domain(self) -> "ItemLista":
        from src.domain.entities import ItemLista
        return ItemLista(
            id=self.id,
            lista_id=self.lista_id,
            produto_id=self.produto_id,
            quantidade=self.quantidade,
            criado_em=self.criado_em,
        )


# ============================================================
# Tabela: categorias
# ============================================================
class CategoriaModel(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relacionamentos N:N via fornecedores_categorias
    fornecedores: Mapped[list["FornecedorModel"]] = relationship(
        "FornecedorModel", secondary="fornecedores_categorias", back_populates="categorias"
    )

    __table_args__ = (
        Index("ix_categoria_nome", "nome"),
    )

    def to_domain(self) -> "Categoria":
        from src.domain.entities import Categoria
        return Categoria(
            id=self.id,
            nome=self.nome,
            descricao=self.descricao,
        )


# ============================================================
# Tabela: fornecedores
# ============================================================
class FornecedorModel(Base):
    __tablename__ = "fornecedores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relacionamentos
    categorias: Mapped[list["CategoriaModel"]] = relationship(
        "CategoriaModel", secondary="fornecedores_categorias", back_populates="fornecedores"
    )
    produtos: Mapped[list["FornecedorProdutoModel"]] = relationship(
        "FornecedorProdutoModel", back_populates="fornecedor", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_fornecedor_nome", "nome"),
        Index("ix_fornecedor_cnpj", "cnpj"),
    )

    def to_domain(self) -> "Fornecedor":
        from src.domain.entities import CNPJ, Fornecedor
        return Fornecedor(
            id=self.id,
            nome=self.nome,
            cnpj=CNPJ(self.cnpj),
            ativo=self.ativo,
            criado_em=self.criado_em,
            categorias=[c.to_domain() for c in self.categorias],
        )


# ============================================================
# Tabela: fornecedores_categorias (Pivô N:N)
# ============================================================
class FornecedorCategoriaModel(Base):
    __tablename__ = "fornecedores_categorias"

    fornecedor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("fornecedores.id", ondelete="CASCADE"), primary_key=True
    )
    categoria_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categorias.id", ondelete="CASCADE"), primary_key=True
    )

    __table_args__ = (
        Index("ix_fc_fornecedor", "fornecedor_id"),
        Index("ix_fc_categoria", "categoria_id"),
    )


# ============================================================
# Tabela: produtos
# ============================================================
class ProdutoModel(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relacionamentos
    itens_lista: Mapped[list["ItemListaModel"]] = relationship("ItemListaModel")
    fornecedores: Mapped[list["FornecedorProdutoModel"]] = relationship(
        "FornecedorProdutoModel", back_populates="produto"
    )

    __table_args__ = (
        Index("ix_produto_nome", "nome"),
    )

    def to_domain(self) -> "Produto":
        from src.domain.entities import Produto, UnidadeMedida
        return Produto(
            id=self.id,
            nome=self.nome,
            unidade=UnidadeMedida(self.unidade),
            ativo=self.ativo,
            criado_em=self.criado_em,
        )


# ============================================================
# Tabela: fornecedores_produtos (Preços e Estoque)
# ============================================================
class FornecedorProdutoModel(Base):
    __tablename__ = "fornecedores_produtos"

    fornecedor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("fornecedores.id", ondelete="CASCADE"), primary_key=True
    )
    produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id", ondelete="RESTRICT"), primary_key=True
    )
    preco: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relacionamentos
    fornecedor: Mapped["FornecedorModel"] = relationship("FornecedorModel", back_populates="produtos")
    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel", back_populates="fornecedores")

    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_fp_preco_positivo"),
        CheckConstraint("estoque >= 0", name="ck_fp_estoque_positivo"),
        Index("ix_fp_fornecedor", "fornecedor_id"),
        Index("ix_fp_produto", "produto_id"),
    )

    def to_domain(self) -> "FornecedorProduto":
        from src.domain.entities import FornecedorProduto
        return FornecedorProduto(
            fornecedor_id=self.fornecedor_id,
            produto_id=self.produto_id,
            preco=self.preco,
            estoque=self.estoque,
            ativo=self.ativo,
        )


# ============================================================
# Tabela: sessoes (Refresh Tokens / Session Management)
# ============================================================
class SessaoModel(Base):
    __tablename__ = "sessoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)  # IPv6 max 45 chars
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    expira_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    revogada_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relacionamento
    usuario: Mapped["UsuarioModel"] = relationship("UsuarioModel")

    __table_args__ = (
        Index("ix_sessao_usuario_expira", "usuario_id", "expira_em"),
        Index("ix_sessao_token_hash", "refresh_token_hash"),
    )

    def to_domain(self) -> "Sessao":
        from src.domain.entities import Sessao
        return Sessao(
            id=self.id,
            usuario_id=self.usuario_id,
            refresh_token_hash=self.refresh_token_hash,
            user_agent=self.user_agent,
            ip=self.ip,
            criado_em=self.criado_em,
            expira_em=self.expira_em,
            revogada_em=self.revogada_em,
        )
