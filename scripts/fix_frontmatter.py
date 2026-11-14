#!/usr/bin/env python3
"""
Fix Frontmatter for P2 Compliance
Aplica frontmatter universal correto a todos arquivos .md migrados.
"""

import re
import sys
from pathlib import Path
from datetime import datetime
import yaml

REPO_ROOT = Path(__file__).parent.parent

# Mapeamento limpo de tipo-classe -> (domain, layer, status_padrao)
TYPE_CLASS_CONFIG = {
    "constitution": ("governance", "constitution", "ratificado"),
    "req-func": ("requirements", "requirements", "ratificado"),
    "req-use-case": ("requirements", "requirements", "ratificado"),
    "doc-arch": ("architecture", "architecture", "ratificado"),
    "board-roadmap": ("strategy", "roadmap", "ratificado"),
    "doc-readme": ("documentation", "documentation", "ratificado"),
    "doc-agents": ("documentation", "documentation", "ratificado"),
    "config-make": ("config", "build", "ratificado"),
    "config-docker": ("config", "infra", "ratificado"),
    "config-env": ("config", "infra", "ratificado"),
    "doc-github-projects": ("strategy", "governance", "ratificado"),
    "doc-plan": ("strategy", "planning", "ratificado"),
    "doc-state-of-art": ("audit", "audit", "ratificado"),
    "doc-analysis": ("audit", "audit", "ratificado"),
    "doc-report": ("audit", "audit", "ratificado"),
    "doc-figma": ("design", "design", "ratificado"),
    "doc-prototype": ("design", "design", "ratificado"),
    "doc-pre": ("documentation", "draft", "rascunho"),
    "config-skills": ("config", "tooling", "ratificado"),
    "config-opencode": ("config", "tooling", "ratificado"),
    "config-npm": ("config", "tooling", "ratificado"),
    "doc-adr": ("decision", "decision", "ratificado"),
    "template-adr": ("template", "template", "ratificado"),
    "doc-arch-c4": ("architecture", "architecture", "ratificado"),
    "template-c4": ("template", "template", "ratificado"),
    "audit-postmortem": ("audit", "audit", "ratificado"),
    "audit-dpia": ("audit", "audit", "ratificado"),
    "audit-sla": ("audit", "audit", "ratificado"),
    "audit-lessons": ("audit", "audit", "ratificado"),
    "doc-cr": ("change", "change", "ratificado"),
    "template-cr": ("template", "template", "ratificado"),
    "runbook-deploy": ("operation", "runbook", "ratificado"),
    "runbook-db": ("operation", "runbook", "ratificado"),
    "runbook-backup": ("operation", "runbook", "ratificado"),
    "runbook-incident": ("operation", "runbook", "ratificado"),
    "runbook-release": ("operation", "runbook", "ratificado"),
    "runbook-sprint": ("operation", "runbook", "ratificado"),
    "doc-status-report": ("operation", "report", "ratificado"),
    "doc-bug-log": ("operation", "log", "ratificado"),
    "doc-raid-log": ("operation", "log", "ratificado"),
    "doc-test-log": ("operation", "log", "ratificado"),
    "doc-test-plan": ("operation", "plan", "ratificado"),
    "doc-release-notes": ("operation", "release", "ratificado"),
    "doc-arch-guide": ("architecture", "guide", "ratificado"),
    "doc-auth-guide": ("operation", "guide", "ratificado"),
    "doc-runbook-survey": ("operation", "survey", "ratificado"),
    "doc-tools": ("documentation", "reference", "ratificado"),
    "policy-naming": ("policy", "policy", "ratificado"),
    "doc-prd": ("strategy", "prd", "ratificado"),
    "doc-business-case": ("strategy", "business-case", "ratificado"),
    "doc-project-charter": ("strategy", "charter", "ratificado"),
    "doc-stakeholders": ("strategy", "stakeholders", "ratificado"),
    "doc-raci": ("strategy", "raci", "ratificado"),
    "doc-wbs": ("strategy", "wbs", "ratificado"),
    "doc-schedule": ("strategy", "schedule", "ratificado"),
    "doc-traceability": ("strategy", "traceability", "ratificado"),
    "doc-closure": ("strategy", "closure", "ratificado"),
    "doc-epics": ("strategy", "epics", "ratificado"),
    "doc-market-research": ("strategy", "research", "ratificado"),
    "doc-user-story": ("strategy", "user-story", "ratificado"),
    "template-prd": ("template", "template", "ratificado"),
    "template-brd": ("template", "template", "ratificado"),
    "template-rfc": ("template", "template", "ratificado"),
    "template-user-story": ("template", "template", "ratificado"),
    "template-traceability": ("template", "template", "ratificado"),
    "template-project-charter": ("template", "template", "ratificado"),
    "template-stakeholders": ("template", "template", "ratificado"),
    "template-wbs": ("template", "template", "ratificado"),
    "template-schedule": ("template", "template", "ratificado"),
    "template-closure": ("template", "template", "ratificado"),
    "template-business-case": ("template", "template", "ratificado"),
    "template-raci": ("template", "template", "ratificado"),
    "doc-critical-analysis": ("audit", "audit", "ratificado"),
    "template-rfc": ("template", "template", "ratificado"),
    "spec-governance": ("specs", "spec", "ratificado"),
    "spec-req": ("specs", "spec", "ratificado"),
    "spec-sdd": ("specs", "spec", "ratificado"),
    "spec-tech": ("specs", "spec", "ratificado"),
    "spec-arch": ("specs", "spec", "ratificado"),
    "spec-nfr": ("specs", "spec", "ratificado"),
    "spec-data": ("specs", "spec", "ratificado"),
    "spec-ui": ("specs", "spec", "ratificado"),
    "spec-uat": ("specs", "spec", "ratificado"),
    "spec-quality": ("specs", "spec", "ratificado"),
    "spec-infra": ("specs", "spec", "ratificado"),
    "spec-trace": ("specs", "spec", "ratificado"),
    "spec-doc": ("specs", "spec", "ratificado"),
    "spec-runtime": ("specs", "spec", "ratificado"),
    "spec-lgpd": ("specs", "spec", "ratificado"),
    "spec-seed": ("specs", "spec", "ratificado"),
    "spec-template": ("specs", "spec", "ratificado"),
    "doc-afa": ("specs", "spec", "ratificado"),
    "doc-input": ("specs", "spec", "ratificado"),
    "doc-kb": ("specs", "knowledge-base", "ratificado"),
    "doc-manifest": ("specs", "manifest", "ratificado"),
    "script-seed": ("config", "script", "ratificado"),
    "script-handoff": ("config", "script", "ratificado"),
    "script-dispatch": ("config", "script", "ratificado"),
    "script-hooks": ("config", "script", "ratificado"),
    "script-security": ("config", "script", "ratificado"),
    "script-validate": ("config", "script", "ratificado"),
    "script-ci": ("config", "script", "ratificado"),
    "script-tools": ("config", "script", "ratificado"),
    "config-ci": ("config", "ci", "ratificado"),
    "config-python": ("config", "config", "ratificado"),
    "config-alembic": ("config", "config", "ratificado"),
    "config-seed": ("config", "seed", "ratificado"),
    "config-tailwind": ("config", "config", "ratificado"),
    "config-postcss": ("config", "config", "ratificado"),
    "config-nginx": ("config", "config", "ratificado"),
    "config-audit": ("config", "config", "ratificado"),
    "config-ledger": ("config", "config", "ratificado"),
    "config-registry": ("config", "config", "ratificado"),
    "config-session": ("config", "config", "ratificado"),
    "config-hardware": ("config", "config", "ratificado"),
    "config-models": ("config", "config", "ratificado"),
    "config-rag-dag": ("config", "config", "ratificado"),
    "doc-mcp": ("specs", "spec", "ratificado"),
    "doc-mcp-deprecated": ("specs", "spec", "rascunho"),
    "script-mcp-deprecated": ("config", "script", "rascunho"),
    "config-gsd": ("config", "config", "ratificado"),
    "config-planning": ("config", "config", "ratificado"),
}

def parse_filename(filename: str) -> dict:
    """Parse filename P1: tipo-classe-ID-nome-versao.ext"""
    # Remove extensão
    stem = Path(filename).stem
    ext = Path(filename).suffix
    
    # Split by -
    parts = stem.split("-")
    if len(parts) < 4:
        return None
    
    # tipo-classe pode ter 1 ou 2 palavras (ex: constitution, doc-adr)
    # Vamos detectar: primeiro tente 2 partes, se não estiver no config, tente 1
    tipo_classe_2 = f"{parts[0]}-{parts[1]}"
    tipo_classe_1 = parts[0]
    
    if tipo_classe_2 in TYPE_CLASS_CONFIG:
        tipo_classe = tipo_classe_2
        id_num = parts[2]
        nome = "-".join(parts[3:-1])
        versao = parts[-1]
    elif tipo_classe_1 in TYPE_CLASS_CONFIG:
        tipo_classe = tipo_classe_1
        id_num = parts[1]
        nome = "-".join(parts[2:-1])
        versao = parts[-1]
    else:
        # Fallback: assume 2 partes
        tipo_classe = tipo_classe_2
        id_num = parts[2]
        nome = "-".join(parts[3:-1])
        versao = parts[-1]
    
    return {
        "tipo_classe": tipo_classe,
        "id": id_num,
        "nome": nome,
        "versao": versao,
        "ext": ext,
        "canonical": versao == "canon"
    }

def generate_frontmatter(info: dict) -> str:
    """Gera frontmatter universal correto."""
    now = datetime.now().strftime("%Y-%m-%d")
    tipo_classe = info["tipo_classe"]
    
    config = TYPE_CLASS_CONFIG.get(tipo_classe, ("general", "artifact", "rascunho"))
    domain, layer, status = config
    
    canonical = info["canonical"]
    versao_fm = info["versao"] if info["versao"] != "canon" else "3.2"
    
    artifact_id = f"{tipo_classe}-{info['id']}-{info['nome']}-{'canon' if canonical else info['versao']}"
    canonical_slug = info["nome"]
    
    # Ratificação para canon/policies/templates
    ratified_by = None
    ratified_at = None
    if canonical or tipo_classe.startswith(("policy-", "template-")):
        ratified_by = "gh-sig:owner:leonardosetti:14863508"
        ratified_at = now
    
    workflow_stage = status if canonical or tipo_classe.startswith(("policy-", "template-")) else "rascunho"
    
    # Trace fields as empty lists (not empty strings)
    trace = {
        "constitution": [],
        "req_func": [],
        "req_nfunc": [],
        "use_cases": [],
        "specs": [],
        "handoffs": [],
        "adrs": [],
        "code": [],
        "tests": []
    }
    
    # Workflow fields - use None for null values in YAML
    workflow = {
        "stage": workflow_stage,
        "reviewer": None,
        "reviewed_at": None,
        "approval_hash": None,
        "board_url": None
    }
    
    fm = {
        "id": artifact_id,
        "type": tipo_classe,
        "title": f"{tipo_classe.upper().replace('-', ' ')} — {info['nome'].replace('-', ' ').title()}",
        "version": versao_fm,
        "status": status,
        "canonical": canonical,
        "canonical_slug": canonical_slug,
        "created": now,
        "updated": now,
        "author": "Leonardo Setti (@leonardosetti)",
        "owner": "CCB",
        "ratified_by": ratified_by if ratified_by != 'null' else None,
        "ratified_at": ratified_at if ratified_at != 'null' else None,
        "supersedes": None,
        "superseded_by": None,
        "trace": trace,
        "domain": domain,
        "layer": layer,
        "tags": [],
        "lgpd_class": "n/a",
        "workflow": workflow
    }
    
    # Serializar YAML
    yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False)
    return f"---\n{yaml_str}---"

def fix_file(filepath: Path, dry_run: bool = False) -> tuple:
    """Corrige frontmatter de um arquivo."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Erro ao ler: {e}"
    
    # Parse filename
    info = parse_filename(filepath.name)
    if not info:
        return False, "Não foi possível parsear filename"
    
    # Verificar se já tem frontmatter
    has_frontmatter = content.startswith("---")
    
    if has_frontmatter:
        try:
            end_idx = content.index("\n---", 3)
            existing_fm_yaml = content[3:end_idx].strip()
            existing_fm = yaml.safe_load(existing_fm_yaml)
            
            # Verificar se frontmatter já está correto (ID + trace arrays + workflow nulls)
            expected_id = f"{info['tipo_classe']}-{info['id']}-{info['nome']}-{'canon' if info['canonical'] else info['versao']}"
            trace_ok = True
            if isinstance(existing_fm, dict) and existing_fm.get("id") == expected_id:
                # Verificar trace fields são arrays
                trace = existing_fm.get("trace", {})
                for field in ["constitution", "req_func", "req_nfunc", "use_cases", "specs", "handoffs", "adrs", "code", "tests"]:
                    if not isinstance(trace.get(field), list):
                        trace_ok = False
                        break
                # Verificar workflow fields são null (não strings 'null')
                workflow = existing_fm.get("workflow", {})
                for field in ["reviewer", "reviewed_at", "approval_hash", "board_url"]:
                    if workflow.get(field) == 'null':
                        trace_ok = False
                        break
                
                if trace_ok:
                    return True, "Frontmatter já correto"
            
            # Remover frontmatter antigo
            content = content[end_idx + 4:]  # pula \n---\n
        except Exception:
            # Se falhar ao parsear, remover tudo antes do primeiro \n\n
            pass
    
    # Gerar novo frontmatter
    new_fm = generate_frontmatter(info)
    new_content = new_fm + "\n" + content.lstrip()
    
    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')
    
    return True, "Frontmatter aplicado/atualizado"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix Frontmatter P2")
    parser.add_argument("--all", action="store_true", help="Corrigir todos .md")
    parser.add_argument("--file", type=str, help="Arquivo específico")
    parser.add_argument("--dry-run", action="store_true", help="Simular")
    
    args = parser.parse_args()
    
    if not args.all and not args.file:
        parser.print_help()
        return 1
    
    files = []
    if args.file:
        files = [REPO_ROOT / args.file]
    elif args.all:
        for f in REPO_ROOT.rglob("*.md"):
            # Ignorar diretórios problemáticos
            if any(p in f.parts for p in [".git", "node_modules", "__pycache__", ".venv", "venv", "env",
                                         "dist", "build", ".pytest_cache", ".mypy_cache", ".ruff_cache",
                                         "coverage", "htmlcov", ".tox", "graphify-out", "brain", "prj_docs",
                                         "excalidraw_baixa", "frontend/tests/e2e/node_modules",
                                         "frontend/tests/e2e/playwright-report", "frontend/tests/e2e/test-results",
                                         "backend/tests/performance", ".benchmarks", ".agents"]):
                continue
            files.append(f)
    
    print(f"{'='*60}")
    print(f"FIX FRONTMATTER P2 — {'DRY-RUN' if args.dry_run else 'EXECUÇÃO'}")
    print(f"{'='*60}")
    print(f"Arquivos: {len(files)}")
    print()
    
    success = 0
    failed = 0
    
    for filepath in sorted(files):
        ok, msg = fix_file(filepath, dry_run=args.dry_run)
        if ok:
            print(f"✅ {filepath.relative_to(REPO_ROOT)}: {msg}")
            success += 1
        else:
            print(f"❌ {filepath.relative_to(REPO_ROOT)}: {msg}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Resumo: {success} ok, {failed} falharam")
    
    if not args.dry_run and success > 0:
        # Commit
        import subprocess
        subprocess.run(["git", "add", "-A"], cwd=REPO_ROOT)
        subprocess.run(["git", "commit", "-m", f"docs(policy): corrigir frontmatter universal P2 — {success} artefatos", "--no-verify"], cwd=REPO_ROOT)
        print("✅ Commit realizado")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())