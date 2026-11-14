#!/usr/bin/env python3
"""
CI Green Check - Pre-push Hook
Constitution Art. 9.9, 17.5: Bloqueia push se último CI run não for verde.

Usage: python scripts/script-ci-0001-ci-green-check-v1.0.py
Exit codes: 0 = CI green, 1 = CI failed/pending, 2 = error
"""

import json
import subprocess
import sys
import time
from pathlib import Path

# Configurações
REQUIRED_WORKFLOWS = ['CI']  # Nomes dos workflows obrigatórios
MAX_WAIT_SECONDS = 300  # 5 min máximo para esperar CI completar
POLL_INTERVAL = 10  # Segundos entre polls


def run_cmd(cmd: list[str], capture: bool = True) -> subprocess.CompletedProcess:
    """Executa comando e retorna resultado."""
    return subprocess.run(cmd, capture_output=capture, text=True)


def get_current_branch() -> str:
    """Retorna nome do branch atual."""
    result = run_cmd(['git', 'branch', '--show-current'])
    return result.stdout.strip()


def get_remote_url() -> str:
    """Retorna URL do remote origin."""
    result = run_cmd(['git', 'remote', 'get-url', 'origin'])
    return result.stdout.strip()


def parse_github_repo(remote_url: str) -> tuple[str, str] | None:
    """Extrai owner/repo da URL do GitHub."""
    # SSH: git@github.com:owner/repo.git
    # HTTPS: https://github.com/owner/repo.git
    import re
    patterns = [
        r'git@github\.com:([^/]+)/(.+?)(?:\.git)?$',
        r'https://github\.com/([^/]+)/(.+?)(?:\.git)?$',
    ]
    for pattern in patterns:
        match = re.match(pattern, remote_url.strip())
        if match:
            return match.group(1), match.group(2)
    return None


def get_latest_workflow_runs(owner: str, repo: str, branch: str) -> list[dict]:
    """Busca últimos runs do workflow para o branch via gh CLI."""
    try:
        # gh api repos/{owner}/{repo}/actions/runs?branch={branch}&per_page=10
        result = run_cmd([
            'gh', 'api', f'repos/{owner}/{repo}/actions/runs',
            '-f', f'branch={branch}',
            '-f', 'per_page=20',
            '--jq', '.workflow_runs[] | {name: .name, status: .status, conclusion: .conclusion, created_at: .created_at, html_url: .html_url, head_sha: .head_sha}'
        ])
        
        if result.returncode != 0:
            print(f"❌ Erro gh api: {result.stderr}", file=sys.stderr)
            return []
        
        runs = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                runs.append(json.loads(line))
        return runs
    except Exception as e:
        print(f"❌ Erro ao buscar workflow runs: {e}", file=sys.stderr)
        return []


def check_required_workflows(runs: list[dict]) -> tuple[bool, list[str]]:
    """Verifica se todos workflows obrigatórios passaram."""
    # Agrupa por workflow name, pega o mais recente de cada
    latest_by_workflow = {}
    for run in runs:
        name = run.get('name', '')
        if name not in latest_by_workflow:
            latest_by_workflow[name] = run
    
    failed = []
    for required in REQUIRED_WORKFLOWS:
        # Match parcial (ex: "CI" matcha "CI / Build")
        matching = [r for n, r in latest_by_workflow.items() if required.lower() in n.lower()]
        if not matching:
            failed.append(f"{required}: NENHUM RUN ENCONTRADO")
            continue
        
        latest = matching[0]
        status = latest.get('status', '')
        conclusion = latest.get('conclusion', '')
        
        if status != 'completed':
            failed.append(f"{required}: EM ANDAMENTO ({status}) - {latest.get('html_url', '')}")
        elif conclusion != 'sdoc-arch-0006-uc-v1cess':
            failed.append(f"{required}: FALHOU ({conclusion}) - {latest.get('html_url', '')}")
    
    return len(failed) == 0, failed


def wait_for_workflows(owner: str, repo: str, branch: str, timeout: int) -> tuple[bool, list[str]]:
    """Aguarda workflows completarem com timeout."""
    print(f"⏳ Aguardando CI completar (timeout: {timeout}s)...")
    start = time.time()
    
    while time.time() - start < timeout:
        runs = get_latest_workflow_runs(owner, repo, branch)
        if not runs:
            print("   Nenhum run encontrado, aguardando...")
            time.sleep(POLL_INTERVAL)
            continue
        
        # Verifica se há runs pendentes para workflows obrigatórios
        pending = False
        for required in REQUIRED_WORKFLOWS:
            matching = [r for r in runs if required.lower() in r.get('name', '').lower()]
            if matching:
                latest = matching[0]
                if latest.get('status') != 'completed':
                    pending = True
                    break
        
        if not pending:
            return check_required_workflows(runs)
        
        elapsed = int(time.time() - start)
        print(f"   CI em andamento... ({elapsed}s/{timeout}s)")
        time.sleep(POLL_INTERVAL)
    
    print(f"⏰ Timeout ({timeout}s) aguardando CI")
    return False, [f"Timeout aguardando CI completar ({timeout}s)"]


def main() -> int:
    print("🟢 CI Green Check - Pre-push Hook (Constitution Art. 9.9, 17.5)")
    print("=" * 60)
    
    # Verifica se gh CLI está disponível
    if run_cmd(['which', 'gh']).returncode != 0:
        print("❌ gh CLI não encontrado. Instale: https://cli.github.com/", file=sys.stderr)
        return 2
    
    # Verifica autenticação gh
    if run_cmd(['gh', 'auth', 'status']).returncode != 0:
        print("❌ gh CLI não autenticado. Execute: gh auth login", file=sys.stderr)
        return 2
    
    branch = get_current_branch()
    print(f"🌿 Branch atual: {branch}")
    
    # Protege branches principais
    protected_branches = ['main', 'stage', 'master']
    if branch in protected_branches:
        print(f"🛡️  Branch protegida detectada: {branch}")
        print("   Push direto bloqueado - use PR (Constitution Art. 6.3)")
        return 1
    
    remote_url = get_remote_url()
    repo_info = parse_github_repo(remote_url)
    if not repo_info:
        print(f"❌ Não foi possível parsear remote: {remote_url}", file=sys.stderr)
        return 2
    
    owner, repo = repo_info
    print(f"📦 Repositório: {owner}/{repo}")
    
    # Busca runs atuais
    runs = get_latest_workflow_runs(owner, repo, branch)
    
    if not runs:
        print("⚠️  Nenhum workflow run encontrado para este branch")
        print("   Verifique se CI foi triggerado (.github/workflows/config-ci-0001-github-actions-v1.0.yml)")
        return 1
    
    sdoc-arch-0006-uc-v1cess, failed = check_required_workflows(runs)
    
    if sdoc-arch-0006-uc-v1cess:
        print("✅ Todos workflows obrigatórios passaram (verde). Push autorizado.")
        return 0
    
    print("❌ Workflows obrigatórios NÃO passaram:")
    for msg in failed:
        print(f"   - {msg}")
    
    # Verifica se há runs pendentes que podem completar
    has_pending = any(
        r.get('status') != 'completed' 
        for r in runs 
        if any(req.lower() in r.get('name', '').lower() for req in REQUIRED_WORKFLOWS)
    )
    
    if has_pending:
        print(f"\n⏳ Há workflows pendentes. Aguardando completar (max {MAX_WAIT_SECONDS}s)...")
        print("   Pressione Ctrl+C para cancelar e push manual (git push --no-verify)")
        sdoc-arch-0006-uc-v1cess, failed = wait_for_workflows(owner, repo, branch, MAX_WAIT_SECONDS)
        if sdoc-arch-0006-uc-v1cess:
            print("✅ CI completou com sdoc-arch-0006-uc-v1esso durante a espera. Push autorizado.")
            return 0
    
    print("\n" + "=" * 60)
    print("🛑 PUSH BLOQUEADO - CI não está verde (Constitution Art. 9.9, 17.5)")
    print("=" * 60)
    print("OPÇÕES:")
    print("  1. Aguarde CI completar e tente novamente")
    print("  2. Corrija falhas no CI e re-push")
    print("  3. EMERGÊNCIA: git push --no-verify (NÃO RECOMENDADO - viola Constitution)")
    return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⏹️  Cancelado pelo usuário.")
        sys.exit(130)