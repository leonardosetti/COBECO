# COBECO Backend — Serviço de Embeddings (FOSS)
# Gera vetores densos para busca semântica via pgvector.
# Modelo fixo: sentence-transformers all-MiniLM-L6-v2 (384 dims, CPU local, Apache 2.0).

from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    """Contrato para geração de embeddings."""

    @abstractmethod
    def gerar(self, texto: str) -> list[float]:
        """Gera um vetor denso para o texto informado."""
        ...


class SentenceTransformersEmbeddingService(EmbeddingService):
    """Implementação FOSS baseada em sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def gerar(self, texto: str) -> list[float]:
        if not texto or not texto.strip():
            raise ValueError("Texto vazio para geração de embedding")
        embedding = self._model.encode(texto.strip(), convert_to_numpy=True)
        return embedding.tolist()


# Instância global (singleton simples) — inicializada na primeira chamada.
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """Retorna o serviço de embeddings, inicializando sob demanda."""
    global _embedding_service
    if _embedding_service is None:
        from src.config import settings

        _embedding_service = SentenceTransformersEmbeddingService(
            settings.EMBEDDING_MODEL
        )
    return _embedding_service
