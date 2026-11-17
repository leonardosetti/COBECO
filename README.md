# COBECO MVP — Comparação de Preços para Listas de Compras

[![CI](https://github.com/leonardosetti/COBECO/actions/workflows/ci.yml/badge.svg)](https://github.com/leonardosetti/COBECO/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Playwright](https://img.shields.io/badge/playwright-1.65+-orange.svg)](https://playwright.dev/)
[![Ruff](https://img.shields.io/badge/ruff-passing-brightgreen.svg)](https://github.com/astral-sh/ruff)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](https://github.com/leonardosetti/COBECO/actions)

---

## 📋 Visão Geral

**COBECO** (Comparação de Bens de Consumo) é um MVP de comparação de preços para listas de compras, desenvolvido como projeto acadêmico da **FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas**.

Permite criar listas de compras, filtrar fornecedores por categoria, comparar preços em tempo real e exportar resultados em PDF.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      COBECO MVP                              │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vanilla JS + Tailwind)  │  Backend (FastAPI)     │
│  http://localhost:8380             │  http://localhost:8000  │
│  - SPA Router                      │  - Clean Architecture   │
│  - Tailwind CSS                    │  - Domain/UseCase/Repo  │
│  - Playwright E2E Tests            │  - PostgreSQL/MySQL     │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   MySQL 8.0       │
                    │   (InnoDB)        │
                    └───────────────────┘
```

---

## 🚀 Quick Start

### Pré-requisitos
- Docker 24+ / Docker Compose 2+
- Git
- (Opcional) Python 3.11+, Node 20+ para desenvolvimento local

### Subir a Stack Completa

```bash
# Clonar
git clone https://github.com/leonardosetti/COBECO.git
cd COBECO

# Subir containers (MySQL + Backend + Frontend + Proxy)
docker compose -f config-docker-0001-docker-compose-v1.0.yml up -d --build

# Verificar saúde
curl http://localhost:8380/health
# → "healthy"
```

### Acessos
| Serviço | URL |
|---------|-----|
| **Frontend** | http://localhost:8380 |
| **API (Swagger)** | http://localhost:8380/openapi.json |
| **Backend Direto** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8380/health |

---

## 🧪 Testes

### Backend (Unit + Integration)

```bash
cd backend
source .venv/bin/activate  # ou python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Unit tests (146 testes)
pytest tests/unit/ -v --cov=src --cov-fail-under=80

# Integration tests (requer MySQL rodando)
pytest tests/integration/ -v
```

### Frontend (E2E - Playwright)

```bash
cd frontend/tests/e2e
cp config-npm-0001-package-v1.0.json package.json
npm install --ignore-scripts
npx playwright test --project=chromium
```

---

## 📦 Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| **Frontend** | Vanilla JS ES6+, Tailwind CSS, Playwright |
| **Backend** | FastAPI 0.115, SQLAlchemy 2.0, Pydantic 2.10 |
| **Database** | MySQL 8.0 (InnoDB), asyncmy driver |
| **Auth** | JWT (HS256), bcrypt (salt=12), httpOnly cookies |
| **PDF** | ReportLab (server-side) |
| **Proxy** | nginx (reverse proxy, TLS ready) |
| **CI/CD** | GitHub Actions (ruff + pytest + coverage + Docker build) |

---

## 📋 Requisitos Implementados (18 RFs)

| ID | Requisito | Status |
|----|-----------|--------|
| RF01 | Cadastrar Usuário | ✅ |
| RF02 | Login (JWT + Refresh, lockout 6/15min) | ✅ |
| RF03 | Logout | ✅ |
| RF04 | Recuperar Senha | ✅ |
| RF05 | Visualizar Perfil | ✅ |
| RF06 | Editar Perfil | ✅ |
| RF07 | Criar Lista (memória + autocomplete) | ✅ |
| RF08 | Salvar/Promover Lista | ✅ |
| RF09 | Listar Minhas Listas | ✅ |
| RF10 | Editar Lista | ✅ |
| RF11 | Excluir Lista (Soft Delete) | ✅ |
| RF12 | Selecionar Categorias | ✅ |
| RF13 | Selecionar Fornecedores | ✅ |
| RF14 | Filtrar Disponibilidade | ✅ |
| RF15 | Calcular Orçamento | ✅ |
| RF16 | Visualizar Resultados (melhor oferta: maior cobertura; empate → menor total) | ✅ |
| RF17 | Exportar PDF (Lista Vencedora — todos, sem login) | ✅ |
| RF18 | Impressão @media print | ✅ |

### Fluxo de visitante (Autenticação Tardia — SPECS §7)
O visitante percorre **todos** os passos sem login: Categorias → Lista (em `sessionStorage`) → Fornecedores → Comparação → Lista Vencedora → PDF. O login é exigido apenas para **salvar** a lista na conta (RF08). Endpoints públicos:
- `POST /v1/comparacao/calcular-efemera` — orçamento a partir de itens em memória (sem auth)
- `POST /v1/export/pdf/vencedora` — PDF da Lista Vencedora (sem auth, itens inline)

---

## 📁 Estrutura do Projeto

```
COBECO/
├── .github/workflows/ci.yml          # CI/CD Pipeline
├── .ai/specs/                        # Specs ratificadas (CCB-001)
├── backend/
│   ├── src/
│   │   ├── domain/                   # Entidades, Repositories, UseCases
│   │   ├── adapters/                 # API Routes, DB Models
│   │   ├── config.py                 # Pydantic Settings
│   │   └── main.py                   # FastAPI App
│   ├── tests/unit/                   # 146 testes unitários
│   ├── tests/integration/            # Testes de integração
│   └── alembic/                      # Migrations
├── frontend/
│   ├── src/
│   │   ├── app.js                    # SPA Router + Views + API Client
│   │   ├── styles/input.css          # Tailwind + @media print
│   │   └── index.html
│   └── tests/e2e/                    # Playwright E2E Tests
├── proxy/
│   └── config-nginx-0003-proxy-nginx-v1.0.conf
├── config-docker-0001-docker-compose-v1.0.yml
└── README.md
```

---

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `SECRET_KEY` | Chave JWT (mín. 32 chars) | ✅ |
| `DATABASE_URL` | URL MySQL (asyncmy) | ✅ |
| `JWT_ALGORITHM` | Algoritmo JWT (HS256) | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração access token | ✅ |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Expiração refresh token | ✅ |
| `RECOVERY_MODE` | `log` ou `email` | ✅ |

---

## 📜 Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

- **Leonardo Setti** — *Tech Lead / Arquiteto* — [@leonardosetti](https://github.com/leonardosetti)
- **Equipe FATEC Taquaritinga** — *ADS 2026*

---

## 📚 Documentação Adicional

- [Especificações Técnicas (.ai/specs/)](.ai/specs/)
- [Decisões de Arquitetura (ADRs)](docs/decisoes/)
- [Plano de Implementação MVP](doc-plan-0001-plano-implementacao-mvp-canon.md)
- [Roadmap (S1–S5)](board-roadmap-0001-roadmap-canon.md)
- [Constituição do Projeto](constitution-0001-constitution-canon.md)

---

**Última atualização:** 2026-11-16  
**Versão:** 0.1.0 (MVP)