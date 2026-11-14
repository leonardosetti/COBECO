---
id: config-ledger-0002-ledger-deprecated-nota-v1.0
type: config-ledger
title: CONFIG LEDGER — Ledger Deprecated Nota
version: v1.0
status: ratificado
canonical: false
canonical_slug: ledger-deprecated-nota
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: null
ratified_at: null
supersedes: null
superseded_by: null
trace:
  constitution: []
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []
domain: config
layer: config
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Ledger operacional — corte de histórico deprecated

## Arquivos

| Arquivo | Conteúdo | Uso |
|---------|----------|-----|
| `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` | Ledger operacional (13 entradas, TA-0100 → TA-0113) | Uso real: `ledger_read` / `ledger_append` via MCP `nexus-ledger` |
| `.ai/agents/config-ledger-0003-ledger-historico-deprecated-v1.0.yaml` | Histórico pré-saneamento (71 entradas, TA-0001 → TA-0065 + TA-DELEG-*) | **Deprecated**: apenas consulta de auditoria/traçabilidade temporal. **Descartado para uso operacional real.** |

## Critério de corte

- Entradas com `task_id` no padrão `TA-NNN` e `N >= 100` (a partir de TA-0100, 04/11/2026) permanecem no ledger operacional.
- Entradas anteriores a TA-0100, `task_id` fora do padrão (`TA-DELEG-*`) ou linhas soltas foram movidas para o histórico deprecated.

## Marcação no histórico

Cada entrada do arquivo deprecated carrega os campos:
- `deprecated: true`
- `motivo_descarte: "historico pre-saneamento — descartado para uso operacional real"`
- `arquivo_origem: "ledger.yaml (antes do saneamento de 05/11/2026)"`

## Regras operacionais (Constituição COBECO)

- Art. 4.10: `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` é SSOT operacional para `current_session`, `audit_trail` e `blocked_tasks`. Modificação somente por script ou MCP validado (`scripts/mcp_nexus_ledger.py`).
- Art. 6.7: informação já processada e registrada não deve ser reprocessada sem necessidade; duplicação factual é violação de SSOT.
- O histórico deprecated é append-only e imutável: não é fonte de verdade para operações em andamento.
