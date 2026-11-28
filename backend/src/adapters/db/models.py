# COBECO Backend — SQLAlchemy Models (Adapters/DB)
# Mapeamento ORM para as 8 tabelas PT-BR (doc-arch-0001-camada-de-dados-canon.md v3.2)
# Clean Architecture: Adapters não vazam para Domain

import json
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import (
        Categoria,
        Fornecedor,
        FornecedorProduto,
        ItemLista,
        Lista,
        Produto,
        Sessao,
        Usuario,
    )

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    DECIMAL,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.database import Base
from src.config import settings


# ============================================================
# Tabela: usuarios
# ============================================================
class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_usuario: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    pergunta_seguranca: Mapped[str] = mapped_column(String(255), nullable=False)
    resposta_seguranca_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
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
        CheckConstraint(
            "LENGTH(nome_usuario) BETWEEN 3 AND 30", name="ck_usuario_nome_usuario_len"
        ),
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
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    categorias: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="IDs das categorias selecionadas (RF12/RF08), JSON texto",
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
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
        # RNF09: composite index for listar_por_usuario with soft delete filter
        Index("ix_lista_usuario_criado_deletado", "usuario_id", "criado_em", "deletado_em"),
    )

    def to_domain(self) -> "Lista":
        from src.domain.entities import Lista

        return Lista(
            id=self.id,
            usuario_id=self.usuario_id,
            nome=self.nome,
            categorias=json.loads(self.categorias) if self.categorias else [],
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
        Integer,
        ForeignKey("produtos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # Relacionamentos
    lista: Mapped["ListaModel"] = relationship("ListaModel", back_populates="itens")
    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel")

    # Constraints
    __table_args__ = (
        CheckConstraint("quantidade BETWEEN 1 AND 9999", name="ck_item_quantidade"),
        UniqueConstraint("lista_id", "produto_id", name="uq_item_lista_produto"),
        # RNF09: explicit composite index for item lookup (covered by unique constraint but explicit for clarity)
        Index("ix_itens_lista_lista_produto", "lista_id", "produto_id"),
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
        "FornecedorModel",
        secondary="fornecedores_categorias",
        back_populates="categorias",
    )

    __table_args__ = (Index("ix_categoria_nome", "nome"),)

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
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # Relacionamentos
    categorias: Mapped[list["CategoriaModel"]] = relationship(
        "CategoriaModel",
        secondary="fornecedores_categorias",
        back_populates="fornecedores",
    )
    produtos: Mapped[list["FornecedorProdutoModel"]] = relationship(
        "FornecedorProdutoModel",
        back_populates="fornecedor",
        cascade="all, delete-orphan",
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
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    marca: Mapped[str | None] = mapped_column(String(100), nullable=True)
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    categoria_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categorias.id"), nullable=True
    )

    # Relacionamentos
    itens_lista: Mapped[list["ItemListaModel"]] = relationship("ItemListaModel")
    fornecedores: Mapped[list["FornecedorProdutoModel"]] = relationship(
        "FornecedorProdutoModel", back_populates="produto"
    )
    categoria: Mapped["CategoriaModel"] = relationship("CategoriaModel")

    nome_tsv: Mapped[TSVECTOR | None] = mapped_column(TSVECTOR, nullable=True)
    marca_tsv: Mapped[TSVECTOR | None] = mapped_column(TSVECTOR, nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.EMBEDDING_DIM), nullable=True
    )

    __table_args__ = (
        Index("ix_produto_nome", "nome"),
        Index("ix_produto_marca", "marca"),
        Index("ix_produto_nome_tsv", "nome_tsv", postgresql_using="gin"),
        Index("ix_produto_marca_tsv", "marca_tsv", postgresql_using="gin"),
        Index("ix_produto_categoria", "categoria_id"),
    )

    def to_domain(self) -> "Produto":
        from src.domain.entities import Produto, UnidadeMedida

        return Produto(
            id=self.id,
            nome=self.nome,
            marca=self.marca,
            unidade=UnidadeMedida(self.unidade),
            ativo=self.ativo,
            criado_em=self.criado_em,
        )


# ============================================================
# Tabela: produto_classes (Mapeamento semântico Marca -> Classe)
# ============================================================
class ProdutoClasseModel(Base):
    __tablename__ = "produto_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    classe_nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    termos_busca: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    marcas_referencia: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    categoria_macro: Mapped[str | None] = mapped_column(String(100), nullable=True)
    termos_busca_tsv: Mapped[TSVECTOR | None] = mapped_column(TSVECTOR, nullable=True)
    marcas_referencia_tsv: Mapped[TSVECTOR | None] = mapped_column(TSVECTOR, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.EMBEDDING_DIM), nullable=True
    )

    __table_args__ = (
        Index("ix_produto_classes_ativo", "ativo"),
        Index("ix_produto_classes_categoria_macro", "categoria_macro"),
        Index("ix_produto_classes_termos_tsv", "termos_busca_tsv", postgresql_using="gin"),
        Index("ix_produto_classes_marcas_tsv", "marcas_referencia_tsv", postgresql_using="gin"),
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
    fornecedor: Mapped["FornecedorModel"] = relationship(
        "FornecedorModel", back_populates="produtos"
    )
    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel", back_populates="fornecedores")

    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_fp_preco_positivo"),
        CheckConstraint("estoque >= 0", name="ck_fp_estoque_positivo"),
        Index("ix_fp_fornecedor", "fornecedor_id"),
        Index("ix_fp_produto", "produto_id"),
        # RNF09: composite index for calcular_disponibilidade and buscar_precos_para_comparacao
        Index(
            "ix_fp_fornecedor_produto_ativo_estoque",
            "fornecedor_id",
            "produto_id",
            "ativo",
            "estoque",
        ),
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
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    refresh_token_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)  # IPv6 max 45 chars
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    expira_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    revogada_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relacionamento
    usuario: Mapped["UsuarioModel"] = relationship("UsuarioModel")

    __table_args__ = (
        Index("ix_sessao_usuario_expira", "usuario_id", "expira_em"),
        Index("ix_sessao_token_hash", "refresh_token_hash"),
        # RNF09: composite index for buscar_ativas_por_usuario (filters revogada_em IS NULL)
        Index("ix_sessao_usuario_revogada_expira", "usuario_id", "revogada_em", "expira_em"),
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
