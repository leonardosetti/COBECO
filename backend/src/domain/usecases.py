# COBECO Backend — Use Cases (Clean Architecture)
# Casos de uso puros de domínio — orquestram entidades e repositórios
# Mapeados para RFs e UCs do SSOT v3.2

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.config import settings
from src.domain.entities import (
    Categoria,
    Email,
    Fornecedor,
    ItemLista,
    Lista,
    OrcamentoComparacao,
    Produto,
    SenhaHash,
    Usuario,
)
from src.domain.repositories import (
    CategoriaRepository,
    ComparacaoRepository,
    ExportacaoRepository,
    FornecedorRepository,
    ListaRepository,
    ProdutoRepository,
    SessaoRepository,
    UsuarioRepository,
)


# ============================================================
# Exceptions de Domínio
# ============================================================
class DomainError(Exception):
    """Erro de regra de negócio"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class UsuarioJaExiste(DomainError):
    def __init__(self, campo: str) -> None:
        super().__init__("USUARIO_JA_EXISTE", f"{campo} já cadastrado")


class CredenciaisInvalidas(DomainError):
    def __init__(self) -> None:
        super().__init__("CREDENCIAIS_INVALIDAS", "Credenciais inválidas")


class RateLimitExcedido(DomainError):
    def __init__(self, minutos: int) -> None:
        self.minutos = minutos
        super().__init__("RATE_LIMIT_EXCEDIDO", f"Tente novamente em {minutos} minutos")


class ListaNaoEncontrada(DomainError):
    def __init__(self) -> None:
        super().__init__("LISTA_NAO_ENCONTRADA", "Lista não encontrada")


class FornecedoresInsuficientes(DomainError):
    def __init__(self) -> None:
        super().__init__("FORNECEDORES_INSUFICIENTES", "Selecione pelo menos 2 fornecedores")


# ============================================================
# Store temporário de tokens de recuperação (RF04, modo log/dev)
# ============================================================
_RECOVERY_TOKENS: dict[str, dict] = {}
_TOKEN_TTL_SECONDS = 15 * 60  # 15 min


def _armazenar_token_recuperacao(nome_usuario: str, token: str) -> None:
    _RECOVERY_TOKENS[token] = {
        "nome_usuario": nome_usuario,
        "expira_em": datetime.now() + timedelta(seconds=_TOKEN_TTL_SECONDS),
        "usado": False,
    }


def _validar_token_recuperacao(nome_usuario: str, token: str) -> bool:
    entrada = _RECOVERY_TOKENS.get(token)
    if not entrada or entrada["usado"]:
        return False
    if entrada["nome_usuario"] != nome_usuario:
        return False
    if datetime.now() > entrada["expira_em"]:
        return False
    entrada["usado"] = True  # uso único
    return True


# ============================================================
# DTOs / Input/Output
# ============================================================
@dataclass
class CriarUsuarioInput:
    nome_usuario: str
    email: str
    nome: str
    senha: str
    pergunta_seguranca: str
    resposta_seguranca: str


@dataclass
class LoginInput:
    nome_usuario: str
    senha: str


@dataclass
class LoginOutput:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    usuario_id: int = 0


@dataclass
class RecuperarSenhaInput:
    nome_usuario: str
    resposta_seguranca: str | None = None
    nova_senha: str | None = None


@dataclass
class CriarListaInput:
    nome: str
    itens: list[dict]  # [{"produto_id": int, "quantidade": int}, ...]
    categorias: list[int]  # IDs das categorias selecionadas (RF12, regra RF08)


@dataclass
class ComparacaoInput:
    lista_id: int
    fornecedor_ids: list[int]
    disponibilidade_minima: float = 0.0


# ============================================================
# Use Case: Autenticação (UC09-UC12, UC16, UC18)
# ============================================================
class CadastrarUsuarioUseCase:
    """UC09 / RF01 — Cadastrar Usuário"""

    def __init__(self, repo: UsuarioRepository, hash_senha_fn: Callable[[str], str]) -> None:
        self.repo = repo
        self.hash_senha = hash_senha_fn

    async def executar(self, input: CriarUsuarioInput) -> Usuario:
        # Validações de domínio
        if await self.repo.buscar_por_nome_usuario(input.nome_usuario):
            raise UsuarioJaExiste("nome_usuario")
        if await self.repo.buscar_por_email(input.email):
            raise UsuarioJaExiste("email")

        # Hash da senha e resposta de segurança (bcrypt salt=12)
        senha_hash = self.hash_senha(input.senha)
        resposta_hash = self.hash_senha(input.resposta_seguranca)

        usuario = Usuario(
            nome_usuario=input.nome_usuario,
            email=Email(input.email),
            nome=input.nome,
            senha_hash=SenhaHash(senha_hash),
            pergunta_seguranca=input.pergunta_seguranca,
            resposta_seguranca_hash=SenhaHash(resposta_hash),
        )

        return await self.repo.criar(usuario)


class LoginUseCase:
    """UC10 / RF02 — Login com JWT"""

    def __init__(
        self,
        repo: UsuarioRepository,
        verificar_senha_fn: Callable[[str, str], bool],
        criar_token_fn: Callable[..., str],
        rate_limiter_fn: Callable[[str], Awaitable[None]],
    ):
        self.repo = repo
        self.verificar_senha = verificar_senha_fn
        self.criar_token = criar_token_fn
        self.rate_limiter = rate_limiter_fn

    async def executar(self, input: LoginInput) -> LoginOutput:
        # Rate limiting (6 tentativas/15min por IP + username)
        await self.rate_limiter(input.nome_usuario)

        usuario = await self.repo.buscar_por_nome_usuario(input.nome_usuario)
        if not usuario or not usuario.esta_ativo():
            raise CredenciaisInvalidas

        if not self.verificar_senha(input.senha, usuario.senha_hash.valor):
            raise CredenciaisInvalidas

        # Gera tokens: access (15min memória) + refresh (7d httpOnly)
        access_token = self.criar_token(
            sub=str(usuario.id),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self.criar_token(
            sub=str(usuario.id),
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            token_type="refresh",
        )

        return LoginOutput(
            access_token=access_token,
            refresh_token=refresh_token,
            usuario_id=usuario.id,  # type: ignore[arg-type]  # id da entidade persistida
        )


class LogoutUseCase:
    """UC11 / RF03 — Logout (invalida refresh token)"""

    def __init__(self, invalidar_refresh_fn: Callable[[str], Awaitable[None]]) -> None:
        self.invalidar_refresh = invalidar_refresh_fn

    async def executar(self, refresh_token: str) -> None:
        await self.invalidar_refresh(refresh_token)


class RecuperarSenhaUseCase:
    """UC12 / RF04 — Recuperar Senha (pergunta de segurança ou token por email)"""

    def __init__(
        self,
        repo: UsuarioRepository,
        hash_senha_fn: Callable[[str], str],
        verificar_senha_fn: Callable[[str, str], bool],
        rate_limiter_fn: Callable[[str], Awaitable[None]],
    ):
        self.repo = repo
        self.hash_senha = hash_senha_fn
        self.verificar_senha = verificar_senha_fn
        self.rate_limiter = rate_limiter_fn

    async def solicitar_reset(self, nome_usuario: str) -> str | None:
        """Retorna token se modo email, None se pergunta de segurança"""
        # Rate limiting já verificado no endpoint
        usuario = await self.repo.buscar_por_nome_usuario(nome_usuario)
        if not usuario:
            # Mensagem genérica (não revela existência)
            return None

        if settings.RECOVERY_MODE == "email":
            # Em produção: enviar token por email
            # Por enquanto, retorna None para forçar uso de pergunta de segurança
            # TODO: Implementar envio de email real
            return None

        # Modo "log" (apenas desenvolvimento) - armazena token temporário, NÃO loga
        import secrets

        token = secrets.token_urlsafe(32)
        _armazenar_token_recuperacao(nome_usuario, token)
        return token

    async def confirmar_reset(
        self,
        nome_usuario: str,
        resposta_ou_token: str,
        nova_senha: str,
    ) -> Usuario:
        usuario = await self.repo.buscar_por_nome_usuario(nome_usuario)
        if not usuario:
            raise CredenciaisInvalidas

        if settings.RECOVERY_MODE == "log":
            # Validar token de recuperação (uso único, 15 min)
            if not _validar_token_recuperacao(nome_usuario, resposta_ou_token):
                raise CredenciaisInvalidas
        # Validar resposta da pergunta de segurança (bcrypt)
        elif not self.verificar_senha(resposta_ou_token, usuario.resposta_seguranca_hash.valor):
            raise CredenciaisInvalidas

        usuario.senha_hash = SenhaHash(self.hash_senha(nova_senha))
        return await self.repo.atualizar(usuario)


class VisualizarPerfilUseCase:
    """UC18 / RF05 — Visualizar Perfil"""

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    async def executar(self, usuario_id: int) -> Usuario:
        usuario = await self.repo.buscar_por_id(usuario_id)
        if not usuario:
            raise DomainError("USUARIO_NAO_ENCONTRADO", "Usuário não encontrado")
        return usuario


class GerenciarPerfilUseCase:
    """UC16 / RF06 — Gerenciar Perfil"""

    def __init__(
        self,
        repo: UsuarioRepository,
        hash_senha_fn: Callable[[str], str],
        verificar_senha_fn: Callable[[str, str], bool],
        sessao_repo: SessaoRepository | None = None,
    ) -> None:
        self.repo = repo
        self.hash_senha = hash_senha_fn
        self.verificar_senha = verificar_senha_fn
        self.sessao_repo = sessao_repo

    async def atualizar(
        self,
        usuario_id: int,
        email: str | None = None,
        nome: str | None = None,
        senha_atual: str | None = None,
        nova_senha: str | None = None,
    ) -> Usuario:
        usuario = await self.repo.buscar_por_id(usuario_id)
        if not usuario:
            raise DomainError("USUARIO_NAO_ENCONTRADO", "Usuário não encontrado")

        # Validações
        if email and email != usuario.email.valor:
            if await self.repo.buscar_por_email(email):
                raise UsuarioJaExiste("email")
            usuario.email = Email(email)

        if nome:
            usuario.nome = nome

        if nova_senha:
            if not senha_atual:
                raise DomainError("SENHA_ATUAL_OBRIGATORIA", "Senha atual é obrigatória")
            if not self.verificar_senha(senha_atual, usuario.senha_hash.valor):
                raise DomainError("SENHA_ATUAL_INCORRETA", "Senha atual incorreta")
            usuario.senha_hash = SenhaHash(self.hash_senha(nova_senha))
            # Revoga todas as sessões do usuário ao alterar senha (segurança)
            if self.sessao_repo:
                await self.sessao_repo.revogar_todas_do_usuario(usuario_id)

        return await self.repo.atualizar(usuario)


# ============================================================
# Use Case: Listas (UC01, UC14, UC15, UC17, UC13)
# ============================================================
class CriarListaMemoriaUseCase:
    """UC01 / RF07 — Criar Lista em Memória (lado do frontend)"""

    # Este caso de uso é implementado no frontend (Vanilla JS + sessionStorage)
    # Backend apenas recebe a lista pronta para persistir
    pass


class SalvarListaUseCase:
    """UC14 / RF08 — Salvar Lista (Persistir)"""

    def __init__(self, repo: ListaRepository, produto_repo: ProdutoRepository):
        self.repo = repo
        self.produto_repo = produto_repo

    async def executar(self, usuario_id: int, input: CriarListaInput) -> Lista:
        # Validar nome da lista
        if not input.nome or not input.nome.strip():
            raise ValueError("nome da lista deve ter 1-100 caracteres")
        if len(input.nome) > 100:
            raise ValueError("nome da lista deve ter 1-100 caracteres")

        # Validar lista não vazia
        if not input.itens:
            raise ValueError("Lista deve ter pelo menos 1 item")

        # Validação de categorias (RF08 / regra de negócio: ≥1 categoria selecionada)
        if not input.categorias or len(input.categorias) == 0:
            raise ValueError("Selecione ao menos 1 categoria antes de salvar a lista (UC03)")

        # Validar produtos existem
        produto_ids = [item["produto_id"] for item in input.itens]
        produtos = await self.produto_repo.buscar_por_ids(produto_ids)
        if len(produtos) != len(produto_ids):
            raise DomainError("PRODUTO_NAO_ENCONTRADO", "Um ou mais produtos não existem")

        # Criar entidade Lista com itens e categorias
        lista = Lista(
            usuario_id=usuario_id,
            nome=input.nome,
            categorias=input.categorias,
            itens=[
                ItemLista(
                    produto_id=item["produto_id"],
                    quantidade=item["quantidade"],
                )
                for item in input.itens
            ],
        )

        return await self.repo.criar(lista)


class ListarMinhasListasUseCase:
    """UC15 / RF09 — Listar Minhas Listas"""

    def __init__(self, repo: ListaRepository):
        self.repo = repo

    async def executar(
        self,
        usuario_id: int,
        pagina: int = 1,
        por_pagina: int = 20,
        busca: str | None = None,
    ) -> tuple[Sequence[Lista], int]:
        return await self.repo.listar_por_usuario(usuario_id, pagina, por_pagina, busca)


class PromoverListaEfemeraUseCase:
    """UC17 / RF08 — Promover Lista Efêmera (após login)"""

    def __init__(self, repo: ListaRepository, produto_repo: ProdutoRepository):
        self.repo = repo
        self.produto_repo = produto_repo

    async def executar(self, usuario_id: int, lista_memoria: dict) -> Lista:
        """Recebe lista do sessionStorage e persiste"""
        input = CriarListaInput(
            nome=lista_memoria["nome"],
            itens=lista_memoria["itens"],
            categorias=lista_memoria.get("categorias", []),
        )
        return await SalvarListaUseCase(self.repo, self.produto_repo).executar(usuario_id, input)


class EditarListaUseCase:
    """UC13 / RF10 — Editar Lista Salva"""

    def __init__(self, repo: ListaRepository, produto_repo: ProdutoRepository):
        self.repo = repo
        self.produto_repo = produto_repo

    async def executar(self, lista_id: int, usuario_id: int, input: CriarListaInput) -> Lista:
        model = await self.repo.buscar_por_id(lista_id, usuario_id)
        if not model:
            raise ListaNaoEncontrada

        # Validar produtos
        produto_ids = [item["produto_id"] for item in input.itens]
        produtos = await self.produto_repo.buscar_por_ids(produto_ids)
        if len(produtos) != len(produto_ids):
            raise DomainError("PRODUTO_NAO_ENCONTRADO", "Um ou mais produtos não existem")

        # Entidade de domínio — o repositório aplica no modelo ORM
        lista = Lista(
            id=model.id,
            usuario_id=model.usuario_id,
            nome=input.nome,
            categorias=input.categorias,
            itens=[
                ItemLista(produto_id=item["produto_id"], quantidade=item["quantidade"])
                for item in input.itens
            ],
        )

        return await self.repo.atualizar(lista)


class ExcluirListaUseCase:
    """UC13 / RF11 — Excluir Lista (Soft Delete)"""

    def __init__(self, repo: ListaRepository):
        self.repo = repo

    async def executar(self, lista_id: int, usuario_id: int, confirmacao_nome: str) -> bool:
        return await self.repo.soft_delete(lista_id, usuario_id, confirmacao_nome)


# ============================================================
# Use Case: Catálogo (UC02, UC03, UC04, UC05)
# ============================================================
class AutocompleteProdutosUseCase:
    """UC02 / RF07 — Autocomplete de Produtos"""

    def __init__(self, repo: ProdutoRepository):
        self.repo = repo

    async def executar(self, query: str, limit: int = 10) -> list[Produto]:
        if len(query) < 2:
            return []
        return await self.repo.autocomplete(query, limit)


class SelecionarCategoriasUseCase:
    """UC03 / RF12 — Selecionar Categorias (Pré-filtro)"""

    def __init__(
        self,
        repo: CategoriaRepository,
        fornecedor_repo: FornecedorRepository,
    ) -> None:
        self.repo = repo
        self.fornecedor_repo = fornecedor_repo

    async def listar_todas(self) -> list[Categoria]:
        return await self.repo.listar_todas()

    async def filtrar_fornecedores(self, categoria_ids: list[int]) -> list[Fornecedor]:
        return await self.fornecedor_repo.listar_por_categorias(categoria_ids)


class SelecionarFornecedoresUseCase:
    """UC04 / RF13 — Selecionar Fornecedores"""

    def __init__(self, repo: FornecedorRepository):
        self.repo = repo

    async def listar_por_categorias(self, categoria_ids: list[int]) -> list[Fornecedor]:
        return await self.repo.listar_por_categorias(categoria_ids)

    async def buscar_disponibilidade(
        self, fornecedor_ids: list[int], produto_ids: list[int]
    ) -> dict[int, float]:
        """% de disponibilidade por fornecedor (UC04)"""
        resultado: dict[int, float] = {}
        total = len(produto_ids) or 1
        for fornecedor_id in fornecedor_ids:
            disp, _aus, _preco = await self.repo.calcular_disponibilidade(
                fornecedor_id, produto_ids
            )
            resultado[fornecedor_id] = round(disp / total * 100, 1)
        return resultado


class FiltrarDisponibilidadeUseCase:
    """UC05 / RF14 — Filtrar por Disponibilidade (Slider 0-100%)"""

    def __init__(self, repo: FornecedorRepository):
        self.repo = repo

    async def executar(
        self,
        fornecedor_ids: list[int],
        produto_ids: list[int],
        min_disponibilidade: float,
    ) -> list[Fornecedor]:
        fornecedores = await self.repo.buscar_por_ids(fornecedor_ids)
        if not produto_ids or min_disponibilidade <= 0:
            return list(fornecedores)
        disponibilidade = await self.buscar_disponibilidade_fornecedores(
            fornecedor_ids, produto_ids
        )
        return [f for f in fornecedores if disponibilidade.get(f.id or 0, 0) >= min_disponibilidade]

    async def buscar_disponibilidade_fornecedores(
        self, fornecedor_ids: list[int], produto_ids: list[int]
    ) -> dict[int, float]:
        """% de disponibilidade por fornecedor para filtragem (UC05)"""
        resultado: dict[int, float] = {}
        total = len(produto_ids) or 1
        for fornecedor_id in fornecedor_ids:
            disp, _aus, _preco = await self.repo.calcular_disponibilidade(
                fornecedor_id, produto_ids
            )
            resultado[fornecedor_id] = round(disp / total * 100, 1)
        return resultado


# ============================================================
# Use Case: Comparação (UC06, UC07)
# ============================================================
class CalcularOrcamentoUseCase:
    """UC06 / RF15 — Calcular Orçamento (Tabela Flat)"""

    def __init__(self, repo: ComparacaoRepository):
        self.repo = repo

    async def executar(self, input: ComparacaoInput) -> OrcamentoComparacao:
        if len(input.fornecedor_ids) < 2:
            raise FornecedoresInsuficientes

        return await self.repo.calcular_orcamento(
            lista_id=input.lista_id,
            fornecedor_ids=input.fornecedor_ids,
            disponibilidade_minima=input.disponibilidade_minima,
        )


class VisualizarResultadosUseCase:
    """UC07 / RF16 — Visualizar Resultados"""

    def __init__(self) -> None:
        # Apenas formata o OrcamentoComparacao para exibição
        # Destaque verde no menor preço, tooltips para ausentes
        pass

    def formatar_para_tabela(self, orcamento: OrcamentoComparacao) -> dict:
        return {
            "lista_id": orcamento.lista_id,
            "lista_nome": orcamento.lista_nome,
            "melhor_fornecedor_id": orcamento.melhor_fornecedor_id,
            "fornecedores": [
                {
                    "fornecedor_id": f.fornecedor_id,
                    "fornecedor_nome": f.fornecedor_nome,
                    "itens_disponiveis": f.itens_disponiveis,
                    "itens_ausentes": f.itens_ausentes,
                    "preco_total": float(f.preco_total),
                    "percentual_disponibilidade": f.percentual_disponibilidade,
                    "eh_melhor": f.fornecedor_id == orcamento.melhor_fornecedor_id,
                    "itens": [
                        {
                            "produto_id": i.produto_id,
                            "produto_nome": i.produto_nome,
                            "unidade": i.unidade,
                            "quantidade": i.quantidade,
                            "preco_unitario": float(i.preco_unitario) if i.preco_unitario else None,
                            "preco_total": float(i.preco_total) if i.preco_total else None,
                            "disponivel": i.disponivel,
                        }
                        for i in f.itens
                    ],
                }
                for f in orcamento.fornecedores
            ],
        }


# ============================================================
# Use Case: Exportação (UC08, UC09)
# ============================================================
class ExportarPDFUseCase:
    """UC08 / RF17 — Exportar Lista em PDF (ReportLab)"""

    def __init__(self, repo: ExportacaoRepository):
        self.repo = repo

    async def executar(self, lista_id: int) -> bytes:
        return await self.repo.gerar_pdf_lista(lista_id)


class ImprimirUseCase:
    """UC09 / RF18 — Imprimir (CSS @media print)"""

    def __init__(self) -> None:
        # Frontend: CSS @media print oculta menus, garante quebras de página
        pass
