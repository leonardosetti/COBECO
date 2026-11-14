"""Módulo de transformação de features para cobeco-sddai-engineer.

Responsabilidade: receber dados brutos, aplicar transformações
determinísticas e produzir features estruturadas.
"""


def transform(data: dict) -> dict:
    """Aplica engenharia de features ao resultado da ingestão.

    Args:
        data: Dicionário com 'content' (texto) e metadados de ingestão,
              ou estrutura de saída do loader {"ok": true, "result": {...}}.

    Returns:
        Dicionário com features extraídas: word_count, char_count,
        unique_words, lines_non_empty, feature_checksum.
    """
    import hashlib

    # Suporta tanto estrutura direta {"content": ...} quanto saída do loader {"result": {"content": ...}}
    inner = data.get("result", data)
    text = inner.get("content", "")
    lines = text.splitlines()
    non_empty = [l for l in lines if l.strip()]
    words = text.split()
    unique = set(words)

    feature_payload = f"{len(words)}|{len(unique)}|{len(non_empty)}|{len(text)}"
    checksum = hashlib.sha256(feature_payload.encode("utf-8")).hexdigest()

    return {
        "source": data.get("path", "unknown"),
        "word_count": len(words),
        "char_count": len(text),
        "unique_words": len(unique),
        "lines_non_empty": len(non_empty),
        "feature_checksum": checksum,
        "features": {
            "lexical_diversity": round(len(unique) / max(len(words), 1), 4),
            "avg_words_per_line": round(len(words) / max(len(non_empty), 1), 2),
        },
    }


def validate_transform_result(result: dict) -> bool:
    """Valida que o resultado da transformação tem os campos obrigatórios."""
    required = {
        "source",
        "word_count",
        "char_count",
        "unique_words",
        "lines_non_empty",
        "feature_checksum",
        "features",
    }
    return required.issubset(result.keys())