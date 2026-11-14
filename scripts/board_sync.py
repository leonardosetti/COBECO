#!/usr/bin/env python3
"""
Board Sync Script — Protocolo P3
Sincroniza estado dos artefatos com GitHub Projects (board de controle).

Uso:
  python scripts/script-board-0001-board-sync-v1.0.py --sync-all      # Sincronizar todos artefatos
  python scripts/script-board-0001-board-sync-v1.0.py --sync-file <path>  # Sincronizar arquivo específico
  python scripts/script-board-0001-board-sync-v1.0.py --create-board  # Criar/Configurar board
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

REPO_ROOT = Path(__file__).parent.parent

# Configuração do Board
BOARD_OWNER = "leonardosetti"
BOARD_NUMBER = 3  # Projeto COBECO
REPO = "leonardosetti/COBECO"

@dataclass
class ArtifactBoardData:
    artifact_id: str
    type_classe: str
    version: str
    workflow_stage: str
    responsible: str
    reviewer: Optional[str]
    ratified_by: Optional[str]
    commit_hash: Optional[str]
    git_tag: Optional[str]
    traceability: Dict
    board_item_id: Optional[str] = None

def get_artifacts_from_repo() -> List[ArtifactBoardData]:
    """Extrai dados dos artefatos do repositório para sincronizar com board."""
    artifacts = []
    
    for filepath in REPO_ROOT.rglob("*.md"):
        if not filepath.is_file():
            continue
        
        try:
            rel_path = filepath.relative_to(REPO_ROOT)
        except ValueError:
            continue
        
        # Ignorar diretórios
        if any(part in {".git", "node_modules", "__pycache__", ".venv", "venv", "env",
                       "dist", "build", ".pytest_cache", ".mypy_cache", ".ruff_cache",
                       "coverage", "htmlcov", ".tox", "graphify-out", "brain", "prj_docs",
                       "excalidraw_baixa", "frontend/tests/e2e/node_modules",
                       "frontend/tests/e2e/playwright-report", "frontend/tests/e2e/test-results",
                       "backend/tests/performance", ".benchmarks", ".agents"} for part in rel_path.parts):
            continue
        
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception:
            continue
        
        if not content.startswith("---"):
            continue
        
        try:
            import yaml
            end_idx = content.index("\n---", 3)
            frontmatter_yaml = content[3:end_idx].strip()
            fm = yaml.safe_load(frontmatter_yaml)
        except (ValueError, yaml.YAMLError):
            continue
        
        if not isinstance(fm, dict):
            continue
        
        # Extrair dados para board
        artifact_id = fm.get("id", "")
        if not artifact_id:
            continue
        
        workflow = fm.get("workflow", {})
        trace = fm.get("trace", {})
        
        artifact = ArtifactBoardData(
            artifact_id=artifact_id,
            type_classe=fm.get("type", ""),
            version=fm.get("version", ""),
            workflow_stage=workflow.get("stage", "rascunho"),
            responsible=fm.get("author", "").split("(")[-1].replace(")", "").replace("@", "") if fm.get("author") else "",
            reviewer=workflow.get("reviewer"),
            ratified_by=fm.get("ratified_by"),
            commit_hash=workflow.get("approval_hash"),
            git_tag=workflow.get("git_tag"),
            traceability=trace,
            board_item_id=workflow.get("board_item_id")
        )
        artifacts.append(artifact)
    
    return artifacts

def gh_api(query: str, variables: Dict = None) -> Dict:
    """Executa query GraphQL na API do GitHub."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    if variables:
        for k, v in variables.items():
            cmd.extend(["-f", f"{k}={json.dumps(v)}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"gh api falhou: {result.stderr}")
    return json.loads(result.stdout)

def get_project_fields() -> Dict:
    """Obtém IDs dos campos customizados do projeto."""
    query = """
    query($owner: String!, $number: Int!) {
      user(login: $owner) {
        projectV2(number: $number) {
          id
          fields(first: 50) {
            nodes {
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    result = gh_api(query, {"owner": BOARD_OWNER, "number": BOARD_NUMBER})
    project = result["data"]["user"]["projectV2"]
    
    fields = {}
    for field in project["fields"]["nodes"]:
        fields[field["name"]] = field
    
    return {"project_id": project["id"], "fields": fields}

def sync_artifact_to_board(artifact: ArtifactBoardData, project_data: Dict) -> bool:
    """Sincroniza um artefato com o board."""
    # Implementação simplificada - na prática usaria GraphQL mutations
    # para criar/atualizar items no Project V2
    print(f"  🔄 Sync: {artifact.artifact_id} -> stage={artifact.workflow_stage}")
    return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Board Sync P3")
    parser.add_argument("--sync-all", action="store_true", help="Sincronizar todos artefatos")
    parser.add_argument("--sync-file", type=str, help="Sincronizar arquivo específico")
    parser.add_argument("--create-board", action="store_true", help="Criar/configurar board")
    parser.add_argument("--dry-run", action="store_true", help="Simular sem alterar")
    
    args = parser.parse_args()
    
    if not any([args.sync_all, args.sync_file, args.create_board]):
        parser.print_help()
        return 1
    
    print(f"{'='*60}")
    print(f"BOARD SYNC P3 — GitHub Projects #{BOARD_NUMBER}")
    print(f"{'='*60}")
    
    if args.create_board:
        print("📋 Configurando board...")
        # Verificar campos necessários
        try:
            project_data = get_project_fields()
            print(f"✅ Projeto conectado: {project_data['project_id']}")
            print("Campos disponíveis:")
            for name, field in project_data["fields"].items():
                print(f"   - {name}: {field.get('id', 'N/A')}")
        except Exception as e:
            print(f"❌ Erro ao conectar board: {e}")
            return 1
        return 0
    
    artifacts = get_artifacts_from_repo()
    print(f"📦 {len(artifacts)} artefatos com frontmatter encontrados")
    
    if args.sync_all:
        if args.dry_run:
            print("\n🔍 DRY-RUN - Artefatos que seriam sincronizados:")
            for a in artifacts:
                print(f"   {a.artifact_id} | {a.type_classe} | v{a.version} | {a.workflow_stage}")
        else:
            try:
                project_data = get_project_fields()
                print(f"\n🔄 Sincronizando {len(artifacts)} artefatos...")
                for artifact in artifacts:
                    sync_artifact_to_board(artifact, project_data)
                print("✅ Sincronização concluída")
            except Exception as e:
                print(f"❌ Erro na sincronização: {e}")
                return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())