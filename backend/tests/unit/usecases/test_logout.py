# COBECO Backend — LogoutUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import LogoutUseCase
from src.domain.entities import Sessao


@pytest.fixture
def mock_invalidar_refresh():
    return AsyncMock()


@pytest.fixture
def usecase(mock_invalidar_refresh):
    return LogoutUseCase(mock_invalidar_refresh)


class TestLogoutUseCase:
    """Testes para LogoutUseCase (UC11/RF03)"""

    @pytest.mark.asyncio
    async def test_executar_chama_invalidar_refresh(self, usecase, mock_invalidar_refresh):
        refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        
        await usecase.executar(refresh_token)
        
        mock_invalidar_refresh.assert_called_once_with(refresh_token)

    @pytest.mark.asyncio
    async def test_executar_com_token_vazio(self, usecase, mock_invalidar_refresh):
        await usecase.executar("")
        
        mock_invalidar_refresh.assert_called_once_with("")

    @pytest.mark.asyncio
    async def test_executar_propaga_erro(self, usecase, mock_invalidar_refresh):
        mock_invalidar_refresh.side_effect = Exception("DB Error")
        
        with pytest.raises(Exception, match="DB Error"):
            await usecase.executar("token")