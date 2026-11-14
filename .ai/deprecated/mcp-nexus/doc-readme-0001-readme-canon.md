---
id: doc-readme-0001-readme-canon
type: doc-readme
title: DOC README — Readme
version: '3.2'
status: ratificado
canonical: true
canonical_slug: readme
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:14863508
ratified_at: '2026-11-14'
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
domain: documentation
layer: documentation
tags: []
lgpd_class: n/a
workflow:
  stage: ratificado
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# MCP `nexus-*` — DESCONTINUADO / DEPRECATED

## Arquivos movidos para cá
- `mcp_nexus_ledger.py`
- `mcp_nexus_dispatch.py`
- `mcp_nexus_kb.py`
- `mcp_nexus_validate.py`
- `mcp_usage_log.py`

## Motivo
Zero calls reais nos agentes (apenas `initialize`/`tools/list` no log de uso). Cada um espelhava leitura/gravação de um único YAML local, substituível por chamada direta de stdlib. Classificado como bloat (ver análise prévia). Removidos do registro ativo em `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc`.

## ADR-017
Status alterado de `ratificado` para `deprecated`. Reativado somente quando provar-se necessário desenvolvimento de MCP nexus (refact/consolidação).

## Reativação
Mover os arquivos de volta para `scripts/` e re-registrar em `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` (blocos `nexus-*` sob `mcpServers` e `mcp.servers`).
