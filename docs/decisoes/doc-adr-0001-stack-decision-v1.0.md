# ADR-001: Decisão de Stack Tecnológica — COBECO MVP

**Status:** Ratificada  
**Data:** 13 de Novembro de 2026  
**Decisores:** CCB (Change Control Board) — FATEC Taquaritinga ADS  
**Contexto:** Constitution.md Art. 1.3, Art. 5.1

---

## Contexto

O projeto COBECO possuía duas propostas de stack tecnológica conflitantes:

| Fonte | Stack | Data |
|-------|-------|------|
| `doc-readme-0001-readme-canon.md` (v31/08/2026) | React 18 + TypeScript + Vite + Tailwind + shadcn/ui (:8080), Node.js 20 + NestJS 10 (:3000), PostgreSQL 16 + Prisma 5 (:5432) | 31/08/2026 |
| `board-roadmap-0001-roadmap-canon.md` (v15/09/2026) | FastAPI + Pydantic backend, MySQL 8 InnoDB, pytest/ruff, ReportLab PDF export | 15/09/2026 |

Nenhuma das duas estava implementada em código — o repositório continha apenas documentação.

---

## Decisão

**Ratifica-se a stack do `board-roadmap-0001-roadmap-canon.md` (FastAPI + MySQL + Vanilla JS) como oficial para o COBECO MVP.**

### Stack Aprovada

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| **Frontend** | Vanilla JS ES6+ + Tailwind CSS + nginx | Zero build runtime, desktop-first (RNF04), leve, FOSS, adequado à equipe acadêmica |
| **Backend** | Python 3.11 + FastAPI + Pydantic + SQLAlchemy 2.0 (async) | OpenAPI automático (SDD), tipagem forte, Clean Architecture manual, curva de aprendizado menor que NestJS |
| **Banco de Dados** | MySQL 8.0 InnoDB | **RNF03/RNF12 explícitos**: ACID, utf8mb4, engine InnoDB obrigatório |
| **ORM / Migrations** | SQLAlchemy 2.0 + Alembic | Async, type-safe, migrations versionadas |
| **PDF Generation** | ReportLab | **RF17/RNF11**: Server-side, A4, <5s para 100 itens |
| **API** | RESTful + OpenAPI (Swagger) | Contratos claros Front↔Back (SDD) |
| **Infraestrutura** | Docker 24 + Docker Compose 2 | Isolamento, reprodutibilidade, camadas ortogonais (spec-005) |
| **CI/CD** | GitHub Actions | Pipeline: ruff + pytest --cov≥80% + build Docker (<5min) |
| **Testes** | pytest + pytest-cov + pytest-asyncio | Cobertura ≥80% (RNF06) |
| **Lint/Format** | ruff + black + mypy | Fast, unified tooling |
| **Auth** | python-jose (JWT) + passlib (bcrypt salt=12) | Seguro, standard |

---

## Justificativas Técnicas

### 1. Alinhamento com Requisitos Não-Funcionais Explícitos
- **RNF03/RNF12** exigem **MySQL InnoDB** explicitamente → board-roadmap-0001-roadmap-canon atende, doc-readme-0001-readme-canon usa PostgreSQL
- **RF17** exige **ReportLab (Python)** para PDF server-side → board-roadmap-0001-roadmap-canon atende, doc-readme-0001-readme-canon não especifica
- **RNF04** exige **Desktop-only ≥1024px** → Vanilla JS + Tailwind é mais KISS que React + shadcn/ui

### 2. Adequação Acadêmica (FATEC ADS)
- Python/FastAPI tem curva de aprendizado menor que TypeScript/NestJS full-stack
- Equipe de 5 integrantes, prazo de 30 dias → menor complexidade operacional
- Stack 100% FOSS, zero dependências pagas

### 3. Princípios Constitdoc-arch-0006-uc-v1ionais
- **Art. 3.1 (KISS)**: "escopo enxuto, dados mockados via seed, UI desktop-first" → Vanilla JS atende melhor
- **Art. 3.7 (YAGNI)**: "nenhuma abstração para depois" → React + NestJS adiciona abstrações desnecessárias
- **Art. 1.2**: "FOSS 100%, LGPD primária, CPU-local" → Ambas atendem, mas board-roadmap-0001-roadmap-canon é mais simples

### 4. Arquitetura de Camadas Ortogonais (spec-005)
- Docker Compose com redes `data` (interno, DB only) e `edge` (externo)
- Proxy nginx na porta 8380 roteia `/` → frontend, `/v1/` → backend
- Sem CORS necessário (mesma origem via proxy)

---

## Consequências

### Positivas
- ✅ Alinhamento total com RNFs explícitos do SSOT v3.2
- ✅ Menor complexidade: single language backend (Python), zero TypeScript build
- ✅ PDF server-side nativo com ReportLab (RF17)
- ✅ MySQL InnoDB nativo (RNF03, RNF12)
- ✅ Adequado ao prazo de 30 dias e equipe acadêmica
- ✅ Clean Architecture manual bem definida (domain/usecases/adapters/infrastrdoc-arch-0006-uc-v1ture)

### Negativas (Mitigadas)
- ⚠️ Clean Architecture não é nativa do FastAPI (vs NestJS) → **Mitigação**: Estrutura `domain/usecases/adapters/infrastrdoc-arch-0006-uc-v1ture` imposta por convenção e code review
- ⚠️ Menos tooling automático que NestJS → **Mitigação**: SQLAlchemy + Pydantic + ruff + mypy cobrem gaps
- ⚠️ Frontend sem React ecosystem → **Mitigação**: MVP desktop-first, Vanilla JS + Tailwind suficiente

---

## Rastreabilidade

- **Origem**: `board-roadmap-0001-roadmap-canon.md` (15/09/2026), `doc-state-of-art-0001-estado-da-arte-v1.0.md` (13/11/2026)
- **Requisitos**: SSOT v3.2 — `req-func-0001-requisitos-funcionais-canon.md`, `req-use-case-0001-casos-de-uso-canon.md`, `doc-arch-0001-camada-de-dados-canon.md`
- **Especificações SDD**: `.ai/specs/spec-004` a `spec-015`
- **Constituição**: `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` Art. 1.3, 3.1, 3.7, 5.1

---

## Aprovação

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| **CCB Chair / Proddoc-arch-0006-uc-v1t Owner** | [Nome] | _______________ | 13/11/2026 |
| **Tech Lead** | [Nome] | _______________ | 13/11/2026 |
| **Arquiteto de Software** | [Nome] | _______________ | 13/11/2026 |
| **Desenvolvedor Backend** | [Nome] | _______________ | 13/11/2026 |
| **Desenvolvedor Frontend** | [Nome] | _______________ | 13/11/2026 |

---

## Próximos Passos

1. ✅ Scaffold completo implementado (Docker, Backend, Frontend, Proxy, CI, Seed, Migrations)
2. ⏳ Implementar Use Cases (Auth, Listas, Catálogo, Comparação, Exportação)
3. ⏳ Implementar testes unitários ≥80% + integração
4. ⏳ Implementar testes E2E com Playwright (incluído no MVP)
5. ⏳ Demo final + Documentação

---

**Fim da ADR-001**  
*Ratificada pelo CCB em 13/11/2026 — Lei suprema do repositório (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 2)*