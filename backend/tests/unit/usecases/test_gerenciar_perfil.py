# COBECO Backend — GerenciarPerfilUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import GerenciarPerfilUseCase, DomainError, UsuarioJaExiste
from src.domain.entities import Usuario, Email, SenhaHash


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.buscar_por_id = AsyncMock()
    repo.buscar_por_email = AsyncMock()
    repo.atualizar = AsyncMock()
    return repo


@pytest.fixture
def hash_senha_fn():
    def hash_fn(senha: str) -> str:
        return f"hashed_{senha}"
    return hash_fn


@pytest.fixture
def verificar_senha_fn():
    def verify_fn(senha: str, hash_: str) -> bool:
        return hash_ == f"hashed_{senha}"
    return verify_fn


@pytest.fixture
def usecase(mock_repo, hash_senha_fn, verificar_senha_fn):
    return GerenciarPerfilUseCase(mock_repo, hash_senha_fn, verificar_senha_fn)


@pytest.fixture
def usuario_exemplo():
    return Usuario(
        id=1,
        nome_usuario="usuarioteste",
        email=Email("teste@exemplo.com"),
        nome="Usuário Teste",
        senha_hash=SenhaHash("hashed_Senha@123"),
        pergunta_seguranca="nome_mae",
        resposta_seguranca_hash=SenhaHash("hashed_Maria"),
    )


class TestGerenciarPerfilUseCase:
    """Testes para GerenciarPerfilUseCase (UC16/RF06)"""

    @pytest.mark.asyncio
    async def test_atualizar_apenas_nome(self, usecase, mock_repo, usuario_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)
        mock_repo.atualizar = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Novo Nome",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
        )

        result = await usecase.atualizar(usuario_id=1, nome="Novo Nome")

        assert result.nome == "Novo Nome"
        assert result.email.valor == "teste@exemplo.com"
        mock_repo.atualizar.assert_called_once()

    @pytest.mark.asyncio
    async def test_atualizar_apenas_email(self, usecase, mock_repo, usuario_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)
        mock_repo.buscar_por_email = AsyncMock(return_value=None)
        mock_repo.atualizar = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("novo@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_Senha@123"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
        )

        result = await usecase.atualizar(usuario_id=1, email="novo@exemplo.com")

        assert result.email.valor == "novo@exemplo.com"
        mock_repo.buscar_por_email.assert_called_once_with("novo@exemplo.com")

    @pytest.mark.asyncio
    async def test_atualizar_email_ja_existe(self, usecase, mock_repo, usuario_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)
        mock_repo.buscar_por_email = AsyncMock(
            return_value=Usuario(
                id=2,
                nome_usuario="outro",
                email=Email("existente@exemplo.com"),
                nome="Outro",
                senha_hash=SenhaHash("hash"),
                pergunta_seguranca="p",
                resposta_seguranca_hash=SenhaHash("hash"),
            )
        )

        with pytest.raises(UsuarioJaExiste, match="email"):
            await usecase.atualizar(usuario_id=1, email="existente@exemplo.com")

    @pytest.mark.asyncio
    async def test_atualizar_senha_sem_senha_atual(self, usecase, mock_repo, usuario_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)

        with pytest.raises(DomainError, match="Senha atual é obrigatória"):
            await usecase.atualizar(usuario_id=1, nova_senha="NovaSenha@123")

    @pytest.mark.asyncio
    async def test_atualizar_senha_atual_incorreta(self, usecase, mock_repo, usuario_exemplo):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)

        with pytest.raises(DomainError, match="Senha atual incorreta"):
            await usecase.atualizar(
                usuario_id=1,
                senha_atual="SenhaErrada@123",
                nova_senha="NovaSenha@123",
            )

    @pytest.mark.asyncio
    async def test_atualizar_senha_com_sucesso(self, usecase, mock_repo, usuario_exemplo, hash_senha_fn):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)
        mock_repo.atualizar = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("teste@exemplo.com"),
                nome="Usuário Teste",
                senha_hash=SenhaHash("hashed_NovaSenha@456"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
        )

        result = await usecase.atualizar(
            usuario_id=1,
            senha_atual="Senha@123",
            nova_senha="NovaSenha@456",
        )

        assert result.senha_hash.valor == "hashed_NovaSenha@456"
        mock_repo.atualizar.assert_called_once()

    @pytest.mark.asyncio
    async def test_atualizar_todos_campos(self, usecase, mock_repo, usuario_exemplo, hash_senha_fn):
        mock_repo.buscar_por_id = AsyncMock(return_value=usuario_exemplo)
        mock_repo.buscar_por_email = AsyncMock(return_value=None)
        mock_repo.atualizar = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="usuarioteste",
                email=Email("novo@exemplo.com"),
                nome="Novo Nome",
                senha_hash=SenhaHash("hashed_NovaSenha@456"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
        )

        result = await usecase.atualizar(
            usuario_id=1,
            email="novo@exemplo.com",
            nome="Novo Nome",
            senha_atual="Senha@123",
            nova_senha="NovaSenha@456",
        )

        assert result.email.valor == "novo@exemplo.com"
        assert result.nome == "Novo Nome"
        assert result.senha_hash.valor == "hashed_NovaSenha@456"

    @pytest.mark.asyncio
    async def test_atualizar_usuario_nao_encontrado(self, usecase, mock_repo):
        mock_repo.buscar_por_id = AsyncMock(return_value=None)

        with pytest.raises(DomainError, match="Usuário não encontrado"):
            await usecase.atualizar(usuario_id=999, nome="Novo")