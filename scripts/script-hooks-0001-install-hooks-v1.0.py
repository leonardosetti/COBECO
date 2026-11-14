#!/usr/bin/env python3
"""
Hook Installer - Instala hooks Git (pre-commit, pre-push)
Constitution Art. 7.7, 9.9, 17.5, 17.7

Usage: python scripts/script-hooks-0001-install-hooks-v1.0.py [--force]
"""

import os
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
HOOKS_DIR = ROOT / '.git' / 'hooks'

PRE_COMMIT_CONTENT = '''#!/bin/bash
# Git pre-commit hook - Constitution Art. 7.7, 17.7
# Secret Scanner + Cross-ref quick check

set -e

echo "🔍 Pre-commit: Secret Scanner (Art. 7.7, 17.7)"
python scripts/script-security-0001-secret-scan-v1.0.py
SECRET_EXIT=$?

if [ $SECRET_EXIT -ne 0 ]; then
    echo "❌ Pre-commit bloqueado: segredos detectados"
    echo "   Use 'git commit --no-verify' APENAS em emergência (violates Constitution)"
    exit 1
fi

echo "✅ Pre-commit passed"
exit 0
'''

PRE_PUSH_CONTENT = '''#!/bin/bash
# Git pre-push hook - Constitution Art. 9.9, 17.5
# CI Green Check

set -e

# Protege branches principais
BRANCH=$(git branch --show-current)
PROTECTED_BRANCHES="main stage master"

for protected in $PROTECTED_BRANCHES; do
    if [ "$BRANCH" = "$protected" ]; then
        echo "🛡️  Branch protegida detectada: $BRANCH"
        echo "   Push direto bloqueado - use PR (Constitution Art. 6.3)"
        exit 1
    fi
done

echo "🟢 Pre-push: CI Green Check (Art. 9.9, 17.5)"
python scripts/script-ci-0001-ci-green-check-v1.0.py
CI_EXIT=$?

if [ $CI_EXIT -ne 0 ]; then
    echo "❌ Pre-push bloqueado: CI não está verde"
    echo "   Use 'git push --no-verify' APENAS em emergência (violates Constitution)"
    exit 1
fi

echo "✅ Pre-push passed"
exit 0
'''

COMMIT_MSG_CONTENT = '''#!/bin/bash
# Git commit-msg hook - Constitution Art. 9.3 (Conventional Commits)
# Valida formato: tipo(escopo): resumo imperativo

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Regex Conventional Commits: tipo(escopo): resumo
# Tipos: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
REGEX='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\([a-zA-Z0-9_-]+\))?: .+'

if ! echo "$COMMIT_MSG" | grep -qE "$REGEX"; then
    echo "❌ Commit message inválido (Constitution Art. 9.3)"
    echo "   Formato: tipo(escopo): resumo imperativo"
    echo "   Tipos: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    echo "   Exemplo: feat(auth): add JWT login endpoint"
    echo "   Seu commit: $COMMIT_MSG"
    exit 1
fi

# Verifica tamanho do resumo (máx 72 chars na primeira linha)
FIRST_LINE=$(echo "$COMMIT_MSG" | head -1)
if [ ${#FIRST_LINE} -gt 72 ]; then
    echo "⚠️  Resumo do commit > 72 chars (${#FIRST_LINE})"
    echo "   Recomendação: mantenha ≤ 72 chars"
fi

exit 0
'''


def write_hook(name: str, content: str) -> bool:
    """Escreve hook no .git/hooks/."""
    hook_path = HOOKS_DIR / name
    try:
        hook_path.write_text(content, encoding='utf-8')
        # Torna executável
        hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"✅ Hook instalado: {name}")
        return True
    except Exception as e:
        print(f"❌ Erro instalando {name}: {e}")
        return False


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Instala hooks Git (Constitution)')
    parser.add_argument('--force', action='store_true', help='Sobrescreve hooks existentes')
    args = parser.parse_args()
    
    print("🔧 Hook Installer - Constitution v2.0")
    print("=" * 50)
    
    if not HOOKS_DIR.exists():
        print(f"❌ Diretório .git/hooks não encontrado: {HOOKS_DIR}")
        return 1
    
    hooks = [
        ('pre-commit', PRE_COMMIT_CONTENT),
        ('pre-push', PRE_PUSH_CONTENT),
        ('commit-msg', COMMIT_MSG_CONTENT),
    ]
    
    sdoc-arch-0006-uc-v1cess = 0
    for name, content in hooks:
        hook_path = HOOKS_DIR / name
        if hook_path.exists() and not args.force:
            print(f"⚠️  {name} já existe (use --force para sobrescrever)")
            continue
        if write_hook(name, content):
            sdoc-arch-0006-uc-v1cess += 1
    
    print(f"\n✅ {sdoc-arch-0006-uc-v1cess}/{len(hooks)} hooks instalados")
    
    if sdoc-arch-0006-uc-v1cess > 0:
        print("\n📋 Hooks ativos:")
        print("   pre-commit:  Secret Scanner (Art. 7.7, 17.7)")
        print("   pre-push:    CI Green Check + Branch Protection (Art. 9.9, 17.5)")
        print("   commit-msg:  Conventional Commits (Art. 9.3)")
        print("\n⚠️  Para bypass de emergência: git commit --no-verify / git push --no-verify")
        print("   (VIOLA CONSTITUTION - USE APENAS EM EMERGÊNCIA REAL)")
    
    return 0 if sdoc-arch-0006-uc-v1cess > 0 else 1


if __name__ == '__main__':
    sys.exit(main())