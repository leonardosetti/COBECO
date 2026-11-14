#!/bin/bash
# sdd-cycle.sh v2 — Ciclo SDD canônico com dispatch validado (FASE S.7)
# Fundamentação: constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 6.1 + Glossário §5 + ADR-006 + Runbook SDD v1.1
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
if ! python3 scripts/script-handoff-0001-parse-handoff-v1.0.py "$HANDOFF_PATH" > /tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/handoff_payload.json; then
  echo "Erro: handoff rejeitado pelo parser (scripts/script-handoff-0001-parse-handoff-v1.0.py)."
  echo "Verifique id/agent/status/critérios e re-promulgue."
  exit 1
fi
echo "✓ Handoff parseado: $(wc -c < /tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/handoff_payload.json) bytes de payload"

# 3. Extrair alvo e construir envelope de dispatch (S.4)
TARGET=$(python3 -c "import json;d=json.load(open('/tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/handoff_payload.json'));h=d['handoffs'][0];print(h.get('meta',{}).get('agent',''))" 2>/dev/null || true)
if [ -z "$TARGET" ]; then
  echo "Erro: handoff sem campo 'agent' parseável."
  exit 1
fi

python3 - "$TARGET" "$HANDOFF" <<'PY' > /tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/dispatch_envelope.json
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
if ! python3 scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py --check /tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/dispatch_envelope.json; then
  echo "Erro: dispatch rejeitado (scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py)."
  echo "Causas prováveis: alvo não promulgado no roster (.ai/agents/config-registry-0001-registry-v1.0.yaml) ou fora da DAG."
  echo "Rode: python3 scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py --report"
  exit 1
fi
echo "✓ Dispatch validado: ${TARGET}"

# 5. Trocar persona ativa (symlink runtime)
ln -sf "${PERSONA}.md" .ai/personas/active.md
echo "✓ Persona ativa: ${PERSONA}"

# 6. Executar OpenCode não-interativo com o payload do handoff
PAYLOAD=$(cat "$HANDOFF_PATH")
echo "✓ Executando handoff ${HANDOFF}..."
config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0 run "${PAYLOAD}" --agent "${PERSONA}"

echo "✓ Ciclo SDD v2 concluído. Comitar artefatos gerados com co-autoria."
