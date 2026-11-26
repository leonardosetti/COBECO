# COBECO Backend — Auth Router (FastAPI)
# Endpoints: POST /v1/auth/cadastrar, POST /v1/auth/login, POST /v1/auth/logout, POST /v1/auth/recuperar-senha

import hashlib
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Optional

from src.domain.entities import Usuario

if TYPE_CHECKING:
    pass

import bcrypt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore[import-untyped]
from jose.exceptions import ExpiredSignatureError, JWTError  # type: ignore[import-untyped]
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.db.database import get_db
from src.adapters.db.models import SessaoModel, UsuarioModel
from src.config import settings
from src.domain.repositories import SessaoRepository, UsuarioRepository
from src.domain.entities import Sessao
from src.domain.usecases import (
    CadastrarUsuarioUseCase,
    CredenciaisInvalidas,
    CriarUsuarioInput,
    DomainError,
    GerenciarPerfilUseCase,
    LoginInput,
    LoginUseCase,
    RateLimitExcedido,
    RecuperarSenhaUseCase,
    UsuarioJaExiste,
)

router = APIRouter(tags=["Autenticação"])

# OAuth2 scheme para Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login", auto_error=False)

# Constantes para mensagens de erro (TRY003 compliance)
MSG_SENHAS_NAO_COINCIDEM = "As senhas não coincidem"
MSG_SENHA_MAIUSCULA = "Senha deve conter pelo menos 1 maiúscula"
MSG_SENHA_MINUSCULA = "Senha deve conter pelo menos 1 minúscula"
MSG_SENHA_NUMERO = "Senha deve conter pelo menos 1 número"
MSG_SENHA_ESPECIAL = "Senha deve conter pelo menos 1 caractere especial"
MSG_SENHA_NOVA_COINCIDE = "As senhas não coincidem"


# ============================================================
# Schemas Pydantic (Request/Response)
# ============================================================
class CadastrarUsuarioRequest(BaseModel):
    nome_usuario: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9]+$")
    email: EmailStr
    nome: str = Field(..., min_length=2, max_length=100)
    senha: str = Field(..., min_length=8)
    confirmar_senha: str
    pergunta_seguranca: str = Field(..., min_length=5)
    resposta_seguranca: str = Field(..., min_length=3)

    def validar_senhas(self):
        if self.senha != self.confirmar_senha:
            raise ValueError(MSG_SENHAS_NAO_COINCIDEM)

        # Validação de complexidade (RF01)
        if not any(c.isupper() for c in self.senha):
            raise ValueError(MSG_SENHA_MAIUSCULA)
        if not any(c.islower() for c in self.senha):
            raise ValueError(MSG_SENHA_MINUSCULA)
        if not any(c.isdigit() for c in self.senha):
            raise ValueError(MSG_SENHA_NUMERO)
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in self.senha):
            raise ValueError(MSG_SENHA_ESPECIAL)


class LoginRequest(BaseModel):
    nome_usuario: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RecuperarSenhaSolicitarRequest(BaseModel):
    nome_usuario: str


class RecuperarSenhaConfirmarRequest(BaseModel):
    nome_usuario: str
    resposta_seguranca: str | None = None
    token: str | None = None
    nova_senha: str = Field(..., min_length=8)
    confirmar_nova_senha: str

    def validar_senhas(self):
        if self.nova_senha != self.confirmar_nova_senha:
            raise ValueError(MSG_SENHA_NOVA_COINCIDE)


class PerfilResponse(BaseModel):
    id: int
    nome_usuario: str
    email: str
    nome: str
    criado_em: str

    class Config:
        from_attributes = True


class AtualizarPerfilRequest(BaseModel):
    email: EmailStr | None = None
    nome: str | None = Field(None, min_length=2, max_length=100)
    senha_atual: str | None = None
    nova_senha: str | None = Field(None, min_length=8)
    confirmar_nova_senha: str | None = None


# ============================================================
# Dependencies
# ============================================================
# ============================================================
# Dependencies
# ============================================================
class UsuarioRepositoryImpl(UsuarioRepository):
    """Implementação SQLAlchemy do UsuarioRepository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: UsuarioModel) -> "Usuario":
        """Converte UsuarioModel para Usuario domain entity"""
        from src.domain.entities import Email, SenhaHash, Usuario

        return Usuario(
            id=model.id,
            nome_usuario=model.nome_usuario,
            email=Email(model.email),
            nome=model.nome,
            senha_hash=SenhaHash(model.senha_hash),
            pergunta_seguranca=model.pergunta_seguranca,
            resposta_seguranca_hash=SenhaHash(model.resposta_seguranca_hash),
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em,
            deletado_em=model.deletado_em,
        )

    def _to_model(self, usuario: "Usuario") -> UsuarioModel:
        """Converte Usuario domain entity para UsuarioModel"""
        return UsuarioModel(
            id=usuario.id,
            nome_usuario=usuario.nome_usuario,
            email=usuario.email.valor,
            nome=usuario.nome,
            senha_hash=usuario.senha_hash.valor,
            pergunta_seguranca=usuario.pergunta_seguranca,
            resposta_seguranca_hash=usuario.resposta_seguranca_hash.valor,
            criado_em=usuario.criado_em,
            atualizado_em=usuario.atualizado_em,
            deletado_em=usuario.deletado_em,
        )

    async def criar(self, usuario) -> "Usuario":
        model = self._to_model(usuario)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def buscar_por_id(self, usuario_id: int):
        result = await self.session.execute(
            select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def buscar_por_nome_usuario(self, nome_usuario: str):
        result = await self.session.execute(
            select(UsuarioModel).where(UsuarioModel.nome_usuario == nome_usuario)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def buscar_por_email(self, email: str):
        result = await self.session.execute(select(UsuarioModel).where(UsuarioModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def _buscar_model(self, usuario_id: int) -> UsuarioModel | None:
        result = await self.session.execute(
            select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        )
        return result.scalar_one_or_none()

    async def atualizar(self, usuario: Usuario) -> Usuario:
        assert usuario.id is not None  # id da entidade persistida
        model = await self._buscar_model(usuario.id)
        if model:
            model.email = usuario.email.valor
            model.nome = usuario.nome
            model.senha_hash = usuario.senha_hash.valor
            model.atualizado_em = datetime.now()
            await self.session.flush()
            return self._to_domain(model)
        raise DomainError("USUARIO_NAO_ENCONTRADO", "Usuário não encontrado")

    async def soft_delete(self, usuario_id: int) -> bool:
        model = await self.buscar_por_id(usuario_id)
        if model:
            model.deletado_em = datetime.now()
            return True
        return False


def get_usuario_repo(session: AsyncSession = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepositoryImpl(session)


# ============================================================
# Sessao Repository Implementation (Refresh Tokens)
# ============================================================
class SessaoRepositoryImpl(SessaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: "SessaoModel") -> Sessao:
        from src.domain.entities import Sessao

        return Sessao(
            id=model.id,
            usuario_id=model.usuario_id,
            refresh_token_hash=model.refresh_token_hash,
            user_agent=model.user_agent,
            ip=model.ip,
            criado_em=model.criado_em,
            expira_em=model.expira_em,
            revogada_em=model.revogada_em,
        )

    def _to_model(self, sessao: Sessao) -> "SessaoModel":
        from src.adapters.db.models import SessaoModel

        return SessaoModel(
            id=sessao.id,
            usuario_id=sessao.usuario_id,
            refresh_token_hash=sessao.refresh_token_hash,
            user_agent=sessao.user_agent,
            ip=sessao.ip,
            criado_em=sessao.criado_em,
            expira_em=sessao.expira_em,
            revogada_em=sessao.revogada_em,
        )

    async def criar(self, sessao: Sessao) -> Sessao:
        model = self._to_model(sessao)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def buscar_por_token_hash(self, token_hash: str) -> Sessao | None:
        from sqlalchemy import select

        from src.adapters.db.models import SessaoModel

        result = await self.session.execute(
            select(SessaoModel).where(SessaoModel.refresh_token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def buscar_ativas_por_usuario(self, usuario_id: int) -> list[Sessao]:
        from datetime import datetime

        from sqlalchemy import select

        from src.adapters.db.models import SessaoModel

        result = await self.session.execute(
            select(SessaoModel).where(
                SessaoModel.usuario_id == usuario_id,
                SessaoModel.revogada_em.is_(None),
                SessaoModel.expira_em > datetime.now(),
            )
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def revogar(self, sessao_id: int) -> bool:
        from sqlalchemy import select

        from src.adapters.db.models import SessaoModel

        result = await self.session.execute(select(SessaoModel).where(SessaoModel.id == sessao_id))
        model = result.scalar_one_or_none()
        if model:
            model.revogada_em = datetime.now()
            return True
        return False

    async def revogar_todas_do_usuario(self, usuario_id: int) -> int:
        """Remove todas as sessões (ativas e revogadas) de um usuário.

        Usado no login para evitar colisão de UNIQUE em refresh_token_hash
        quando tokens gerados em sequência colidem (ex: testes rápidos com
        mesmo iat). Em produção, garante single-session por usuário.
        """
        from sqlalchemy import delete

        from src.adapters.db.models import SessaoModel

        result = await self.session.execute(
            delete(SessaoModel).where(SessaoModel.usuario_id == usuario_id)
        )
        await self.session.flush()
        return result.rowcount or 0

    async def limpar_expiradas(self) -> int:
        from datetime import datetime

        from sqlalchemy import select

        from src.adapters.db.models import SessaoModel

        result = await self.session.execute(
            select(SessaoModel).where(
                SessaoModel.revogada_em.is_(None),
                SessaoModel.expira_em <= datetime.now(),
            )
        )
        count = 0
        for model in result.scalars().all():
            model.revogada_em = datetime.now()
            count += 1
        return count


def get_sessao_repo(session: AsyncSession = Depends(get_db)) -> SessaoRepository:
    return SessaoRepositoryImpl(session)


def hash_senha(senha: str) -> str:
    """Hash bcrypt com salt=12 (RF01)"""
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=12)).decode()


def hash_refresh_token(token: str) -> str:
    """Hash SHA256 para refresh tokens (JWT são longos >72 bytes, bcrypt truncaria)"""
    return hashlib.sha256(token.encode()).hexdigest()


def verificar_senha(senha: str, hash: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash.encode())


def criar_token(sub: str, expires_delta: timedelta, token_type: str = "access") -> str:
    """Cria JWT token com jti aleatório para garantir unicidade do refresh_token_hash."""
    from datetime import datetime

    import secrets

    expire = datetime.now(UTC) + expires_delta
    payload = {
        "sub": sub,
        "exp": expire,
        "type": token_type,
        "iat": datetime.now(UTC),
        "jti": secrets.token_hex(8),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decodificar_token(token: str) -> dict[str, Any]:
    """Decodifica e valida JWT"""
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> UsuarioModel:
    """Dependency para obter usuário autenticado"""
    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")
    payload = decodificar_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Token inválido")

    repo = UsuarioRepositoryImpl(session)
    usuario = await repo.buscar_por_id(int(payload["sub"]))
    if not usuario or not usuario.esta_ativo():
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario


async def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
):
    """Retorna usuário autenticado ou None — permite fluxo de visitante (RF17)."""
    if not token:
        return None
    try:
        return await get_current_user(token, session)
    except HTTPException:
        return None


# Rate limiting simples em memória (produção: Redis)
_tentativas_login: dict[str, list[float]] = {}
_tentativas_recovery: dict[str, list[float]] = {}


async def rate_limiter_login(nome_usuario: str, ip: str | None = None):
    """6 tentativas/15min por IP + username (rate limiting híbrido)"""
    import time

    agora = time.time()
    chave = f"login:{ip or 'unknown'}:{nome_usuario}"
    if chave not in _tentativas_login:
        _tentativas_login[chave] = []

    # Limpa tentativas antigas (>15min)
    _tentativas_login[chave] = [t for t in _tentativas_login[chave] if agora - t < 900]

    # Adiciona a tentativa atual e verifica limite (6 tentativas -> lockout na 7ª)
    _tentativas_login[chave].append(agora)
    if len(_tentativas_login[chave]) > 6:
        raise RateLimitExcedido(15)


async def rate_limiter_recovery(nome_usuario: str):
    """3 tentativas/hora para recovery"""
    import time

    agora = time.time()
    chave = f"recovery:{nome_usuario}"
    if chave not in _tentativas_recovery:
        _tentativas_recovery[chave] = []

    _tentativas_recovery[chave] = [t for t in _tentativas_recovery[chave] if agora - t < 3600]

    if len(_tentativas_recovery[chave]) >= 3:
        raise RateLimitExcedido(60)

    _tentativas_recovery[chave].append(agora)


# ============================================================
# Endpoints
# ============================================================
@router.post(
    "/cadastrar",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
    summary="UC09/RF01 - Cadastrar Usuário (com auto-login)",
)
async def cadastrar_usuario(
    response: Response,
    request: CadastrarUsuarioRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
):
    try:
        request.validar_senhas()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    usecase = CadastrarUsuarioUseCase(repo, hash_senha)
    try:
        usuario = await usecase.executar(
            CriarUsuarioInput(
                nome_usuario=request.nome_usuario,
                email=request.email,
                nome=request.nome,
                senha=request.senha,
                pergunta_seguranca=request.pergunta_seguranca,
                resposta_seguranca=request.resposta_seguranca,
            )
        )

        # Auto-login: gera tokens
        access_token = criar_token(
            sub=str(usuario.id),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = criar_token(
            sub=str(usuario.id),
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            token_type="refresh",
        )

        # Salva refresh token no banco
        refresh_hash = hash_refresh_token(refresh_token)
        sessao = Sessao(
            usuario_id=usuario.id,
            refresh_token_hash=refresh_hash,
            expira_em=datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await sessao_repo.criar(sessao)

        # Set refresh token como httpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    except UsuarioJaExiste:
        # Mensagem genérica (não revela qual campo)
        raise HTTPException(status_code=400, detail="Credenciais inválidas")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="UC10/RF02 - Login com JWT",
)
async def login(
    response: Response,
    http_request: Request,
    request: LoginRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
):
    import structlog

    logger = structlog.get_logger()

    client_ip = http_request.client.host if http_request.client else "unknown"

    async def _rate_limit(nome_usuario: str) -> None:
        await rate_limiter_login(nome_usuario, client_ip)

    usecase = LoginUseCase(repo, verificar_senha, criar_token, _rate_limit)
    try:
        tokens = await usecase.executar(
            LoginInput(
                nome_usuario=request.nome_usuario,
                senha=request.senha,
            )
        )
        logger.info("login_sucesso", nome_usuario=request.nome_usuario, ip=client_ip)
    except CredenciaisInvalidas:
        logger.warning("login_falha_credenciais", nome_usuario=request.nome_usuario, ip=client_ip)
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    except RateLimitExcedido as e:
        logger.warning(
            "login_rate_limit", nome_usuario=request.nome_usuario, ip=client_ip, minutos=e.minutos
        )
        raise HTTPException(status_code=429, detail=f"Tente novamente em {e.minutos} minutos")

    # Revoga todas as sessões ativas do usuário (single-session por segurança e
    # evita colisão de UNIQUE em refresh_token_hash quando tokens colidem em testes rápidos)
    await sessao_repo.revogar_todas_do_usuario(tokens.usuario_id)

    # Salva refresh token no banco (hash SHA256)
    refresh_hash = hash_refresh_token(tokens.refresh_token)
    sessao = Sessao(
        usuario_id=tokens.usuario_id,
        refresh_token_hash=refresh_hash,
        expira_em=datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    await sessao_repo.criar(sessao)

    # Set refresh token como httpOnly cookie (SameSite=Strict, Secure em produção)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=not settings.DEBUG,  # Secure=True quando não DEBUG (HTTPS)
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )

    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        expires_in=tokens.expires_in,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="UC11/RF03 - Logout",
)
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(None),
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
):
    # Revoga sessão no banco se refresh token fornecido
    if refresh_token:
        refresh_hash = hash_refresh_token(refresh_token)
        sessao = await sessao_repo.buscar_por_token_hash(refresh_hash)
        if sessao:
            assert sessao.id is not None  # PK após persistência
            await sessao_repo.revogar(sessao.id)

    response.delete_cookie(key="refresh_token", path="/", httponly=True, samesite="strict")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="UC10/RF02 - Refresh Access Token",
)
async def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(None),
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    """Renova access token usando refresh token (cookie httpOnly) com rotação de refresh token"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token não fornecido")

    # Verifica refresh token no banco
    refresh_hash = hash_refresh_token(refresh_token)
    sessao = await sessao_repo.buscar_por_token_hash(refresh_hash)
    if not sessao or not sessao.esta_ativa():
        response.delete_cookie(key="refresh_token", path="/", httponly=True, samesite="strict")
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

    # Busca usuário
    usuario = await repo.buscar_por_id(sessao.usuario_id)
    if not usuario or not usuario.esta_ativo():
        if sessao.id is not None:
            await sessao_repo.revogar(sessao.id)
        response.delete_cookie(key="refresh_token", path="/", httponly=True, samesite="strict")
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # ROTAÇÃO DE REFRESH TOKEN: revoga o antigo e cria novo (segurança: detecta replay)
    if sessao.id is not None:
        await sessao_repo.revogar(sessao.id)

    # Gera novo par de tokens
    access_token = criar_token(
        sub=str(usuario.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    novo_refresh_token = criar_token(
        sub=str(usuario.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )

    # Salva novo refresh token no banco (hash SHA256)
    novo_refresh_hash = hash_refresh_token(novo_refresh_token)
    nova_sessao = Sessao(
        usuario_id=usuario.id,
        refresh_token_hash=novo_refresh_hash,
        expira_em=datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    await sessao_repo.criar(nova_sessao)

    # Set novo refresh token como httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=novo_refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=novo_refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/recuperar-senha/solicitar",
    summary="UC12/RF04 - Solicitar Recuperação de Senha",
)
async def solicitar_recuperacao_senha(
    request: RecuperarSenhaSolicitarRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    await rate_limiter_recovery(request.nome_usuario)

    usecase = RecuperarSenhaUseCase(repo, hash_senha, verificar_senha, rate_limiter_recovery)
    token = await usecase.solicitar_reset(request.nome_usuario)

    # Sempre retorna sucesso (não revela se usuário existe)
    if token and settings.RECOVERY_MODE == "log":
        return {"message": "Se o usuário existir, token de recuperação foi logado no servidor"}
    return {"message": "Se o usuário existir, instruções foram enviadas"}


@router.post(
    "/recuperar-senha/confirmar",
    summary="UC12/RF04 - Confirmar Recuperação de Senha",
)
async def confirmar_recuperacao_senha(
    request: RecuperarSenhaConfirmarRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    try:
        request.validar_senhas()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    usecase = RecuperarSenhaUseCase(repo, hash_senha, verificar_senha, rate_limiter_recovery)
    try:
        await usecase.confirmar_reset(
            request.nome_usuario,
            request.resposta_seguranca or request.token or "",
            request.nova_senha,
        )
        return {"message": "Senha alterada com sucesso"}
    except CredenciaisInvalidas:
        raise HTTPException(status_code=400, detail="Token/resposta inválida ou expirada")


@router.get(
    "/perfil",
    response_model=PerfilResponse,
    summary="UC18/RF05 - Visualizar Perfil",
)
async def visualizar_perfil(
    current_user=Depends(get_current_user),  # Domain entity Usuario
):
    return PerfilResponse(
        id=current_user.id,
        nome_usuario=current_user.nome_usuario,
        email=current_user.email.valor,
        nome=current_user.nome,
        criado_em=current_user.criado_em.isoformat(),
    )


@router.put(
    "/perfil",
    response_model=PerfilResponse,
    summary="UC16/RF06 - Gerenciar Perfil",
)
async def gerenciar_perfil(
    request: AtualizarPerfilRequest,
    current_user: UsuarioModel = Depends(get_current_user),
    repo: UsuarioRepository = Depends(get_usuario_repo),
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
):
    if request.nova_senha and request.nova_senha != request.confirmar_nova_senha:
        raise HTTPException(status_code=400, detail="As senhas não coincidem")

    usecase = GerenciarPerfilUseCase(repo, hash_senha, verificar_senha, sessao_repo)
    try:
        usuario = await usecase.atualizar(
            usuario_id=current_user.id,
            email=request.email,
            nome=request.nome,
            senha_atual=request.senha_atual,
            nova_senha=request.nova_senha,
        )
        return PerfilResponse(
            id=usuario.id,  # type: ignore[arg-type]  # id da entidade persistida
            nome_usuario=usuario.nome_usuario,
            email=usuario.email.valor,
            nome=usuario.nome,
            criado_em=usuario.criado_em.isoformat(),
        )
    except DomainError as e:
        raise HTTPException(status_code=400, detail=e.message)
