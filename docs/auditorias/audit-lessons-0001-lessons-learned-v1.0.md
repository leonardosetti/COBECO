---
id: audit-lessons-0001-lessons-learned-v1.0
type: audit-lessons
title: AUDIT LESSONS — Lessons Learned
version: v1.0
status: ratificado
canonical: false
canonical_slug: lessons-learned
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
domain: audit
layer: audit
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Lições Aprendidas Consolidadas — COBECO MVP

**Documento:** Registro de Lições Aprendidas (Lessons Learned)  
**Versão:** 1.0  
**Data:** 30/10/2026  
**Autor:** Leonardo Setti (Tech Lead / PO)  
**Fonte:** Post-Mortem (27/10/2026), Retrospectivas de Sprint, RAID Log, Team Feedback  
**Classificação:** Interno — Conhecimento Institdoc-arch-0006-uc-v1ional  
**Objetivo:** Capturar conhecimento tácito e explícito para reutilização em projetos futuros da equipe/FATEC

---

## 1. Lições de Governança e Processo

### 1.1 Sprint 0 Obrigatório (Não Negociável)
> **Liçao:** **Nunca inicie código sem Sprint 0 dedicado a Charter, RACI, ADR, GitHub Projects, Docker.**
>
> **Contexto:** Tentamos misturar governança (Charter, RACI) com Sprint 1 (Auth + Docs). Resultado: stack conflitante descoberta tarde (I-001), GitHub Projects não configurado (I-002), atraso risco.
>
> **Aplicação Futura:**
> - Sprint 0 = 5 dias fixos: Charter + Business Case + Stakeholders + RACI + WBS + Schedule + ADR-001 + Constitution + GitHub Projects + Docker Compose validado
> - **Gate 1** obrigatório antes de Sprint 1: CCB assina Charter + RACI + ADR-001
> - Zero código escrito antes do Gate 1

### 1.2 Constitution como Lei Suprema Funciona
> **Liçao:** **Uma Constitution ratificada pelo CCB elimina bikeshedding e acelera decisões técnicas.**
>
> **Contexto:** Constitution v2.0 ratificada 13/11/2025 (antes do projeto). Definia: stack (Art 1.3), KISS/YAGNI (Art 3.1/3.7), CCB authority (Art 5.1), SDD flow (Art 6), DoD (Art 6.3).
>
> **Resultado:** 0 discussões sobre stack, 0 debates sobre "clean architecture opcional", CCB decidia em minutos.
>
> **Aplicação Futura:** Todo projeto inicia com Constitution ratificada. Se não existe, criar no Sprint 0.

### 1.3 Spec-First (SDD) + Handoff = Zero Integração Surpresa
> **Liçao:** **Spec-first com handoff parser → L0 dispatch garante contrato Front↔Back estável.**
>
> **Contexto:** 16 Specs ratificadas, cada uma com handoff processado por `handoff_parser.py` → `nexus_dispatcher.py`. Contrato OpenAPI no Spec → Handoff → Implementação.
>
> **Resultado:** 0 breaking changes Front↔Back, 0 reuniões "o endpoint mudou", integração suave.
>
> **Aplicação Futura:** SDD obrigatório. Nenhuma tarefa de código sem Spec ratificada + Handoff processado.

---

## 2. Lições Técnicas e de Arquitetura

### 2.1 ADR-001 no Sprint 0 Economiza Sprints Inteiros
> **Liçao:** **Decidir stack no Sprint 0 com ADR ratificado evita 2+ sprints de thrashing.**
>
> **Contexto:** Duas stacks conflitantes (React/NestJS/PostgreSQL vs FastAPI/MySQL/Vanilla JS). ADR-001 ratificada dia 13/11 (antes do Kick-off 15/09).
>
> **Impacto:** Se decidíssemos na Sprint 1: ~2 sprints perdidas, retrabalho frontend+backend, morale baixa.
>
> **Aplicação Futura:** ADR-001 (Stack) + ADR-002 (Clean Arch) + ADR-003 (Auth) no Sprint 0. Ratificados pelo CCB.

### 2.2 Clean Architecture 4 Camadas (Manual) — Disciplina > Framework
> **Liçao:** **Clean Architecture manual em FastAPI exige convenção + code review, mas dá controle total.**
>
> **Contexto:** FastAPI não impõe Clean Arch (diferente de NestJS). Definimos: `domain/` (entities + rules), `usecases/`, `adapters/` (repos, pdf, auth), `infrastrdoc-arch-0006-uc-v1ture/` (config, migrations, seed), `api/` (routers). Code review (R-01..R-07) verifica Dependency Rule.
>
> **Resultado:** 0 vazamento de framework no Domain. Testes unitários puros (mock adapters). Troca de DB/ORM seria trivial.
>
> **Aplicação Futura:** Estrutura de pastas obrigatória no template do projeto. Code review checklist inclui "Domain não importa FastAPI/SQLAlchemy/Pydantic".

### 2.3 Vanilla JS + Tailwind — Desktop-First Funciona para MVP
> **Liçao:** **Vanilla JS ES6+ modular + Tailwind atende desktop-first MVP sem build step.**
>
> **Contexto:** RNF04 exigia desktop-first ≥1024px. React + build step adicionaria complexidade. Escolhemos: modules ES6 (`import`/`export`), roteamento hash-based, `sessionStorage` para estado, componentes UI reutilizáveis (Toast, Modal, Autocomplete, DataTable).
>
> **Resultado:** Zero build, zero dependências npm (exceto dev), deploy = arquivos estáticos nginx. Performance excelente.
>
> **Cuidado:** Bus factor Frontend = 1 (apenas 1 dev sabia). **Mitigação:** Pair programming rotativo + documentação de componentes.

### 2.4 MySQL 8.0 InnoDB + SQLAlchemy 2.0 Async — Sólido
> **Liçao:** **MySQL InnoDB + SQLAlchemy 2.0 async + Alembic atende ACID, migrações, performance.**
>
> **Contexto:** RNF03/RNF12 exigiam MySQL InnoDB. Usamos: `asyncpg` não (MySQL), `pymysql` driver, `sqlalchemy.ext.asyncio`, connection pool, Alembic para migrations.
>
> **Problemas Encontrados/Resolvidos:**
> - `utf8mb4_unicode_ci` bug no 8.0.33 → upgrade 8.0.36 (I-004)
> - FK cascade comportamento inesperado → documentado no DER
> - Seed performance → bulk insert + disable FK checks temporário
>
> **Aplicação Futura:** MySQL 8.0.36+ fixo no config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0. Seed script com `session.bulk_save_objects` + `ForeignKeyChecks=0` temporário.

---

## 3. Lições de Qualidade e Testes

### 3.1 TDD desde Sprint 1 = Cobertura Natural (83%)
> **Liçao:** **TDD obrigatório no Definition of Done faz cobertura ≥80% ser consequência, não meta final.**
>
> **Contexto:** DoD atualizado Sprint 0: "Testes unitários escritos ANTES do código + cobertura ≥80% nos módulos tocados".
>
> **Resultado:** Cobertura final 83% (meta 80%). 0 corrida na Sprint 5. Testes guiaram design (ex: Auth UseCases testáveis pois puros).
>
> **Aplicação Futura:** TDD no DoD desde dia 1. Meta intermediária: 60% fim S2, 70% fim S3, 75% fim S4.

### 3.2 Benchmark Automatizado no CI (Seed + PDF)
> **Liçao:** **Performance requirements (RNF08 <10s seed, RNF11 <5s PDF) devem ser testes no CI com threshold.**
>
> **Contexto:** Seed 18s → 4.2s (I-007), PDF 7s → 3.8s (I-008). Ambos descobertos tarde, corrigidos sob pressão.
>
> **Solução Implementada:**
> - `make seed` no CI com `pytest --timeout=10` + threshold
> - `make pdf-bench` no CI com `pytest --timeout=5` + threshold
> - CI falha se exceder → PR bloqueado
>
> **Aplicação Futura:** Todo RNF de performance vira teste de CI com threshold. Code review valida.

### 3.3 Padrões E2E Obrigatórios = 0 Flaky
> **Liçao:** **Definir padrões E2E no DoD (data-testid, retry, waitForLoadState) elimina flakiness.**
>
> **Contexto:** Testes flaky (I-009) devido a seletores CSS Tailwind + race condition.
>
> **Padrões Estabelecidos (DoD):**
> - Seletores: `data-testid="..."` obrigatório (nunca classe CSS)
> - `retries: 2` no Playwright config
> - `await page.waitForLoadState('networkidle')` antes de assertions
> - Code review duplo: Dev + QA (não só QA)
>
> **Resultado:** 0 flaky nos últimos 20 runs CI.

---

## 4. Lições de Equipe e Gestão

### 4.1 Pair Programming no Caminho Crítico (Auth, PDF, Cálculo)
> **Liçao:** **Pair programming em tarefas de alto risco/incerteza acelera e melhora qualidade.**
>
> **Aplicado Em:**
> - Auth (UC09-UC12): 2 devs Backend → 0 bugs críticos, conhecimento compartilhado
> - PDF ReportLab: 1 dev Back + 1 dev QA (performance) → 3.8s vs 7s
> - Cálculo Orçamento: 1 dev Back + 1 dev Front (integração) → contrato estável
>
> **Regra Futura:** Tarefas no Critical Path + risco alto/incerteza = pair programming obrigatório.

### 4.2 Bus Factor Frontend = 1 — Risco Crítico
> **Liçao:** **Nunca ter bus factor 1 em área crítica. Cross-train desde Sprint 1.**
>
> **Contexto:** Apenas Eduardo sabia Vanilla JS + Tailwind + componentes. Se adoecesse, projeto parava.
>
> **Mitigação Aplicada (Tardia):**
> - Pair programming rotativo: Eduardo + Fabrício (Sprint 2), Eduardo + Nicholas (Sprint 3), Eduardo + Nicolas (Sprint 4)
> - Documentação de componentes UI (doc-readme-0001-readme-canon em `frontend/components/`)
>
> **Regra Futura:** RACI define bus factor mínimo 2 por área. Pair programming rotativo desde Sprint 1.

### 4.3 Docs ABNT Pair Writing + Revisão Semanal
> **Liçao:** **Documentação ABNT não é "tarefa de documento" — é pair writing PO+dev + revisão orientador semanal.**
>
> **Contexto:** Docs iniciaram Sprint 1 (tarde), revisão só no fim → orientador pediu ajustes (I-010).
>
> **Processo Corrigido:**
> - Dia 1 (Sprint 0): Template ABNT validado com orientador
> - Pair writing: PO (conteúdo/estrutura) + Dev (formatação/LaTeX/Word)
> - Revisão orientador: 15min/semana (não 30min/quinzena)
> - Entrega incremental: Capítulos revisados conforme escritos
>
> **Resultado:** Nota final 9.2 (meta 8.0), 0 ajustes na versão final.

### 4.4 Planning Poker + Spike para Tarefas > 3 SP
> **Liçao:** **Estimar sem Planning Poker + spike para desconhecido causa surpresas de performance (PDF, Seed).**
>
> **Processo Futuro:**
> - Planning Poker obrigatório no Sprint Planning (todas tarefas)
> - Referência histórica: registrar SP vs horas reais para calibrar
> - **Spike obrigatório** para: tarefas > 3 SP, tecnologia nova, RNF de performance
> - Spike = timeboxed (4h), entrega: PoC + estimativa calibrada + decisão go/no-go

---

## 5. Lições de Ferramentas e Automação

### 5.1 Mermaid C4 Diagrams = Docs-as-Code Real
> **Liçao:** **Diagramas Mermaid no repo (renderizam no GitHub) substituem ferramentas externas (Draw.io, Ldoc-arch-0006-uc-v1idchart).**
>
> **Vantagens:** Versionados (diff no PR), zero licença, zero sync manual, acessíveis, vive junto ao código.
>
> **Aplicação Futura:** Todo diagrama arquitetural em Mermaid. Template C4 pronto no repo.

### 5.2 GitHub Projects (Beta) + Milestones + Labels = Rastreabilidade Visual
> **Liçao:** **Projects (beta) com campos customizados (Sprint, Prioridade, RACI) substitui planilhas + Jira leve.**
>
> **Configuração Usada:**
> - Colunas: Backlog → Sprint Backlog → In Progress → Review → Done
> - Campos: Sprint (S1-S5), Prioridade (P0/P1/P2), Camada, Tipo, RACI (R/A/C/I)
> - Automação: Issue movida para "In Progress" quando branch criada; "Review" quando PR aberta; "Done" quando merge
>
> **Resultado:** Standup em 10 min (olhar board), 0 planilhas paralelas.

### 5.3 Automatizar RAID Log via GitHub Labels
> **Liçao:** **RAID Log manual vira dívida. Automatizar via `gh issue list --label risk,issue,dependency` → markdown.**
>
> **Implementação Futura (Próximo Projeto):**
> - Labels: `risk`, `issue`, `dependency`, `assumption`
> - GitHub Action diário: coleta issues com essas labels → gera `RAID-LOG.md` → commit
> - Sprint Review: apenas revisar diff do RAID Log auto-gerado

### 5.4 `make` como Interface Única (Dev + CI + Deploy)
> **Liçao:** **config-make-0001-makefile-v1 com targets padronizados (`up`, `down`, `test`, `test-cov`, `ci`, `seed`, `migrate`, `health`, `backup`, `ports-free`) unifica fluxo local e CI.**
>
> **Targets Essenciais:**
> ```makefile
> up: docker compose up -d --build
> down: docker compose down -v
> test: pytest
> test-cov: pytest --cov-fail-under=80
> ci: ruff + mypy + test-cov + docker build
> seed: docker compose exec backend python scripts/seed.py
> migrate: docker compose exec backend alembic upgrade head
> health: curl -sf localhost:8380/health && curl -sf localhost:8000/health
> backup: mysqldump + gzip
> ports-free: lsof -ti:8380,8000,3306 | xargs kill -9
> ```

---

## 6. Checklist de Reutilização (Próximo Projeto)

| Item | Template/Artefato | Localização | Status |
|------|-------------------|-------------|--------|
| ✅ | Constitution v2.0 | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` | Reutilizar + ajustar Art 1.3 (stack) |
| ✅ | Project Charter | `docs/strategy/TEMPLATE-PROJECT-CHARTER.md` | Adaptar escopo/datas |
| ✅ | Business Case | `docs/strategy/TEMPLATE-BUSINESS-CASE.md` | Adaptar contexto |
| ✅ | Stakeholder Register | `docs/strategy/TEMPLATE-STAKEHOLDERS.md` | Atualizar nomes |
| ✅ | Matriz RACI | `docs/strategy/TEMPLATE-RACI.md` | Atualizar papéis |
| ✅ | WBS | `docs/strategy/TEMPLATE-WBS.md` | Adaptar pacotes |
| ✅ | Schedule (Gantt) | `docs/strategy/TEMPLATE-SCHEDULE.md` | Ajustar datas |
| ✅ | PRD | `docs/strategy/TEMPLATE-PRD.md` | Adaptar RFs/RNFs |
| ✅ | User Story (Gherkin) | `docs/strategy/TEMPLATE-USER-STORY.md` | Pronto |
| ✅ | Traceability | `docs/strategy/TEMPLATE-TRACEABILITY.md` | Pronto |
| ✅ | C4 Templates | `docs/arquitetura/template-c4-0001-c4-v1.0.md` | Pronto |
| ✅ | ADR Template | `docs/decisoes/template-adr-0001-adr-v1.0.md` | Pronto |
| ✅ | RFC Template | `docs/rfc/template-rfc-0001-rfc-v1.0.md` | Pronto |
| ✅ | CR Template | `docs/change/template-cr-0001-cr-v1.0.md` | Pronto |
| ✅ | RAID Log Template | `docs/operacao/template-raid-log-0001-raid-log-v1.0.md` | Pronto |
| ✅ | Runbook Template | `docs/operacao/template-runbook-0001-runbook-v1.0.md` | Pronto |
| ✅ | Release Notes Template | `docs/operacao/template-release-notes-0001-release-notes-v1.0.md` | Pronto |
| ✅ | Status Report Template | `docs/operacao/template-status-report-0001-status-report-v1.0.md` | Pronto |
| ✅ | Post-Mortem Template | `docs/auditorias/template-postmortem-0001-postmortem-v1.0.md` | Pronto |
| ✅ | Docker Compose | `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` + `config-env-0001-env-example-v1.0.example` | Ajustar stack |
| ✅ | config-make-0001-makefile-v1 | `config-make-0001-makefile-v1` | Ajustar targets |
| ✅ | CI/CD | `.github/workflows/config-ci-0001-github-actions-v1.0.yml` | Ajustar jobs |
| ✅ | GitHub Projects Setup | Script `scripts/setup-github-projects.sh` | Criar |

---

## 7. Métricas de Referência (Baseline para Próximos Projetos)

| Métrica | COBECO MVP | Target Próximo |
|---------|------------|----------------|
| Duração Sprint 0 | 5 dias | 5 dias |
| Sprints Execução | 5 (6 dias cada) | 5-6 |
| Cobertura Testes | 83% | ≥ 85% |
| Lead Time (PR→Deploy) | 1.2 dias | < 1 dia |
| Deploy Frequency | 1/sprint | 2/sprint |
| MTTR | 15 min | < 10 min |
| Change Failure Rate | 0% | 0% |
| Bugs Críticos Produção | 0 | 0 |
| Docs ABNT Nota | 9.2 | ≥ 9.0 |
| Bus Factor Mínimo | 2 (Back) / 1 (Front) | 2 todas áreas |
| Pair Programming % | ~30% tarefas críticas | 50% tarefas críticas |
| Spike % Tarefas > 3 SP | 0% (falha) | 100% |
| Benchmark CI (Seed/PDF) | Sim (2) | Sim (todos RNF perf) |
| E2E Flaky Rate | 0% (final) | 0% |

---

## 8. Aprovação e Arquivamento

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| **Tech Lead / PO** | Leonardo Setti | _______________ | 30/10/2026 |
| **Arquiteto** | Nicholas Anthony | _______________ | 30/10/2026 |
| **Dev Backend 1** | Fabrício Cabral | _______________ | 30/10/2026 |
| **Dev Backend 2** | Nicholas Anthony | _______________ | 30/10/2026 |
| **Dev Frontend** | Eduardo Passarelli | _______________ | 30/10/2026 |
| **QA Lead** | Nicolas Mallouk | _______________ | 30/10/2026 |

---

**Localização:** `docs/auditorias/audit-lessons-0001-lessons-learned-v1.0.md` (repo Git)  
**Backup:** Sharepoint FATEC / pasta do projeto  
**Retenção:** Permanente — Conhecimento institdoc-arch-0006-uc-v1ional FATEC ADS

---

**Fim das Lições Aprendidas — COBECO MVP**  
*Conhecimento tácito tornado explícito para o próximo ciclo. "O único erro é não aprender com o erro."*