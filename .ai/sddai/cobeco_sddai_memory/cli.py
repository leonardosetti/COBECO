"""CLI do cobeco-sddai-memory.

Uso:
    python -m cobeco_sddai_memory.cli --threshold <gb> --output <json_saida>
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from optimizer import optimize, validate_optimize_result  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cobeco-sddai-memory",
        description="Otimização de memória para SDDAI (custom do zero)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=10.0,
        help="Limite de memória em GB (padrão: 10.0)",
    )
    parser.add_argument(
        "--output",
        required=False,
        help="Caminho para salvar o resultado em JSON (opcional)",
    )
    args = parser.parse_args()

    try:
        result = optimize(memory_threshold_gb=args.threshold)
    except Exception as exc:  # noqa: BLE001
        print(
            json.dumps({"ok": False, "error": f"Erro na otimização: {exc}"}),
            file=sys.stderr,
        )
        return 1

    if not validate_optimize_result(result):
        print(
            json.dumps({"ok": False, "error": "Resultado de otimização inválido"}),
            file=sys.stderr,
        )
        return 1

    output = {"ok": True, "package": "cobeco-sddai-memory", "result": result}

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())