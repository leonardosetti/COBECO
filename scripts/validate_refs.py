#!/usr/bin/env python3
"""
Cross-Reference Validator - CI Gate
Constitution Art. 17.7, 17.8: Valida referências cruzadas em docs Markdown.

Verifica:
- docs/... (estrategia, arquitetura, operacao, change, decisoes, auditorias, rfc)
- .ai/specs/spec-*.spec.md
- .ai/handoffs/HF-*.md
- backend/src/..., frontend/...
- Links externos (GitHub, URLs) - apenas avisos

Usage: python scripts/validate_refs.py [--fix] [--ci]
Exit codes: 0 = clean, 1 = broken refs found, 2 = error
"""

import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


# Diretórios raiz do projeto
ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / 'docs'
AI_DIR = ROOT / '.ai'
BACKEND_DIR = ROOT / 'backend'
FRONTEND_DIR = ROOT / 'frontend'

# Padrões de referência interna válida
VALID_REF_PREFIXES = [
    'docs/',
    '.ai/specs/',
    '.ai/handoffs/',
    'backend/',
    'frontend/',
    'scripts/',
    'proxy/',
    'Makefile',
    'docker-compose',
    '.github/',
    'constitution.md',
    'board_roadmap.md',
    'REQUISITOS.md',
    'CASOSDEUSO.md',
    'CAMADADEDADOS.md',
    'GITHUB_PROJECTS.md',
    'AGENTS.md',
]

# Padrões de link markdown: [texto](caminho) ou [texto](caminho#ancora)
MD_LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Padrões de link wiki-style: [[caminho]] ou [[caminho|texto]]
WIKI_LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')

# Padrão para referências de issue/PR: #123, PR#123, Issue#123
ISSUE_REF_PATTERN = re.compile(r'(?:#|PR#|Issue#)(\d+)')

# Extensões de arquivo a escanear
SCAN_EXTENSIONS = {'.md', '.markdown', '.txt'}

# Arquivos/pastas a ignorar
IGNORE_PATHS = {
    'node_modules/', '.git/', '__pycache__/', '.venv/', 'venv/', 'env/',
    'dist/', 'build/', '.pytest_cache/', '.mypy_cache/', '.ruff_cache/',
    'coverage/', 'htmlcov/', '.tox/', '*.egg-info/', 'graphify-out/',
    '.DS_Store', 'Thumbs.db', 'log_llama.txt', '*.bkp',
    'pre_DOCUMENTO.md', 'COBECO_figma_export.html',
    'COBECO_prtp_high_v', 'COBECO_prtp_low_v',
    'der.drawio', 'uc.drawio', 'Projeto_COBECO.docx',
    'macro_report.md', 'relatorio_analitico_COBECO.md',
    'analise_REQ_CasosDeUso.md', 'analise-UseCase-consistencia.md',
    'frontend/node_modules/', 'frontend/tests/e2e/node_modules/',
    'backend/', '.ai/', '.agents/', '.opencode/',  # Will be handled by should_scan logic
}


class RefValidator:
    def __init__(self, fix_mode: bool = False, ci_mode: bool = False):
        self.fix_mode = fix_mode
        self.ci_mode = ci_mode
        self.errors: list[dict] = []
        self.warnings: list[dict] = []
        self.fixed_count = 0
        self.existing_files_cache: dict[str, bool] = {}
    
    def should_scan(self, filepath: Path) -> bool:
        """Verifica se arquivo deve ser escaneado."""
        if filepath.suffix.lower() not in SCAN_EXTENSIONS:
            return False
        for ignore in IGNORE_PATHS:
            if ignore.endswith('/'):
                if str(filepath).startswith(ignore) or f'/{ignore}' in str(filepath):
                    return False
            else:
                import fnmatch
                if fnmatch.fnmatch(filepath.name, ignore):
                    return False
        return True
    
    def file_exists(self, path: str) -> bool:
        """Verifica se arquivo existe (com cache)."""
        if path in self.existing_files_cache:
            return self.existing_files_cache[path]
        
        full_path = ROOT / path
        exists = full_path.exists()
        self.existing_files_cache[path] = exists
        return exists
    
    def resolve_ref(self, base_file: Path, ref: str) -> str | None:
        """Resolve referência relativa ao arquivo base."""
        # URL absoluta - ignora (validação externa opcional)
        if ref.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return None
        
        # Ancora apenas (#section) - válida no mesmo arquivo
        if ref.startswith('#'):
            return 'anchor'
        
        # Referência absoluta do projeto (docs/, .ai/, etc.)
        for prefix in VALID_REF_PREFIXES:
            if ref.startswith(prefix):
                return ref
        
        # Referência relativa - resolve relativo ao arquivo base
        base_dir = base_file.parent
        resolved = (base_dir / ref).resolve()
        
        # Verifica se está dentro do projeto
        try:
            resolved.relative_to(ROOT)
            return str(resolved.relative_to(ROOT))
        except ValueError:
            # Fora do projeto
            return None
    
    def validate_file(self, filepath: Path) -> None:
        """Valida referências em um arquivo."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            self.warnings.append({
                'file': str(filepath.relative_to(ROOT)),
                'type': 'read_error',
                'message': f'Não foi possível ler: {e}',
            })
            return
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Links markdown [texto](url)
            for match in MD_LINK_PATTERN.finditer(line):
                text, url = match.groups()
                self.check_link(filepath, line_num, text, url)
            
            # Wiki links [[path]] ou [[path|text]]
            for match in WIKI_LINK_PATTERN.finditer(line):
                self.check_wiki_link(filepath, line_num, match.group(1))
            
            # Referências a issues/PRs
            for match in ISSUE_REF_PATTERN.finditer(line):
                self.check_issue_ref(filepath, line_num, match.group(1))
    
    def check_link(self, filepath: Path, line_num: int, text: str, url: str) -> None:
        """Valida um link markdown."""
        # Ignora URLs externas (validação opcional)
        if url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            self.warnings.append({
                'file': str(filepath.relative_to(ROOT)),
                'line': line_num,
                'type': 'external_link',
                'message': f'Link externo: {url} (validação manual recomendada)',
            })
            return
        
        # Ignora ancoras
        if url.startswith('#'):
            return
        
        resolved = self.resolve_ref(filepath, url)
        if resolved is None:
            self.errors.append({
                'file': str(filepath.relative_to(ROOT)),
                'line': line_num,
                'type': 'broken_ref',
                'message': f'Referência inválida/fora do projeto: {url}',
                'text': text,
                'url': url,
            })
            return
        
        if resolved == 'anchor':
            return
        
        if not self.file_exists(resolved):
            self.errors.append({
                'file': str(filepath.relative_to(ROOT)),
                'line': line_num,
                'type': 'broken_ref',
                'message': f'Arquivo referenciado não existe: {resolved}',
                'text': text,
                'url': url,
                'resolved': resolved,
            })
    
    def check_wiki_link(self, filepath: Path, line_num: int, content: str) -> None:
        """Valida wiki-style link [[path]] ou [[path|text]]."""
        parts = content.split('|', 1)
        path = parts[0].strip()
        text = parts[1].strip() if len(parts) > 1 else path
        
        # Mesmo tratamento que link normal
        if path.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            self.warnings.append({
                'file': str(filepath.relative_to(ROOT)),
                'line': line_num,
                'type': 'external_wiki_link',
                'message': f'Wiki link externo: {path}',
            })
            return
        
        if path.startswith('#'):
            return
        
        resolved = self.resolve_ref(filepath, path)
        if resolved is None:
            self.errors.append({
                'file': str(filepath.relative_to(ROOT)),
                'line': line_num,
                'type': 'broken_wiki_ref',
                'message': f'Wiki referência inválida/fora do projeto: {path}',
                'text': text,
                'path': path,
            })
            return
        
        if resolved == 'anchor':
            return
        
        if not self.file_exists(resolved):
            self.errors.append({
                'file': str(filepath.relative_to(ROOT)),
                'line': line_num,
                'type': 'broken_wiki_ref',
                'message': f'Arquivo wiki referenciado não existe: {resolved}',
                'text': text,
                'path': path,
                'resolved': resolved,
            })
    
    def check_issue_ref(self, filepath: Path, line_num: int, issue_num: str) -> None:
        """Valida referência a issue/PR #123."""
        # No MVP, apenas avisa - validação real exigiria GitHub API
        self.warnings.append({
            'file': str(filepath.relative_to(ROOT)),
            'line': line_num,
            'type': 'issue_ref',
            'message': f'Referência a issue/PR #{issue_num} (validar manualmente no GitHub)',
        })
    
    def run(self) -> int:
        """Executa validação completa."""
        print("🔗 Cross-Reference Validator (Constitution Art. 17.7, 17.8)")
        print("=" * 60)
        
        # Coleta todos arquivos markdown
        md_files = []
        for ext in SCAN_EXTENSIONS:
            md_files.extend(ROOT.rglob(f'*{ext}'))
        
        md_files = [f for f in md_files if self.should_scan(f)]
        print(f"📋 Arquivos a validar: {len(md_files)}")
        
        for filepath in md_files:
            self.validate_file(filepath)
        
        # Relatório
        print()
        if self.errors:
            print(f"❌ ERROS ENCONTRADOS: {len(self.errors)}")
            print("=" * 60)
            for err in self.errors:
                print(f"📄 {err['file']}:{err['line']}")
                print(f"   {err['message']}")
                if 'resolved' in err:
                    print(f"   Resolved: {err['resolved']}")
                print()
        else:
            print("✅ Nenhuma referência quebrada encontrada.")
        
        if self.warnings:
            print(f"⚠️  AVISOS: {len(self.warnings)}")
            for warn in self.warnings[:10]:  # Limita display
                print(f"   {warn['file']}:{warn['line']} - {warn['message']}")
            if len(self.warnings) > 10:
                print(f"   ... e mais {len(self.warnings) - 10} avisos")
        
        print()
        if self.errors:
            print("🛑 VALIDAÇÃO FALHOU - Corrija as referências quebradas antes de merge.")
            return 1
        
        print("✅ VALIDAÇÃO PASSOU - Todas referências internas válidas.")
        return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Cross-Reference Validator')
    parser.add_argument('--fix', action='store_true', help='Tenta corrigir refs automaticamente (MVP: não implementado)')
    parser.add_argument('--ci', action='store_true', help='Modo CI (exit code 1 se erros)')
    args = parser.parse_args()
    
    validator = RefValidator(fix_mode=args.fix, ci_mode=args.ci)
    return validator.run()


if __name__ == '__main__':
    sys.exit(main())