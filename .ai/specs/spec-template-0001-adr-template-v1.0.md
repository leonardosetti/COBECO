---
id: spec-template-0001-adr-template-v1.0
type: spec-template
title: SPEC TEMPLATE — Adr Template
version: v1.0
status: ratificado
canonical: false
canonical_slug: adr-template
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
# Template Canônico de ADR — COBECO

Este template é a **norma de template para ADRs** do projeto COBECO. Toda ADR nova ou emendada deve seguir esta estrutura. Não criar nova ADR sobrepondo regras de ADR anterior; usar emenda de versão (ADR-LOG).

## 1. Nomenclatura do arquivo (ADR-018)

`decisoes-adr-NNN-nome_artefato.md`

- `tipo_artefato` = `decisoes` (pasta `docs/decisoes/`)
- `id_artefato` = `adr-NNN` (ex.: `adr-001`, `adr-016`)
- `nome_artefato` = slug EN, kebab-case, descritivo curto (ex.: `stack`, `kanban`, `metricas`, `regime-tap`)
- Extensão: `.md`

## 2. Frontmatter YAML (obrigatório, único bloco)

Campos na ordem:

| Campo | Tipo | Obrigatório | Exemplo |
|-------|------|-------------|---------|
| `id` | slug | sim | `decisoes-adr-001-stack` |
| `title` | string | sim | `ADR-001 — Stack Tecnológica FOSS` |
| `version` | semver | sim | `1.1.0` |
| `class` | enum | sim | `decisao-adr` |
| `status` | enum | sim | `draft\|ratificado\|active\|supersedida\|deprecated\|obsoleto` |
| `owner` | slug | sim | `agent-project-analyst` |
| `derived-from` | lista | sim | `docs/decisoes/adr-001-stack.md (normalizado em 2026-11-05)` |
| `last-revised` | date | sim | `2026-11-05` |
| `lgpd-class` | string | sim | `n/a` |
| `tags` | lista | sim | `- decisoes\n- docs` |
| `data-decisao` | date | sim | `19/09/2026` |
| `data-formalizacao` | date | sim | `28/10/2026` |
| `decisor` | string | sim | `GP Leonardo (CCB único)` |
| `instrumento-ccb` | string | não | `RAT-2026-10-31-A13` |
| `gatilhos` | texto | sim | `G1, G3, G4` |
| `rastreabilidade` | texto | sim | `TAP §X; EAP Nx; REQ-xx; ADR-0xx` |
| `dominio-pmbok` | texto | sim | `Trabalho do Projeto + Abordagem de Desenvolvimento` |
| `processo-pmbok-6` | texto | não | `4.6` |
| `supersede` | slug | não | `decisoes-adr-010-stack-infraestrutura` |
| `superseded-by` | slug | não | `decisoes-adr-001-stack` |
| `kill-switch` | texto | sim | `screened` ou vetores aplicáveis |

## 3. Estrutura do corpo (obrigatório, nesta ordem)

### 3.1 Tabela de metadados (logo após o frontmatter)

```
| Campo | Valor |
|-------|-------|
| Versão | 1.1.0 |
| Status | Ratificado |
| Data da decisão | 19/09/2026 |
| Data de formalização | 28/10/2026 |
| Decisor | GP Leonardo (CCB único) |
| Gatilhos G1–G4 | G1, G3, G4 |
| Rastreabilidade | TAP §3; EAP N4.1; REQ-12 |
| Domínio PMBOK 7ª | ... |
| Processo PMBOK 6ª | ... |
```

### 3.2 Contexto
### 3.3 Decisão
### 3.4 Alternativas Consideradas (tabela, quando houver ≥ 2 opções)
### 3.5 Consequências e Trade-offs (positivas / negativas e riscos / fallback / trade-offs aceitos)
### 3.6 Sobreposição de Decisões (tabela: ADR sobreposta, Natureza, Motivo, Domínio PMBOK 7ª, Data) — omitir se nenhuma
### 3.7 kill_switch (ou `Não aplicável diretamente.`)
### 3.8 Governança (custódia, emenda, auditoria)
### 3.9 Histórico (tabela: Versão, Data, Autor, Mudança)
### 3.10 Ratificação (instrumento CCB, data, status) — omitir se ainda não ratificada
### 3.11 Referências (lista de links a arquivos canônicos)

## 4. Regras de cross-reference

- Citar sempre com versão pinada: `[ADR-010 v1.0.0](docs/decisoes/adr-010-stack-infraestrutura.md)`
- Nunca citar `docs/archive/` como fonte viva
- Versão desconhecida → `UNKNOWN-GAP`, não omitir
- Um fato = um local; não duplicar texto de outra ADR, usar cross-reference

## 5. Ratificação e promulgação

Somente após revisão deste template e do corpo, a ADR é submetida ao CCB (GP Leonardo) para ratificação via instrumento `RAT-YYYY-MM-DD-A##`, com registro em `docs/decisoes/adr-log.md` e `docs/governanca/ccb-log.md`.