# COBECO Backend — Auth Router (FastAPI)
# Endpoints: POST /v1/auth/cadastrar, POST /v1/auth/login, POST /v1/auth/logout, POST /v1/auth/recuperar-senha

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import timedelta
import bcrypt
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from src.config import settings
from src.domain.usecases import (
    CadastrarUsuarioUseCase, LoginUseCase, LogoutUseCase,
    RecuperarSenhaUseCase, VisualizarPerfilUseCase, GerenciarPerfilUseCase,
    CriarUsuarioInput, LoginInput, RecuperarSenhaInput,
    UsuarioJaExiste, CredenciaisInvalidas, RateLimitExcedido,
)
from src.domain.repositories import UsuarioRepository
from src.adapters.db.models import UsuarioModel
from src.domain.entities import SenhaHash
from src.adapters.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(tags=["Autenticação"])

# OAuth2 scheme para Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login", auto_error=False)


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
            raise ValueError("As senhas não coincidem")

        # Validação de complexidade (RF01)
        if not any(c.isupper() for c in self.senha):
            raise ValueError("Senha deve conter pelo menos 1 maiúscula")
        if not any(c.islower() for c in self.senha):
            raise ValueError("Senha deve conter pelo menos 1 minúscula")
        if not any(c.isdigit() for c in self.senha):
            raise ValueError("Senha deve conter pelo menos 1 número")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in self.senha):
            raise ValueError("Senha deve conter pelo menos 1 caractere especial")


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
    resposta_seguranca: Optional[str] = None
    token: Optional[str] = None
    nova_senha: str = Field(..., min_length=8)
    confirmar_nova_senha: str

    def validar_senhas(self):
        if self.nova_senha != self.confirmar_nova_senha:
            raise ValueError("As senhas não coincidem")


class PerfilResponse(BaseModel):
    id: int
    nome_usuario: str
    email: str
    nome: str
    criado_em: str

    class Config:
        from_attributes = True


class AtualizarPerfilRequest(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    senha_atual: Optional[str] = None
    nova_senha: Optional[str] = Field(None, min_length=8)
    confirmar_nova_senha: Optional[str] = None


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
        from src.domain.entities import Usuario, Email, SenhaHash
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
        from src.domain.entities import Usuario
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
        result = await self.session.execute(
            select(UsuarioModel).where(UsuarioModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def atualizar(self, usuario) -> "Usuario":
        model = await self.buscar_por_id(usuario.id)
        if model:
            # Need to get the model again for update
            result = await self.session.execute(
                select(UsuarioModel).where(UsuarioModel.id == usuario.id)
            )
            db_model = result.scalar_one_or_none()
            if db_model:
                db_model.email = usuario.email.valor
                db_model.nome = usuario.nome
                db_model.senha_hash = usuario.senha_hash.valor
                db_model.atualizado_em = datetime.now()
            return self._to_domain(db_model)
        return None

    async def soft_delete(self, usuario_id: int) -> bool:
        model = await self.buscar_por_id(usuario_id)
        if model:
            model.deletado_em = datetime.now()
            return True
        return False


def get_usuario_repo(session: AsyncSession = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepositoryImpl(session)


def hash_senha(senha: str) -> str:
    """Hash bcrypt com salt=12 (RF01)"""
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=12)).decode()


def verificar_senha(senha: str, hash: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash.encode())


def criar_token(sub: str, expires_delta: timedelta, token_type: str = "access") -> str:
    """Cria JWT token"""
    from datetime import datetime, timezone
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": sub,
        "exp": expire,
        "type": token_type,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decodificar_token(token: str) -> dict:
    """Decodifica e valida JWT"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
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


# Rate limiting simples em memória (produção: Redis)
_tentativas_login = {}
_tentativas_recovery = {}


async def rate_limiter_login(nome_usuario: str):
    """6 tentativas/15min por username"""
    import time
    agora = time.time()
    chave = f"login:{nome_usuario}"
    if chave not in _tentativas_login:
        _tentativas_login[chave] = []

    # Limpa tentativas antigas (>15min)
    _tentativas_login[chave] = [t for t in _tentativas_login[chave] if agora - t < 900]

    if len(_tentativas_login[chave]) >= 6:
        raise RateLimitExcedido(15)

    _tentativas_login[chave].append(agora)


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
    response_model=dict,
    summary="UC09/RF01 - Cadastrar Usuário",
)
async def cadastrar_usuario(
    request: CadastrarUsuarioRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    try:
        request.validar_senhas()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    usecase = CadastrarUsuarioUseCase(repo, hash_senha)
    try:
        usuario = await usecase.executar(CriarUsuarioInput(
            nome_usuario=request.nome_usuario,
            email=request.email,
            nome=request.nome,
            senha=request.senha,
            pergunta_seguranca=request.pergunta_seguranca,
            resposta_seguranca=request.resposta_seguranca,
        ))
        return {"message": "Conta criada com sucesso", "usuario_id": usuario.id}
    except UsuarioJaExiste as e:
        # Mensagem genérica (não revela qual campo)
        raise HTTPException(status_code=400, detail="Credenciais inválidas")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="UC10/RF02 - Login com JWT",
)
async def login(
    response: Response,
    request: LoginRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    await rate_limiter_login(request.nome_usuario)

    usecase = LoginUseCase(repo, verificar_senha, criar_token, rate_limiter_login)
    try:
        tokens = await usecase.executar(LoginInput(
            nome_usuario=request.nome_usuario,
            senha=request.senha,
        ))
    except CredenciaisInvalidas:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Set refresh token como httpOnly cookie (SameSite=Strict)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,  # True em produção com HTTPS
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
    refresh_token: Optional[str] = Cookie(None),
):
    # Invalida refresh token (implementar blacklist em produção)
    response.delete_cookie(key="refresh_token", path="/", httponly=True, samesite="strict")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/recuperar-senha/solicitar",
    summary="UC12/RF04 - Solicitar Recuperação de Senha",
)
async def solicitar_recuperacao_senha(
    request: RecuperarSenhaSolicitarRequest,
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    await rate_limiter_recovery(request.nome_usuario)

    usecase = RecuperarSenhaUseCase(repo, hash_senha, rate_limiter_recovery)
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

    usecase = RecuperarSenhaUseCase(repo, hash_senha, rate_limiter_recovery)
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
    current_user: UsuarioModel = Depends(get_current_user),
):
    return PerfilResponse(
        id=current_user.id,
        nome_usuario=current_user.nome_usuario,
        email=current_user.email,
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
):
    if request.nova_senha and request.nova_senha != request.confirmar_nova_senha:
        raise HTTPException(status_code=400, detail="As senhas não coincidem")

    usecase = GerenciarPerfilUseCase(repo, hash_senha, verificar_senha)
    try:
        usuario = await usecase.atualizar(
            usuario_id=current_user.id,
            email=request.email,
            nome=request.nome,
            senha_atual=request.senha_atual,
            nova_senha=request.nova_senha,
        )
        return PerfilResponse(
            id=usuario.id,
            nome_usuario=usuario.nome_usuario,
            email=usuario.email.valor,
            nome=usuario.nome,
            criado_em=usuario.criado_em.isoformat(),
        )
    except DomainError as e:
        raise HTTPException(status_code=400, detail=e.message)