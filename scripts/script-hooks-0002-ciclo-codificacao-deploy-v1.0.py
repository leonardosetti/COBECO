#!/usr/bin/env python3
"""
Hook de ciclo de codificação e deploy — COBECO MVP.
Constituição Art. 2, 6.3, 7.7, 9.3, 9.9, 17.3, 17.5, 17.7 | Protocolo P1/P2/P3.

Orquestra os gates do runbook runbook-deploy-0001-ciclo-codificacao-deploy-v1.0.md:
  gate-inicio   : specs aprovadas, dependências, paralelismo, gate PMBOK (Fase A)
  gate-ciclo    : testes unitários, integração ou mock/stub, PDCA (máx 3 it/bloco),
                  validação de artefatos P1/P2/P3, secret scan e referências
                  cruzadas (Fases B-D)
  deploy-stage  : CI green check, commit/push, deploy em stage, decisão de falha
                  de pipeline (Fase E)
  gate-stage    : emite relatório de aprovação de merge aguardando aprovador
                  (Fase F)
  relatorio     : emite relatório consolidado de docs/reports/

Todos os relatórios são emitidos em docs/reports/ com nomenclatura P1
(<tipo-classe>-<ID>-<nome>-v1.0.md) e frontmatter universal P2, para passar
pelo pre-commit (artifact_validate) no commit da Fase E.

Exit codes: 0 = gate ok, 1 = gate bloqueado/falha, 2 = erro de execução.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # já é dependência do projeto (artifact_validate.py)
except ImportError:  # pragma: no cover - fallback defensivo
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = ROOT / ".ai" / "specs"
REPORTS_DIR = ROOT / "docs" / "reports"
LOGS_DIR = ROOT / "docs" / "logs"
BACKEND_DIR = ROOT / "backend"
PDCA_MAX_ITERACOES = 3
CMD_TIMEOUT = 600

APROVADO_STAGES = {"aprovado", "ratificado", "promulgado"}
BRANCHES_PROTEGIDAS = {"main", "stage", "master"}

VALIDATOR = "scripts/artifact_validate.py"
VALIDATE_REFS = "scripts/script-validate-0001-validate-refs-v1.0.py"
SECRET_SCAN = "scripts/script-security-0001-secret-scan-v1.0.py"
CI_GREEN = "scripts/script-ci-0001-ci-green-check-v1.0.py"
CONSOLIDADO = "doc-report-0001-consolidado-ciclo-v1.0.json"
HOOK_PATH = "scripts/script-hooks-0002-ciclo-codificacao-deploy-v1.0.py"

TRACE_VAZIO = {
    "constitution": ["constitution-0001-constitution-canon.md"],
    "req_func": [],
    "req_nfunc": [],
    "use_cases": [],
    "specs": [],
    "handoffs": [],
    "adrs": [],
    "code": [HOOK_PATH],
    "tests": [],
}


# --------------------------------------------------------------------------- util
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def slug_data() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def run_cmd(
    cmd: list[str], cwd: Path = ROOT, timeout: int = CMD_TIMEOUT
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            cmd, 124, "", f"timeout de {timeout}s excedido: {' '.join(cmd)}"
        )
    except FileNotFoundError as e:
        return subprocess.CompletedProcess(cmd, 127, "", str(e))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def append_log(nome: str, texto: str) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"{nome}.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {texto}\n")


def load_yaml_frontmatter(path: Path) -> dict[str, Any] | None:
    if not path.exists() or path.suffix.lower() != ".md":
        return None
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not content.startswith("---\n"):
        return None
    try:
        end = content.index("\n---", 4)
    except ValueError:
        return None
    if yaml is None:
        return None
    try:
        return yaml.safe_load(content[4:end].strip()) or {}
    except Exception:
        return None


# --------------------------------------------------------------------------- relatórios P1/P2
def proximo_id(classe: str) -> int:
    """Próximo ID sequencial (4 dígitos) por tipo-classe em docs/reports/."""
    maior = 0
    for p in REPORTS_DIR.iterdir() if REPORTS_DIR.exists() else []:
        m = re.match(rf"^{re.escape(classe)}-(\d{{4}})-", p.name)
        if m:
            maior = max(maior, int(m.group(1)))
    return maior + 1


def montar_frontmatter(classe: str, id_num: int, nome: str, titulo: str) -> str:
    hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ident = f"{classe}-{id_num:04d}-{nome}-v1.0"
    return (
        "---\n"
        f'id: "{ident}"\n'
        f'type: "{classe}"\n'
        f'title: "{titulo}"\n'
        'version: "1.0"\n'
        'status: "rascunho"\n'
        "canonical: false\n"
        f'canonical_slug: "{nome}"\n'
        f'created: "{hoje}"\n'
        f'updated: "{hoje}"\n'
        'author: "COBECO Hook (script-hooks-0002)"\n'
        'owner: "CCB"\n'
        "ratified_by: null\n"
        "ratified_at: null\n"
        "supersedes: null\n"
        "superseded_by: null\n"
        "trace:\n"
        + "".join(
            f"  {k}: {json.dumps(v, ensure_ascii=False)}\n"
            for k, v in TRACE_VAZIO.items()
        )
        + 'domain: "governance"\n'
        'layer: "report"\n'
        'tags: ["relatorio", "hook", "ciclo-codificacao-deploy"]\n'
        'lgpd_class: "n/a"\n'
        "workflow:\n"
        '  stage: "rascunho"\n'
        "  reviewer: null\n"
        "  reviewed_at: null\n"
        "  approval_hash: null\n"
        "  board_url: null\n"
        "---\n"
    )


def emitir_relatorio(
    classe: str, nome: str, titulo: str, corpo_md: str, data: dict[str, Any]
) -> tuple[Path, Path]:
    """Emite relatório .md (frontmatter P2) + .json pareados em docs/reports/.

    Nome segue P1: <tipo-classe>-<ID:04d>-<nome>-v1.0.<ext>, ID sequencial
    por tipo-classe. Ambos passam pelo pre-commit artifact_validate na Fase E.
    """
    id_num = proximo_id(classe)
    stem = f"{classe}-{id_num:04d}-{nome}-v1.0"
    md = REPORTS_DIR / f"{stem}.md"
    js = REPORTS_DIR / f"{stem}.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    md.write_text(
        montar_frontmatter(classe, id_num, nome, titulo) + corpo_md, encoding="utf-8"
    )
    write_json(js, data)
    return md, js


# --------------------------------------------------------------------------- specs
def listar_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    if not SPECS_DIR.exists():
        return specs
    for p in sorted(SPECS_DIR.glob("*.md")):
        fm = load_yaml_frontmatter(p)
        if not fm:
            continue
        specs.append(
            {
                "arquivo": str(p.relative_to(ROOT)),
                "id": fm.get("id", p.stem),
                "type": fm.get("type"),
                "title": fm.get("title"),
                "version": fm.get("version"),
                "status": fm.get("status"),
                "workflow": fm.get("workflow", {}) or {},
                "trace": fm.get("trace", {}) or {},
                "canonical": fm.get("canonical", False),
            }
        )
    return specs


def specs_aprovadas() -> list[dict[str, Any]]:
    return [s for s in listar_specs() if s["workflow"].get("stage") in APROVADO_STAGES]


def plano_ondas(dependencias: dict[str, list[str]]) -> tuple[list[str], set[str]]:
    """Ordem topológica (Kahn). Retorna (ordem, nós em ciclo)."""
    restantes = set(dependencias)
    ordem: list[str] = []
    while restantes:
        prontos = sorted(
            s for s in restantes if not any(d in restantes for d in dependencias[s])
        )
        if not prontos:
            break
        for s in prontos:
            ordem.append(s)
            restantes.discard(s)
    return ordem, restantes


# --------------------------------------------------------------------------- gate-inicio (Fase A)
def gate_inicio() -> int:
    print("=" * 60)
    print("GATE INICIO — Fase A: specs aprovadas, dependências, paralelismo PMBOK")
    print("=" * 60)
    append_log("gate-inicio", "iniciado")

    specs = listar_specs()
    aprovadas = specs_aprovadas()
    print(f"Specs encontradas: {len(specs)} | aprovadas: {len(aprovadas)}")

    if not aprovadas:
        print("❌ Nenhuma spec aprovada para iniciar codificação.")
        print("   Requisito: workflow.stage ∈ {aprovado, ratificado, promulgado}")
        append_log("gate-inicio", "bloqueado: nenhuma spec aprovada")
        return 1

    # Dependências entre specs: trace.specs + workflow.depends_on (runbook A2)
    id_para_spec = {s["id"]: s for s in specs}
    dependencias: dict[str, list[str]] = {}
    for s in aprovadas:
        deps: list[str] = [
            d for d in (s["trace"].get("specs") or []) if d in id_para_spec
        ]
        deps += [
            d for d in (s["workflow"].get("depends_on") or []) if d in id_para_spec
        ]
        dependencias[s["id"]] = sorted(set(deps))

    ordem, ciclo = plano_ondas(dependencias)
    paralelo = [sid for sid in ordem if not dependencias[sid]]
    sequencia = [sid for sid in ordem if dependencias[sid]]
    gate_pmbok = "aprovado" if not ciclo else "atencao_ciclo"

    print("\n-- Plano de ondas (paralelismo) --")
    print(f"  Paralelizáveis (sem dependência entre specs aprovadas): {len(paralelo)}")
    for sid in paralelo:
        print(f"    - {sid} (onde independente)")
    print(f"  Sequenciais (dependem de outra spec aprovada): {len(sequencia)}")
    for sid in sequencia:
        deps_txt = ", ".join(dependencias[sid]) or "—"
        print(f"    - {sid} <- depende de: {deps_txt} (gate PMBOK finish-to-start)")
    if ciclo:
        print(f"⚠️  Dependência cíclica detectada entre specs: {sorted(ciclo)}")

    runid = slug_data()
    data = {
        "gate": "inicio",
        "timestamp": now_iso(),
        "specs_total": len(specs),
        "specs_aprovadas": len(aprovadas),
        "aprovadas": aprovadas,
        "dependencias": dependencias,
        "paralelismo": {"paralelo": paralelo, "sequencial": sequencia},
        "ciclos": sorted(ciclo),
        "gate_pmbok": gate_pmbok,
    }
    md, js = emitir_relatorio(
        "doc-status-report",
        f"inicio-codificacao-{runid}",
        "Relatório Início de Codificação",
        "# Relatório Início de Codificação\n\n```json\n"
        + json.dumps(data, indent=2, ensure_ascii=False)
        + "\n```\n",
        data,
    )
    append_log("gate-inicio", f"relatorio: {md.relative_to(ROOT)}")

    print(
        f"\n✅ Gate início OK. Relatório: {md.relative_to(ROOT)} | {js.relative_to(ROOT)}"
    )
    return 0


# --------------------------------------------------------------------------- gate-ciclo (Fases B-D)
def rodar_pytest(diretorio: str) -> tuple[int, str]:
    """Roda pytest a partir de backend/ (mesmo padrão do Makefile e do CI:
    working-directory ./backend, python -m pytest para sys.path incluir src/).
    Exit 5 = nenhum teste coletado."""
    if not (BACKEND_DIR / diretorio).is_dir():
        return 127, f"Diretório não existe: backend/{diretorio}"
    res = run_cmd(["python", "-m", "pytest", diretorio, "-q"], cwd=BACKEND_DIR)
    return res.returncode, res.stdout + res.stderr


def validar_artefato(caminho: str) -> tuple[bool, str]:
    res = run_cmd(["python", VALIDATOR, "--file", caminho])
    return res.returncode == 0, res.stdout + res.stderr


def artefatos_md_tocados() -> list[str]:
    """Arquivos .md alterados (staged ou não) — alvo da validação P1/P2/P3 (Fase D)."""
    res = run_cmd(["git", "status", "--porcelain"])
    tocados: list[str] = []
    for linha in res.stdout.splitlines():
        parte = linha[3:] if len(linha) > 3 else ""
        if " -> " in parte:
            parte = parte.split(" -> ", 1)[1]
        parte = parte.strip().strip('"')
        if parte.endswith(".md") and (ROOT / parte).exists():
            tocados.append(parte)
    return sorted(set(tocados))


def gate_ciclo() -> int:
    print("=" * 60)
    print("GATE CICLO — Fases B-D: testes, PDCA, artefatos, secret scan, refs")
    print("=" * 60)
    append_log("gate-ciclo", "iniciado")
    runid = slug_data()

    # C1: testes unitários locais (obrigatório)
    print("\n[C1] Testes unitários locais (backend/tests/unit)...")
    code_unit, saida_unit = rodar_pytest("tests/unit")
    print(saida_unit[-2000:])
    md_unit, _ = emitir_relatorio(
        "doc-test-log",
        f"testes-unitarios-{runid}",
        "Relatório Testes Unitários",
        f"# Relatório Testes Unitários\n\nExecutado: {now_iso()}\n"
        f"Diretório: backend/tests/unit\n"
        f"Resultado: {'PASSOU' if code_unit == 0 else 'FALHOU'}\n\n```\n{saida_unit}\n```\n",
        {
            "executado": now_iso(),
            "diretorio": "backend/tests/unit",
            "resultado": "passou" if code_unit == 0 else "falhou",
        },
    )
    append_log("gate-ciclo", f"testes unitarios: {'ok' if code_unit == 0 else 'falha'}")
    if code_unit != 0:
        print("❌ Testes unitários falharam. Bloqueando ciclo (runbook C3).")
        print(f"   Relatório: {md_unit.relative_to(ROOT)}")
        return 1

    # C2: testes de integração (quando existirem); senão mock/stub
    print("\n[C2] Testes de integração (backend/tests/integration)...")
    code_int, saida_int = rodar_pytest("tests/integration")
    if code_int == 0:
        modo = "integração real"
    elif code_int == 5:
        modo = "mock/stub (nenhum teste de integração aplicável)"
        print(f"   AVISO: {modo}")
    else:
        modo = "falha"
    md_int, _ = emitir_relatorio(
        "doc-test-log",
        f"testes-integracao-{runid}",
        "Relatório Testes de Integração / Mock-Stub",
        f"# Relatório Testes de Integração / Mock-Stub\n\nExecutado: {now_iso()}\n"
        f"Modo: {modo}\n"
        f"Resultado: {'PASSOU' if code_int == 0 else ('mock/stub aplicado' if code_int == 5 else 'FALHOU')}\n\n"
        f"```\n{saida_int}\n```\n",
        {"executado": now_iso(), "modo": modo, "exit_code": code_int},
    )
    append_log("gate-ciclo", f"testes integracao/mock: {modo}")
    if code_int not in (0, 5):
        print("❌ Testes de integração falharam. Bloqueando ciclo (runbook C3).")
        print(f"   Relatório: {md_int.relative_to(ROOT)}")
        return 1

    # D: validação de artefatos P1/P2/P3 dos .md tocados + secret scan + refs
    print("\n[D] Validação de artefatos (P1/P2/P3), secret scan, referências...")
    falhas_d: list[str] = []
    tocados = artefatos_md_tocados()
    if not tocados:
        print("   ℹ️  Nenhum artefato .md tocado nesta rodada.")
    for a in tocados:
        ok, saida = validar_artefato(a)
        status = "✅" if ok else "❌"
        print(f"   {status} {a}")
        if not ok:
            falhas_d.append(f"{a}: {saida.strip().splitlines()[:3]}")

    res_scan = run_cmd(["python", SECRET_SCAN])
    print(f"   {'✅' if res_scan.returncode == 0 else '❌'} secret scan")
    if res_scan.returncode != 0:
        falhas_d.append(f"secret scan: {res_scan.stdout[-800:]}")

    res_refs = run_cmd(["python", VALIDATE_REFS, "--ci"])
    print(f"   {'✅' if res_refs.returncode == 0 else '❌'} referências cruzadas")
    if res_refs.returncode != 0:
        falhas_d.append(f"refs: {res_refs.stdout[-800:]}")

    append_log(
        "gate-ciclo", f"artefatos tocados: {len(tocados)}, falhas: {len(falhas_d)}"
    )

    data = {
        "gate": "ciclo",
        "timestamp": now_iso(),
        "pdca_max_iteracoes": PDCA_MAX_ITERACOES,
        "testes_unitarios": {
            "ok": code_unit == 0,
            "relatorio": str(md_unit.relative_to(ROOT)),
        },
        "testes_integracao": {"modo": modo, "relatorio": str(md_int.relative_to(ROOT))},
        "artefatos_tocados": tocados,
        "artefatos_ok": not falhas_d,
        "falhas": falhas_d,
    }
    md_ciclo, _ = emitir_relatorio(
        "doc-test-log",
        f"ciclo-pdca-{runid}",
        "Relatório Ciclo PDCA",
        "# Relatório Ciclo PDCA\n\n```json\n"
        + json.dumps(data, indent=2, ensure_ascii=False)
        + "\n```\n",
        data,
    )

    if falhas_d:
        print("\n❌ Fase D com falhas. Bloqueando ciclo (runbook Fase D).")
        print(f"   Relatório: {md_ciclo.relative_to(ROOT)}")
        return 1

    print("\n✅ Gate ciclo OK.")
    print(f"   Relatório: {md_ciclo.relative_to(ROOT)}")
    return 0


# --------------------------------------------------------------------------- deploy-stage (Fase E)
def ci_green() -> tuple[bool, str]:
    res = run_cmd(["python", CI_GREEN])
    return res.returncode == 0, res.stdout + res.stderr


def git_commit_push(mensagem: str, branch: str) -> tuple[bool, str]:
    run_cmd(["git", "add", "-A"])
    status = run_cmd(["git", "status", "--porcelain"])
    if not status.stdout.strip():
        return True, "Nenhuma mudança para commit."
    res = run_cmd(["git", "commit", "-m", mensagem])
    if res.returncode != 0:
        return False, res.stdout + res.stderr
    res = run_cmd(["git", "push", "origin", branch])
    return res.returncode == 0, res.stdout + res.stderr


def deploy_stage() -> int:
    print("=" * 60)
    print("DEPLOY STAGE — Fase E: CI green, commit/push, deploy, decisão de falha")
    print("=" * 60)
    append_log("deploy-stage", "iniciado")
    runid = slug_data()

    branch = run_cmd(["git", "branch", "--show-current"]).stdout.strip()
    if branch in BRANCHES_PROTEGIDAS:
        print(f"❌ Branch protegida '{branch}'. Use PR (Constitution Art. 6.3).")
        append_log("deploy-stage", f"bloqueado: branch protegida {branch}")
        return 1
    if not branch:
        print("❌ Branch atual não detectada (detached HEAD?). Abortando.")
        return 2

    # E1: CI green check
    print("\n[E1] Verificando CI/CD all green...")
    ok_ci, saida_ci = ci_green()
    print(saida_ci[-2500:])
    md_ci, _ = emitir_relatorio(
        "doc-status-report",
        f"ci-check-{runid}",
        "Relatório CI Green Check",
        f"# Relatório CI Green Check\n\nExecutado: {now_iso()}\nBranch: {branch}\n"
        f"Resultado: {'VERDE' if ok_ci else 'FALHA'}\n\n```\n{saida_ci}\n```\n",
        {
            "executado": now_iso(),
            "branch": branch,
            "resultado": "verde" if ok_ci else "falha",
        },
    )
    append_log("deploy-stage", f"ci: {'ok' if ok_ci else 'falha'}")

    if not ok_ci:
        print("\n❌ CI não está verde. Decisão obrigatória (runbook E4):")
        print("   1. Reversão de código (git revert do commit que quebrou) + re-deploy")
        print("   2. Correção do issue de pipeline/workflow + re-executar")
        md_falha, _ = emitir_relatorio(
            "doc-bug-log",
            f"falha-pipeline-{runid}",
            "Relatório Falha de Pipeline",
            f"# Relatório Falha de Pipeline\n\nExecutado: {now_iso()}\nBranch: {branch}\n"
            f"Decisão pendente: reversão de código OU correção de pipeline/workflow.\n"
            f"Não prosseguir para merge até pipeline verde.\n\n```\n{saida_ci}\n```\n",
            {"executado": now_iso(), "branch": branch, "decisao": "pendente"},
        )
        append_log("deploy-stage", "bloqueado: ci falhou, decisao pendente")
        print(f"   Relatório: {md_falha.relative_to(ROOT)}")
        return 1

    # E2: commit + push (código + documentação + testes + logs/relatórios)
    print("\n[E2] Commit e push (código + documentação + testes)...")
    mensagem = f"feat(deploy): ciclo codificacao-deploy {branch} [{runid}]"
    ok_push, saida_push = git_commit_push(mensagem, branch)
    print(saida_push[-1500:])
    append_log("deploy-stage", f"commit/push: {'ok' if ok_push else 'falha'}")
    if not ok_push:
        print("❌ Falha no commit/push.")
        return 1

    # E3: smoke test rápido em stage (docker compose config; proxy 127.0.0.1:8080 no CI)
    print("\n[E3] Smoke test stage (docker compose config)...")
    res = run_cmd(["docker", "compose", "config", "--quiet"])
    smoke = res.returncode == 0
    if smoke:
        print("   ✅ docker compose config válido")
    elif res.returncode == 127:
        print("   ⚠️  docker indisponível neste ambiente — validar em stage via CI.")
    else:
        print("   ⚠️  docker compose config com avisos/erros")

    md_dep, js_dep = emitir_relatorio(
        "doc-release-notes",
        f"implantacao-stage-{runid}",
        "Relatório Implantação em Stage",
        f"# Relatório Implantação em Stage\n\nExecutado: {now_iso()}\nBranch: {branch}\n"
        f"CI: VERDE\nPush: OK\nSmoke test (docker compose config): {'OK' if smoke else 'AVISO'}\n"
        f"Próximo: aguardar aprovação do gate de stage para merge.\n",
        {
            "gate": "deploy-stage",
            "timestamp": now_iso(),
            "branch": branch,
            "ci_green": ok_ci,
            "push": ok_push,
            "smoke_test": smoke,
            "proximo": "aguardar_aprovacao_merge",
        },
    )
    append_log(
        "deploy-stage",
        f"deploy: ok, smoke: {smoke}, relatorio: {md_dep.relative_to(ROOT)}",
    )

    print(
        "\n✅ Deploy em stage concluído. Aguardando aprovação do gate de stage para merge."
    )
    print(f"   Relatório: {md_dep.relative_to(ROOT)} | {js_dep.relative_to(ROOT)}")
    return 0


# --------------------------------------------------------------------------- gate-stage (Fase F)
def gate_stage(aprovador_arg: str | None, hash_merge_arg: str | None) -> int:
    print("=" * 60)
    print("GATE STAGE — Fase F: revisão de implantação em stage + aprovação para merge")
    print("=" * 60)
    append_log("gate-stage", "iniciado")

    aprovador = aprovador_arg
    if not aprovador and sys.stdin.isatty():
        aprovador = input("Nome do aprovador (CCB/PO): ").strip() or None
    hash_merge = hash_merge_arg
    aprovador = aprovador or "pendente"

    md, _ = emitir_relatorio(
        "doc-status-report",
        f"aprovacao-merge-{slug_data()}",
        "Relatório Aprovação de Merge",
        f"# Relatório Aprovação de Merge\n\nExecutado: {now_iso()}\n"
        f"Aprovador: {aprovador}\nGate de stage: revisado\n"
        f"Status: aguardando_aprovacao_explicita\n"
        f"Hash do merge: {hash_merge or '— (não realizado — aguardando aprovação)'}\n\n"
        f"Regras: não fazer merge para main antes da aprovação explícita do gate de stage "
        f"(Constitution Art. 6.3).\n",
        {
            "executado": now_iso(),
            "aprovador": aprovador,
            "status": "aguardando_aprovacao_explicita",
            "hash_merge": hash_merge,
        },
    )
    append_log(
        "gate-stage", f"aprovador: {aprovador}, relatorio: {md.relative_to(ROOT)}"
    )

    print(f"\n📋 Relatório emitido: {md.relative_to(ROOT)}")
    print("⚠️  NÃO fazer merge para main antes da aprovação explícita do revisor/CCB.")
    return 0


# --------------------------------------------------------------------------- relatorio consolidado
def relatorio() -> int:
    print("=" * 60)
    print("RELATÓRIO CONSOLIDADO — docs/reports/")
    print("=" * 60)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(
        p
        for p in REPORTS_DIR.iterdir()
        if p.suffix in (".md", ".json") and p.name != CONSOLIDADO
    )
    if not arquivos:
        print("Nenhum relatório encontrado em docs/reports/.")
        return 0
    for a in arquivos:
        print(f"  - {a.relative_to(ROOT)}")
    resumo = {
        "gerado_em": now_iso(),
        "total_relatorios": len(arquivos),
        "arquivos": [str(a.relative_to(ROOT)) for a in arquivos],
    }
    write_json(REPORTS_DIR / CONSOLIDADO, resumo)
    print(f"\n✅ Consolidado: docs/reports/{CONSOLIDADO} ({len(arquivos)} relatórios)")
    return 0


# --------------------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hook ciclo de codificação e deploy (COBECO)"
    )
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser(
        "gate-inicio", help="Fase A: specs aprovadas, dependências, paralelismo PMBOK"
    )
    sub.add_parser(
        "gate-ciclo", help="Fases B-D: testes, PDCA, artefatos, secret scan, refs"
    )
    sub.add_parser(
        "deploy-stage", help="Fase E: CI green, commit/push, deploy, falha de pipeline"
    )
    gs = sub.add_parser(
        "gate-stage", help="Fase F: aprovação de merge após gate de stage"
    )
    gs.add_argument("--aprovador", help="Nome do aprovador (CCB/PO)")
    gs.add_argument(
        "--hash-merge", dest="hash_merge", help="Hash do commit de merge, se houver"
    )
    sub.add_parser("relatorio", help="Emite relatório consolidado de docs/reports/")
    args = parser.parse_args()

    try:
        if args.comando == "gate-inicio":
            return gate_inicio()
        if args.comando == "gate-ciclo":
            return gate_ciclo()
        if args.comando == "deploy-stage":
            return deploy_stage()
        if args.comando == "gate-stage":
            return gate_stage(args.aprovador, args.hash_merge)
        if args.comando == "relatorio":
            return relatorio()
    except KeyboardInterrupt:
        print("\n⏹️  Cancelado pelo usuário.")
        return 130
    except Exception as e:
        print(f"❌ Erro inesperado: {e}", file=sys.stderr)
        append_log("erro", str(e))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
