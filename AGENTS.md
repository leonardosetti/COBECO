# COBECO — AGENTS.md

## Repo state: código publicado, Constitution v2.0 vigente

O repositório está publicado em `git@github.com:leonardosetti/COBECO.git` (branch `main`, commit `8e2d295`).
Aplicação completa: backend FastAPI, frontend Vanilla JS + Tailwind, nginx proxy, Docker Compose,
seed SQL, Alembic, CI GitHub Actions, specs SDD, Constitution v2.0.

Não assumir "docs only" — todo o scaffold do MVP já existe e está versionado.

## Lei suprema

`constitution.md` v2.0 é a lei suprema do repositório (SSOT normativo). Todos os artefatos devem
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
- `docker-compose.yml`, `docker-compose.override.yml`, `Makefile` — infra
- `.github/workflows/ci.yml` — CI/CD
- `constitution.md` — lei suprema
- `REQUISITOS.md`, `CASOSDEUSO.md`, `CAMADADEDADOS.md` — SSOT v3.2
- `board_roadmap.md` — marcos S1–S5
- `.ai/specs/*.md` — especificações SDD
- `.ai/handoffs/HF-*.md` — handoffs de execução
- `docs/decisoes/` — ADRs
- `docs/strategy/`, `docs/rfc/`, `docs/change/` — estratégia (PRD, BRD, RFC, CR)
- `docs/operacao/`, `docs/auditorias/` — operação (Runbook, Post-Mortem, SLA, DPIA)
- `docs/arquitetura/` — diagramas C4
- `.opencode/` — config do OpenCode (não versionar segredos)
- `.env` — NÃO commitar (já no `.gitignore`)

## Git workflow

- Branch: `feat/UC-XX-descricao`
- Fluxo: branch → PR → CI green → code review (rubrica R-01..R-07) → gatekeeper → aprovação humana (CCB) → merge `main` → kanban "Done"
- Labels: P0/P1/P2; camada frontend/backend/database/infra/docs; tipo feature/bug/test/chore
- Remotes: `origin git@github.com:leonardosetti/COBECO.git`; locais `main`, `stage`; `integracao-leonardo` remote-only
- DoD: Clean Architecture 4 camadas, queries parameterizadas, PT-BR, cobertura ≥80%, OpenAPI atualizado, `docker compose up` sem config manual

## Convenções

- Idioma: PT-BR (docs, DB, variáveis, comentários, mensagens de erro)
- Commits: Conventional Commits (tipo(escopo): resumo imperativo, ex: `feat(api): add GET /perfil`)
- Sem segredos em repositório (`.env`, `secrets/`, `*.pem`, `*.key` no `.gitignore`)
- Dados sintéticos apenas (LGPD, Constitution Art. 3.5)

## Comandos (verificados)

`cp .env.example .env` → `docker compose up -d --build` → `make health` → `make test` / `make test-cov` / `make ci` / `make seed` / `make migrate`

## Método SDD (Constitution Art. 6)

Todo fluxo entra como spec (`.ai/specs/*.md`) e sai como handoff (`.ai/handoffs/HF-*.md`).
Handoff passa por `handoff_parser.py` antes do dispatch do L0 (`agent-nexus-prime-ultimate` via `scripts/nexus_dispatcher.py`).
Cadeia de merge: reviewer → qa-sdet → CI verde → gatekeeper → aprovação humana.

## Templates de elite

`docs/decisoes/TEMPLATE-ADR.md`, `.ai/specs/TEMPLATE-SPEC.md`,
`docs/strategy/TEMPLATE-PRD.md`, `docs/rfc/TEMPLATE-RFC.md`,
`docs/change/TEMPLATE-CR.md`, `docs/operacao/TEMPLATE-RUNBOOK.md`,
`docs/operacao/TEMPLATE-TEST-PLAN.md`, `docs/operacao/TEMPLATE-CHANGELOG.md`,
`docs/operacao/TEMPLATE-TECH-DEBT.md`, `docs/strategy/TEMPLATE-USER-STORY.md`,
`docs/auditorias/TEMPLATE-POST-MORTEM.md`,
`docs/auditorias/TEMPLATE-SLA-SLO-SLI.md`,
`docs/auditorias/TEMPLATE-DPIA-THREAT.md`

## Comandos úteis

`make up` | `make down` | `make test` | `make test-cov` | `make lint` | `make seed` | `make migrate` | `make ci` | `make health` | `make clean`
