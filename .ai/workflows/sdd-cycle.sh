#!/bin/bash
# sdd-cycle.sh v2 — Ciclo SDD canônico com dispatch validado (FASE S.7)
# Fundamentação: constitution.md Art. 6.1 + Glossário §5 + ADR-006 + Runbook SDD v1.1
# Pipeline: handoff → parser (S.2) → dispatcher (S.4) → orchestrator → agente

set -euo pipefail

PERSONA=${1:-"coder"}
HANDOFF=${2:-"000-smoke-test.md"}
HANDOFF_PATH=".ai/handoffs/${HANDOFF}"

# 1. Validar pré-requisitos
if [ ! -f "$HANDOFF_PATH" ]; then
  echo "Erro: handoff ${HANDOFF_PATH} não encontrado."
  exit 1
fi

if ! curl -s http://127.0.0.1:8080/health | grep -q "ok"; then
  echo "Erro: llama-server inativo na porta 8080."
  echo "Ação: sudo systemctl start llama-server"
  exit 1
fi

# 2. Parse do handoff (S.2) — fail-closed: handoff malformado aborta o ciclo
if ! python3 scripts/handoff_parser.py "$HANDOFF_PATH" > /tmp/opencode/handoff_payload.json; then
  echo "Erro: handoff rejeitado pelo parser (scripts/handoff_parser.py)."
  echo "Verifique id/agent/status/critérios e re-promulgue."
  exit 1
fi
echo "✓ Handoff parseado: $(wc -c < /tmp/opencode/handoff_payload.json) bytes de payload"

# 3. Extrair alvo e construir envelope de dispatch (S.4)
TARGET=$(python3 -c "import json;d=json.load(open('/tmp/opencode/handoff_payload.json'));h=d['handoffs'][0];print(h.get('meta',{}).get('agent',''))" 2>/dev/null || true)
if [ -z "$TARGET" ]; then
  echo "Erro: handoff sem campo 'agent' parseável."
  exit 1
fi

python3 - "$TARGET" "$HANDOFF" <<'PY' > /tmp/opencode/dispatch_envelope.json
import json, sys
target, handoff = sys.argv[1], sys.argv[2]
print(json.dumps({
    "task_id": "TA-" + handoff.split(".")[0].replace("HF-", "").zfill(3),
    "sender": "agent-orchestrator",
    "target": target,
    "action": "dispatch",
    "handoff": handoff.replace(".md", ""),
}))
PY

# 4. Gate do dispatcher — fail-closed
if ! python3 scripts/nexus_dispatcher.py --check /tmp/opencode/dispatch_envelope.json; then
  echo "Erro: dispatch rejeitado (scripts/nexus_dispatcher.py)."
  echo "Causas prováveis: alvo não promulgado no roster (.ai/agents/registry.yaml) ou fora da DAG."
  echo "Rode: python3 scripts/nexus_dispatcher.py --report"
  exit 1
fi
echo "✓ Dispatch validado: ${TARGET}"

# 5. Trocar persona ativa (symlink runtime)
ln -sf "${PERSONA}.md" .ai/personas/active.md
echo "✓ Persona ativa: ${PERSONA}"

# 6. Executar OpenCode não-interativo com o payload do handoff
PAYLOAD=$(cat "$HANDOFF_PATH")
echo "✓ Executando handoff ${HANDOFF}..."
opencode run "${PAYLOAD}" --agent "${PERSONA}"

echo "✓ Ciclo SDD v2 concluído. Comitar artefatos gerados com co-autoria."
