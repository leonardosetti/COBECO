#!/usr/bin/env python3
"""
Nexus Dispatcher - L0 Agent Dispatcher (STUB MVP)
Constitution Art. 17.3: Dispatch via L0 (scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py).

MVP: Recebe handoff JSON, valida schema mínimo, loga dispatch,
retorna dod + kill_switch para compatibilidade SDD flow.

Usage: python scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py <handoff_file.json>
       echo '{"task_id":"TA-001","spec_id":"spec-004"}' | python scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py

Exit codes: 0 = dispatched, 1 = validation error, 2 = dispatch error
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


# Schema mínimo obrigatório no handoff
REQUIRED_FIELDS = [
    'task_id',      # Ex: TA-001
    'spec_id',      # Ex: spec-004
    'origin',       # Ex: HF-0500
    'wave',         # Ex: WS-1
]

OPTIONAL_FIELDS = [
    'priority',     # P0/P1/P2
    'assignee',     # agent slug
    'context',      # dict adicional
    'deadline',     # ISO datetime
]


def validate_handoff(handoff: dict) -> tuple[bool, list[str]]:
    """Valida handoff contra schema mínimo."""
    errors = []
    
    for field in REQUIRED_FIELDS:
        if field not in handoff:
            errors.append(f"Campo obrigatório ausente: {field}")
        elif not handoff[field]:
            errors.append(f"Campo obrigatório vazio: {field}")
    
    # Valida formato task_id (TA-NNNN)
    if 'task_id' in handoff:
        import re
        if not re.match(r'^TA-\d{4}$', handoff['task_id']):
            errors.append(f"task_id formato inválido: {handoff['task_id']} (esperado TA-NNNN)")
    
    # Valida formato spec_id (spec-NNN-...)
    if 'spec_id' in handoff:
        import re
        if not re.match(r'^spec-\d{3}-', handoff['spec_id']):
            errors.append(f"spec_id formato inválido: {handoff['spec_id']} (esperado spec-NNN-...)")
    
    # Valida formato origin (HF-NNNN)
    if 'origin' in handoff:
        import re
        if not re.match(r'^HF-\d{4}$', handoff['origin']):
            errors.append(f"origin formato inválido: {handoff['origin']} (esperado HF-NNNN)")
    
    # Valida formato wave (WS-N)
    if 'wave' in handoff:
        import re
        if not re.match(r'^WS-\d+$', handoff['wave']):
            errors.append(f"wave formato inválido: {handoff['wave']} (esperado WS-N)")
    
    return len(errors) == 0, errors


def log_dispatch(handoff: dict, dispatch_id: str, result: dict) -> None:
    """Loga dispatch em arquivo JSONL para auditoria."""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'dispatch_id': dispatch_id,
        'handoff': handoff,
        'result': result,
    }
    
    log_path = Path('.ai/handoffs/dispatch_log.jsonl')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


def dispatch_to_l0(handoff: dict) -> dict:
    """
    STUB MVP: Simula dispatch para L0 agent.
    Em produção, aqui chamaria o agent L0 real via HTTP/CLI/IPC.
    """
    task_id = handoff.get('task_id', 'UNKNOWN')
    spec_id = handoff.get('spec_id', 'UNKNOWN')
    
    # Simula processamento
    print(f"🚀 [L0 Dispatcher] Dispatching task {task_id} for spec {spec_id}")
    print(f"   Origin: {handoff.get('origin')}")
    print(f"   Wave: {handoff.get('wave')}")
    print(f"   Priority: {handoff.get('priority', 'P1')}")
    
    # TODO: Integração real com L0 agent
    # response = requests.post('http://localhost:8080/dispatch', json=handoff)
    # return response.json()
    
    # MVP: Retorna sucesso simulado
    return {
        'status': 'dispatched',
        'dispatched_at': datetime.utcnow().isoformat() + 'Z',
        'agent': 'l0-nexus-prime-ultimate',
        'estimated_duration_seconds': 300,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py <handoff_file.json>", file=sys.stderr)
        print("       echo '{\"task_id\":\"TA-001\",\"spec_id\":\"spec-004\",...}' | python scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py", file=sys.stderr)
        return 1
    
    input_source = sys.argv[1]
    
    try:
        if input_source == '-':
            # Read from stdin
            handoff = json.load(sys.stdin)
        else:
            # Read from file
            with open(input_source, 'r', encoding='utf-8') as f:
                handoff = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {input_source}", file=sys.stderr)
        return 1
    
    # Valida handoff
    valid, errors = validate_handoff(handoff)
    if not valid:
        print("❌ Handoff validation failed:", file=sys.stderr)
        for err in errors:
            print(f"   - {err}", file=sys.stderr)
        return 1
    
    # Gera dispatch ID
    dispatch_id = f"DISP-{uuid.uuid4().hex[:8].upper()}"
    
    # Dispatch para L0
    try:
        l0_result = dispatch_to_l0(handoff)
    except Exception as e:
        print(f"❌ Dispatch error: {e}", file=sys.stderr)
        result = {
            'status': 'error',
            'error': str(e),
            'dod': False,
            'kill_switch': 'activated',
        }
        log_dispatch(handoff, dispatch_id, result)
        return 2
    
    # Resultado final com dod + kill_switch (Constitution Art. 17.3)
    result = {
        'status': 'success',
        'dispatch_id': dispatch_id,
        'task_id': handoff['task_id'],
        'spec_id': handoff['spec_id'],
        'l0_result': l0_result,
        'dod': True,                    # Definition of Done - dispatch completo
        'kill_switch': 'screened',      # Kill switch screened (não ativado)
    }
    
    # Log para auditoria
    log_dispatch(handoff, dispatch_id, result)
    
    # Output JSON para consumo por scripts
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0


if __name__ == '__main__':
    sys.exit(main())