# COBECO — AGENTS.md

## Repo state: docs only, no source code yet
This repository is in the documentation/design phase (README: "Fase 1: Setup e Infra"). There is NO application code:
- No `package.json`, `docker-compose.yml`, `.env.example`, `requirements.txt`, `prisma/`, `src/`, or `.github/` workflows exist
- Do not look for or assume a test suite, dev server, lint config, or build command — none are present yet
- Root contents: markdown specs, diagrams (`.drawio`, `.excalidraw`), HTML/PNG exports, and `docx` monographs

## Directory ownership
- `brain/md/` — MVP specs, requirement refinements, use-case flows, user manual
- `brain/_old-artifact/` — superseded drafts (do not rely on)
- `brain/diagrams/` — Draw.io/Excalidraw sources: DER, use cases, state machine, low-fi prototypes
- `prj_docs/` — group work instructions (`wrk_grp.md`) and ABNT monograph template
- `excalidraw_baixa/` — exported low-fidelity prototype SVGs
- Root `.md` files — project docs in Portuguese (README, REQUISITOS, CASOSDEUSO, CAMADADEDADOS, etc.)

## Stack: two conflicting plans — verify before writing code
Neither plan is verified by code; ask the team which to implement before scaffolding:
- README.md (updated 31/08/2026): React 18 + TS + Vite + Tailwind + shadcn/ui (:8080), Node.js 20 + NestJS 10 (:3000), PostgreSQL 16 + Prisma 5 (:5432), Docker Compose, GitHub Actions, Jest + Vitest
- board_roadmap.md (dated 15/09/2026): FastAPI + Pydantic backend, MySQL 8 InnoDB, pytest/ruff, ReportLab PDF export

## Git workflow (documented in board_roadmap.md)
- Branch pattern: `feat/UC-XX-descricao` (UC = use case number)
- Flow: branch → PR → CI green → code review → merge to `main` → Kanban "Done"
- Labels: priority P0/P1/P2; layer frontend/backend/database/infra/docs; type feature/bug/test/chore
- Kanban columns: Backlog → Sprint Backlog → In Progress → Review → Done
- Definition of Done: Clean Architecture 4 layers, parameterized queries only, PT-BR DB/variable naming, unit tests without coverage regression, OpenAPI contract updated, works via `docker compose up` with no manual config
- Remotes: `origin git@github.com:leonardosetti/COBECO.git`; local branches `main`, `stage`; `integracao-leonardo` is remote-only

## Language conventions
- Docs, DB schema, and variable naming: Portuguese (PT-BR) — per DoD and DER v3.2
- Existing commit messages are in Portuguese

## Commands (planned, NOT verified — no code to run yet)
Per README only: `cp .env.example .env` → `docker-compose up -d --build` → `docker-compose exec backend npm run test` / `frontend npm run test`
Do not run these until the corresponding files exist.

## What to avoid
- Do not scaffold NestJS/React/FastAPI/MySQL/Prisma files based on the README — the stack decision is unresolved
- Do not reference `.github/` workflows, `opencode.json`, or other instruction files — none exist in this repo
