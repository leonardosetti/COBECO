---
id: ai-agents-ledger-deprecated-nota
title: Ledger operacional — corte de histórico deprecated
type: conhecimento
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/agents/ledger-deprecated-nota.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- agents
- docs
- adequado-a-norma
---
# Ledger operacional — corte de histórico deprecated

## Arquivos

| Arquivo | Conteúdo | Uso |
|---------|----------|-----|
| `.ai/agents/ledger.yaml` | Ledger operacional (13 entradas, TA-0100 → TA-0113) | Uso real: `ledger_read` / `ledger_append` via MCP `nexus-ledger` |
| `.ai/agents/ledger-historico-deprecated.yaml` | Histórico pré-saneamento (71 entradas, TA-0001 → TA-0065 + TA-DELEG-*) | **Deprecated**: apenas consulta de auditoria/traçabilidade temporal. **Descartado para uso operacional real.** |

## Critério de corte

- Entradas com `task_id` no padrão `TA-NNN` e `N >= 100` (a partir de TA-0100, 04/11/2026) permanecem no ledger operacional.
- Entradas anteriores a TA-0100, `task_id` fora do padrão (`TA-DELEG-*`) ou linhas soltas foram movidas para o histórico deprecated.

## Marcação no histórico

Cada entrada do arquivo deprecated carrega os campos:
- `deprecated: true`
- `motivo_descarte: "historico pre-saneamento — descartado para uso operacional real"`
- `arquivo_origem: "ledger.yaml (antes do saneamento de 05/11/2026)"`

## Regras operacionais (Constituição COBECO)

- Art. 4.10: `.ai/agents/ledger.yaml` é SSOT operacional para `current_session`, `audit_trail` e `blocked_tasks`. Modificação somente por script ou MCP validado (`scripts/mcp_nexus_ledger.py`).
- Art. 6.7: informação já processada e registrada não deve ser reprocessada sem necessidade; duplicação factual é violação de SSOT.
- O histórico deprecated é append-only e imutável: não é fonte de verdade para operações em andamento.
