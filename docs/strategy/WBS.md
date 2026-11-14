# EAP / WBS (Estrutura Analítica do Projeto) — COBECO MVP

**Versão:** 1.0  
**Data:** 29/09/2026 (Gate 2)  
**Responsável:** Leonardo Setti (Tech Lead)  
**Aprovação:** CCB (Gate 2)  
**Base:** PMBOK 7 + Scrum Sprints

---

## Convenção de Numeração

```
1.0  Projeto COBECO MVP
  1.1  Fase 1: Iniciação e Planejamento (Sprint 0)
  1.2  Fase 2: Execução - Sprints 1 a 5
    1.2.1  Sprint 1: Setup, Docs e Auth
    1.2.2  Sprint 2: Listas e Catálogo
    1.2.3  Sprint 3: Pré-filtro e Comparação
    1.2.4  Sprint 4: Export, Perfil e Polish
    1.2.5  Sprint 5: Buffer, QA e Demo
  1.3  Fase 3: Encerramento
```

---

## 1.0 Projeto COBECO MVP

### 1.1 Fase 1: Iniciação e Planejamento (Sprint 0 - Pré-jogo)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.1.1 | Project Charter | Criar e aprovar Charter formal | PO | 1 dia | — | `docs/strategy/PROJECT-CHARTER.md` |
| 1.1.2 | Business Case | Documentar justificativa acadêmica | PO | 0,5 dia | 1.1.1 | `docs/strategy/BUSINESS-CASE.md` |
| 1.1.3 | Stakeholder Register | Mapear stakeholders e comunicação | PO | 0,5 dia | 1.1.1 | `docs/strategy/STAKEHOLDERS.md` |
| 1.1.4 | Matriz RACI | Definir responsabilidades | Tech Lead | 0,5 dia | 1.1.1 | `docs/strategy/RACI.md` |
| 1.1.5 | WBS (esta) | Decompor escopo em pacotes | Tech Lead | 0,5 dia | 1.1.1 | `docs/strategy/WBS.md` |
| 1.1.6 | Cronograma (Gantt) | Sequenciar atividades com dependências | Tech Lead | 0,5 dia | 1.1.5 | `docs/strategy/SCHEDULE.md` |
| 1.1.7 | ADR-001 Stack | Ratificar stack tecnológica | Arquiteto | 1 dia | — | `docs/decisoes/doc-adr-0001-stack-decision-v1.0.md` |
| 1.1.8 | Constitution v2.0 | Validar lei suprema do repo | CCB | 0,5 dia | — | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` |
| 1.1.9 | GitHub Projects Setup | Milestones, labels, board, issues | Tech Lead | 1 dia | 1.1.4 | Projeto GitHub ativo |
| 1.1.10 | Ambiente Dev | Docker, seed, migrations, CI | Dev Backend | 1 dia | 1.1.7 | `docker compose up` funcional |

**Duração Fase 1:** 5 dias (pode paralelizar 1.1.1-1.1.6 + 1.1.7-1.1.10)

---

### 1.2 Fase 2: Execução - Sprints 1 a 5

#### 1.2.1 Sprint 1: Setup, Docs e Auth (Dias 1-6)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.2.1.1 | PRD | Consolidar req-func-0001-requisitos-funcionais-canon + req-use-case-0001-casos-de-uso-canon | PO | 1 dia | 1.1.1 | `docs/strategy/PRD.md` |
| 1.2.1.2 | User Stories (RF01-RF04) | Escrever US + Critérios Aceite Gherkin | PO | 1 dia | 1.2.1.1 | `docs/strategy/user-stories/US-*.md` + Issues GitHub |
| 1.2.1.3 | Diagramas C4 | Contexto, Containers, Componentes | Arquiteto | 1 dia | 1.1.7 | `docs/arquitetura/C4-*.md` |
| 1.2.1.4 | RAID Log Inicial | Riscos, premissas, issues, dependências | Tech Lead | 0,5 dia | 1.1.3 | `docs/operacao/doc-raid-log-0001-raid-log-v1.0.md` |
| 1.2.1.5 | Test Plan | Estratégia de testes unit/E2E | QA | 0,5 dia | 1.2.1.2 | `docs/operacao/doc-test-plan-0001-test-plan-v1.0.md` |
| 1.2.1.6 | Docker Compose Prod | Infra completa (nginx, backend, DB) | Dev Backend | 1 dia | 1.1.10 | `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` validado |
| 1.2.1.7 | Schema MySQL (8 tabelas) | DER implementado + migrations | Dev Backend | 1 dia | 1.1.7 | `alembic upgrade head` |
| 1.2.1.8 | Seed Script | 11 cat, 10 forn, 50 prod, 300 preços | Dev Backend | 1 dia | 1.2.1.7 | `scripts/seed.py` <10s |
| 1.2.1.9 | UC09: Cadastrar Usuário | Endpoint + validação + bcrypt + segurança | Dev Backend | 1,5 dia | 1.2.1.7 | `POST /v1/usuarios` |
| 1.2.1.10 | UC10: Login JWT | Access (15min) + Refresh (7d, cookie) | Dev Backend | 1,5 dia | 1.2.1.9 | `POST /v1/auth/login` |
| 1.2.1.11 | UC11: Logout | Invalidar refresh cookie | Dev Backend | 0,5 dia | 1.2.1.10 | `POST /v1/auth/logout` |
| 1.2.1.12 | UC12: Recuperar Senha | Pergunta segurança ou token stdout | Dev Backend | 1 dia | 1.2.1.9 | `POST /v1/auth/recover` |
| 1.2.1.13 | Frontend Auth Pages | Login, Cadastro, Recuperar (Vanilla JS) | Dev Frontend | 2 dias | 1.2.1.9 | Páginas funcionais |
| 1.2.1.14 | Docs ABNT | Documentação formal para entrega | PO + Equipe | 3 dias | 1.2.1.1 | PDF ABNT |

**Gate 2 (Fim Sprint 1):** PRD + US + C4 + NFRs + Test Plan + RAID Log aprovados pelo CCB

---

#### 1.2.2 Sprint 2: Listas e Catálogo (Dias 7-12)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.2.2.1 | User Stories (RF07-RF11) | US + Critérios Aceite | PO | 0,5 dia | 1.2.1.2 | Issues GitHub |
| 1.2.2.2 | UC02: Autocomplete Produtos | Debounce 300ms, normalização | Dev Frontend | 1 dia | 1.2.1.13 | Componente funcional |
| 1.2.2.3 | UC01: Lista em Memória | sessionStorage, soma qtd, validação | Dev Frontend | 1 dia | 1.2.2.2 | Estado cliente |
| 1.2.2.4 | UC14: Salvar Lista (Persistir) | Transação MySQL BEGIN/COMMIT | Dev Backend | 1 dia | 1.2.1.7 | `POST /v1/listas` |
| 1.2.2.5 | UC17: Promover Lista Efêmera | Modal login → migrar sessionStorage→DB | Dev Frontend | 1 dia | 1.2.2.3, 1.2.2.4 | Fluxo completo |
| 1.2.2.6 | UC15: Listar Minhas Listas | Paginação 20/pág, ordenação, soft delete | Dev Backend | 1 dia | 1.2.2.4 | `GET /v1/listas` |
| 1.2.2.7 | UC13: Editar/Excluir Lista | Update + soft delete com confirmação | Dev Backend | 1 dia | 1.2.2.6 | `PUT/DELETE /v1/listas/{id}` |
| 1.2.2.8 | Frontend Listas CRUD | Dashboard, Criar/Editar, Excluir | Dev Frontend | 2 dias | 1.2.2.4, 1.2.2.6 | Telas completas |

---

#### 1.2.3 Sprint 3: Pré-filtro e Comparação (Dias 13-18)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.2.3.1 | User Stories (RF12-RF16) | US + Critérios Aceite | PO | 0,5 dia | 1.2.2.1 | Issues GitHub |
| 1.2.3.2 | UC03: Selecionar Categorias | 11 checkboxes, filtra fornecedores API | Dev Frontend | 1 dia | 1.2.2.8 | Tela pré-filtro |
| 1.2.3.3 | UC04: Selecionar Fornecedores | Checkboxes + % disponibilidade, min 2 | Dev Frontend | 1 dia | 1.2.3.2 | Seleção fornecedores |
| 1.2.3.4 | UC05: Filtrar Disponibilidade | Slider 0-100%, tempo real | Dev Frontend | 1 dia | 1.2.3.3 | Filtro dinâmico |
| 1.2.3.5 | UC06: Calcular Orçamento | Endpoint flat table, cache 5min, timeout 10s | Dev Backend | 1,5 dia | 1.2.2.4 | `POST /v1/orcamento` |
| 1.2.3.6 | UC07: Visualizar Resultados | Tabela ordenada preço ASC, highlight verde | Dev Frontend | 1,5 dia | 1.2.3.5 | Tela resultados |

---

#### 1.2.4 Sprint 4: Export, Perfil e Polish (Dias 19-24)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.2.4.1 | User Stories (RF05, RF06, RF17, RF18) | US + Critérios Aceite | PO | 0,5 dia | 1.2.3.1 | Issues GitHub |
| 1.2.4.2 | UC08/UC29: Export PDF | ReportLab, A4 server-side, visitantes+auth | Dev Backend | 1,5 dia | 1.2.2.4 | `POST /v1/export/pdf` |
| 1.2.4.3 | UC09: Otimização Impressão | CSS @media print, headers repetidos | Dev Frontend | 1 dia | 1.2.4.2 | Print-ready |
| 1.2.4.4 | UC18: Visualizar Perfil | Dados read-only + editáveis | Dev Backend | 1 dia | 1.2.1.9 | `GET/PUT /v1/perfil` |
| 1.2.4.5 | UC16: Gerenciar Perfil | Email, nome, senha (senha atual), ACID | Dev Backend | 1 dia | 1.2.4.4 | Transação perfil |
| 1.2.4.6 | Frontend Perfil | Tela visualizar + editar | Dev Frontend | 1 dia | 1.2.4.4 | Telas perfil |
| 1.2.4.7 | Feedback Visual Global | Toast, skeletons, modais confirmação | Dev Frontend | 1 dia | 1.2.2.8 | Componentes UI |

---

#### 1.2.5 Sprint 5: Buffer, QA e Demo (Dias 25-30)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.2.5.1 | Cobertura Testes ≥80% | pytest --cov-fail-under=80 | QA + Devs | 2 dias | Todas specs | CI verde |
| 1.2.5.2 | Testes E2E Playwright | Fluxos críticos cadastro→comparação→PDF | QA | 1,5 dia | 1.2.4.2 | `frontend/tests/e2e/` |
| 1.2.5.3 | CI/CD Pipeline | ruff + pytest + build Docker <5min | DevOps | 1 dia | 1.1.10 | `.github/workflows/config-ci-0001-github-actions-v1.0.yml` |
| 1.2.5.4 | Runbooks | Deploy, rollback, seed, migrate, backup | DevOps | 1 dia | 1.2.5.3 | `docs/operacao/RUNBOOK-*.md` |
| 1.2.5.5 | Release Notes v0.1.0 | Changelog + notas de release | PO | 0,5 dia | 1.2.5.1 | `CHANGELOG.md` + GitHub Release |
| 1.2.5.6 | Refinar doc-readme-0001-readme-canon + OpenAPI | Instruções docker compose, arquitetura | PO | 0,5 dia | 1.2.5.3 | `doc-readme-0001-readme-canon.md` atualizado |
| 1.2.5.7 | Preparação Apresentação | Roteiro 35min, falas divididas, ensaio | Equipe | 1,5 dia | 1.2.5.1 | Slides + Demo pronta |
| 1.2.5.8 | Post-Mortem / Lições | Blameless RCA, ações preventivas | Tech Lead | 0,5 dia | 1.2.5.7 | `docs/auditorias/audit-postmortem-0001-postmortem-v1.0.md` |
| 1.2.5.9 | Termo de Encerramento | Aceite formal, lições consolidadas | PO | 0,5 dia | 1.2.5.8 | `docs/strategy/CLOSURE.md` |

**Gate 3 (Fim Sprint 5):** Cobertura ≥80% + Runbooks + Release Notes + Demo funcional → CCB + Orientador

---

### 1.3 Fase 3: Encerramento (Pós-Apresentação)

| WBS ID | Pacote de Trabalho | Descrição | Responsável | Duração | Dependências | Entregável |
|--------|-------------------|-----------|-------------|---------|--------------|------------|
| 1.3.1 | Apresentação Final | Demo para banca, 35min | Equipe | 1 dia | 1.2.5.7 | Apresentação realizada |
| 1.3.2 | Avaliação Banca | Nota final, feedback | Banca | 1 dia | 1.3.1 | Ata de avaliação |
| 1.3.3 | Arquivamento | Repo público, docs finais, lições | PO | 1 dia | 1.3.2 | Repo GitHub público |
| 1.3.4 | Retrospectiva Final | O que funcionou, melhorias futuras | Equipe | 0,5 dia | 1.3.1 | `docs/auditorias/RETROSPECTIVA.md` |

**Gate 4 (Encerramento):** Termo de Encerramento + Lições + Post-Mortem → CCB + Banca

---

## Resumo de Esforço por Sprint

| Sprint | Dias | Pacotes de Trabalho | Esforço Estimado (h) | Foco Principal |
|--------|------|---------------------|----------------------|----------------|
| Sprint 0 (Fase 1) | 5 | 10 | ~200h | Governança, Infra, Stack |
| Sprint 1 | 6 | 14 | ~350h | Auth, Docs, Schema, Seed |
| Sprint 2 | 6 | 8 | ~300h | Listas, Catálogo, CRUD |
| Sprint 3 | 6 | 6 | ~280h | Comparação, Cálculo |
| Sprint 4 | 6 | 7 | ~300h | PDF, Perfil, UI Polish |
| Sprint 5 | 6 | 9 | ~320h | Testes, CI, Demo, Encerramento |
| Encerramento | 3 | 4 | ~80h | Apresentação, Arquivamento |
| **TOTAL** | **38** | **58** | **~1.830h** | |

> **Nota:** Esforço total ~1.830h para equipe de 5 pessoas = ~366h/pessoa em 38 dias úteis = ~9,6h/dia/pessoa. Ajustar escopo se necessário (buffer na Sprint 5).

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 29/09/2026 | Leonardo Setti | Criação inicial baseada no roadmap | CCB (Gate 2) |

---

**Fim da EAP / WBS — COBECO MVP**  
*Esta WBS deve ser sincronizada com GitHub Projects (Issues + Milestones).*