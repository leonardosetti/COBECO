# COBECO MVP — Comparação de Preços para Listas de Compras

[![CI](https://github.com/leonardosetti/COBECO/actions/workflows/config-ci-0001-github-actions-v1.0.yml/badge.svg)](https://github.com/leonardosetti/COBECO/actions/workflows/config-ci-0001-github-actions-v1.0.yml)
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

**Stack:**

| Camada             | Tecnologia                                               |
| ------------------ | -------------------------------------------------------- |
| **Frontend** | Vanilla JS ES6+, Tailwind CSS, Playwright (E2E)          |
| **Backend**  | FastAPI 0.115, SQLAlchemy 2.0, Pydantic 2.10             |
| **Database** | MySQL 8.0 (InnoDB), driver aiomysql/pymysql              |
| **Auth**     | JWT (HS256), bcrypt (salt=12), cookies httpOnly          |
| **PDF**      | ReportLab (server-side)                                  |
| **Proxy**    | nginx (reverse proxy, TLS ready)                         |
| **CI/CD**    | GitHub Actions (ruff + pytest + coverage + Docker build) |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      COBECO MVP                             │
├────────────────────────────────────┬────────────────────────┤
│  Frontend (Vanilla JS + Tailwind)  │  Backend (FastAPI)     │
│  http://localhost:8380             │  http://localhost:8000 │
│  - SPA Router                      │  - Clean Architecture  │
│  - Tailwind CSS                    │  - Domain/UseCase/Repo │
│  - Playwright E2E Tests            │  - PostgreSQL/MySQL    │
└─────────────────────────────┬──────┴────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   MySQL 8.0       │
                    │   (InnoDB)        │
                    └───────────────────┘
```

---

## 🚀 Execução Local (Docker Compose — recomendado)

Este é o caminho mais simples e o que garante replicabilidade para terceiros. Tudo sobe com um único comando.

### Pré-requisitos

- [Docker](https://docs.docker.com/engine/install/) 24+
- [Docker Compose](https://docs.docker.com/compose/install/) 2+
- [Git](https://git-scm.com/)

### Passos

```bash
# 1. Clonar o repositório
git clone https://github.com/leonardosetti/COBECO.git
cd COBECO

# 2. Criar o arquivo de variáveis de ambiente (obrigatório)
cp config-env-0001-env-example-v1.0.example .env
# (Opcional) edite o .env para ajustar SECRET_KEY, senhas do MySQL, etc.

# 3. Subir a stack completa (MySQL + migrações + seed + backend + frontend + proxy)
docker compose -f config-docker-0001-docker-compose-v1.0.yml up -d --build

# 4. Aguardar os serviços ficarem saudáveis (aguardar ~30s)
docker compose -f config-docker-0001-docker-compose-v1.0.yml ps

# 5. Verificar saúde
curl http://localhost:8380/health
# → "healthy"
```

### Acessos após subir

| Serviço                        | URL                                                                         |
| ------------------------------- | --------------------------------------------------------------------------- |
| **Frontend**              | http://localhost:8380                                                       |
| **API (Swagger/OpenAPI)** | http://localhost:8380/openapi.json                                          |
| **Backend direto**        | http://localhost:8000/docs                                                  |
| **Health Check**          | http://localhost:8380/health                                                |
| **MySQL**                 | localhost:3306 (usuário: `cobeco`, senha: `cobeco`, banco: `cobeco`) |

### Comandos úteis

```bash
# Ver logs de todos os serviços
docker compose -f config-docker-0001-docker-compose-v1.0.yml logs -f

# Parar containers (mantém dados do banco no volume)
docker compose -f config-docker-0001-docker-compose-v1.0.yml down

# Parar e APAGAR o volume do banco (destroi dados)
docker compose -f config-docker-0001-docker-compose-v1.0.yml down -v

# Reconstruir e subir do zero
docker compose -f config-docker-0001-docker-compose-v1.0.yml up -d --build
```

---

## 💻 Execução Local (Desenvolvimento sem Docker)

Se preferir rodar localmente sem containers, você precisará de MySQL 8.0 rodando na máquina.

### Backend

```bash
cd backend

# Criar ambiente virtual
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -e ".[dev]"

# Criar .env do backend (baseado no exemplo)
cp ../config-env-0001-env-example-v1.0.example .env
# edite DATABASE_URL para apontar ao seu MySQL local

# Rodar migrações
alembic upgrade head

# Aplicar seed (dados determinísticos)
mysql -u cobeco -p cobeco < seed.sql

# Iniciar o servidor
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

O frontend é estático (Vanilla JS + CSS). Sirva os arquivos de `frontend/src/` com qualquer servidor estático, por exemplo:

```bash
cd frontend/src
# Com Python 3
python3 -m http.server 8380
# Ou com Node (serve/npx serve, etc.)
```

O proxy nginx encaminha `/` para o frontend e `/v1/` para o backend. Sem o proxy, ajuste a base URL da API no `frontend/src/app.js`.

---

## 🧪 Testes

### Backend (Unit + Integration + Contract)

```bash
cd backend
source .venv/bin/activate   # ou use o container
pip install -e ".[dev]"

# Todos os testes com cobertura (falha se abaixo de 80%)
pytest tests/unit tests/integration tests/contract -v --tb=short --cov=src --cov-fail-under=80

# Apenas unitários
pytest tests/unit -v

# Apenas integração (requer MySQL rodando)
pytest tests/integration -v
```

### Frontend (E2E — Playwright)

```bash
cd frontend/tests/e2e
npm install
npx playwright install --with-deps
npx playwright test --project=chromium
```

Os E2Es exigem o stack (backend + frontend) rodando em `http://localhost:8380`.

---

## 📦 Estrutura do Projeto

```
COBECO/
├── .github/workflows/ci.yml          # CI/CD Pipeline (GitHub Actions)
├── config-docker-0001-docker-compose-v1.0.yml   # Orquestração Docker
├── config-env-0001-env-example-v1.0.example     # Exemplo de variáveis de ambiente
├── config-make-0001-makefile-v1.0                # Makefile (atalhos de dev)
├── README.md                                       # Este arquivo
├── SPECS.md                                        # Especificações técnicas v3.3 (SSOT)
├── backend/
│   ├── src/                                        # Código fonte (domain, adapters, main)
│   ├── alembic/                                    # Migrações do banco
│   ├── seed.sql                                    # Seed determinístico
│   ├── scripts/                                    # Scripts de geração de seed
│   ├── tests/                                      # Testes unit, integration, contract, security
│   ├── pyproject.toml                              # Dependências Python
│   └── config-docker-0003-backend-dockerfile-v1.0 # Dockerfile do backend
├── frontend/
│   ├── src/                                        # app.js, index.html, styles
│   ├── tests/e2e/                                  # Testes E2E Playwright
│   └── config-docker-0004-frontend-dockerfile-v1.0 # Dockerfile do frontend
├── proxy/
│   ├── config-nginx-0003-proxy-nginx-v1.0.conf    # Reverse proxy nginx
│   └── Dockerfile                                  # Dockerfile do proxy
└── docs/                                           # Documentação adicional (ADRs, etc.)
```

---

## 📋 Requisitos Implementados (18 RFs)

| ID   | Requisito                                                                     | Status |
| ---- | ----------------------------------------------------------------------------- | ------ |
| RF01 | Cadastrar Usuário                                                            | ✅     |
| RF02 | Login (JWT + Refresh, lockout 6/15min)                                        | ✅     |
| RF03 | Logout                                                                        | ✅     |
| RF04 | Recuperar Senha                                                               | ✅     |
| RF05 | Visualizar Perfil                                                             | ✅     |
| RF06 | Editar Perfil                                                                 | ✅     |
| RF07 | Criar Lista (memória + autocomplete)                                         | ✅     |
| RF08 | Salvar/Promover Lista                                                         | ✅     |
| RF09 | Listar Minhas Listas                                                          | ✅     |
| RF10 | Editar Lista                                                                  | ✅     |
| RF11 | Excluir Lista (Soft Delete)                                                   | ✅     |
| RF12 | Selecionar Categorias                                                         | ✅     |
| RF13 | Selecionar Fornecedores                                                       | ✅     |
| RF14 | Filtrar Disponibilidade                                                       | ✅     |
| RF15 | Calcular Orçamento                                                           | ✅     |
| RF16 | Visualizar Resultados (melhor oferta: maior cobertura; empate → menor total) | ✅     |
| RF17 | Exportar PDF (Lista Vencedora — todos, sem login)                            | ✅     |
| RF18 | Impressão @media print                                                       | ✅     |

**Fluxo de visitante (Autenticação Tardia):** o visitante percorre todos os passos sem login: Categorias → Lista (em `sessionStorage`) → Fornecedores → Comparação → Lista Vencedora → PDF. O login é exigido apenas para salvar a lista na conta (RF08).

Endpoints públicos:

- `POST /v1/comparacao/calcular-efemera` — orçamento a partir de itens em memória (sem auth)
- `POST /v1/export/pdf/vencedora` — PDF da Lista Vencedora (sem auth, itens inline)

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do repositório (exemplo em `config-env-0001-env-example-v1.0.example`):

| Variável                       | Descrição                  | Obrigatório | Padrão    |
| ------------------------------- | ---------------------------- | ------------ | ---------- |
| `SECRET_KEY`                  | Chave JWT (mín. 32 chars)   | ✅           | —         |
| `DATABASE_URL`                | URL MySQL (aiomysql/asyncmy) | ✅           | —         |
| `MYSQL_ROOT_PASSWORD`         | Senha root do MySQL          | ✅           | —         |
| `MYSQL_DATABASE`              | Nome do banco                | ✅           | `cobeco` |
| `MYSQL_USER`                  | Usuário do banco            | ✅           | `cobeco` |
| `MYSQL_PASSWORD`              | Senha do usuário do banco   | ✅           | —         |
| `JWT_ALGORITHM`               | Algoritmo JWT (HS256)        | ✅           | `HS256`  |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração access token     | ✅           | `15`     |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Expiração refresh token    | ✅           | `7`      |
| `RECOVERY_MODE`               | `log` ou `email`         | ✅           | `log`    |
| `NGINX_PORT`                  | Porta do proxy               | ❌           | `8380`   |

**Importante:** o arquivo `.env` está no `.gitignore` e nunca deve ser commitado. Cada desenvolvedor cria o seu próprio localmente.

---

## 📜 Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

- **Leonardo Setti** — *Tech Lead / Arquiteto* — [@leonardosetti](https://github.com/leonardosetti)
- **Equipe FATEC Taquaritinga** — *ADS 2026*

---

## 📚 Documentação Adicional

- [Especificações Técnicas (SPECS.md v3.3, SSOT)](SPECS.md)
- [Plano de Implementação MVP](doc-plan-0001-plano-implementacao-mvp-canon.md)
- [Roadmap (S1–S5)](board-roadmap-0001-roadmap-canon.md)
- [Constituição do Projeto](constitution-0001-constitution-canon.md)
- [Casos de Uso e Requisitos](doc-analysis-0001-analise-requisitos-casos-uso-v1.0.md)

---

**Última atualização:** 2026-11-24
**Versão:** 0.1.0 (MVP)

---

## ❓ Este projeto é replicável localmente por terceiros?

**Sim.** O projeto é replicável localmente por terceiros por meio de **Docker Compose**, que é o caminho suportado e recomendado.

### O que garante a replicabilidade

| Item                                   | Status       | Comentário                                                                        |
| -------------------------------------- | ------------ | ---------------------------------------------------------------------------------- |
| `docker-compose.yml`                 | ✅ Trackado  | Orquestra MySQL + migrações + seed + backend + frontend + proxy                  |
| Dockerfiles (backend, frontend, proxy) | ✅ Trackados | Imagens self-contained                                                             |
| Seed SQL (`backend/seed.sql`)        | ✅ Trackado  | Popula o banco com dados determinísticos (11 cat, 10 forn, 50 prod, ~300 preços) |
| Migrações Alembic                    | ✅ Trackadas | `alembic upgrade head` cria o schema automaticamente                             |
| `.env.example`                       | ✅ Trackado  | Modelo para o `.env` local (não versionado)                                     |
| `.gitignore`                         | ✅ Trackado  | Impede commit de segredos e artefatos de build                                     |

### O que o terceiro precisa providenciar

1. **Docker + Docker Compose** instalados na máquina.
2. **Criar o arquivo `.env`** a partir de `config-env-0001-env-example-v1.0.example` (o `.env` é gitignorado; cada desenvolvedor gera o seu).
3. **Portas livres:** `8380` (proxy), `8000` (backend direto), `3306` (MySQL).

### Comandos de replicação (do `git clone` ao funcionando)

```bash
git clone https://github.com/leonardosetti/COBECO.git
cd COBECO
cp config-env-0001-env-example-v1.0.example .env
docker compose -f config-docker-0001-docker-compose-v1.0.yml up -d --build
curl http://localhost:8380/health   # → "healthy"
```

### Limitações / pontos de atenção

- O arquivo `.env` não está versionado (por segurança). Sem ele, variáveis como `SECRET_KEY` ficam vazias e a autenticação JWT pode falhar. **Sempre crie o `.env` antes de subir.**
- O volume `db_data` persiste dados entre reiniciar. Para limpar tudo e recomeçar do zero: `docker compose -f config-docker-0001-docker-compose-v1.0.yml down -v`.
- O frontend é desktop-only (RNF04: ≥1024px, sem mobile).
- A CI roda em Ubuntu (GitHub Actions). Em Windows, recomenda-se Docker Desktop com WSL2.

Se não quiser usar Docker, a replicação manual exige instalar MySQL 8.0, Python 3.11 e configurar o backend manualmente — caminho possível, mas não é o fluxo principal documentado.
