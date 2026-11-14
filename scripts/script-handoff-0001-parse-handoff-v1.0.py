#!/usr/bin/env python3
"""
Handoff Parser - Parse .ai/handoffs/HF-*.md → metadata JSON
Constitution Art. 17.3, SDD flow: Parser para extração de metadata dos handoffs.

MVP: Extrai frontmatter YAML + seções conhecidas do markdown.
Suporta: task_id, spec_id, origin, wave, priority, assignee, deadline.

Usage: python scripts/script-handoff-0001-parse-handoff-v1.0.py <handoff_file.md>
       python scripts/script-handoff-0001-parse-handoff-v1.0.py --all  # Processa todos HF-*.md

Output: JSON para stdout (array de objetos ou objeto único)
Exit codes: 0 = sdoc-arch-0006-uc-v1cess, 1 = parse error, 2 = file not found
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# Regex para frontmatter YAML (entre --- ou +++)
FRONTMATTER_PATTERN = re.compile(
    r'^(?:---|\+\+\+)\s*\n(.*?)\n(?:---|\+\+\+)\s*\n',
    re.DOTALL | re.MULTILINE
)

# Campos esperados no frontmatter
EXPECTED_FIELDS = {
    'id': str,           # HF-NNNN
    'title': str,
    'version': str,
    'status': str,       # rascunho | processado | arquivado
    'date': str,         # ISO date
    'author': str,
    'origin': str,       # HF-NNNN (self-ref)
    'task': str,         # TA-NNNN
    'wave': str,         # WS-N
    'priority': str,     # P0/P1/P2
    'assignee': str,     # agent slug
    'deadline': str,     # ISO datetime
    'trace': list,       # rastreabilidade
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extrai frontmatter YAML e retorna (metadata, remaining_content)."""
    match = FRONTMATTER_PATTERN.search(content)
    if not match:
        return {}, content
    
    yaml_text = match.group(1)
    remaining = content[match.end():]
    
    # Parse YAML simples (sem PyYAML dependency no MVP)
    metadata = {}
    for line in yaml_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            # Tenta converter tipos
            if value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif re.match(r'^\d+\.\d+$', value):
                value = float(value)
            metadata[key] = value
    
    return metadata, remaining


def extract_sections(content: str) -> dict:
    """Extrai seções markdown conhecidas (## 1. Título, etc.)."""
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        # Detecta heading nível 2 ou 3
        heading_match = re.match(r'^(##+)\s+(.+)$', line)
        if heading_match:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = heading_match.group(2).strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def parse_handoff_file(filepath: Path) -> dict:
    """Parse um arquivo de handoff HF-*.md."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except FileNotFoundError:
        return {'error': f'File not found: {filepath}', 'file': str(filepath)}
    except Exception as e:
        return {'error': f'Read error: {e}', 'file': str(filepath)}
    
    # Extrai frontmatter
    metadata, remaining = parse_frontmatter(content)
    
    # Valida campos obrigatórios
    required = ['id', 'task', 'origin', 'wave']
    missing = [f for f in required if f not in metadata]
    if missing:
        metadata['_parse_warnings'] = [f'Missing required fields: {missing}']
    
    # Extrai seções do corpo
    sections = extract_sections(remaining)
    
    # Normaliza campos conhecidos
    result = {
        'file': str(filepath),
        'parsed_at': datetime.utcnow().isoformat() + 'Z',
        'metadata': metadata,
        'sections': sections,
    }
    
    # Adiciona campos derivados para compatibilidade SDD
    if 'id' in metadata:
        result['handoff_id'] = metadata['id']
    if 'task' in metadata:
        result['task_id'] = metadata['task']
    if 'origin' in metadata:
        result['origin_handoff'] = metadata['origin']
    if 'wave' in metadata:
        result['wave'] = metadata['wave']
    if 'spec_id' in metadata:
        result['spec_id'] = metadata['spec_id']
    elif 'spec' in metadata:
        result['spec_id'] = metadata['spec']
    
    return result


def parse_all_handoffs(handoffs_dir: Path = Path('.ai/handoffs')) -> list[dict]:
    """Parse todos arquivos HF-*.md no diretório."""
    if not handoffs_dir.exists():
        return [{'error': f'Directory not found: {handoffs_dir}'}]
    
    results = []
    for filepath in sorted(handoffs_dir.glob('HF-*.md')):
        if filepath.name in ('INDEX.md', 'TEMPLATE-HANDOFF.md'):
            continue
        results.append(parse_handoff_file(filepath))
    
    return results


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/script-handoff-0001-parse-handoff-v1.0.py <handoff_file.md>", file=sys.stderr)
        print("       python scripts/script-handoff-0001-parse-handoff-v1.0.py --all", file=sys.stderr)
        return 1
    
    if sys.argv[1] == '--all':
        results = parse_all_handoffs()
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    
    filepath = Path(sys.argv[1])
    result = parse_handoff_file(filepath)
    
    if 'error' in result:
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1 if 'not found' in result['error'].lower() else 2
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())