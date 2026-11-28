#!/usr/bin/env python3
"""
Secret Scanner - Pre-commit Hook
Constitution Art. 7.7, 17.7: Bloqueia commit se segredos detectados em staged files.

Usage: python scripts/script-security-0001-secret-scan-v1.0.py
Exit codes: 0 = clean, 1 = secrets found
"""

import re
import subprocess
import sys
from pathlib import Path

# Padrões de segredos (regex compilados)
SECRET_PATTERNS = [
    # Arquivos de ambiente e segredos
    (r'config-env-0001-env-example-v1.0(\.local|\.prod|\.dev)?$', 'Arquivo config-env-0001-env-example-v1.0'),
    (r'secrets/', 'Diretório secrets/'),
    (r'\.pem$', 'Chave privada .pem'),
    (r'\.key$', 'Chave .key'),
    (r'\.secret$', 'Arquivo .secret'),
    (r'\.crt$', 'Certificado .crt'),
    
    # Padrões de conteúdo (AWS, GitHub, JWT, API Keys, etc.)
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
    (r'(?i)(aws[_\-]?secret[_\-]?access[_\-]?key|aws_secret_access_key)\s*[=:]\s*["\']?[a-zA-Z0-9/+=]{40}', 'AWS Secret Access Key'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
    (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
    (r'ghu_[a-zA-Z0-9]{36}', 'GitHub User Token'),
    (r'ghs_[a-zA-Z0-9]{36}', 'GitHub Server Token'),
    (r'ghr_[a-zA-Z0-9]{36}', 'GitHub Refresh Token'),
    (r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*', 'JWT Token'),
    (r'sk-[a-zA-Z0-9]{48}', 'OpenAI API Key'),
    (r'xoxb-[a-zA-Z0-9-]{50,}', 'Slack Bot Token'),
    (r'xoxp-[a-zA-Z0-9-]{50,}', 'Slack User Token'),
    (r'api_[a-zA-Z0-9]{32,}', 'Generic API Key'),
    (r'secret[_\-]?key[_\-]?[=:]\s*["\']?[a-zA-Z0-9+/=]{20,}', 'Secret Key Assignment'),
    (r'password[_\-]?[=:]\s*["\']?[a-zA-Z0-9!@#$%^&*()]{8,}', 'Password Assignment'),
    (r'PRIVATE KEY-----[\s\S]*?-----END PRIVATE KEY', 'Private Key Block'),
    (r'BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY', 'Private Key Header'),
]

# Arquivos/pastas a ignorar (allowlist)
IGNORE_PATHS = [
    '.git/',
    'node_modules/',
    '__pycache__/',
    '.venv/',
    'venv/',
    'env/',
    'dist/',
    'build/',
    '.pytest_cache/',
    '.mypy_cache/',
    '.ruff_cache/',
    'coverage/',
    'htmlcov/',
    '.tox/',
    '*.egg-info/',
    '*.pyc',
    '*.pyo',
    '*.so',
    'graphify-out/',
    'log_llama.txt',
    '*.bkp',
    '.DS_Store',
    'Thumbs.db',
    'docs/relatorios/',
    'doc-pre-0001-pre-documento-v1.0.md',
    'doc-figma-0001-figma-export-v1.0.html',
    'COBECO_prtp_high_v*.html',
    'COBECO_prtp_low_v*.excalidraw',
    'COBECO_prtp_low_v*.png',
    'der.drawio',
    'der.drawio.png',
    'doc-arch-0006-doc-arch-0006-uc-v1-v1.0',
    'doc-arch-0006-doc-arch-0006-uc-v1-v1.0.png',
    'doc-arch-0006-doc-arch-0006-uc-v1-v1.0.xml',
    'Projeto_COBECO.docx',
    # Template/example files (falsos positivos comuns)
    'config-env-0001-env-example-v1.0.example',
    'config-env-0001-env-example-v1.0.local',
    '*.example',
    '*.template',
    'TEMPLATE-*.md',
    'docs/operacao/TEMPLATE-*.md',
    'docs/strategy/TEMPLATE-*.md',
    'docs/decisoes/TEMPLATE-*.md',
    'docs/change/TEMPLATE-*.md',
    'docs/auditorias/TEMPLATE-*.md',
    'docs/rfc/TEMPLATE-*.md',
    'docs/arquitetura/TEMPLATE-*.md',
    'docs/operacao/doc-arch-0007-guia-arquitetural-v1.0.md',
    'docs/operacao/doc-arch-0008-guia-arquitetural-v2.0.md',
    'docs/operacao/doc-runbook-survey-0001-levantamento-runbooks-hooks-sanitizacao-v1.0.md',
    'docs/operacao/RELEASE-NOTES-*.md',
    'docs/strategy/user-stories/US-*.md',
    'scripts/script-security-0001-secret-scan-v1.0.py',  # Scanner itself contains patterns
    'doc-report-0002-macro-report-v1.0.md',
    'doc-report-0001-relatorio-analitico-v1.0.md',
    'doc-analysis-0001-analise-requisitos-casos-uso-v1.0.md',
    'doc-analysis-0002-analise-use-case-consistencia-v1.0.md',
]

# Extensões de arquivo a escanear (text-based)
SCAN_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.yaml', '.yml',
    '.md', '.txt', '.ini', '.cfg', '.conf', '.config',
    'config-env-0001-env-example-v1.0', 'config-env-0001-env-example-v1.0.example', 'config-env-0001-env-example-v1.0.local', 'config-env-0001-env-example-v1.0.prod', 'config-env-0001-env-example-v1.0.dev',
    '.sh', '.bash', '.zsh', '.fish',
    '.sql', '.db', '.sqlite',
    '.toml', '.ini', '.cfg',
    '.dockerfile', 'Dockerfile',
    '.gitignore', '.gitattributes',
    '.editorconfig',
    'config-make-0001-makefile-v1',
    'requirements.txt', 'requirements-dev.txt',
    'config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json', 'config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
}

# Padrões de arquivo a ignorar (binários, imagens, etc.)
IGNORE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar',
    '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
    '.ttf', '.woff', '.woff2', '.eot', '.otf',
    '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mov', '.mkv',
    '.pyc', '.pyo', '.pyd',
}


def get_staged_files() -> list[str]:
    """Retorna lista de arquivos staged para commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '-z'],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip('\x00').split('\x00')
        return [f for f in files if f]
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao obter staged files: {e}", file=sys.stderr)
        return []


def should_ignore_path(filepath: str) -> bool:
    """Verifica se caminho deve ser ignorado."""
    for pattern in IGNORE_PATHS:
        if pattern.endswith('/'):
            if filepath.startswith(pattern) or f'/{pattern}' in filepath:
                return True
        else:
            # Padrão de arquivo (glob simples)
            import fnmatch
            if fnmatch.fnmatch(filepath, pattern) or fnmatch.fnmatch(Path(filepath).name, pattern):
                return True
    return False


def should_scan_file(filepath: str) -> bool:
    """Verifica se arquivo deve ser escaneado."""
    if should_ignore_path(filepath):
        return False
    
    path = Path(filepath)
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return False
    
    # Se não tem extensão conhecida, tenta ler como texto
    if path.suffix.lower() not in SCAN_EXTENSIONS:
        # Verifica se é arquivo de texto tentando ler
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read(1024)
        except (UnicodeDecodeError, OSError):
            return False
    
    return True


def scan_file(filepath: str) -> list[tuple[str, str, int]]:
    """Escaneia arquivo por segredos. Retorna lista de (padrão, descrição, linha)."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, OSError):
        return findings
    
    for line_num, line in enumerate(lines, 1):
        for pattern, description in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((pattern, description, line_num))
    
    return findings


def main() -> int:
    print("🔍 Secret Scanner - Pre-commit Hook (Constitution Art. 7.7, 17.7)")
    print("=" * 60)
    
    staged_files = get_staged_files()
    if not staged_files:
        print("ℹ️  Nenhum arquivo staged para commit.")
        return 0
    
    print(f"📋 Arquivos staged: {len(staged_files)}")
    
    all_findings = []
    scanned_count = 0
    ignored_count = 0
    
    for filepath in staged_files:
        if not Path(filepath).exists():
            # Arquivo deletado no commit
            continue
            
        if should_ignore_path(filepath):
            ignored_count += 1
            continue
            
        if should_scan_file(filepath):
            scanned_count += 1
            findings = scan_file(filepath)
            if findings:
                all_findings.append((filepath, findings))
    
    print(f"📊 Escaneados: {scanned_count} | Ignorados (allowlist): {ignored_count}")
    print()
    
    if all_findings:
        print("🚨 SEGREDOS DETECTADOS - COMMIT BLOQUEADO (Constitution Art. 7.7, 17.7)")
        print("=" * 60)
        for filepath, findings in all_findings:
            print(f"\n📄 {filepath}:")
            for pattern, description, line_num in findings:
                print(f"   Line {line_num}: {description}")
                print(f"   Pattern: {pattern}")
        print("\n" + "=" * 60)
        print("🛑 AÇÃO NECESSÁRIA:")
        print("   1. Remova os segredos dos arquivos acima")
        print("   2. Use variáveis de ambiente (config-env-0001-env-example-v1.0) ou GitHub Secrets")
        print("   3. Se for falso positivo, adicione ao allowlist em secret_scan.py")
        print("   4. Para emergência: git commit --no-verify (NÃO RECOMENDADO)")
        return 1
    
    print("✅ Nenhum segredo detectado. Commit autorizado.")
    return 0


if __name__ == '__main__':
    sys.exit(main())