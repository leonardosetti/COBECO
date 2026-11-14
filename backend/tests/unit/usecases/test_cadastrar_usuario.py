# COBECO Backend — CadastrarUsuarioUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.domain.usecases import (
    CadastrarUsuarioUseCase, CriarUsuarioInput,
    UsuarioJaExiste, DomainError
)
from src.domain.entities import Usuario, Email, SenhaHash


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.buscar_por_nome_usuario = AsyncMock(return_value=None)
    repo.buscar_por_email = AsyncMock(return_value=None)
    repo.criar = AsyncMock()
    return repo


@pytest.fixture
def hash_senha_fn():
    def hash_fn(senha: str) -> str:
        return f"hashed_{senha}"
    return hash_fn


@pytest.fixture
def usecase(mock_repo, hash_senha_fn):
    return CadastrarUsuarioUseCase(mock_repo, hash_senha_fn)


class TestCadastrarUsuarioUseCase:
    """Testes para CadastrarUsuarioUseCase (UC09/RF01)"""

    @pytest.mark.asyncio
    async def test_executar_sucesso(self, usecase, mock_repo, hash_senha_fn):
        input_data = CriarUsuarioInput(
            nome_usuario="novousuario",
            email="novo@teste.com",
            nome="Novo Usuário",
            senha="Senha@123",
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria Silva",
        )

        # Mock do retorno do repo.criar
        usuario_criado = Usuario(
            id=1,
            nome_usuario=input_data.nome_usuario,
            email=Email(input_data.email),
            nome=input_data.nome,
            senha_hash=SenhaHash(hash_senha_fn(input_data.senha)),
            pergunta_seguranca=input_data.pergunta_seguranca,
            resposta_seguranca_hash=SenhaHash(hash_senha_fn(input_data.resposta_seguranca)),
        )
        mock_repo.criar.return_value = usuario_criado

        result = await usecase.executar(input_data)

        assert result.id == 1
        assert result.nome_usuario == "novousuario"
        assert result.email.valor == "novo@teste.com"
        assert result.nome == "Novo Usuário"
        assert result.pergunta_seguranca == "nome_mae"

        # Verifica se repo.criar foi chamado com senha hasheada
        mock_repo.criar.assert_called_once()
        called_usuario = mock_repo.criar.call_args[0][0]
        assert called_usuario.senha_hash.valor == "hashed_Senha@123"
        assert called_usuario.resposta_seguranca_hash.valor == "hashed_Maria Silva"

    @pytest.mark.asyncio
    async def test_executar_usuario_ja_existe_nome_usuario(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=Usuario(id=1))

        input_data = CriarUsuarioInput(
            nome_usuario="existente",
            email="novo@teste.com",
            nome="Novo",
            senha="Senha@123",
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(UsuarioJaExiste, match="nome_usuario"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_email_ja_existe(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=None)
        mock_repo.buscar_por_email = AsyncMock(return_value=Usuario(id=1))

        input_data = CriarUsuarioInput(
            nome_usuario="novousuario",
            email="existente@teste.com",
            nome="Novo",
            senha="Senha@123",
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(UsuarioJaExiste, match="email"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_senha_fraca_sem_maiuscula(self, usecase):
        input_data = CriarUsuarioInput(
            nome_usuario="usuario",
            email="usuario@teste.com",
            nome="Usuario",
            senha="senha@123",  # sem maiúscula
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(ValueError, match="Senha deve conter pelo menos 1 maiúscula"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_senha_fraca_sem_minuscula(self, usecase):
        input_data = CriarUsuarioInput(
            nome_usuario="usuario",
            email="usuario@teste.com",
            nome="Usuario",
            senha="SENHA@123",  # sem minúscula
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(ValueError, match="Senha deve conter pelo menos 1 minúscula"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_senha_fraca_sem_digito(self, usecase):
        input_data = CriarUsuarioInput(
            nome_usuario="usuario",
            email="usuario@teste.com",
            nome="Usuario",
            senha="Senha@abc",  # sem dígito
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(ValueError, match="Senha deve conter pelo menos 1 número"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_senha_fraca_sem_especial(self, usecase):
        input_data = CriarUsuarioInput(
            nome_usuario="usuario",
            email="usuario@teste.com",
            nome="Usuario",
            senha="Senha123",  # sem caractere especial
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(ValueError, match="Senha deve conter pelo menos 1 caractere especial"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_senha_muito_curta(self, usecase):
        input_data = CriarUsuarioInput(
            nome_usuario="usuario",
            email="usuario@teste.com",
            nome="Usuario",
            senha="Sen@1",  # menos de 8 chars
            pergunta_seguranca="nome_mae",
            resposta_seguranca="Maria",
        )

        with pytest.raises(ValueError, match="Senha deve conter pelo menos 8 caracteres"):
            await usecase.executar(input_data)