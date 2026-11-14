---
id: doc-readme-0001-readme-canon
type: doc-readme
title: DOC README — Readme
version: '3.2'
status: ratificado
canonical: true
canonical_slug: readme
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
domain: documentation
layer: documentation
tags: []
lgpd_class: n/a
workflow:
  stage: ratificado
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# 🛒 COBECO - Cotação de Bens de Consumo (MVP)

**Sistema de Comparação de Preços para Listas de Compras**  
_Projeto acadêmico da disciplina de Laboratório de Engenharia de Software_  
_FATEC Taquaritinga - Análise e Desenvolvimento de Sistemas_

---

## 📖 Sobre o Projeto

### O Problema

Comparar preços manualmente entre múltiplos fornecedores é uma tarefa demorada, repetitiva e propensa a erros. Para piorar, nem sempre um único fornecedor possui todos os produtos desejados, forçando o consumidor a fracionar suas compras e perder tempo recalculando totais.

### A Solução

O **COBECO** é um MVP (Produto Mínimo Viável) que automatiza esse processo. Trata-se de uma aplicação web desktop-first que permite ao usuário:

1. **Criar listas de compras** personalizadas com itens, quantidades e categorias
2. **Submeter essas listas** a um motor de comparação que cruza os dados com um catálogo interno de fornecedores (populado via seed)
3. **Visualizar orçamentos consolidados** em uma tabela comparativa clara e objetiva
4. **Identificar lacunas** — o sistema destaca quais produtos estão faltando em cada fornecedor
5. **Tomar a melhor decisão** com base no menor custo consolidado
6. **Exportar para PDF** (ReportLab server-side) ou imprimir otimizado

### Por que esse MVP é único?

Diferente de ferramentas complexas que dependem de web scraping ou APIs externas em tempo real, o COBECO adota uma abordagem **pragmática e realista**:

- ✅ **Dados mockados via seed** — foco 100% na lógica de negócio
- ✅ **Motor de comparação simplificado** — tabela flat ao invés de agrupamentos complexos
- ✅ **Stack moderna e FOSS** — FastAPI, MySQL, Vanilla JS, Docker
- ✅ **Clean Architecture** — separação clara de responsabilidades
- ✅ **SDD (Specification-Driven Development)** — API-first com OpenAPI

---

## 🎯 Objetivos do Projeto

### Objetivo Geral

Desenvolver um MVP funcional e minimalista que automatize a comparação de preços entre fornecedores a partir de listas de compras criadas pelo usuário, fornecendo orçamentos claros e evidenciando produtos ausentes em cada cenário.

### Objetivos Específicos (Entregáveis do MVP)

- ✅ Implementar autenticação segura (cadastro, login, recuperação de senha)
- ✅ Permitir CRUD completo de listas de compras (criar, editar, excluir, listar)
- ✅ Manter um cadastro interno de fornecedores, categorias e produtos (via seed)
- ✅ Desenvolver o motor de comparação que gera tabela flat com disponibilidade e preços
- ✅ Exibir comparativos destacando o melhor orçamento e os produtos faltantes
- ✅ Garantir a persistência dos dados em banco relacional (MySQL 8 InnoDB)
- ✅ Estabelecer comunicação robusta entre Frontend e Backend via API RESTful (OpenAPI)
- ✅ Exportar listas para PDF (ReportLab) e impressão otimizada

---

## ⚙️ Premissas e Restrições Fundamentais

| Pilar | Aplicação no Projeto |
|-------|---------------------|
| 🧼 **KISS (Keep It Simple)** | Escopo enxuto: dados mockados (sem APIs externas), UI exclusiva para desktop, lógica de negócio direta |
| 🏛️ **Clean Architecture** | Separação rígida entre Domínio, Casos de Uso, Adaptadores e Frameworks |
| ⚡ **ACID** | Operações no banco de dados garantem Atomicidade, Consistência, Isolamento e Durabilidade (MySQL InnoDB) |
| 📐 **SDD (Spec-Driven)** | API RESTful definida via OpenAPI antes da implementação (API-First) |
| 🧪 **Qualidade** | Testes unitários críticos com cobertura >80%, CI/CD básico no GitHub Actions |
| 📦 **Containerização** | Frontend, Backend e Banco de Dados rodam em containers Docker isolados |
| 📊 **Metodologia Ágil** | Desenvolvimento guiado por quadro Kanban para visualizar o fluxo de tarefas |

---

## 🧩 Principais Funcionalidades (Escopo MVP)

### Módulo de Autenticação

- Cadastro de novos usuários (nome_usuario, nome, email, senha, pergunta de segurança)
- Login/Logout seguro com JWT (access 15min memória + refresh 7 dias cookie httpOnly)
- Recuperação de senha via pergunta de segurança ou token no stdout (modo dev)

### Módulo de Listas de Compras

- CRUD completo: Criação, edição, exclusão e listagem com paginação
- Adição de itens com campos: Produto (autocomplete), Quantidade
- Lista efêmera em memória (sessionStorage) promovida ao banco após login

### Módulo de Fornecedores e Catálogo (Seed)

- Dados populados automaticamente na inicialização do sistema
- 10 fornecedores + 50 produtos com preços variáveis (±20%)
- 11 categorias MACRO com relacionamento N:N (fornecedor ↔ categorias)

### Módulo de Comparação de Preços

- Pré-filtro por categorias (checkboxes)
- Seleção de fornecedores com % de disponibilidade
- Slider de disponibilidade mínima (0-100%)
- Motor de cálculo: tabela flat (disponíveis, ausentes, preço total)
- Ordenação por preço ASC com destaque verde na melhor oferta

### Módulo de Exportação

- Exportação para PDF (UTF-8, A4, ReportLab server-side) — funciona sem login
- Impressão otimizada via navegador (CSS `@media print`)

---

## 🛠️ Stack Tecnológica (FOSS - Gratuita e Open Source)

| Camada | Tecnologias | Motivo da Escolha |
|--------|-------------|-------------------|
| **Frontend** | Vanilla JS ES6+ + Tailwind CSS + nginx | Zero build runtime, desktop-first, leve, FOSS |
| **Backend** | Python 3.11 + FastAPI + Pydantic + SQLAlchemy | Clean Architecture manual, OpenAPI automático, tipagem forte |
| **Banco de Dados** | MySQL 8.0 InnoDB | ACID, utf8mb4, engine InnoDB (RNF03, RNF12) |
| **ORM / Migrations** | SQLAlchemy 2.0 + Alembic | Async, type-safe, migrations versionadas |
| **PDF Generation** | ReportLab | Server-side, A4, <5s para 100 itens (RF17, RNF11) |
| **API** | RESTful + OpenAPI (Swagger) | Contratos claros entre Front e Back (SDD) |
| **Infraestrutura** | Docker 24 + Docker Compose 2 | Isolamento dos serviços, reprodutibilidade |
| **CI/CD** | GitHub Actions | Pipeline automatizado: ruff + pytest --cov + build |
| **Testes** | pytest + pytest-cov + pytest-asyncio | Cobertura ≥80% (RNF06) |
| **Lint/Format** | ruff + black + mypy | Fast, unified tooling |
| **Auth** | python-jose (JWT) + passlib (bcrypt salt=12) | Seguro, standard |

---

## 🏗️ Arquitetura Geral (Docker Compose)

```
┌─────────────────────────────────────────────────────────────────┐
│                        DOCKER NETWORKS                          │
├──────────────────────────┬──────────────────────────────────────┤
│       DATA (interno)     │         EDGE (externo)               │
│  ┌─────────────────┐     │  ┌───────────┐  ┌───────────────┐   │
│  │      DB         │     │  │  BACKEND  │  │   FRONTEND    │   │
│  │   MySQL 8.0     │◄────┤  │ FastAPI   │  │  Vanilla JS   │   │
│  │   Porta: 3306   │     │  │ Porta:8000│  │   nginx:80    │   │
│  └─────────────────┘     │  └─────┬─────┘  └───────┬───────┘   │
│                          │        │               │            │
│                          │        └───────┬───────┘            │
│                          │                ▼                    │
│                          │        ┌───────────────┐            │
│                          │        │    PROXY      │            │
│                          │        │   nginx:8080  │            │
│                          │        │  / -> frontend│            │
│                          │        │  /v1/ -> back │            │
│                          │        └───────────────┘            │
└──────────────────────────┴──────────────────────────────────────┘
```

- **Frontend** (nginx) serve arquivos estáticos + SPA fallback
- **Backend** (FastAPI) aplica regras de negócio e acessa DB via SQLAlchemy async
- **Banco de Dados** (MySQL) armazena usuários, listas, fornecedores, produtos e preços
- **Seed** executado automaticamente na subida do container DB
- **Proxy** (nginx) roteia `/` para frontend e `/v1/` para backend — **sem CORS** (mesma origem)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Docker 24+ e Docker Compose 2+
- Make (opcional, para comandos padronizados)
- Git

### Passos Rápidos

```bash
# 1. Clone o repositório
git clone https://github.com/leonardosetti/COBECO.git
cd COBECO

# 2. Copie o arquivo de variáveis de ambiente
cp config-env-0001-env-example-v1.0.example config-env-0001-env-example-v1.0
# Edite config-env-0001-env-example-v1.0 e preencha NVIDIA_NIM_API_KEY e GITHUB_TOKEN

# 3. Suba os containers (desenvolvimento com hot reload)
make up
# ou: docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml up -d --build

# 4. Acesse a aplicação no navegador
# Frontend + Proxy: http://localhost:8080
# Backend API:      http://localhost:8080/v1/
# Swagger Docs:     http://localhost:8080/v1/docs

# 5. (Opcional) Execute os testes
make test
# ou: docker compose exec backend pytest -v --cov=src --cov-fail-under=80
```

**Nota:** O banco de dados já será populado com fornecedores, categorias e produtos de exemplo assim que subir (via `seed.sql` automático).

---

## 📋 Comandos Úteis (config-make-0001-makefile-v1)

```bash
make up           # Sobe ambiente dev com hot reload
make down         # Para containers
make logs         # Logs de todos os serviços
make test         # Roda testes backend (pytest)
make test-cov     # Testes com cobertura
make lint         # Lint (ruff)
make lint-fix     # Lint com auto-fix
make format       # Formata (black)
make type-check   # Type checking (mypy)
make migrate      # Roda migrações Alembic
make seed         # Executa seed SQL baseline
make seed-generate # Regenera backend/config-seed-0001-seed-v1.0.sql a partir da fonte canônica
make seed-expanded SEED_EXPANDED_CONFIRM=SIM # Seed expandido (destrutivo no mock local)
make db-reset     # Reset completo do banco (CUIDADO)
make frontend-build  # Build Tailwind CSS
make ci           # Simula pipeline CI local
make clean        # Limpeza total (containers, volumes, imagens)
make health       # Verifica saúde dos serviços
```

---

## 📋 Escopo: O que NÃO está incluso (Out of Scope)

Para manter o KISS e entregar dentro do prazo (30 dias), os seguintes itens estão deliberadamente fora do escopo desta versão:

- ❌ Integração com APIs reais de e-commerce ou web scraping
- ❌ Desenvolvimento de aplicativos mobile nativos (Android/iOS)
- ❌ Processamento de pagamentos ou intermediação financeira
- ❌ Cálculo de fretes ou roteirização logística
- ❌ Suporte a múltiplos idiomas ou moedas (apenas BRL)
- ❌ Autenticação via OAuth (Google/Facebook)
- ❌ BDD/E2E tests completos (apenas unitários críticos)
- ❌ PWA / Service Workers

---

## 🧠 Princípios de Desenvolvimento Adotados

| Princípio | Aplicação no Projeto |
|-----------|---------------------|
| **UI/UX Desktop-First** | Interface otimizada para telas ≥1024px, feedback visual claro (spinners, skeletons, toasts) |
| **Clean Code** | Código legível, nomenclatura significativa (PT-BR), funções com responsabilidade única |
| **Clean Architecture** | Separação entre Domínio, Casos de Uso, Adaptadores e Frameworks |
| **ACID** | Garantia de atomicidade, consistência, isolamento e durabilidade nas operações de banco |
| **SDD (Spec-Driven)** | Contratos OpenAPI definidos antes do desenvolvimento |
| **CI/CD** | Pipeline automatizado no GitHub Actions para validar builds e execução de testes |
| **Kanban** | Gestão do projeto com quadro Kanban (GitHub Projects) para visualização do fluxo |

---

## 📅 Cronograma e Status Atual

| Fase | Duração | Status | Entregas |
|------|---------|--------|----------|
| **Fase 1: Setup e Infra** | 3 dias | 🟢 Concluída | Docker, DB, Seed, CI, Scaffold |
| **Fase 2: Backend Core** | 10 dias | ⏳ Em andamento | Auth, Listas, Catálogo, Comparação |
| **Fase 3: Frontend Core** | 10 dias | ⏳ Aguardando | Views, Autocomplete, Comparação, PDF |
| **Fase 4: Testes e Refinamento** | 5 dias | ⏳ Aguardando | Cobertura ≥80%, Polish, Bugs |
| **Fase 5: Deploy e Validação** | 2 dias | ⏳ Aguardando | Demo, Docs finais, Apresentação |
| **TOTAL** | **30 dias** | 🚩 **Data Limite: 13/11/2026** | |

**Metodologia de Gestão:** Kanban (GitHub Projects)  
**Rituais:** Daily Standup (19:00), Sprint Planning/Review/Retrospectiva (sextas-feiras)

---

## 📂 Estrutura do Projeto

```
COBECO/
├── .github/workflows/          # CI/CD GitHub Actions
├── .ai/                        # SDD: specs, handoffs, agents, workflows
├── backend/                    # FastAPI + SQLAlchemy + Alembic
│   ├── src/
│   │   ├── domain/             # Entidades, Value Objects, Repositories (interfaces)
│   │   ├── usecases/           # Casos de uso puros (Clean Architecture)
│   │   ├── adapters/           # API (FastAPI), DB (SQLAlchemy), External
│   │   └── infrastrdoc-arch-0006-uc-v1ture/     # Config, Security, External services
│   ├── tests/                  # Unit + Integration tests
│   ├── scripts/                # Fonte canônica e gerador do seed
│   ├── alembic/                # Migrations
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── seed.sql                # Dados mockados (10 forn, 50 prod, 11 cat)
│   └── Dockerfile
├── frontend/                   # Vanilla JS + Tailwind + nginx
│   ├── src/
│   │   ├── app.js              # SPA router + state + API client
│   │   ├── styles/input.css    # Tailwind directives
│   │   └── index.html
│   ├── nginx.conf              # Produção
│   ├── nginx.dev.conf          # Desenvolvimento
│   ├── config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json
│   └── Dockerfile
├── proxy/                      # nginx reverse proxy
│   └── nginx.conf
├── config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml          # Produção
├── config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml # Desenvolvimento (hot reload)
├── config-make-0001-makefile-v1                    # Comandos padronizados
├── config-env-0001-env-example-v1.0.example                # Template variáveis ambiente
├── .gitignore
├── doc-readme-0001-readme-canon.md                   # Este arquivo
├── constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md             # Lei suprema do projeto
├── doc-agents-0001-agents-canon.md                   # Estado do repo e convenções
├── req-func-0001-requisitos-funcionais-canon.md               # SSOT v3.2 (18 RFs)
├── req-use-case-0001-casos-de-uso-canon.md               # SSOT v3.2 (29 UCs)
├── doc-arch-0001-camada-de-dados-canon.md            # SSOT v3.2 (8 tabelas PT-BR)
├── board-roadmap-0001-roadmap-canon.md            # Roadmap Kanban + DoD
└── doc-state-of-art-0001-estado-da-arte-v1.0.md # Análise completa do projeto
```

---

## 🔐 Segurança e Compliance

- **Zero segredos no repo**: `config-env-0001-env-example-v1.0.example` sem valores reais, `.gitignore` rigoroso
- **LGPD**: Apenas dados sintéticos no seed; sem PII real
- **Auth**: bcrypt salt=12, JWT access em memória, refresh httpOnly+SameSite=Strict
- **Rate limiting**: 6 req/15min por IP + username
- **Validação**: Pydantic em todas as fronteiras HTTP
- **Erros**: Nunca expõem tracebacks, payloads ou dados financeiros
- **CORS**: Não necessário (proxy same-origin)

---

## 📝 Licenças e Compliance

Todas as tecnologias utilizadas são **FOSS** (Free and Open Source Software):

- **FastAPI, Starlette, Uvicorn**: MIT
- **SQLAlchemy, Alembic**: MIT
- **Pydantic**: MIT
- **MySQL**: GPL (community edition)
- **ReportLab**: BSD
- **Tailwind CSS**: MIT
- **nginx**: BSD-2-Clause
- **Docker**: Apache 2.0
- **GitHub Actions**: Free para repos públicos

---

## 🚀 Próximos Passos

1. ✅ Scaffold completo: Docker, DB, Backend, Frontend, Proxy, CI
2. ⏳ Implementar Use Cases de Autenticação (UC09-UC12, UC16, UC18)
3. ⏳ Implementar Use Cases de Listas (UC01, UC14, UC15, UC17, UC13)
4. ⏳ Implementar Use Cases de Catálogo (UC02, UC03, UC04, UC05)
5. ⏳ Implementar Use Cases de Comparação (UC06, UC07)
6. ⏳ Implementar Exportação PDF (UC08, UC09)
7. ⏳ Frontend: Views, Autocomplete, Comparação, PDF
8. ⏳ Testes unitários ≥80% + CI passing
9. ⏳ Demo final + Documentação

---

## 📞 Contato e Governança

**Canais de Comunicação:**

- **WhatsApp:** [#COBECO-MVP](https://chat.whatsapp.com/LV33cRZKwFAAoaPljTcvLx)
- **Documentação:** [GitHub](https://github.com/leonardosetti/COBECO)
- **Email:** TBD

**Equipe:**

- **Proddoc-arch-0006-uc-v1t Owner:** [Nome do Stakeholder]
- **Tech Lead:** [Nome do Desenvolvedor Sênior]
- **Arquiteto de Software:** [Nome do Arquiteto]

---

**Este doc-readme-0001-readme-canon é um documento vivo e será atualizado conforme o progresso do desenvolvimento.**

**Última atualização:** 13 de Novembro de 2026  
**Stack definida:** FastAPI + MySQL + Vanilla JS (board-roadmap-0001-roadmap-canon ratificado pelo CCB)