---
id: doc-mcp-0002-ratificacao-ccb-v1.0
type: doc-mcp
title: DOC MCP — Ratificacao Ccb
version: v1.0
status: ratificado
canonical: false
canonical_slug: ratificacao-ccb
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
# Ratificação e Promulgação de MCPs — CCB/GP

## Identidade
- Projeto: COBECO
- Domínio de controle: `.ai/mcp/` (escopo local)
- Única fonte de verdade: `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` (bloco `mcpServers`)
- Instrumento de ratificação: presente documento (CCB/GP)

## Decisão de escopo

**Preferência: escopo LOCAL (projeto).**

Justificativas:
1. Soberania de dados e ausência de dependência de cloud (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 4, princípio FOSS-first).
2. Todos os artefatos de controle MCP sob mesmo domínio (repositório COBECO): configuração em `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc`, servidores em `scripts/mcp_*.py`, inventário em `.ai/mcp/`.
3. Caminhos relativos funcionam com `cwd` = raiz do projeto; não há dependência de caminhos absolutos de máquina (exceto `github-remote`, opcional).
4. Nenhum servidor requer instalação global; provisionamento via `python3` (stdlib) ou `npx -y` de pacotes oficiais do `@modelcontextprotocol`.
5. `github-remote` é exceção controlada: requer `GITHUB_TOKEN` do ambiente de execução (variável de ambiente, não versionada), mantido como opcional/externo.

Escopo global foi rejeitado porque acopla servidores a uma máquina/usuário específico, espalha artefatos fora do domínio do projeto e viola o princípio de soberania local.

## Servidores ratificados e promulgados

| Nome | Arquivo de servidor | Escopo | Rede | Aval CCB/GP |
|---|---|---|---|---|
| nexus-ledger | `scripts/mcp_nexus_ledger.py` | local | não | ratificado |
| nexus-dispatch | `scripts/mcp_nexus_dispatch.py` | local | não | ratificado |
| nexus-kb | `scripts/mcp_nexus_kb.py` | local | não | ratificado |
| nexus-validate | `scripts/mcp_nexus_validate.py` | local | não | ratificado |
| filesystem | `@modelcontextprotocol/server-filesystem` (npx) | local | não | ratificado |
| github-remote | `@modelcontextprotocol/server-github` (npx) | remoto (opcional) | sim | ratificado (condicional a `GITHUB_TOKEN`) |

## Verificação de ativação

Cada servidor foi submetido a handshake MCP `initialize` (protocolVersion `2024-11-05`) e respondeu com `serverInfo` e `capabilities.tools` presentes. Todos ativos.

## Co-assinatura (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 5.4)

| Campo | Valor |
|---|---|
| Versão do instrumento | 1.0.0 |
| Data | 2026-11-04 |
| Papel do ratificador humano | Gerente de Projeto — CCB de membro único |
| Instrumento de ratificação | Promulgação expressa do CCB (presente documento) |
| SHA-256 do conteúdo normativo | (a calcular sobre `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` e `.ai/mcp/` excluindo este bloco) |
| Hash do commit Git | (a preencher no commit de fechamento) |
| Status | VIGENTE-PLENA |

## Obrigações contínuas

- Qualquer adição, remoção ou mudança de servidor MCP requer nova ratificação CCB/GP e atualização deste instrumento.
- `nexus-validate` deve ser executado periodicamente para validar sintaxe dos servidores `scripts/mcp_*.py`.
- `github-remote` só é considerado ativo quando `GITHUB_TOKEN` está presente no ambiente de execução.
