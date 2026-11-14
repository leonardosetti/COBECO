#!/usr/bin/env python3
"""
Artifact Validation Script — Protocolo P1/P2/P3
Validação de nomenclatura, frontmatter, rastreabilidade e workflow.

Uso:
  python scripts/script-validate-0002-artifact-validate-v1.0.py --all           # Validar todo repositório
  python scripts/script-validate-0002-artifact-validate-v1.0.py --file <path>   # Validar arquivo específico
  python scripts/script-validate-0002-artifact-validate-v1.0.py --fix           # Tentar corrigir automaticamente
"""

import os
import re
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent

# Tipos-classe válidos (P1)
VALID_TYPE_CLASSES = {
    "constitution", "req-func", "req-use-case", "doc-arch", "board-roadmap",
    "doc-readme", "doc-agents", "config-make", "config-docker", "config-env",
    "doc-github-projects", "doc-plan", "doc-state-of-art", "doc-analysis",
    "doc-report", "doc-figma", "doc-prototype", "doc-pre", "config-skills",
    "config-opencode", "config-npm", "doc-adr", "template-adr", "doc-arch-c4",
    "template-c4", "audit-postmortem", "audit-dpia", "audit-sla", "audit-lessons",
    "doc-cr", "template-cr", "runbook-deploy", "runbook-db", "runbook-backup",
    "runbook-incident", "runbook-release", "runbook-sprint", "doc-status-report",
    "doc-bug-log", "doc-raid-log", "doc-test-log", "doc-test-plan",
    "doc-release-notes", "doc-arch-guide", "doc-auth-guide", "doc-runbook-survey",
    "doc-tools", "policy-naming", "doc-prd", "doc-business-case", "doc-project-charter",
    "doc-stakeholders", "doc-raci", "doc-wbs", "doc-schedule", "doc-traceability",
    "doc-closure", "doc-epics", "doc-market-research", "doc-user-story",
    "template-prd", "template-brd", "template-rfc", "template-user-story",
    "template-traceability", "template-project-charter", "template-stakeholders",
    "template-wbs", "template-schedule", "template-closure", "template-business-case",
    "template-raci", "doc-critical-analysis", "template-rfc",
    "spec-governance", "spec-req", "spec-sdd", "spec-tech", "spec-arch",
    "spec-nfr", "spec-data", "spec-ui", "spec-uat", "spec-quality",
    "spec-infra", "spec-trace", "spec-doc", "spec-runtime", "spec-lgpd",
    "spec-seed", "spec-template", "doc-afa", "doc-input", "doc-kb", "doc-manifest",
    "script-seed", "script-handoff", "script-dispatch", "script-hooks",
    "script-security", "script-validate", "script-ci", "script-tools",
    "config-ci", "config-python", "config-alembic", "config-seed",
    "config-tailwind", "config-postcss", "config-nginx", "config-npm",
    "config-audit", "config-ledger", "config-registry", "config-session",
    "config-hardware", "config-models", "config-rag-dag",
    "doc-mcp", "doc-mcp-deprecated", "script-mcp-deprecated",
    "config-gsd", "config-planning",
    "hf-exec",
}

# Campos obrigatórios do frontmatter universal (P2)
REQUIRED_FRONTMATTER_FIELDS = {
    "id", "type", "title", "version", "status", "canonical", "canonical_slug",
    "created", "updated", "author", "owner", "ratified_by", "ratified_at",
    "supersedes", "superseded_by", "trace", "domain", "layer", "tags",
    "lgpd_class", "workflow"
}

REQUIRED_TRACE_FIELDS = {
    "constitution", "req_func", "req_nfunc", "use_cases", "specs",
    "handoffs", "adrs", "code", "tests"
}

REQUIRED_WORKFLOW_FIELDS = {
    "stage", "reviewer", "reviewed_at", "approval_hash", "board_url"
}

VALID_STATUS = {"rascunho", "revisao", "aprovado", "rejeitado", "ratificado", "promulgado", "obsoleto"}
VALID_WORKFLOW_STAGES = {"rascunho", "revisao", "aprovado", "rejeitado", "ratificado", "promulgado", "obsoleto"}
VALID_LGPD = {"n/a", "PII-zero", "PII-sintetico"}

@dataclass
class ValidationResult:
    file: Path
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

def validate_filename_p1(filepath: Path) -> Tuple[bool, List[str], Dict]:
    """Valida nomenclatura P1: kebab-case, tipo-classe, ID, nome, versão."""
    errors = []
    info = {}
    
    name = filepath.name
    
    # Padrão: tipo-classe-ID-nome-versao.ext
    # tipo-classe pode ser palavra única (constitution) ou composto (doc-adr, req-func)
    pattern = r'^([a-z]+(?:-[a-z]+)*)-(\d{4})-([a-z0-9-]+)-(v\d+\.\d+|canon)\.([a-z0-9]+)$'
    match = re.match(pattern, name)
    
    if not match:
        errors.append(f"Nome '{name}' não segue padrão P1: <tipo-classe>-<ID:04d>-<nome-kebab>-<vX.Y|canon>.<ext>")
        return False, errors, info
    
    tipo_classe, id_num, nome, versao, ext = match.groups()
    
    if tipo_classe not in VALID_TYPE_CLASSES:
        errors.append(f"Tipo-classe '{tipo_classe}' não está na lista de prefixos reservados")
    
    # Validar ID numérico sequencial (por tipo-classe)
    try:
        id_int = int(id_num)
        if id_int <= 0:
            errors.append(f"ID '{id_num}' deve ser positivo")
    except ValueError:
        errors.append(f"ID '{id_num}' não é numérico")
    
    # Validar versão
    if versao != "canon":
        if not re.match(r'^v\d+\.\d+$', versao):
            errors.append(f"Versão '{versao}' deve ser 'vX.Y' ou 'canon'")
    else:
        info["canonical"] = True
    
    info["tipo_classe"] = tipo_classe
    info["id"] = id_num
    info["nome"] = nome
    info["versao"] = versao
    info["ext"] = ext
    
    return len(errors) == 0, errors, info

def validate_frontmatter_p2(filepath: Path, p1_info: Dict) -> Tuple[bool, List[str], List[str]]:
    """Valida frontmatter universal P2."""
    errors = []
    warnings = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f"Erro ao ler arquivo: {e}")
        return False, errors, warnings
    
    # Extrair frontmatter YAML
    if not content.startswith("---"):
        errors.append("Arquivo não possui frontmatter YAML (deve iniciar com ---)")
        return False, errors, warnings
    
    try:
        # Encontrar segundo ---
        end_idx = content.index("\n---", 3)
        frontmatter_yaml = content[3:end_idx].strip()
        fm = yaml.safe_load(frontmatter_yaml)
    except (ValueError, yaml.YAMLError) as e:
        errors.append(f"Frontmatter YAML inválido: {e}")
        return False, errors, warnings
    
    if not isinstance(fm, dict):
        errors.append("Frontmatter deve ser um objeto YAML (dicionário)")
        return False, errors, warnings
    
    # Validar campos obrigatórios
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm:
            errors.append(f"Campo obrigatório ausente no frontmatter: {field}")
    
    if errors:
        return False, errors, warnings
    
    # Validar consistência ID/filename
    expected_id = f"{p1_info['tipo_classe']}-{p1_info['id']}-{p1_info['nome']}-{'canon' if p1_info['versao'] == 'canon' else p1_info['versao']}"
    if fm.get("id") != expected_id:
        errors.append(f"Frontmatter 'id' ({fm.get('id')}) não corresponde ao filename ({expected_id})")
    
    if fm.get("type") != p1_info["tipo_classe"]:
        errors.append(f"Frontmatter 'type' ({fm.get('type')}) não corresponde ao tipo-classe do filename ({p1_info['tipo_classe']})")
    
    # Validar version
    expected_version = p1_info["versao"] if p1_info["versao"] != "canon" else fm.get("version", "3.2")
    if fm.get("version") != expected_version and not (p1_info["versao"] == "canon" and fm.get("version") in ["3.2", "2.0", "1.0"]):
        warnings.append(f"Frontmatter 'version' ({fm.get('version')}) pode não corresponder à versão do filename ({p1_info['versao']})")
    
    # Validar status
    if fm.get("status") not in VALID_STATUS:
        errors.append(f"Status inválido: {fm.get('status')}. Válidos: {VALID_STATUS}")
    
    # Validar canonical
    if p1_info["versao"] == "canon" and not fm.get("canonical", False):
        errors.append("Arquivo 'canon' deve ter frontmatter 'canonical: true'")
    elif p1_info["versao"] != "canon" and fm.get("canonical", False):
        warnings.append("Arquivo versionado (não canon) tem canonical: true")
    
    # Validar trace
    trace = fm.get("trace", {})
    if not isinstance(trace, dict):
        errors.append("Campo 'trace' deve ser um objeto")
    else:
        for field in REQUIRED_TRACE_FIELDS:
            if field not in trace:
                warnings.append(f"Campo 'trace.{field}' ausente (recomendado para rastreabilidade)")
            elif not isinstance(trace[field], list):
                errors.append(f"Campo 'trace.{field}' deve ser uma lista")
    
    # Validar workflow
    workflow = fm.get("workflow", {})
    if not isinstance(workflow, dict):
        errors.append("Campo 'workflow' deve ser um objeto")
    else:
        for field in REQUIRED_WORKFLOW_FIELDS:
            if field not in workflow:
                warnings.append(f"Campo 'workflow.{field}' ausente")
        if workflow.get("stage") not in VALID_WORKFLOW_STAGES:
            errors.append(f"Workflow stage inválido: {workflow.get('stage')}")
    
    # Validar lgpd_class
    if fm.get("lgpd_class") not in VALID_LGPD:
        errors.append(f"lgpd_class inválido: {fm.get('lgpd_class')}. Válidos: {VALID_LGPD}")
    
    # Validar ratified_by para canon/policies/templates
    if p1_info["versao"] == "canon" or p1_info["tipo_classe"].startswith(("policy-", "template-")):
        if not fm.get("ratified_by"):
            errors.append("Artefato canon/policy/template deve ter 'ratified_by' preenchido")
        if not fm.get("ratified_at"):
            errors.append("Artefato canon/policy/template deve ter 'ratified_at' preenchido")
    
    return len(errors) == 0, errors, warnings

def validate_cross_references(filepath: Path, fm: Dict) -> Tuple[bool, List[str], List[str]]:
    """Valida rastreabilidade e referências cruzadas."""
    errors = []
    warnings = []
    
    trace = fm.get("trace", {})
    
    # Verificar se referências existem (arquivos locais)
    for field_name, refs in trace.items():
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if not ref:
                continue
            # Se for caminho local (não URL)
            if not ref.startswith(("http://", "https://", "mailto:", "ssh://", "git@")):
                # Verificar se arquivo existe
                ref_path = REPO_ROOT / ref
                if not ref_path.exists():
                    warnings.append(f"Referência local não encontrada: trace.{field_name} -> {ref}")
    
    return len(errors) == 0, errors, warnings

def validate_workflow_consistency(filepath: Path, fm: Dict) -> Tuple[bool, List[str], List[str]]:
    """Valida consistência do workflow (P3)."""
    errors = []
    warnings = []
    
    workflow = fm.get("workflow", {})
    stage = workflow.get("stage")
    status = fm.get("status")
    
    # stage e status devem ser consistentes
    if stage != status:
        warnings.append(f"Workflow stage ('{stage}') difere de status ('{status}')")
    
    # Se ratificado/promulgado, deve ter approval_hash e ratified_by
    if stage in ["ratificado", "promulgado"]:
        if not workflow.get("approval_hash"):
            warnings.append("Artefato ratificado/promulgado deve ter 'workflow.approval_hash'")
        if not fm.get("ratified_by"):
            warnings.append("Artefato ratificado/promulgado deve ter 'ratified_by'")
        if not fm.get("ratified_at"):
            warnings.append("Artefato ratificado/promulgado deve ter 'ratified_at'")
    
    # Se promulgado, deve ter commit hash no board_url ou approval_hash
    if stage == "promulgado":
        if not workflow.get("board_url"):
            warnings.append("Artefato promulgado deve ter 'workflow.board_url'")
    
    return len(errors) == 0, errors, warnings

def validate_file(filepath: Path) -> ValidationResult:
    """Validação completa de um arquivo."""
    result = ValidationResult(file=filepath, valid=True)
    
    # P1: Nomenclatura
    p1_valid, p1_errors, p1_info = validate_filename_p1(filepath)
    if not p1_valid:
        result.valid = False
        result.errors.extend([f"[P1] {e}" for e in p1_errors])
    else:
        result.info.append(f"[P1] OK: tipo={p1_info['tipo_classe']}, id={p1_info['id']}, nome={p1_info['nome']}, versão={p1_info['versao']}")
    
    # P2/P3: Apenas para .md com frontmatter
    if filepath.suffix.lower() == ".md":
        try:
            content = filepath.read_text(encoding='utf-8')
            if content.startswith("---"):
                # Validar frontmatter
                end_idx = content.index("\n---", 3)
                frontmatter_yaml = content[3:end_idx].strip()
                fm = yaml.safe_load(frontmatter_yaml)
                
                if isinstance(fm, dict):
                    # P2: Frontmatter universal
                    fm_valid, fm_errors, fm_warnings = validate_frontmatter_p2(filepath, p1_info)
                    if not fm_valid:
                        result.valid = False
                        result.errors.extend([f"[P2] {e}" for e in fm_errors])
                    result.warnings.extend([f"[P2] {w}" for w in fm_warnings])
                    
                    # Cross-references
                    ref_valid, ref_errors, ref_warnings = validate_cross_references(filepath, fm)
                    result.warnings.extend([f"[REF] {w}" for w in ref_warnings])
                    
                    # P3: Workflow
                    wf_valid, wf_errors, wf_warnings = validate_workflow_consistency(filepath, fm)
                    result.warnings.extend([f"[P3] {w}" for w in wf_warnings])
                else:
                    result.warnings.append("[P2] Frontmatter não é dicionário válido")
            else:
                result.warnings.append("[P2] Arquivo .md sem frontmatter YAML")
        except Exception as e:
            result.errors.append(f"[P2] Erro ao validar frontmatter: {e}")
            result.valid = False
    
    return result

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validação Protocolo P1/P2/P3")
    parser.add_argument("--all", action="store_true", help="Validar todo repositório")
    parser.add_argument("--file", type=str, help="Validar arquivo específico")
    parser.add_argument("--fix", action="store_true", help="Tentar corrigir automaticamente (não implementado)")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    
    args = parser.parse_args()
    
    if not args.all and not args.file:
        parser.print_help()
        return 1
    
    files_to_check = []
    
    if args.file:
        files_to_check = [REPO_ROOT / args.file]
    elif args.all:
        for filepath in REPO_ROOT.rglob("*"):
            if filepath.is_file() and not any(part in IGNORE_DIRS for part in filepath.parts):
                if filepath.suffix.lower() in {".md", ".py", ".js", ".ts", ".json", ".yml", ".yaml", ".toml"}:
                    files_to_check.append(filepath)
    
    print(f"{'='*60}")
    print(f"VALIDAÇÃO PROTOCOLO P1/P2/P3")
    print(f"{'='*60}")
    print(f"Arquivos a validar: {len(files_to_check)}")
    print()
    
    results = []
    total_errors = 0
    total_warnings = 0
    
    for filepath in sorted(files_to_check):
        result = validate_file(filepath)
        results.append(result)
        total_errors += len(result.errors)
        total_warnings += len(result.warnings)
        
        if not args.json:
            status = "✅" if result.valid else "❌"
            print(f"{status} {filepath.relative_to(REPO_ROOT)}")
            for err in result.errors:
                print(f"   ❌ {err}")
            for warn in result.warnings:
                print(f"   ⚠️  {warn}")
            for info in result.info:
                print(f"   ℹ️  {info}")
            if result.errors or result.warnings:
                print()
    
    # Resumo
    valid_count = sum(1 for r in results if r.valid)
    invalid_count = len(results) - valid_count
    
    if args.json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "valid": valid_count,
            "invalid": invalid_count,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "results": [
                {
                    "file": str(r.file.relative_to(REPO_ROOT)),
                    "valid": r.valid,
                    "errors": r.errors,
                    "warnings": r.warnings,
                    "info": r.info
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"RESUMO:")
        print(f"   Total: {len(results)}")
        print(f"   Válidos: {valid_count}")
        print(f"   Inválidos: {invalid_count}")
        print(f"   Erros: {total_errors}")
        print(f"   Avisos: {total_warnings}")
    
    return 0 if invalid_count == 0 else 1

# Import IGNORE_DIRS from migrate script
IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "coverage", "htmlcov", ".tox", "*.egg-info",
    "graphify-out", "brain", "prj_docs", "excalidraw_baixa",
    "frontend/tests/e2e/node_modules", "frontend/tests/e2e/playwright-report",
    "frontend/tests/e2e/test-results", "backend/tests/performance",
    ".benchmarks", ".agents",
}

if __name__ == "__main__":
    sys.exit(main())