"""CLI do cobeco-sddai-loader.

Uso:
    python -m cobeco_sddai_loader.cli --source <caminho> --output <json_saida>
"""

import argparse
import json
import sys
from pathlib import Path

# Adiciona o pai ao path para importar o módulo ingest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest import ingest, validate_ingest_result  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cobeco-sddai-loader",
        description="Carregamento e ingestão de dados de entrada (SDDAI)",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Caminho do arquivo de origem a ser ingerido",
    )
    parser.add_argument(
        "--output",
        required=False,
        help="Caminho para salvar o resultado em JSON (opcional)",
    )
    args = parser.parse_args()

    try:
        result = ingest(args.source)
    except FileNotFoundError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1

    if not validate_ingest_result(result):
        print(
            json.dumps({"ok": False, "error": "Resultado de ingestão inválido"}),
            file=sys.stderr,
        )
        return 1

    output = {"ok": True, "package": "cobeco-sddai-loader", "result": result}

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())