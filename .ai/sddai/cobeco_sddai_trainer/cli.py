"""CLI do cobeco-sddai-trainer.

Uso:
    python -m cobeco_sddai_trainer.cli --input <json_features> --epochs <n> --output <json_saida>
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import train, validate_train_result  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cobeco-sddai-trainer",
        description="Treinamento de modelos ML para SDDAI (custom do zero)",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do JSON com resultado da engenharia de features",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=1,
        help="Número de épocas de treinamento (padrão: 1)",
    )
    parser.add_argument(
        "--output",
        required=False,
        help="Caminho para salvar o resultado em JSON (opcional)",
    )
    args = parser.parse_args()

    try:
        input_data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(
            json.dumps({"ok": False, "error": f"Erro ao ler entrada: {exc}"}),
            file=sys.stderr,
        )
        return 1

    try:
        result = train(input_data, epochs=args.epochs)
    except Exception as exc:  # noqa: BLE001
        print(
            json.dumps({"ok": False, "error": f"Erro no treinamento: {exc}"}),
            file=sys.stderr,
        )
        return 1

    if not validate_train_result(result):
        print(
            json.dumps({"ok": False, "error": "Resultado de treinamento inválido"}),
            file=sys.stderr,
        )
        return 1

    output = {"ok": True, "config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0": "cobeco-sddai-trainer", "result": result}

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())