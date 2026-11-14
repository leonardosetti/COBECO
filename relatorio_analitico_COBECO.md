# 📋 RELATÓRIO ANALÍTICO — COBECO MVP Acadêmico v3.1

**Documento de Decisão Arquitetural (ADR) Consolidado**
**Data:** 12 de Setembro de 2026
**Versão:** 3.1 (Final — SSOT)
**Classificação:** Documento de Governança Técnica
**Status:** ✅ APROVADO para Implementação
**Público-Alvo:** Equipe de Desenvolvimento, QA, Product Owner (Professor), Stakeholders Acadêmicos

---

## 📑 SUMÁRIO EXECUTIVO

Este documento consolida **todas as decisões arquiteturais** do projeto COBECO — Cotação de Bens de Consumo — após duas rodadas analíticas de refinamento. O relatório serve como **Single Source of Truth (SSOT)** para a implementação do MVP Acadêmico em 30 dias.

**Decisão Central:** Aplicar rigorosamente os princípios **KISS** (Keep It Simple, Stupid), **YAGNI** (You Aren't Gonna Need It) e **SDD** (Specification-Driven Development) em uma stack minimalista (HTML/JS + Python/FastAPI + SQLite3), mantendo Clean Architecture em 4 camadas e ACID via SQLite3 WAL mode.

**Entregáveis do MVP:**

- ✅ 8 tabelas no SQLite3 - Revisão, usar o SGBD MySql (incluindo pivô `supplier_categories`)
- ✅ 16 Requisitos Funcionais (RF01–RF16) + 10 Requisitos Não Funcionais (RNF01–RNF10)
- ✅ 6 ADRs formais aprovados
- ✅ 4 Camadas de Clean Architecture
- ✅ 30 dias de desenvolvimento em 5 sprints
- ✅ Cobertura de testes ≥80%

---

## 1. DECISÕES ARQUITETURAIS CONSOLIDADAS (ADRs)

### 1.1 Matriz de Aprovação dos ADRs

| ADR               | Decisão                                             | Status                  | Princípio        | Esforço |
| ----------------- | ---------------------------------------------------- | ----------------------- | ----------------- | -------- |
| **ADR-001** | Frontend Vanilla JS + ES6 Modules                    | ✅ APROVADO             | KISS + YAGNI      | Baixo    |
| **ADR-002** | Backend FastAPI (Python 3.12)                        | ✅ APROVADO             | SDD + KISS        | Baixo    |
| **ADR-003** | SQLite3 com WAL Mode - Revisão usar o SGBD MySql    | ✅ APROVADO             | KISS + ACID       | Zero     |
| **ADR-004** | JWT Stateless (access memória + refresh httpOnly)   | ✅ APROVADO COM AJUSTES | KISS + Segurança | Médio   |
| **ADR-005** | Export CSV Client-Side (Blob)                        | ✅ APROVADO             | KISS + YAGNI      | Baixo    |
| **ADR-006** | Recuperação de Senha — Dupla Via (log + pergunta) | ✅ APROVADO COM AJUSTES | KISS + YAGNI      | Baixo    |

### 1.2 Detalhamento dos ADRs

#### 🔵 ADR-001: Frontend sem Framework

| Aspecto                  | Detalhe                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **Contexto**       | MVP acadêmico, sem necessidade de reatividade complexa                                                                 |
| **Decisão**       | HTML5 + CSS3 + Tailwind (CDN) + Vanilla JS com ES6 Modules (`type="module"`)                                          |
| **Justificativa**  | Zero build step, zero npm, zero bundler. Aprendizado máximo. Deploy trivial.                                           |
| **Consequências** | Código mais verboso, sem reatividade automática. Compensado com funções`render()` explícitas.                    |
| **Estrutura**      | 8 módulos ES6:`app.js`, `state.js`, `api.js`, `auth.js`, `list.js`, `compare.js`, `export.js`, `ui.js` |

#### 🔵 ADR-002: Backend com FastAPI

| Aspecto                  | Detalhe                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **Contexto**       | Python + OpenAPI-first (SDD nativo)                                                        |
| **Decisão**       | FastAPI como framework web, Pydantic para validação                                      |
| **Justificativa**  | Gera OpenAPI automaticamente em`/openapi.json`. Async nativo. Mais KISS que Django.      |
| **Consequências** | Clean Architecture não é enforceada pelo framework — disciplina manual via code review. |
| **Estrutura**      | 4 camadas:`domain/` → `usecases/` → `adapters/` → `routers/`                    |

#### 🔵 ADR-003: SQLite3 com WAL Mode

| Aspecto                  | Detalhe                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| **Contexto**       | Banco simples, ACID, sem servidor externo                                                     |
| **Decisão**       | SQLite3 com`PRAGMA journal_mode=WAL` e `PRAGMA foreign_keys=ON`                           |
| **Justificativa**  | KISS máximo. Zero configuração. ACID suportado. Adequado para single-user/low-concurrency. |
| **Consequências** | Single-writer. Sem tipos ENUM. Arquivo único (volume Docker obrigatório).                   |
| **Configuração** | `busy_timeout=5000`, `row_factory=sqlite3.Row`, volume `./data:/app/data`               |

#### 🔵 ADR-004: JWT Stateless com Ajustes de Segurança

| Aspecto                         | Detalhe                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Contexto**              | API stateless, sem tabela de sessões, sem Redis                                                       |
| **Decisão**              | JWT via`python-jose`: Access Token (15min, em memória JS) + Refresh Token (7 dias, cookie httpOnly) |
| **Justificativa**         | Stateless = alinhado com Clean Architecture. YAGNI para Redis.                                         |
| **Ajustes de Segurança** | Access em memória (não localStorage) → imune a XSS. Refresh com`SameSite=Strict` → imune a CSRF. |
| **Rate Limiting**         | 6 tentativas consecutivas → lockout 15min (anti-DDoS)                                                 |

#### 🔵 ADR-005: Export Client-Side

| Aspecto                  | Detalhe                                                                  |
| ------------------------ | ------------------------------------------------------------------------ |
| **Contexto**       | Export CSV deve funcionar para visitantes (sem login)                    |
| **Decisão**       | Geração 100% no frontend via`Blob` + `URL.createObjectURL()`       |
| **Justificativa**  | KISS. Funciona para listas efêmeras e salvas. Zero carga no backend.    |
| **Consequências** | UTF-8 + BOM nativo. Delimitador`;`. Sem endpoint de export no backend. |

#### 🔵 ADR-006: Recuperação de Senha — Dupla Via

| Aspecto                  | Detalhe                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **Contexto**       | MVP acadêmico sem serviço de email                                                       |
| **Decisão**       | Via A: Token logado no stdout (dev). Via B: Pergunta de segurança (produção acadêmica) |
| **Justificativa**  | KISS + utilizável em demo real. Toggle via`RECOVERY_MODE` env var.                      |
| **Consequências** | Documentar como limitação conhecida. Não utilizável em produção real.                |

---

## 2. MODELO DE DADOS FINAL — DER v3.1

### 2.1 Correção Conceitual Crítica

> **⚠️ Mudança Fundamental:** Categorias são classificações **MACRO de FORNECEDORES**, não de produtos. Um fornecedor (ex: Leroy Merlin) pode pertencer a múltiplas categorias (Material de Construção, Ferramentas, Jardinagem, Decoração).

### 2.2 Diagrama Entidade-Relacionamento (v3.1)

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ username (UQ)       │
│ email (UQ)          │
│ name                │
│ password_hash       │
│ security_question   │
│ security_answer_hash│
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │ 1:N
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│       lists         │         │    list_items       │
├─────────────────────┤         ├─────────────────────┤
│ id (PK)             │◄───1:N──┤ id (PK)             │
│ user_id (FK)        │         │ list_id (FK)        │
│ name                │         │ product_id (FK)     │
│ created_at          │         │ quantity            │
│ updated_at          │         │ created_at          │
│ deleted_at          │         └──────────┬──────────┘
└─────────────────────┘                    │ N:1
                                           ▼
                                  ┌─────────────────────┐
                                  │      products       │
                                  ├─────────────────────┤
                                  │ id (PK)             │
                                  │ name                │
                                  │ unit                │
                                  │ active              │
                                  │ created_at          │
                                  └──────────┬──────────┘
                                             │ 1:N
                                             ▼
                                  ┌─────────────────────┐
                                  │ supplier_products   │
                                  ├─────────────────────┤
                                  │ supplier_id (FK)    ├──┐
                                  │ product_id (FK)     │  │
                                  │ price               │  │
                                  │ stock               │  │
                                  │ active              │  │
                                  └─────────────────────┘  │
                                                           │ N:1
┌─────────────────────┐                                    │
│     categories      │                                    │
├─────────────────────┤                                    │
│ id (PK)             │                                    │
│ name (UQ)           │                                    │
│ description         │                                    │
└──────────┬──────────┘                                    │
           │                                               │
           │ N:N                                           │
           ▼                                               │
┌─────────────────────┐                                    │
│ supplier_categories │                                    │
│    (TABELA PIVÔ)    ├────────────────────────────────────┘
├─────────────────────┤
│ supplier_id (FK)    │
│ category_id (FK)    │
└──────────┬──────────┘
           │ N:1
           ▼
┌─────────────────────┐
│     suppliers       │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ cnpj (UQ)           │
│ active              │
│ created_at          │
└─────────────────────┘
```

### 2.3 Especificação das 8 Tabelas

| Tabela                  | Campos                                                                                                    | Constraints                                 | Seed                         |
| ----------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ---------------------------- |
| `users`               | id, username, email, name, password_hash, security_question, security_answer_hash, created_at, updated_at | UNIQUE(username), UNIQUE(email)             | 1 admin                      |
| `lists`               | id, user_id, name, created_at, updated_at, deleted_at                                                     | FK(user_id) CASCADE, soft delete            | —                           |
| `list_items`          | id, list_id, product_id, quantity                                                                         | FK(list_id), FK(product_id), CHECK(qty > 0) | —                           |
| `categories`          | id, name, description                                                                                     | UNIQUE(name)                                | **5 categorias macro** |
| `suppliers`           | id, name, cnpj, active, created_at                                                                        | UNIQUE(cnpj)                                | **10 fornecedores**    |
| `supplier_categories` | supplier_id, category_id                                                                                  | PK(supplier_id, category_id), FKs           | **~20 relações N:N** |
| `products`            | id, name, unit, active, created_at                                                                        | —                                          | **50 produtos**        |
| `supplier_products`   | supplier_id, product_id, price, stock, active                                                             | PK(supplier_id, product_id), FKs            | **~300 preços**       |

### 2.4 Seed de Dados — Exemplo

```python
# Categorias MACRO (para fornecedores)
categories = [
    "Supermercado",
    "Material de Construção",
    "Hardware e Informática",
    "Roupas e Calçados",
    "Lojas de Departamento"
]

# Fornecedores com múltiplas categorias (N:N)
suppliers = [
    {"name": "Mercado Bom", "cnpj": "11.222.333/0001-44",
     "categories": ["Supermercado"]},
    {"name": "Leroy Merlin", "cnpj": "22.333.444/0001-55",
     "categories": ["Material de Construção", "Hardware e Informática"]},
    {"name": "Magazine Luiza", "cnpj": "33.444.555/0001-66",
     "categories": ["Lojas de Departamento", "Hardware e Informática"]},
    # ... até 10 fornecedores
]

# Produtos (agnósticos à categoria)
products = [
    {"name": "Arroz Tipo 1 5kg", "unit": "un"},
    {"name": "Martelo de Unha 25mm", "unit": "un"},
    {"name": "Notebook i5 8GB", "unit": "un"},
    # ... até 50 produtos
]
```

---

## 3. STACK TECNOLÓGICA DEFINITIVA

### 3.1 Matriz de Tecnologias

| Camada             | Tecnologia                                               | Versão       | Justificativa             |
| ------------------ | -------------------------------------------------------- | ------------- | ------------------------- |
| **Frontend** | HTML5 + CSS3 + Tailwind (CDN) + Vanilla JS (ES6 modules) | —            | KISS + YAGNI              |
| **Backend**  | Python + FastAPI + Pydantic + Pydantic-Settings          | 3.12 / 0.110+ | SDD nativo                |
| **Banco**    | SQLite3 (WAL mode)                                       | 3.45+         | ACID + zero config        |
| **Auth**     | python-jose (JWT) + bcrypt                               | Latest        | Stateless + seguro        |
| **Export**   | Blob + URL.createObjectURL() (client-side)               | —            | KISS                      |
| **CI/CD**    | Docker + Docker Compose + GitHub Actions                 | Latest        | Reprodutibilidade         |
| **Seed**     | Script Python no entrypoint do container                 | —            | 10 forn + 50 prod + 5 cat |
| **Kanban**   | GitHub Projects (5 colunas)                              | —            | Gestão ágil             |
| **Testes**   | pytest + pytest-cov                                      | Latest        | Cobertura ≥80%           |
| **Lint**     | ruff                                                     | Latest        | Qualidade de código      |

### 3.2 Diagrama da Stack

```
┌─────────────────────────────────────────────────────┐
│              BROWSER (Desktop ≥1024px)              │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │  HTML5   │  │ Tailwind │  │  JS (ES6 Modules) │  │
│  │  (Telas) │  │  (CDN)   │  │  (Lógica + DOM)   │  │
│  └─────┬────┘  └────┬─────┘  └────────┬──────────┘  │
│        └────────────┼─────────────────┘             │
│                     │ fetch()                       │
└─────────────────────┼───────────────────────────────┘
                      │ HTTP/JSON
                      ▼
┌─────────────────────────────────────────────────────┐
│                 DOCKER CONTAINER                    │
│  ┌──────────────────────────────────────────────┐   │
│  │              FastAPI (Python 3.12)           │   │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────────┐  │   │
│  │  │ Routers │ │ UseCases │ │   Domain      │  │   │
│  │  │ (API)   │ │ (Logic)  │ │   (Entities)  │  │   │
│  │  └────┬────┘ └────┬─────┘ └───────┬───────┘  │   │
│  │       └───────────┼───────────────┘          │   │
│  │                   │                          │   │
│  │  ┌────────────────▼────────────────────────┐ │   │
│  │  │     Adapters (sqlite3 / Pydantic)       │ │   │
│  │  └────────────────┬────────────────────────┘ │   │
│  └───────────────────┼──────────────────────────┘   │
│                      │                              │
│  ┌───────────────────▼───────────────────────────┐  │
│  │          SQLite3 (cobeco.db + WAL)            │  │
│  │   users | lists | list_items | products |     │  │
│  │   suppliers | prices | categories |           │  │
│  │   supplier_categories                         │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 4. ESTRUTURA DE CÓDIGO — CLEAN ARCHITECTURE

### 4.1 Layout de Diretórios

```
cobeco/
├── docker-compose.yml
├── Dockerfile
├── Makefile                    # seed, test, run, lint
├── README.md
├── .env.example
│
├── frontend/                   # Servido como static files pelo FastAPI
│   ├── index.html              # Tela de entrada: Criar Lista
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html          # Minhas Listas
│   ├── compare.html            # Seleção + Comparação
│   ├── profile.html
│   ├── css/
│   │   └── style.css           # Customizações + @media print
│   └── js/
│       ├── app.js              # Entry point + router simples
│       ├── state.js            # AppState + sessionStorage
│       ├── api.js              # fetch() wrappers (consome OpenAPI)
│       ├── auth.js             # Login/logout/register
│       ├── list.js             # CRUD de listas
│       ├── compare.js          # Seleção + motor de comparação
│       ├── export.js           # CSV via Blob
│       └── ui.js               # Toasts, modais, render helpers
│
├── backend/
│   ├── main.py                 # FastAPI app + CORS + static mount
│   ├── config.py               # Settings via pydantic-settings
│   │
│   ├── domain/                 # 🟢 Camada de Domínio (pura, sem deps)
│   │   ├── entities.py         # Dataclasses: User, List, Product, Supplier
│   │   ├── rules.py            # Regras de negócio puras
│   │   └── exceptions.py       # Domain exceptions
│   │
│   ├── usecases/               # 🔵 Camada de Casos de Uso
│   │   ├── auth_usecase.py     # Login, register, logout, recovery
│   │   ├── list_usecase.py     # CRUD de listas
│   │   ├── compare_usecase.py  # Motor de comparação
│   │   └── export_usecase.py   # Geração de CSV (se backend)
│   │
│   ├── adapters/               # 🟡 Camada de Adaptadores
│   │   ├── database.py         # sqlite3 connection + WAL
│   │   ├── repositories.py     # CRUD operations (Repository pattern)
│   │   ├── schemas.py          # Pydantic models (request/response)
│   │   └── security.py         # bcrypt, JWT, rate limiter
│   │
│   ├── routers/                # 🔴 Camada de Framework (API)
│   │   ├── auth_router.py      # POST /auth/login, /auth/register
│   │   ├── list_router.py      # CRUD /api/lists
│   │   ├── compare_router.py   # POST /api/compare
│   │   └── catalog_router.py   # GET /api/products, /api/suppliers
│   │
│   ├── seed.py                 # Script de seed (10 forn + 50 prod + 5 cat)
│   └── tests/                  # pytest
│       ├── test_auth.py
│       ├── test_list.py
│       ├── test_compare.py
│       ├── test_domain_rules.py
│       └── conftest.py
│
├── openapi/
│   └── openapi.json            # Exportado via /openapi.json
│
└── .github/
    ├── workflows/
    │   └── ci.yml              # lint → test → build
    └── projects/               # Kanban configurado
```

### 4.2 Regras de Clean Architecture

| Camada             | Pode depender de   | Não pode depender de       |
| ------------------ | ------------------ | --------------------------- |
| **Domain**   | Nada (pura)        | UseCases, Adapters, Routers |
| **UseCases** | Domain             | Adapters, Routers           |
| **Adapters** | Domain, UseCases   | Routers                     |
| **Routers**  | UseCases, Adapters | Domain diretamente          |

---

## 5. PLANO DE IMPLEMENTAÇÃO — 30 DIAS

### 5.1 Cronograma de Sprints

| Sprint       | Dias   | Foco                     | Entregáveis                                                            | RFs              |
| ------------ | ------ | ------------------------ | ----------------------------------------------------------------------- | ---------------- |
| **S1** | 1–6   | Setup + Auth             | Docker, seed, OpenAPI, login/cadastro/logout, recuperação (dupla via) | RF01–RF04       |
| **S2** | 7–12  | Listas + Catálogo       | CRUD listas, autocomplete, persistência, categorias de fornecedores    | RF06–RF10       |
| **S3** | 13–18 | Comparação             | Seleção fornecedores (por categoria), motor flat, resultados          | RF11–RF15       |
| **S4** | 19–24 | Export + Perfil + Polish | CSV client-side, impressão, perfil, testes 80%                         | RF05, RF16, RF17 |
| **S5** | 25–30 | Buffer + Demo            | Bug fixes, documentação, apresentação, deploy                       | Todos            |

### 5.2 Kanban — GitHub Projects (5 Colunas)

| Coluna                  | Labels               | Critério de Entrada           | Critério de Saída       |
| ----------------------- | -------------------- | ------------------------------ | ------------------------- |
| 📋**Backlog**     | `P1`, `P2`       | Requisito aprovado no SSOT     | Priorizado para sprint    |
| 🎯**Sprint**      | `P0`, `sprint-N` | Sprint planning realizado      | Desenvolvimento iniciado  |
| 🔨**In Progress** | `in-progress`      | Branch criada (`feat/UC-XX`) | PR aberto                 |
| 👀**Review**      | `review`           | PR aberto + CI verde           | Aprovado por ≥1 reviewer |
| ✅**Done**        | `done`             | Merge em`main`               | Deploy em staging         |

### 5.3 Convenções de Branch

| Tipo    | Padrão             | Exemplo                     |
| ------- | ------------------- | --------------------------- |
| Feature | `feat/UC-XX-nome` | `feat/UC-09-cadastro`     |
| Fix     | `fix/issue-XX`    | `fix/issue-12-rate-limit` |
| Docs    | `docs/nome`       | `docs/openapi-spec`       |
| Release | `release/vX.Y`    | `release/v1.0`            |

---

## 6. MATRIZ DE RISCOS E MITIGAÇÕES

### 6.1 Riscos Técnicos

| #  | Risco                                   | Prob.  | Impacto | Mitigação                                             |
| -- | --------------------------------------- | ------ | ------- | ------------------------------------------------------- |
| R1 | Vanilla JS vira "spaghetti"             | Alta   | Médio  | Módulos ES6 + funções puras + code review            |
| R2 | SQLite3 corrompe                        | Baixa  | Alto    | WAL mode + volume Docker + backup diário               |
| R3 | JWT access token vazado                 | Média | Alto    | Expiry curto (15min) + memória (não localStorage)     |
| R4 | Categoria mal interpretada              | Média | Médio  | Documentação clara: "categorias são de FORNECEDORES" |
| R5 | Recuperação de senha não utilizável | Alta   | Baixo   | Dupla via (log + pergunta de segurança)                |
| R6 | Clean Architecture não respeitada      | Média | Alto    | Code review rigoroso + lint rules                       |
| R7 | Alunos não conhecem Python             | Média | Alto    | FastAPI é intuitivo;`/docs` automático              |

### 6.2 Riscos de Escopo

| #   | Risco                            | Prob.  | Impacto | Mitigação                                         |
| --- | -------------------------------- | ------ | ------- | --------------------------------------------------- |
| R8  | Scope creep (novos RFs)          | Alta   | Alto    | SSOT congelado; mudanças via ADR complementar      |
| R9  | Prazo estourado                  | Média | Alto    | Sprint 5 como buffer; P1 cortável                  |
| R10 | Professora exige "mais robustez" | Baixa  | Alto    | Clean Architecture + testes 80% + OpenAPI compensam |

---

## 7. RECOMENDAÇÕES OPERACIONAIS

### 7.1 ✅ Fazer (Aprovar Imediatamente)

| # | Ação                                                                              | Responsável | Justificativa                 |
| - | ----------------------------------------------------------------------------------- | ------------ | ----------------------------- |
| 1 | **Implementar DER v3.1** com tabela pivô `supplier_categories`             | Dev + DBA    | Alinhamento com domínio real |
| 2 | **Adotar todos os ADRs** com ajustes propostos                                | Tech Lead    | Consistência arquitetural    |
| 3 | **Estruturar frontend em módulos ES6** (um módulo por funcionalidade)       | Frontend Dev | KISS + manutenibilidade       |
| 4 | **Usar Pydantic para TODA validação** (request/response/entidades)          | Backend Dev  | Type-safety + SDD             |
| 5 | **Documentar OpenAPI antes de implementar** cada endpoint (SDD)               | Arquiteto    | Contrato antes do código     |
| 6 | **Testes unitários ≥80%** focados em regras de negócio (domain + usecases) | QA + Dev     | Qualidade garantida           |
| 7 | **Criar repositório GitHub + Project Kanban**                                | Tech Lead    | Gestão ágil                 |
| 8 | **Setup Docker Compose + FastAPI skeleton**                                   | Dev          | Reprodutibilidade             |

### 7.2 ⚠️ Fazer com Disciplina

| # | Ação                                                       | Guard-Rail           | Consequência se Violado |
| - | ------------------------------------------------------------ | -------------------- | ------------------------ |
| 1 | **Clean Architecture em 4 camadas**                    | Code review rigoroso | PR rejeitado             |
| 2 | **Parameterized queries em TODAS operações sqlite3** | Zero exceções      | Vulnerabilidade SQLi     |
| 3 | **JWT access em memória** (não localStorage)         | Segurança           | Vulnerabilidade XSS      |
| 4 | **Rate limiting** em todos endpoints sensíveis        | Auth, recovery       | Vulnerabilidade DDoS     |
| 5 | **Contrato OpenAPI escrito ANTES** de implementar      | SDD                  | Retrabalho               |
| 6 | **Módulos ES6** — um módulo por tela/funcionalidade | Frontend             | Código bagunçado       |

### 7.3 ❌ Evitar (YAGNI)

| #  | Item                                                         | Justificativa                                        |
| -- | ------------------------------------------------------------ | ---------------------------------------------------- |
| 1  | **React, Vue, Angular** ou qualquer framework frontend | MVP acadêmico não precisa de virtual DOM           |
| 2  | **ORM pesado** (SQLAlchemy)                            | Usar sqlite3 stdlib + Repository pattern             |
| 3  | **Redis, Memcached** ou qualquer cache externo         | SQLite3 WAL é suficiente                            |
| 4  | **Serviço de email** para recuperação de senha      | Dupla via (log + pergunta)                           |
| 5  | **Microserviços**                                     | Monólito modular é suficiente                      |
| 6  | **Suporte mobile**                                     | Desktop-only (≥1024px)                              |
| 7  | **TypeScript no frontend**                             | Stack já simplificada; Pydantic no backend compensa |
| 8  | **BDD/E2E tests** no MVP                               | Testes unitários 80% são suficientes               |
| 9  | **PDF nativo**                                         | Impressão via navegador + CSV                       |
| 10 | **Persistência de comparações**                     | Apenas listas são persistidas                       |

---

## 8. CRITÉRIOS DE ACEITE DO MVP

### 8.1 Critérios Funcionais

| #  | Critério                                                                            | Verificação      |
| -- | ------------------------------------------------------------------------------------ | ------------------ |
| C1 | Usuário consegue criar lista, selecionar fornecedores, comparar e ver melhor oferta | Demo ao vivo       |
| C2 | Fluxo completo (cadastro → comparação) em <5 minutos                              | Cronometrado       |
| C3 | Export CSV funciona para visitantes E autenticados                                   | Teste manual       |
| C4 | Impressão otimizada para A4 via Ctrl+P                                              | Teste manual       |
| C5 | Rate limiting bloqueia após 6 tentativas                                            | Teste automatizado |

### 8.2 Critérios Técnicos

| #   | Critério                                      | Métrica             |
| --- | ---------------------------------------------- | -------------------- |
| C6  | Cobertura de testes ≥80%                      | `pytest --cov`     |
| C7  | API <500ms p95                                 | `curl + time`      |
| C8  | Zero vulnerabilidades críticas (OWASP Top 10) | Code review          |
| C9  | ACID garantido (zero dados órfãos)           | Teste de transação |
| C10 | OpenAPI 100% documentado                       | `/docs` acessível |

### 8.3 Critérios de Qualidade

| #   | Critério                                     | Verificação  |
| --- | --------------------------------------------- | -------------- |
| C11 | Clean Architecture respeitada                 | Code review    |
| C12 | Parameterized queries em 100% das operações | Grep + review  |
| C13 | JWT access em memória (não localStorage)    | Code review    |
| C14 | Seed popula DB em <10s                        | `make seed`  |
| C15 | Pipeline CI <5min                             | GitHub Actions |

---

## 9. PRÓXIMOS PASSOS IMEDIATOS

### 9.1 Checklist de Aprovação

| # | Ação                                             | Responsável | Prazo    | Status |
| - | -------------------------------------------------- | ------------ | -------- | ------ |
| 1 | Aprovar este relatório (ADR consolidado)          | Stakeholders | Dia 1    | ⏳     |
| 2 | Criar repositório GitHub + Project Kanban         | Tech Lead    | Dia 1    | ⏳     |
| 3 | Gerar contrato OpenAPI 3.0 (SDD)                   | Arquiteto    | Dia 2–3 | ⏳     |
| 4 | Setup Docker Compose + FastAPI skeleton            | Dev          | Dia 2–3 | ⏳     |
| 5 | Implementar`seed.py` (10 forn + 50 prod + 5 cat) | Dev          | Dia 3–4 | ⏳     |
| 6 | Novo Diagrama de Casos de Uso (XML Draw.io)        | Arquiteto    | Dia 4–5 | ⏳     |
| 7 | Novo DER (XML Draw.io)                             | Arquiteto    | Dia 5–6 | ⏳     |
| 8 | Protótipo de Baixa Fidelidade (9 telas)           | UX/Dev       | Dia 6–7 | ⏳     |

### 9.2 Artefatos Pendentes

| Artefato                           | Formato          | Status      |
| ---------------------------------- | ---------------- | ----------- |
| Diagrama de Casos de Uso v3.1      | XML Draw.io      | ⏳ Pendente |
| DER v3.1                           | XML Draw.io      | ⏳ Pendente |
| Diagrama de Transição de Estados | XML Draw.io      | ⏳ Pendente |
| Protótipo de Baixa Fidelidade     | Figma/Excalidraw | ⏳ Pendente |
| Contrato OpenAPI 3.0               | JSON             | ⏳ Pendente |
| README.md                          | Markdown         | ⏳ Pendente |

---

## 10. GOVERNANÇA E COMUNICAÇÃO

### 10.1 Papéis e Responsabilidades

| Papel                               | Responsabilidade                             |
| ----------------------------------- | -------------------------------------------- |
| **Product Owner (Professor)** | Aprovar escopo, validar entregas, demo final |
| **Tech Lead**                 | Code review, decisões técnicas, mentoring  |
| **Arquiteto de Software**     | ADRs, DER, UCD, OpenAPI                      |
| **Dev Frontend**              | HTML/CSS/JS, módulos ES6, UX                |
| **Dev Backend**               | FastAPI, SQLite3, regras de negócio         |
| **QA**                        | Testes unitários, cobertura 80%             |

### 10.2 Rituais Ágeis

| Ritual          | Frequência     | Duração |
| --------------- | --------------- | --------- |
| Daily Standup   | Diário         | 15min     |
| Sprint Planning | Semanal (sexta) | 1h        |
| Sprint Review   | Semanal (sexta) | 15min     |
| Retrospectiva   | Semanal (sexta) | 30min     |

### 10.3 Canais de Comunicação

- **GitHub:** Repositório oficial + Issues + Projects (Kanban)
- **GitHub Actions:** CI/CD pipeline
- **WhatsApp:** Grupo do projeto para comunicação rápida
- **Documentação:** README.md + `/docs` (Swagger)

---

## 11. CONCLUSÃO E APROVAÇÃO

### 11.1 Síntese das Decisões

✅ **DER v3.1** com tabela pivô `supplier_categories` — categorias são de FORNECEDORES (N:N)
✅ **Stack minimalista** — HTML/JS + Python/FastAPI + SQLite3 + Docker
✅ **6 ADRs aprovados** com ajustes de segurança e usabilidade
✅ **Clean Architecture** em 4 camadas com disciplina rigorosa
✅ **SDD** via OpenAPI nativo do FastAPI
✅ **ACID** via SQLite3 WAL mode
✅ **30 dias** de desenvolvimento em 5 sprints
✅ **8 tabelas** no banco de dados
✅ **16 RFs + 10 RNFs** cobertos
✅ **Kanban** no GitHub Projects

### 11.2 Princípios Aplicados

| Princípio                   | Como foi aplicado                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| **KISS**               | Stack simples, zero frameworks, zero cache externo, zero microserviços                 |
| **YAGNI**              | Sem email real, sem PDF nativo, sem mobile, sem BDD, sem persistência de comparações |
| **SDD**                | OpenAPI antes do código, Pydantic para validação, contratos versionados              |
| **Clean Architecture** | 4 camadas ortogonais, dependência apenas para dentro                                   |
| **ACID**               | SQLite3 WAL + transações explícitas + foreign keys                                   |

### 11.3 Veredito Final

> **O projeto COBECO MVP Acadêmico v3.1 está PRONTO para implementação.**
>
> Todas as decisões arquiteturais foram validadas, os riscos identificados e mitigados, e o cronograma é realista para 30 dias de desenvolvimento.
>
> A stack minimalista (HTML/JS + Python/FastAPI + SQLite3) combinada com Clean Architecture rigorosa e SDD via OpenAPI garante:
>
> - ✅ Aprendizado máximo para MVP acadêmico
> - ✅ Qualidade técnica (testes 80%, ACID, segurança)
> - ✅ Entregabilidade (30 dias, 5 sprints)
> - ✅ Demonstrabilidade (1 comando: `docker compose up`)

---

## 12. ASSINATURAS DE APROVAÇÃO

| Papel                                               | Nome                      | Data                 | Status        |
| --------------------------------------------------- | ------------------------- | -------------------- | ------------- |
| **Product Owner (THAIS CRISTINA CASAGRANDE)** | _________________________ | ___/___/2026 | ⏳ Aguardando |
| **Tech Lead**                                 | _________________________ | ___/___/2026 | ⏳ Aguardando |
| **Arquiteto de Software**                     | _________________________ | ___/___/2026 | ⏳ Aguardando |
| **Dev Frontend**                              | _________________________ | ___/___/2026 | ⏳ Aguardando |
| **Dev Backend**                               | _________________________ | ___/___/2026 | ⏳ Aguardando |

---

> *"A simplicidade é a sofisticação suprema."* — Leonardo da Vinci
>
> *"Make it work, make it right, make it fast."* — Kent Beck
>
> *"You aren't gonna need it."* — Ron Jeffries

---

**FIM DO RELATÓRIO ANALÍTICO FINAL — COBECO MVP Acadêmico v3.1**

**Próxima Ação Imediata:** Aprovação deste documento e início da Sprint 1 (Setup + Auth).
