"""Módulo de ingestão de dados para cobeco-sddai-loader.

Responsabilidade: ler dados de entrada de fontes locais,
validar integridade básica e preparar para o próximo estágio.
"""


def ingest(source_path: str) -> dict:
    """Lê um arquivo de entrada e retorna metadados + conteúdo bruto.

    Args:
        source_path: Caminho relativo ou absoluto para o arquivo de origem.

    Returns:
        Dicionário com 'path', 'size_bytes', 'lines', 'checksum_sha256', 'content'.
    """
    import hashlib
    from pathlib import Path

    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {source_path}")

    data = src.read_bytes()
    checksum = hashlib.sha256(data).hexdigest()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()

    return {
        "path": str(src.resolve()),
        "size_bytes": len(data),
        "lines": len(lines),
        "checksum_sha256": checksum,
        "content": text,
    }


def validate_ingest_result(result: dict) -> bool:
    """Valida que o resultado da ingestão tem os campos obrigatórios."""
    required = {"path", "size_bytes", "lines", "checksum_sha256", "content"}
    return required.issubset(result.keys()) and result["size_bytes"] > 0