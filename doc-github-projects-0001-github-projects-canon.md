---
id: doc-github-projects-0001-github-projects-canon
type: doc-github-projects
title: DOC GITHUB PROJECTS — Github Projects
version: '3.2'
status: ratificado
canonical: true
canonical_slug: github-projects
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
domain: strategy
layer: governance
tags: []
lgpd_class: n/a
workflow:
  stage: ratificado
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# COBECO — Cards do GitHub Projects (MVP)

**Objetivo:** criar milestones, labels, project board e issues no GitHub a partir do `board-roadmap-0001-roadmap-canon.md` e `req-func-0001-requisitos-funcionais-canon.md v3.2`.  
**Convenção:** nomes de variáveis/DB em PT-BR; branch `feat/UC-XX-descricao`; DoD no template de PR.

---

## 1. Labels obrigatórias

Criar no repositório (`gh label create`):

| Nome | Cor | Descrição |
|---|---|---|
| `P0` | `d73a4a` | Prioridade — crítico/bloqueante |
| `P1` | `fbca04` | Prioridade — alto |
| `P2` | `0e8a16` | Prioridade — médio/backlog |
| `camada: frontend` | `1d76db` | Frontend (Vanilla JS/Tailwind) |
| `camada: backend` | `6f42c1` | Backend (FastAPI/Pydantic) |
| `camada: database` | `006b75` | Database (MySQL InnoDB) |
| `camada: infra` | `808080` | Infra (Docker/CI) |
| `camada: docs` | `0052cc` | Documentação |
| `tipo: feature` | `a2eeef` | Tipo — feature |
| `tipo: bug` | `b60205` | Tipo — bug |
| `tipo: test` | `c5def5` | Tipo — teste |
| `tipo: chore` | `ffffff` | Tipo — chore |

Comando exemplo:
```
gh label create P0 --color d73a4a --description "Prioridade: crítico/bloqueante"
```

---

## 2. Milestones (5)

| Milestone | Descrição | Prazo | RFs atendidos |
|---|---|---|---|
| `S1: Setup, Docs e Auth` | Infra Docker, Schema MySQL, Seed e Autenticação completa + Entrega da Documentação | 2026-09-20 | RF01, RF02, RF03, RF04 |
| `S2: Listas e Catálogo` | CRUD de listas, persistência ACID, autocomplete e promoção de lista efêmera | 2026-09-26 | RF07, RF08, RF09, RF10, RF11 |
| `S3: Pré-filtro e Comparação` | Seleção de categorias, fornecedores, slider de disponibilidade e motor de cálculo flat | 2026-10-02 | RF12, RF13, RF14, RF15, RF16 |
| `S4: Export, Perfil e Polish` | Geração de PDF (ReportLab), impressão A4, gestão de perfil e feedbacks visuais | 2026-10-08 | RF05, RF06, RF17, RF18 |
| `S5: Buffer, QA e Demo` | Cobertura ≥80%, refinamento de performance, docs finais e ensaio da apresentação | 2026-10-15 | Todos (QA e polish) |

Comando exemplo:
```
gh api repos/leonardosetti/COBECO/milestones -f title="S1: Setup, Docs e Auth" -f due_on="2026-09-20T19:00:00Z"
```

---

## 3. Project board (kanban)

Colunas (views):
1. `📋 Backlog` — aprovado no SSOT v3.2
2. `🎯 Sprint Backlog` — selecionado para a Sprint ativa
3. `🔨 In Progress` — branch criada, desenvolvimento em andamento
4. `👀 Review` — PR aberto, CI verde, aguardando Code Review
5. `✅ Done` — merge na `main`, DoD atendido

Criar board classico ou projects (beta) e vincular milestones S1–S5.

---

## 4. Issues / cards por Sprint

### Sprint 1 — Setup, Docs e Auth

| # | Título | Milestone | Labels | RFs | Branch |
|---|---|---|---|---|---|
| DOCS-P0 | Finalizar e Entregar Documentação ABNT | S1 | `P0`, `camada: docs` | RF01–RF04 | `feat/UC-XX-docs-abnt` |
| INFRA-P0 | Setup Docker Compose (FastAPI + MySQL InnoDB) | S1 | `P0`, `camada: infra` | infra | `feat/UC-XX-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0` |
| DB-P0 | Criar Schema do Banco (8 Tabelas PT-BR) | S1 | `P0`, `camada: database` | infra | `feat/UC-XX-schema-db` |
| DB-P0 | Implementar Script de Seed (`seed.py`) | S1 | `P0`, `camada: database` | RNF08 | `feat/UC-XX-seed` |
| BACKEND-P0 | UC09: Cadastrar Usuário (RF01) | S1 | `P0`, `camada: backend` | RF01 | `feat/UC-09-cadastrar-usuario` |
| BACKEND-P0 | UC10: Realizar Login com JWT (RF02) | S1 | `P0`, `camada: backend` | RF02 | `feat/UC-10-login-jwt` |
| BACKEND-P1 | UC11: Realizar Logout (RF03) | S1 | `P1`, `camada: backend` | RF03 | `feat/UC-11-logout` |
| BACKEND-P1 | UC12: Recuperar Senha (RF04) | S1 | `P1`, `camada: backend` | RF04 | `feat/UC-12-recuperar-senha` |

### Sprint 2 — Listas e Catálogo

| # | Título | Milestone | Labels | RFs | Branch |
|---|---|---|---|---|---|
| FRONTEND-P0 | UC02: Autocomplete de Produtos (RF07) | S2 | `P0`, `camada: frontend` | RF07 | `feat/UC-02-autocomplete` |
| FRONTEND-P0 | UC01: Criar Lista em Memória (RF07) | S2 | `P0`, `camada: frontend` | RF07 | `feat/UC-01-lista-memoria` |
| BACKEND-P0 | UC14: Salvar Lista / Persistir (RF08) | S2 | `P0`, `camada: backend` | RF08 | `feat/UC-14-salvar-lista` |
| FRONTEND-P0 | UC17: Promover Lista Efêmera (RF08) | S2 | `P0`, `camada: frontend` | RF08 | `feat/UC-17-promover-lista` |
| BACKEND-P0 | UC15: Listar Minhas Listas (RF09) | S2 | `P0`, `camada: backend` | RF09 | `feat/UC-15-listar-listas` |
| BACKEND-P1 | UC13: Editar e Excluir Lista (RF10, RF11) | S2 | `P1`, `camada: backend` | RF10, RF11 | `feat/UC-13-editar-excluir-lista` |

### Sprint 3 — Pré-filtro e Comparação

| # | Título | Milestone | Labels | RFs | Branch |
|---|---|---|---|---|---|
| FRONTEND-P0 | UC03: Selecionar Categorias (Pré-filtro) (RF12) | S3 | `P0`, `camada: frontend` | RF12 | `feat/UC-03-categorias` |
| FRONTEND-P0 | UC04: Selecionar Fornecedores (RF13) | S3 | `P0`, `camada: frontend` | RF13 | `feat/UC-04-fornecedores` |
| FRONTEND-P1 | UC05: Filtrar por Disponibilidade (RF14) | S3 | `P1`, `camada: frontend` | RF14 | `feat/UC-05-disponibilidade` |
| BACKEND-P0 | UC06: Calcular Orçamento (RF15) | S3 | `P0`, `camada: backend` | RF15 | `feat/UC-06-calcular-orcamento` |
| FRONTEND-P0 | UC07: Visualizar Resultados (RF16) | S3 | `P0`, `camada: frontend` | RF16 | `feat/UC-07-visualizar-resultados` |

### Sprint 4 — Exportação, Perfil e Polish

| # | Título | Milestone | Labels | RFs | Branch |
|---|---|---|---|---|---|
| BACKEND-P0 | UC08/UC29: Exportar Lista em PDF (RF17) | S4 | `P0`, `camada: backend` | RF17 | `feat/UC-08-export-pdf` |
| FRONTEND-P1 | UC09: Otimização para Impressão (RF18) | S4 | `P1`, `camada: frontend` | RF18 | `feat/UC-09-imprimir` |
| BACKEND-P1 | UC18: Visualizar Perfil (RF05) | S4 | `P1`, `camada: backend` | RF05 | `feat/UC-18-visualizar-perfil` |
| BACKEND-P1 | UC16: Gerenciar Perfil (RF06) | S4 | `P1`, `camada: backend` | RF06 | `feat/UC-16-gerenciar-perfil` |
| FRONTEND-P1 | UI/UX: Feedback Visual Global (RNF05) | S4 | `P1`, `camada: frontend` | RNF05 | `feat/UC-XX-feedback-visual` |

### Sprint 5 — Buffer, QA e Demo

| # | Título | Milestone | Labels | RFs | Branch |
|---|---|---|---|---|---|
| TEST-P0 | Cobertura de Testes Unitários ≥80% (RNF06) | S5 | `P0`, `tipo: test` | RNF06 | `feat/UC-XX-testes` |
| INFRA-P1 | Pipeline CI/CD GitHub Actions (RNF07) | S5 | `P1`, `camada: infra` | RNF07 | `feat/UC-XX-ci-cd` |
| DOCS-P1 | Refinar doc-readme-0001-readme-canon.md e OpenAPI (RNF02) | S5 | `P1`, `camada: docs` | RNF02 | `feat/UC-XX-docs` |
| CHORE-P0 | Preparação da Apresentação Final | S5 | `P0`, `tipo: chore` | Todos | `feat/UC-XX-apresentacao` |

---

## 5. Definição de Pronto (DoD) — template de PR

Adicionar checklist a todo Pull Request:

- [ ] Código segue Clean Architecture (4 camadas) e não vaza dependências de framework para o Domain
- [ ] Todas as queries no backend usam *parameterized queries* (proteção contra SQLi)
- [ ] Nomenclatura do banco de dados e variáveis está em PT-BR conforme DER v3.2
- [ ] Testes unitários foram escritos e a cobertura não diminuiu
- [ ] O contrato OpenAPI (`/docs`) foi atualizado (SDD)
- [ ] Funciona corretamente via `docker compose up` sem configuração manual extra

---

## 6. Comandos `gh` para criar no GitHub

Executar a partir da raiz do repo (exige autenticação `gh auth login`):

```bash
# Labels
gh label create P0 --color d73a4a --description "Prioridade: crítico/bloqueante"
gh label create P1 --color fbca04 --description "Prioridade: alto"
gh label create P2 --color 0e8a16 --description "Prioridade: médio/backlog"
gh label create "camada: frontend" --color 1d76db
gh label create "camada: backend" --color 6f42c1
gh label create "camada: database" --color 006b75
gh label create "camada: infra" --color 808080
gh label create "camada: docs" --color 0052cc
gh label create "tipo: feature" --color a2eeef
gh label create "tipo: bug" --color b60205
gh label create "tipo: test" --color c5def5
gh label create "tipo: chore" --color ffffff

# Milestones
gh api repos/leonardosetti/COBECO/milestones -f title="S1: Setup, Docs e Auth" -f due_on="2026-09-20T19:00:00Z"
gh api repos/leonardosetti/COBECO/milestones -f title="S2: Listas e Catálogo" -f due_on="2026-09-26T19:00:00Z"
gh api repos/leonardosetti/COBECO/milestones -f title="S3: Pré-filtro e Comparação" -f due_on="2026-10-02T19:00:00Z"
gh api repos/leonardosetti/COBECO/milestones -f title="S4: Export, Perfil e Polish" -f due_on="2026-10-08T19:00:00Z"
gh api repos/leonardosetti/COBECO/milestones -f title="S5: Buffer, QA e Demo" -f due_on="2026-10-15T19:00:00Z"

# Project board (classic) — exemplo
gh project create --owner leonardosetti --title "COBECO MVP"
# depois criar colunas Backlog, Sprint Backlog, In Progress, Review, Done

# Exemplo de issue
gh issue create --title "UC09: Cadastrar Usuário (RF01)" --body "Endpoint + validação Pydantic..." \
  --milestone "S1: Setup, Docs e Auth" --label "P0,camada: backend"
```

---

## 7. Fluxo (board-roadmap-0001-roadmap-canon.md)

Branch → PR → CI green → code review → merge em `main` → kanban "Done".  
Labels: prioridade P0/P1/P2; camada frontend/backend/database/infra/docs; tipo feature/bug/test/chore.  
Remotes: `origin git@github.com:leonardosetti/COBECO.git`; locais `main`, `stage`; `integracao-leonardo` remote-only.
