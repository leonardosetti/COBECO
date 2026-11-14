---
id: doc-mcp-0001-inventario-v1.0
type: doc-mcp
title: DOC MCP — Inventario
version: v1.0
status: ratificado
canonical: false
canonical_slug: inventario
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
domain: specs
layer: spec
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Inventário de MCPs — COBECO

Status: ratificado e promulgado (CCB/GP)
Domínio de controle: `.ai/mcp/` (escopo local do projeto COBECO)
Única fonte de verdade de configuração: `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` (bloco `mcpServers`)

## Princípio de escopo

**Escopo LOCAL (projeto).** Todos os servidores MCP são provisionados dentro do repositório COBECO, com configuração em `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` e servidores residentes em `scripts/mcp_*.py` (locais) ou pacotes npx oficiais (filesystem, github-remote). Nenhum servidor requer instalação global. Nenhum depende de credencial global de máquina.

Exceção: `github-remote` requer `GITHUB_TOKEN` do ambiente de execução (variável de ambiente, não versão no repo). É mantido como opcional/externo porque o modelo de governo do COBECO proíbe dependência de cloud como requisito (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 4, soberania de dados).

## Servidores ratificados

| Nome | Comando | Transporte | Rede | Domínio | Versão reportada | Status |
|---|---|---|---|---|---|---|
| nexus-ledger | `python3 scripts/mcp_nexus_ledger.py` | stdio | não | local | 0.1.0 | ativo |
| nexus-dispatch | `python3 scripts/mcp_nexus_dispatch.py` | stdio | não | local | 0.1.0 | ativo |
| nexus-kb | `python3 scripts/mcp_nexus_kb.py` | stdio | não | local | 0.1.0 | ativo |
| nexus-validate | `python3 scripts/mcp_nexus_validate.py` | stdio | não | local | 0.1.0 | ativo |
| filesystem | `npx -y @modelcontextprotocol/server-filesystem --allow-read ...` | stdio | não | local (npx cache) | 2.1.0 | ativo |
| github-remote | `npx -y @modelcontextprotocol/server-github` | stdio | sim (GitHub API) | remoto | 0.6.2 | ativo (opcional) |

## Artefatos de controle

- `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` — bloco `mcpServers` (única fonte de verdade consumida pelo OpenCode).
- `.ai/mcp/doc-mcp-0002-ratificacao-ccb-v1.0.md` — ratificação formal CCB/GP deste inventário.
- `.ai/mcp/ledge_mcp.yaml` (gerado por nexus-ledger) — trilha de auditoria das operações MCP (se aplicável).

## Novos MCPs

Qualquer novo servidor MCP deve ser adicionado ao bloco `mcpServers` de `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc`, ter script local equivalente em `scripts/mcp_*.py` quando aplicável, e ser ratificado via CCB/GP antes de entrar em produção.
