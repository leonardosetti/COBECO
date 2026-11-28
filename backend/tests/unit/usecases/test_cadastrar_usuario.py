# COBECO Backend — CadastrarUsuarioUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import CadastrarUsuarioUseCase, CriarUsuarioInput
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


def criar_input_valido(overrides=None):
    """Cria input válido para testes."""
    base = {
        "nome_usuario": "novousuario",
        "email": "novo@teste.com",
        "nome": "Novo Usuário",
        "senha": "Senha@123",
        "pergunta_seguranca": "nome_mae",
        "resposta_seguranca": "Maria Silva",
    }
    if overrides:
        base.update(overrides)
    return CriarUsuarioInput(**base)


class TestCadastrarUsuarioUseCase:
    """Testes para CadastrarUsuarioUseCase (UC09/RF1)"""

    @pytest.mark.asyncio
    async def test_executar_sdoc_arch_006_uc_v1esso(self, usecase, mock_repo, hash_senha_fn):
        input_data = criar_input_valido()

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

        mock_repo.criar.assert_called_once()
        called_usuario = mock_repo.criar.call_args[0][0]
        assert called_usuario.senha_hash.valor == "hashed_Senha@123"
        assert called_usuario.resposta_seguranca_hash.valor == "hashed_Maria Silva"

    @pytest.mark.asyncio
    async def test_executar_usuario_ja_existe_nome_usuario(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="existente",
                email=Email("existente@teste.com"),
                nome="Existente",
                senha_hash=SenhaHash("hash"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hash"),
            )
        )

        input_data = criar_input_valido({"nome_usuario": "existente"})

        with pytest.raises(Exception, match="nome_usuario"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_executar_email_ja_existe(self, usecase, mock_repo):
        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=None)
        mock_repo.buscar_por_email = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="outro",
                email=Email("existente@teste.com"),
                nome="Outro",
                senha_hash=SenhaHash("hash"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hash"),
            )
        )

        input_data = criar_input_valido({"email": "existente@teste.com"})

        with pytest.raises(Exception, match="email"):
            await usecase.executar(input_data)

    @pytest.mark.asyncio
    async def test_senha_fraca_nao_validada_no_usecase(self, usecase, mock_repo):
        """Validação de força da senha ocorre na camada API (Pydantic), não no usecase."""
        input_data = criar_input_valido({"senha": "fraca"})

        mock_repo.buscar_por_nome_usuario = AsyncMock(return_value=None)
        mock_repo.buscar_por_email = AsyncMock(return_value=None)
        mock_repo.criar = AsyncMock(
            return_value=Usuario(
                id=1,
                nome_usuario="novousuario",
                email=Email("novo@teste.com"),
                nome="Novo Usuário",
                senha_hash=SenhaHash("hashed_fraca"),
                pergunta_seguranca="nome_mae",
                resposta_seguranca_hash=SenhaHash("hashed_Maria"),
            )
        )

        result = await usecase.executar(input_data)
        assert result.nome_usuario == "novousuario"
