# COBECO Backend — ExportarPDFUseCase Unit Tests

import pytest
from unittest.mock import AsyncMock
from src.domain.usecases import ExportarPDFUseCase
from src.domain.repositories import ExportacaoRepository


@pytest.fixture
def mock_repo():
    repo = AsyncMock(spec=ExportacaoRepository)
    repo.gerar_pdf_lista = AsyncMock()
    return repo


@pytest.fixture
def usecase(mock_repo):
    return ExportarPDFUseCase(mock_repo)


class TestExportarPDFUseCase:
    """Testes para ExportarPDFUseCase (UC08/RF17)"""

    @pytest.mark.asyncio
    async def test_executar_chama_repositorio(self, usecase, mock_repo):
        pdf_bytes = b"%PDF-1.4 mock pdf content"
        mock_repo.gerar_pdf_lista = AsyncMock(return_value=pdf_bytes)

        result = await usecase.executar(lista_id=1)

        assert result == pdf_bytes
        assert result.startswith(b"%PDF")
        mock_repo.gerar_pdf_lista.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_executar_propaga_erro_lista_nao_encontrada(self, usecase, mock_repo):
        from src.adapters.api.exportacao import HTTPException

        mock_repo.gerar_pdf_lista = AsyncMock(
            side_effect=HTTPException(status_code=404, detail="Lista não encontrada")
        )

        with pytest.raises(HTTPException) as exc_info:
            await usecase.executar(lista_id=999)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_executar_propaga_erro_lista_vazia(self, usecase, mock_repo):
        from src.adapters.api.exportacao import HTTPException

        mock_repo.gerar_pdf_lista = AsyncMock(
            side_effect=HTTPException(status_code=400, detail="Lista vazia")
        )

        with pytest.raises(HTTPException) as exc_info:
            await usecase.executar(lista_id=1)

        assert exc_info.value.status_code == 400
