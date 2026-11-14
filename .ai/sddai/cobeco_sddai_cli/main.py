"""Orquestrador do pipeline SDDAI.

Executa o fluxo completo:
  1. cobeco-sddai-loader   (ingestão)
  2. cobeco-sddai-memory   (otimização de memória)
  3. cobeco-sddai-engineer (engenharia de features)
  4. cobeco-sddai-trainer  (treinamento)

Todos os componentes são invocados via subprocess, mantendo
isolamento e sem dependências entre pacotes.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

PACKAGE_MAP = {
    "loader": "cobeco_sddai_loader.cli",
    "engineer": "cobeco_sddai_engineer.cli",
    "trainer": "cobeco_sddai_trainer.cli",
    "memory": "cobeco_sddai_memory.cli",
}


def run_component(package_module: str, args: list) -> dict:
    """Executa um componente SDDAI via subprocess Python -m.

    Args:
        package_module: Nome do módulo (ex: cobeco_sddai_loader.cli).
        args: Lista de argumentos de linha de comando.

    Returns:
        Dicionário com 'ok', 'stdout', 'stderr', 'returncode'.
    """
    cmd = [sys.executable, "-m", package_module] + args
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        result = {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "command": " ".join(cmd),
        }

        if stdout:
            try:
                result["stdout_parsed"] = json.loads(stdout)
            except json.JSONDecodeError:
                result["stdout_raw"] = stdout

        if stderr:
            result["stderr"] = stderr

        return result
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "returncode": -1,
            "error": f"Timeout após 300s: {' '.join(cmd)}",
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "returncode": -1, "error": str(exc)}


def run_pipeline(source_path: str, epochs: int = 1, memory_threshold_gb: float = 10.0) -> dict:
    """Executa o pipeline SDDAI completo.

    Args:
        source_path: Caminho do arquivo de dados de entrada.
        epochs: Número de épocas para treinamento.
        memory_threshold_gb: Limite de memória em GB.

    Returns:
        Dicionário com o resultado de cada etapa e status geral.
    """
    pipeline_id = f"sddai-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    results = {}

    # Etapa 1: Ingestão
    print("[SDDAI] Etapa 1/4 — Ingestão de dados (cobeco-sddai-loader)...")
    r1 = run_component(
        PACKAGE_MAP["loader"],
        ["--source", source_path, "--output", f"/tmp/{pipeline_id}-loader.json"],
    )
    results["loader"] = r1
    if not r1["ok"]:
        return _finalize(pipeline_id, results, status="failed", stage="loader")

    # Etapa 2: Otimização de memória
    print("[SDDAI] Etapa 2/4 — Otimização de memória (cobeco-sddai-memory)...")
    r2 = run_component(
        PACKAGE_MAP["memory"],
        ["--threshold", str(memory_threshold_gb), "--output", f"/tmp/{pipeline_id}-memory.json"],
    )
    results["memory"] = r2
    if not r2["ok"]:
        return _finalize(pipeline_id, results, status="failed", stage="memory")

    # Etapa 3: Engenharia de features
    print("[SDDAI] Etapa 3/4 — Engenharia de features (cobeco-sddai-engineer)...")
    loader_out = r1.get("stdout_parsed", {})
    ingest_result = loader_out.get("result", {})
    r3 = run_component(
        PACKAGE_MAP["engineer"],
        ["--input", f"/tmp/{pipeline_id}-loader.json", "--output", f"/tmp/{pipeline_id}-engineer.json"],
    )
    results["engineer"] = r3
    if not r3["ok"]:
        return _finalize(pipeline_id, results, status="failed", stage="engineer")

    # Etapa 4: Treinamento
    print("[SDDAI] Etapa 4/4 — Treinamento de modelo (cobeco-sddai-trainer)...")
    r4 = run_component(
        PACKAGE_MAP["trainer"],
        ["--input", f"/tmp/{pipeline_id}-engineer.json", "--epochs", str(epochs), "--output", f"/tmp/{pipeline_id}-trainer.json"],
    )
    results["trainer"] = r4
    if not r4["ok"]:
        return _finalize(pipeline_id, results, status="failed", stage="trainer")

    return _finalize(pipeline_id, results, status="completed", stage=None)


def _finalize(pipeline_id: str, results: dict, status: str, stage: str) -> dict:
    """Monta o resultado final do pipeline."""
    all_ok = all(r.get("ok", False) for r in results.values())
    return {
        "pipeline_id": pipeline_id,
        "status": status,
        "failed_stage": stage,
        "all_components_ok": all_ok,
        "components": results,
        "summary": {
            "loader_ok": results.get("loader", {}).get("ok", False),
            "memory_ok": results.get("memory", {}).get("ok", False),
            "engineer_ok": results.get("engineer", {}).get("ok", False),
            "trainer_ok": results.get("trainer", {}).get("ok", False),
        },
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="cobeco-sddai-cli",
        description="Orquestrador unificado do pipeline SDDAI (custom do zero)",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Caminho do arquivo de dados de entrada",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=1,
        help="Número de épocas de treinamento (padrão: 1)",
    )
    parser.add_argument(
        "--memory-threshold",
        type=float,
        default=10.0,
        help="Limite de memória em GB (padrão: 10.0)",
    )
    parser.add_argument(
        "--run",
        required=False,
        help="Nome do workflow SDDAI (ex: data_optimization)",
    )
    args = parser.parse_args()

    if args.run:
        print(f"[SDDAI] Workflow: {args.run}")

    result = run_pipeline(
        source_path=args.source,
        epochs=args.epochs,
        memory_threshold_gb=args.memory_threshold,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_components_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())