---
id: ai-deprecated-mcp-nexus-readme
title: MCP `nexus-*` — DESCONTINUADO / DEPRECATED
type: readme
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/deprecated/mcp-nexus/doc-readme-0001-readme-canon.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- mcp-nexus
- docs
- adequado-a-norma
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
