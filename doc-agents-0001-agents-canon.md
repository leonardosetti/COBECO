---
# === IDENTIFICAÇÃO UNIVERSAL ===
id: "doc-agents-0001-agents-canon"
type: "doc-agents"
title: "DOC AGENTS — Agents"
version: "3.2"
status: "ratificado"
canonical: true
canonical_slug: "agents"

# === METADADOS DE GOVERNANÇA ===
created: "2026-11-14"
updated: "2026-11-14"
author: "Leonardo Setti (@leonardosetti)"
owner: "CCB"
ratified_by: "gh-sig:owner:leonardosetti:14863508"
ratified_at: "2026-11-14"
supersedes: null
superseded_by: null

# === RASTREABILIDADE (SSOT) ===
trace:
  constitution: ""
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []

# === CLASSIFICAÇÃO ===
domain: "documentation"
layer: "documentation"
tags: []
lgpd_class: "n/a"

# === WORKFLOW STATUS (P3) ===
workflow:
  stage: "ratificado"
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# COBECO — doc-agents-0001-agents-canon.md

## Repo state: código publicado, Constitution v2.0 vigente

O repositório está publicado em `git@github.com:leonardosetti/COBECO.git` (branch `main`, commit `8e2d295`).
Aplicação completa: backend FastAPI, frontend Vanilla JS + Tailwind, nginx proxy, Docker Compose,
seed SQL, Alembic, CI GitHub Actions, specs SDD, Constitution v2.0.

Não assumir "docs only" — todo o scaffold do MVP já existe e está versionado.

## Lei suprema

`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` v2.0 é a lei suprema do repositório (SSOT normativo). Todos os artefatos devem
estar alinhados a ela antes de qualquer merge.

## Stack oficial (ADR-001 ratificado, 13/11/2026)

| Camada | Tecnologia | Porta |
|---|---|---|
| Banco | MySQL 8.0 InnoDB | 3306 (rede `data`, interna) |
| Backend | Python 3.11 + FastAPI + SQLAlchemy 2.0 + Alembic | 8000 (rede `edge`) |
| Frontend | Vanilla JS ES6+ + Tailwind CSS + nginx | 80 |
| Proxy | nginx (porta 8380 exposta) | 8380 |
| PDF | ReportLab | server-side |
| CI | GitHub Actions (`ruff` + `pytest --cov≥80` + `mypy` + build) | — |

## Diretórios

- `backend/` — FastAPI, domain/usecases/adapters, config, main, testes
- `frontend/` — Vanilla JS, Tailwind, index.html, app.js, testes E2E (Playwright)
- `proxy/` — nginx.conf
- `scripts/` — automação (Python preferencial)
- `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml`, `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml`, `config-make-0001-makefile-v1` — infra
- `.github/workflows/config-ci-0001-github-actions-v1.0.yml` — CI/CD
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` — lei suprema
- `req-func-0001-requisitos-funcionais-canon.md`, `req-use-case-0001-casos-de-uso-canon.md`, `doc-arch-0001-camada-de-dados-canon.md` — SSOT v3.2
- `board-roadmap-0001-roadmap-canon.md` — marcos S1–S5
- `.ai/specs/*.md` — especificações SDD
- `.ai/handoffs/HF-*.md` — handoffs de execução
- `docs/decisoes/` — ADRs
- `docs/strategy/`, `docs/rfc/`, `docs/change/` — estratégia (PRD, BRD, RFC, CR)
- `docs/operacao/`, `docs/auditorias/` — operação (Runbook, Post-Mortem, SLA, DPIA)
- `docs/arquitetura/` — diagramas C4
- `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/` — config do OpenCode (não versionar segredos)
- `config-env-0001-env-example-v1.0` — NÃO commitar (já no `.gitignore`)

## Git workflow

- Branch: `feat/UC-XX-descricao`
- Fluxo: branch → PR → CI green → code review (rubrica R-01..R-07) → gatekeeper → aprovação humana (CCB) → merge `main` → kanban "Done"
- Labels: P0/P1/P2; camada frontend/backend/database/infra/docs; tipo feature/bug/test/chore
- Remotes: `origin git@github.com:leonardosetti/COBECO.git`; locais `main`, `stage`; `integracao-leonardo` remote-only
- DoD: Clean Architecture 4 camadas, queries parameterizadas, PT-BR, cobertura ≥80%, OpenAPI atualizado, `docker compose up` sem config manual

## Convenções

- Idioma: PT-BR (docs, DB, variáveis, comentários, mensagens de erro)
- Commits: Conventional Commits (tipo(escopo): resumo imperativo, ex: `feat(api): add GET /perfil`)
- Sem segredos em repositório (`config-env-0001-env-example-v1.0`, `secrets/`, `*.pem`, `*.key` no `.gitignore`)
- Dados sintéticos apenas (LGPD, Constitution Art. 3.5)

## Comandos (verificados)

`cp config-env-0001-env-example-v1.0.example config-env-0001-env-example-v1.0` → `docker compose up -d --build` → `make health` → `make test` / `make test-cov` / `make ci` / `make seed` / `make migrate`

## Método SDD (Constitution Art. 6)

Todo fluxo entra como spec (`.ai/specs/*.md`) e sai como handoff (`.ai/handoffs/HF-*.md`).
Handoff passa por `handoff_parser.py` antes do dispatch do L0 (`agent-nexus-prime-ultimate` via `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py`).
Cadeia de merge: reviewer → qa-sdet → CI verde → gatekeeper → aprovação humana.

## Templates de elite

`docs/decisoes/template-adr-0001-adr-v1.0.md`, `.ai/specs/template-spec-0001-spec-v1.0.md`,
`docs/strategy/TEMPLATE-PRD.md`, `docs/rfc/template-rfc-0001-rfc-v1.0.md`,
`docs/change/template-cr-0001-cr-v1.0.md`, `docs/operacao/template-runbook-0001-runbook-v1.0.md`,
`docs/operacao/template-test-plan-0001-test-plan-v1.0.md`, `docs/operacao/template-changelog-0001-changelog-v1.0.md`,
`docs/operacao/template-tech-debt-0001-tech-debt-v1.0.md`, `docs/strategy/TEMPLATE-USER-STORY.md`,
`docs/auditorias/template-postmortem-0001-postmortem-v1.0.md`,
`docs/auditorias/template-sla-0001-sla-slo-sli-v1.0.md`,
`docs/auditorias/template-dpia-0001-dpia-threat-v1.0.md`

## Comandos úteis

`make up` | `make down` | `make test` | `make test-cov` | `make lint` | `make seed` | `make migrate` | `make ci` | `make health` | `make clean`
