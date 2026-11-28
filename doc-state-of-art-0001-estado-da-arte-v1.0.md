---
id: doc-state-of-art-0001-estado-da-arte-v1.0
type: doc-state
title: DOC STATE — Art 0001 Estado Da Arte
version: v1.0
status: rascunho
canonical: false
canonical_slug: art-0001-estado-da-arte
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
domain: general
layer: artifact
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# RELATÓRIO DE ESTADO DA ARTE — COBECO MVP
**Data:** 13 de Novembro de 2026  
**Versão:** 1.0  
**Status:** Análise completa — pronto para tomada de decisão

---

## 1. RESUMO EXECUTIVO

O projeto **COBECO** (Cotação de Bens de Consumo) está na **fase de documentação/design (Fase 1: Setup e Infra)**. **Não existe código-fonte de aplicação** — apenas especificações, diagramas, docs ABNT e infraestrutura de agentes SDD.

### Conflito Crítico de Stack
| Fonte | Stack Proposta | Data |
|-------|----------------|------|
| `doc-readme-0001-readme-canon.md` | React 18 + TS + Vite + Tailwind + shadcn/ui (:8080), **Node.js 20 + NestJS 10** (:3000), **PostgreSQL 16 + Prisma 5** (:5432), Docker Compose, GitHub Actions, Jest + Vitest | 31/08/2026 |
| `board-roadmap-0001-roadmap-canon.md` | **FastAPI + Pydantic** backend, **MySQL 8 InnoDB**, pytest/ruff, ReportLab PDF export | 15/09/2026 |

**Decisão pendente:** O CCB (Change Control Board) deve ratificar qual stack implementar antes de qualquer scaffold.

---

## 2. ESTRUTURA SDD — VALIDAÇÃO E SANITIZAÇÃO

### 2.1 Hierarquia Normativa (Constitution.md Art. 2) — ✅ CONFORME
```
1. constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md (lei suprema) ✅
2. doc-agents-0001-agents-canon.md (estado do repo) ✅
3. req-func-0001-requisitos-funcionais-canon.md + req-use-case-0001-casos-de-uso-canon.md + doc-arch-0001-camada-de-dados-canon.md (SSOT v3.2) ✅
4. board-roadmap-0001-roadmap-canon.md + doc-readme-0001-readme-canon.md (planejamento) ⚠️ CONFLITO DE STACK
5. ADRs (docs/decisoes/) — não existem ainda
6. Especificações SDD (.ai/specs/) ✅ 15 specs ativas
7. Código-fonte — não existe
8. Arquivos de agente (.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/) ✅
```

### 2.2 Corpus de Specs SDD (.ai/specs/) — 15 specs ativas
| Spec | Título | Status | Versão | Origem |
|------|--------|--------|--------|--------|
| spec-001 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta | ratificada | 0.1.0 | TA-0002 |
| spec-002 | requisitos-review-round-1 | ratificada | 0.1.0 | TA-0003 |
| spec-003 | sdd-conf-memory | ratificada | 0.1.0 | TA-0004 |
| spec-004 | backend-mvp-v1 | ratificada | 0.1.0 | TA-0005 |
| spec-005 | container-layers-v1 | ratificada | 0.2.0 | TA-0029 |
| spec-006 | nfr-consolidados-v1 | ratificada | 0.1.0 | TA-0051 |
| spec-007 | invoice-data-model-v1 | ratificada | 0.1.0 | TA-0052 |
| spec-008 | frontend-web-responsive-v1 | ratificada | 0.1.0 | TA-0053 |
| spec-009 | uat-produto-v1 | ratificada | 0.1.0 | TA-0054 |
| spec-010 | qualidade-pdca-ishikawa-v1 | ratificada | 0.1.0 | TA-0055 |
| spec-011 | cicd-pipeline-v1 | ratificada | 0.1.0 | TA-0056 |
| spec-012 | rastreabilidade-prompts-sdd-v1 | ratificada | 0.1.0 | TA-0057 |
| spec-013 | documentacao-tecnica-v1 | ratificada | 0.1.0 | TA-0058 |
| spec-014 | runtime-agentes-ci-layers-v1 | ratificada | 0.1.0 | TA-0059 |
| spec-015 | lgpd-produto-proposta-v1 | draft (cond. CCB) | 0.1.0 | TA-0060 |

### 2.3 Artefatos Não-Specs em .ai/specs/ (requerem realocação)
- `input-canonico-v4.1.1.md` → **pinned/ambiguous** (ADR-011 imutável o classifica como spec)
- `requisitos.md` (0 B) → placeholder vazio
- `tap.md` (0 B) → placeholder vazio
- `eap.md` → documento vivo
- `MANIFEST.md` → auditoria de normalização
- `kb-taxonomy.md`, `afa-changelog.md` → conhecimento operacional
- `spec-adr-template.spec.md` → template

### 2.4 Handoffs — 56 catalogados (.ai/handoffs/INDEX.md)
Pipeline SDD funcional: `handoff → parser → dispatcher → orchestrator → agente`

### 2.5 Gaps SDD Identificados
| Gap | Descrição | Severidade |
|-----|-----------|------------|
| G-01 | Constitution cita `agent-orchestrator` (legacy) mas registry tem `agent-nexus-prime-ultimate` | Alta |
| G-02 | Co-assinatura humana pendente sem mecanismo de fechamento material | Alta |
| G-03 | Ausência de cláusula Docker/camadas ortogonais na Constitution | Média |
| G-04 | YAGNI e first-principles não codificados no Art. 3 | Média |
| — | ADRs (`docs/decisoes/`) não existem — necessário para decisões de stack | Crítica |

---

## 3. ARQUITETURA DE AGENTES — ANÁLISE COMPLETA

### 3.1 Roster SSOT (.ai/agents/config-registry-0001-registry-v1.0.yaml)
- **Orquestrador L0:** `agent-nexus-prime-ultimate` (promulgado)
- **Camadas:** L0 (orchestrator), L1 (leads), L2 (specialists), META (forge)
- **Agentes promulgados:** ~30+ agentes definidos
- **Dispatcher:** `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py` (usa sender legacy `agent-orchestrator` — **bug**)

### 3.2 Personas (.ai/personas/)
- `active.md` (symlink runtime), `coder.md`, `pm.md`, `reviewer.md`, `tester.md`, `_base.md`

### 3.3 Workflows (.ai/workflows/)
- `sdd-cycle.sh` v2 — ciclo canônico com validação fail-closed

### 3.4 SDDAI Engine (.ai/sddai/) — 5 submódulos Python
| Módulo | Função | Arquivos |
|--------|--------|----------|
| cobeco_sddai_cli | Pipeline unificado | main.py, cli.py |
| cobeco_sddai_loader | Ingestão de dados | ingest.py, cli.py |
| cobeco_sddai_engineer | Engenharia de features | transform.py, cli.py |
| cobeco_sddai_memory | Otimização de memória | optimizer.py, cli.py |
| cobeco_sddai_trainer | Treinamento de modelo | train.py, cli.py |

### 3.5 MCP Servers Configurados (.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc)
| Server | Tipo | Status |
|--------|------|--------|
| filesystem | local (npx) | ✅ Ativo |
| github | docker (ghcr.io/github/github-mcp-server) | ✅ Ativo |
| github-kanban | npx (@sunwood-ai-labs) | ✅ Ativo |
| github-remote | npx (@modelcontextprotocol/server-github) | ✅ Ativo |
| imagem | npx (mcp-image) | ✅ Ativo |
| memoria | npx (@modelcontextprotocol/server-memory) | ✅ Ativo |
| word-live | uvx (word-mcp-live) | ✅ Ativo |
| gsd | npx (@opengsd/gsd-core) | ✅ Ativo |

### 3.6 RAG/DAG Config (.ai/config/config-rag-dag-0001-rag-dag-config-v1.0.yaml)
```yaml
dag_nodes: [data_ingestion, preprocessing, vectorization, query_handling]
dependencies: preprocessing→data_ingestion, vectorization→preprocessing, query_handling→vectorization
model: qwen30b-moe (local, CPU-optimized)
```

### 3.7 Models Catalog (.ai/config/config-models-0001-models-catalog-v1.0.yaml)
```yaml
primary: Qwen3-30B-A3B Q4_K_M
fallback: Qwen 14B Q4_K_M
batch: Qwen 72B Q4_K_M
deprecated: Qwen3.8-27B Q4_K_M  ← **CONFLITA com config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc que usa qwen-32b local**
context_configured: 32768
context_effective: 24000
output_max: 4096
```

---

## 4. CONFIGURAÇÕES DE AMBIENTE — AUSÊNCIAS CRÍTICAS

| Arquivo | Status | Ação Requerida |
|---------|--------|----------------|
| `config-env-0001-env-example-v1.0.example` | **AUSENTE** | Criar com variáveis para stack escolhida |
| `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` | **AUSENTE** | Criar conforme stack ratificada |
| `Dockerfile` (frontend/backend) | **AUSENTE** | Criar conforme stack ratificada |
| `config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json` / `requirements.txt` / `pyproject.toml` | **AUSENTE** | Criar conforme stack ratificada |
| `.github/workflows/` | **AUSENTE** | Criar CI/CD pós-decisão de stack |
| `prisma/schema.prisma` ou `alembic/` | **AUSENTE** | Criar conforme stack ratificada |
| `.gitignore` | **AUSENTE** | Criar (excluir config-env-0001-env-example-v1.0, node_modules, __pycache__, .planning/vector.db, etc.) |
| `config-make-0001-makefile-v1` / `justfile` | **AUSENTE** | Opcional — padronizar comandos |

---

## 5. STACK TECNOLÓGICA — ANÁLISE DE CONFLITO E RECOMENDAÇÃO

### 5.1 Comparação Objetiva

| Critério | doc-readme-0001-readme-canon (NestJS/PostgreSQL) | board-roadmap-0001-roadmap-canon (FastAPI/MySQL) |
|----------|---------------------------|------------------------------|
| **Linguagem** | TypeScript (full-stack) | Python (backend) + JS vanilla (frontend) |
| **Framework Backend** | NestJS 10 (Clean Architecture nativo) | FastAPI + Pydantic (Clean Architecture manual) |
| **ORM** | Prisma 5 (type-safe) | SQLAlchemy/Pydantic ou stdlib MySQL |
| **Banco** | PostgreSQL 16 (ACID, JSON, avançado) | MySQL 8 InnoDB (ACID, exigido por RNF03/RNF12) |
| **PDF Export** | Não especificado (puppeteer?) | ReportLab (server-side, RF17) |
| **Testes** | Jest + Vitest | pytest + pytest-cov (≥80%) |
| **Lint** | ESLint/Prettier | ruff |
| **Frontend** | React 18 + Vite + Tailwind + shadcn/ui | Vanilla JS ES6 + Tailwind (desktop-first) |
| **Autenticação** | JWT + refresh tokens (memória + httpOnly) | JWT + refresh tokens (mesmo) |
| **Seed** | Prisma seed | Python script (<10s) |

### 5.2 Fatores Decisivos do Projeto
1. **RNF03/RNF12** exigem **MySQL InnoDB** explicitamente → board-roadmap-0001-roadmap-canon alinhado
2. **RF17** exige **ReportLab (Python)** para PDF server-side → board-roadmap-0001-roadmap-canon alinhado
3. **Constitution Art. 1.2**: "FOSS 100%, LGPD primária, CPU-local (8700G / 60GB / llama.cpp), zero cloud, zero CUDA" → ambos compatíveis
4. **Constitution Art. 3.1**: "KISS: escopo enxuto, dados mockados via seed, UI desktop-first" → board-roadmap-0001-roadmap-canon (Vanilla JS) mais KISS
5. **Constitution Art. 3.2**: "Clean Architecture: separação entre Domínio, Casos de Uso, Adaptadores, Frameworks" → NestJS tem isso nativo; FastAPI requer disciplina manual
6. **Equipe acadêmica** (FATEC ADS): Python/FastAPI tem curva de aprendizado menor que NestJS/TypeScript full-stack

### 5.3 RECOMENDAÇÃO: **board-roadmap-0001-roadmap-canon (FastAPI + MySQL + Vanilla JS)**
**Justificativa:** Alinhamento total com RNFs explícitos (MySQL InnoDB, ReportLab), menor complexidade operacional (single language backend), adequação acadêmica, KISS real. NestJS/React adiciona complexidade TypeScript full-stack sem benefício para MVP de 30 dias.

---

## 6. MODELO LLM — MIGRAÇÃO OBRIGATÓRIA

### 6.1 Estado Atual (.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc)
```json
{
  "model": "local/qwen-32b",
  "providers": {
    "local": {
      "models": {
        "qwen-32b": {
          "modelID": "/var/lib/llama.cpp/models/qwen3.8-27b-q4_k_m.gguf",
          "limit": { "context": 47500, "output": 8192 }
        }
      }
    }
  }
}
```

### 6.2 Requisito do Usuário
> **Substituir integralmente `local/qwen-32b` por Nvidia NIM: Nemotron 3 Ultra 550B A55B (cloud)**

### 6.3 Configuração Alvo — config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc Atualizado
```json
{
  "$schema": "https://config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0.ai/config.json",
  "model": "nvidia/nemotron-3-ultra-550b-a55b",
  "providers": {
    "nvidia": {
      "name": "NVIDIA NIM",
      "config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0": "@config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "https://integrate.api.nvidia.com/v1",
        "apiKey": "${NVIDIA_NIM_API_KEY}"
      },
      "models": {
        "nemotron-3-ultra": {
          "name": "Nemotron 3 Ultra 550B A55B",
          "modelID": "nvidia/nemotron-3-ultra",
          "capabilities": {
            "tools": true,
            "input": ["text"],
            "output": ["text"]
          },
          "limit": {
            "context": 128000,
            "output": 8192
          },
          "body": {
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": 8192
          }
        }
      }
    }
  },
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash", "Shell"],
    "deny": [
      "Bash(pip *)",
      "Bash(pacman *)",
      "Bash(systemctl *)",
      "Bash(sudo *)",
      "Bash(curl * | sh)",
      "Bash(wget * -O- | sh)"
    ]
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", "@modelcontextprotocol/server-filesystem",
        "--allow-read", ".ai/specs",
        "--allow-read", "docs",
        "--allow-read", "scripts",
        "--allow-read", ".ai/handoffs"
      ],
      "env": {}
    },
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "github-kanban": {
      "command": "npx",
      "args": ["-y", "@sunwood-ai-labs/github-kanban-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "github-remote": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "gsd": {
      "command": ["npx", "-y", "-p", "@opengsd/gsd-core", "gsd-mcp-server", "--no-prompts"],
      "enabled": true
    }
  },
  "permission": {
    "read": { "/lab/FATEC/202602/lab_eng_software/COBECO/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/*": "allow" },
    "external_directory": { "/lab/FATEC/202602/lab_eng_software/COBECO/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/*": "allow" }
  }
}
```

### 6.4 Variáveis de Ambiente Necessárias (config-env-0001-env-example-v1.0.example)
```bash
# NVIDIA NIM API Key (obter em https://build.nvidia.com/)
NVIDIA_NIM_API_KEY=seu_token_aqui

# GitHub Personal Access Token (para MCP servers)
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Stack FastAPI/MySQL
DATABASE_URL=mysql+pymysql://cobeco:cobeco@db:3306/cobeco
SECRET_KEY=gere_com_openssl_rand_hex_32
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
RECOVERY_MODE=log

# Frontend (Vanilla JS servido pelo nginx proxy)
FRONTEND_ORIGIN=http://localhost:8080
```

### 6.5 Permissões Bash Necessárias (adicionar ao config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc)
```json
"permissions": {
  "allow": ["Read", "Write", "Edit", "Bash", "Shell"],
  "deny": [
    "Bash(pip *)",
    "Bash(pacman *)",
    "Bash(systemctl *)",
    "Bash(sudo *)",
    "Bash(curl * | sh)",
    "Bash(wget * -O- | sh)"
  ]
}
```
> **Nota:** `python`, `uvicorn`, `npm`, `npx` agora **permitidos** (removidos do deny).

---

## 7. ARQUITETURA ÓTIMA PROPOSTA — SDD + AGENTES + DEPLOY

### 7.1 Estrutura de Diretórios Reorganizada
```
COBECO/
├── .github/
│   └── workflows/
│       ├── ci.yml              # ruff + pytest --cov + build
│       └── cd.yml              # docker build/push (tags)
├── .ai/
│   ├── agents/
│   │   ├── registry.yaml       # SSOT roster (sync via script)
│   │   └── locks/              # Lock files para coordenação
│   ├── config/
│   │   ├── hardware-profile.yaml
│   │   ├── models-catalog.yaml  # Atualizado para Nemotron
│   │   └── rag_dag_config.yaml
│   ├── handoffs/               # 56+ handoffs (append-only)
│   ├── mcp/
│   │   └── mcp-nexus/          # Nexus MCP server
│   ├── personas/
│   │   ├── active.md → coder.md (symlink)
│   │   ├── coder.md, pm.md, reviewer.md, tester.md, _base.md
│   ├── specs/                  # 15 specs ativas + template
│   │   ├── spec-001-...spec.md
│   │   └── spec-adr-template.spec.md
│   ├── sddai/                  # Engine SDDAI (5 módulos)
│   └── workflows/
│       └── sdd-cycle.sh        # Ciclo canônico
├── docs/
│   ├── decisoes/               # ADRs (criar ADR-001: Stack Decision)
│   ├── uat/                    # Evidências UAT (por rodada)
│   └── analise/                # Backlogs, relatórios
├── brain/
│   ├── md/                     # MVP specs, manual, refinamentos
│   ├── diagrams/               # Draw.io/Excalidraw sources
│   └── _old-artifact/          # Legacy (readonly)
├── prj_docs/                   # ABNT template, wrk_grp.md
├── excalidraw_baixa/           # SVGs exportados
├── scripts/
│   ├── auto-adesao-tools.sh    # Setup FOSS tools
│   ├── sync_agent_registry.py  # Sync registry.yaml ↔ disk
│   ├── validate_nexus_yaml.py  # Validação contratos
│   ├── nexus_dispatcher.py     # Dispatcher (corrigir sender)
│   ├── handoff_parser.py       # Parser S.2
│   └── seed.py                 # Seed MySQL (board-roadmap-0001-roadmap-canon)
├── .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/
│   ├── config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc          # CONFIGURADO PARA NEMOTRON 3 ULTRA
│   ├── mcp.json                # MCP servers locais
│   ├── agents/                 # Agent definitions
│   ├── commands/               # Custom commands
│   ├── gsd-core/               # GSD core
│   ├── hooks/                  # Hooks
│   ├── plugins/                # Plugins
│   └── scripts/                # Scripts internos
├── .planning/
│   ├── config.json             # GSD config
│   └── graphs/                 # Graphify output
├── frontend/                   # Vanilla JS + Tailwind (nginx served)
│   ├── src/
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── app.js
│   │   ├── components/
│   │   └── utils/
│   ├── nginx.conf
│   └── Dockerfile
├── backend/                    # FastAPI + Pydantic + SQLAlchemy
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── domain/             # Entidades, value objects, domain events
│   │   ├── usecases/           # Casos de uso (Clean Architecture)
│   │   ├── adapters/           # Repositories, controllers, presenters
│   │   │   ├── api/            # FastAPI routers
│   │   │   └── db/             # SQLAlchemy models, repositories
│   │   └── infrastructure/     # External services, migrations
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── alembic/                # Migrations
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
├── config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml          # db + backend + frontend + proxy
├── config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml # Dev overrides (hot reload)
├── config-env-0001-env-example-v1.0.example                # Template (sem segredos)
├── .gitignore
├── config-make-0001-makefile-v1                    # Comandos padronizados
├── doc-readme-0001-readme-canon.md                   # Atualizado para stack escolhida
├── constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md             # Lei suprema (atualizar Art. 1.2 se necessário)
├── doc-agents-0001-agents-canon.md                   # Este arquivo (atualizado)
├── req-func-0001-requisitos-funcionais-canon.md               # SSOT v3.2
├── req-use-case-0001-casos-de-uso-canon.md               # SSOT v3.2
├── doc-arch-0001-camada-de-dados-canon.md            # SSOT v3.2
├── board-roadmap-0001-roadmap-canon.md            # Roadmap Kanban
└── doc-figma-0001-figma-export-v1.0.html    # Protótipos (manter)
```

### 7.2 Docker Compose — Arquitetura de Camadas Ortogonais (spec-005)
```yaml
# config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml
services:
  db:
    image: mysql:8.0
    command: --default-authentication-plugin=mysql_native_password --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    environment:
      MYSQL_DATABASE: cobeco
      MYSQL_USER: cobeco
      MYSQL_PASSWORD: cobeco
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - db_data:/var/lib/mysql
      - ./backend/config-seed-0001-seed-v1.0.sql:/docker-entrypoint-initdb.d/seed.sql:ro
    networks: [data]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10

  migrate:
    build: ./backend
    command: alembic upgrade head
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: mysql+pymysql://cobeco:cobeco@db:3306/cobeco
    networks: [data]

  backend:
    build: ./backend
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      migrate:
        condition: service_completed_successfully
    environment:
      DATABASE_URL: mysql+pymysql://cobeco:cobeco@db:3306/cobeco
      SECRET_KEY: ${SECRET_KEY}
      JWT_ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 15
      REFRESH_TOKEN_EXPIRE_DAYS: 7
      RECOVERY_MODE: log
    networks: [data, edge]
    volumes:
      - ./backend:/app
    expose: ["8000"]

  frontend:
    build: ./frontend
    command: nginx -g "daemon off;"
    depends_on: [backend]
    networks: [edge]
    expose: ["80"]
    volumes:
      - ./frontend:/app

  proxy:
    image: nginx:alpine
    ports: ["8080:8080"]
    volumes:
      - ./proxy/config-nginx-0003-proxy-nginx-v1.0.conf:/etc/nginx/nginx.conf:ro
    depends_on: [frontend, backend]
    networks: [edge]

networks:
  data:
    internal: true
  edge:
    internal: false

volumes:
  db_data:
```

### 7.3 Proxy Nginx (spec-005 / hf-exec-0030)
```nginx
# proxy/config-nginx-0003-proxy-nginx-v1.0.conf
events { worker_connections 1024; }
http {
  upstream frontend { server frontend:80; }
  upstream backend { server backend:8000; }
  server {
    listen 8080;
    server_name localhost;
    # Frontend
    location / {
      proxy_pass http://frontend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
    # Backend API
    location /v1/ {
      proxy_pass http://backend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
}
```

### 7.4 CI/CD GitHub Actions (.github/workflows/config-ci-0001-github-actions-v1.0.yml)
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint-test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_DATABASE: cobeco_test
          MYSQL_USER: test
          MYSQL_PASSWORD: test
          MYSQL_ROOT_PASSWORD: root
        ports: [3306:3306]
        options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=3s --health-retries=10
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - name: Install deps
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run migrations
        run: |
          cd backend
          DATABASE_URL=mysql+pymysql://test:test@localhost:3306/cobeco_test alembic upgrade head
      - name: Lint (ruff)
        run: |
          cd backend
          ruff check src tests
      - name: Test (pytest --cov)
        run: |
          cd backend
          pytest --cov=src --cov-report=term-missing --cov-fail-under=80
      - name: Build Docker images
        run: |
          docker compose build
```

---

## 8. PLANO DE AÇÃO — EXECUÇÃO IMEDIATA

### Fase 0: Decisão de Stack (CCB) — **HOJE**
- [ ] Apresentar este relatório ao CCB
- [ ] Ratificar stack: **FastAPI + MySQL + Vanilla JS** (board-roadmap-0001-roadmap-canon)
- [ ] Emitir ADR-001: Stack Decision

### Fase 1: Scaffold Completo (Dias 1-3)
- [ ] Criar `config-env-0001-env-example-v1.0.example` com variáveis acima
- [ ] Criar `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` + `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml`
- [ ] Criar `backend/` com FastAPI, SQLAlchemy, Pydantic, Alembic, pytest, ruff
- [ ] Criar `frontend/` com Vanilla JS, Tailwind, nginx
- [ ] Criar `proxy/` com nginx.conf
- [ ] Criar `.github/workflows/config-ci-0001-github-actions-v1.0.yml`
- [ ] Criar `config-make-0001-makefile-v1` com targets: `up`, `down`, `logs`, `test`, `lint`, `seed`, `migrate`
- [ ] Atualizar `doc-readme-0001-readme-canon.md` para refletir stack escolhida
- [ ] Atualizar `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` Art. 1.2 se necessário
- [ ] Commit inicial + push para `origin/main`

### Fase 2: Configuração Opencode + Nemotron (Paralelo)
- [ ] Substituir `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc` pela versão Nemotron 3 Ultra
- [ ] Configurar `NVIDIA_NIM_API_KEY` no ambiente
- [ ] Testar `config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0 run "health check"` com novo modelo
- [ ] Remover dependência do llama.cpp local (liberar porta 8080 para proxy)

### Fase 3: Seed + Schema (Dias 3-5)
- [ ] Implementar `backend/config-seed-0001-seed-v1.0.py` (10 fornecedores, 50 produtos, 11 categorias, ~300 preços)
- [ ] Criar migrations Alembic para 8 tabelas PT-BR (doc-arch-0001-camada-de-dados-canon.md)
- [ ] Validar `docker compose up` sobe tudo sem config manual

### Fase 4: Desenvolvimento por Sprints (board-roadmap-0001-roadmap-canon.md)
- Sprint 1 (Dias 6-11): Auth + Schema + Seed
- Sprint 2 (Dias 12-17): Listas + Catálogo + Autocomplete
- Sprint 3 (Dias 18-23): Pré-filtro + Comparação
- Sprint 4 (Dias 24-29): PDF Export (ReportLab) + Perfil + Polish
- Sprint 5 (Dia 30): QA + Demo + Docs finais

---

## 9. RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| CCB não decide stack hoje | Média | Bloqueia tudo | Timebox: decisão até 14/11 12h; default = board-roadmap-0001-roadmap-canon |
| Nemotron 3 Ultra indisponível/rate-limited | Baixa | Para desenvolvimento | Fallback: manter qwen-32b local como provider secundário no config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc |
| Seed MySQL >10s | Baixa | Viola RNF08 | Otimizar bulk insert; usar LOAD DATA INFILE |
| PDF ReportLab >5s (100 itens) | Média | Viola RNF11 | Otimizar template; cache de fontes; async generation |
| Cobertura testes <80% | Média | Porta CI | TDD desde Sprint 1; gate no CI |
| Dados sensíveis em commit | Baixa | LGPD/Compliance | `.gitignore` rigoroso; `config-env-0001-env-example-v1.0.example` sem segredos; pre-commit hook `detect-secrets` |
| Conflito registry.yaml vs dispatcher | Alta (já existe) | Agentes não despacham | Corrigir `nexus_dispatcher.py` sender para `agent-nexus-prime-ultimate` |

---

## 10. CHECKLIST DE CONFORMIDADE CONSTITUTION.MD

| Artigo | Requisito | Status | Ação |
|--------|-----------|--------|------|
| Art. 1.2 | FOSS 100%, CPU-local, zero cloud, zero CUDA | ⚠️ Parcial | Nemotron é cloud API — **exceção CCB necessária** (Art. 5.1) |
| Art. 1.3 | Escopo congelado: 18 RFs, 29 UCs, 8 tabelas | ✅ | SSOT v3.2 aprovado |
| Art. 3.1 | KISS: dados mockados, UI desktop-first | ✅ | board-roadmap-0001-roadmap-canon alinhado |
| Art. 3.2 | Clean Architecture 4 camadas | ⏳ Pendente | Scaffold backend com domain/usecases/adapters/infrastructure |
| Art. 3.3 | ACID: transações explícitas, InnoDB | ✅ | MySQL 8 InnoDB no board-roadmap-0001-roadmap-canon |
| Art. 3.4 | SDD: spec + handoff par | ✅ | 15 specs + 56 handoffs ativos |
| Art. 3.5 | LGPD: dados sintéticos apenas | ✅ | Seed sem PII real |
| Art. 3.6 | FOSS-first | ✅ | Stack 100% FOSS |
| Art. 3.7 | YAGNI | ✅ | Escopo MVP fechado |
| Art. 4.1 | Roster SSOT = registry.yaml | ✅ | Promulgado |
| Art. 4.2 | Orquestrador L0 = agent-nexus-prime-ultimate | ⚠️ Bug | Corrigir dispatcher sender |
| Art. 4.3 | Half-duplex parcel com dod/kill_switch | ✅ | Implementado no ciclo |
| Art. 4.4 | Kill Switch não-negociável | ✅ | Vetores LGPD, vigilância, bypass CI |
| Art. 5.1 | Humano = CCB chair único | ✅ | Governança definida |
| Art. 6.1 | Fluxo spec → handoff | ✅ | Pipeline funcional |
| Art. 6.2 | Parser antes do dispatch | ✅ | sdd-cycle.sh valida |
| Art. 6.3 | Cadeia reviewer → qa-sdet → CI → gatekeeper → humano | ⏳ Pendente | Implementar no CI/CD |
| Art. 7.1 | Zero segredos no repo | ⏳ Pendente | `.gitignore` + `config-env-0001-env-example-v1.0.example` + pre-commit |
| Art. 8.1 | Cobertura ≥80% | ⏳ Pendente | Gate no CI |
| Art. 8.2 | Testes determinísticos | ⏳ Pendente | pytest fixtures, mock time/DB |
| Art. 8.3 | Review rubric-citado (R-01..R-07) | ⏳ Pendente | Template PR com rubrica |

---

## 11. PRÓXIMOS PASSOS IMEDIATOS (PARA EXECUÇÃO AGORA)

```bash
# 1. Backup do config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc atual
cp .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc.backup

# 2. Aplicar nova configuração Nemotron 3 Ultra
cat > .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/config-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-0001-config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0-v1.0.jsonc << 'EOF'
{ ... conteúdo da seção 6.3 ... }
EOF

# 3. Criar config-env-0001-env-example-v1.0.example
cat > config-env-0001-env-example-v1.0.example << 'EOF'
{ ... conteúdo da seção 6.4 ... }
EOF

# 4. Corrigir dispatcher sender (bug G-01)
sed -i 's/agent-orchestrator/agent-nexus-prime-ultimate/g' scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py

# 5. Criar config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml (conforme seção 7.2)
# 6. Criar backend/frontend/proxy scaffold
# 7. Commit e push
git add -A
git commit -m "chore: scaffold completo stack FastAPI/MySQL/Vanilla JS + Nemotron 3 Ultra config"
git push origin main
```

---

## 12. CONCLUSÃO

O projeto COBECO possui **documentação de alto nível completa e rigorosa** (SSOT v3.2, 15 specs SDD, 56 handoffs, roster de agentes, Constitution), mas **zero código executável**. O conflito de stack entre doc-readme-0001-readme-canon e board-roadmap-0001-roadmap-canon é o único bloqueante crítico.

**Recomendação unânime da análise:** Ratificar **board-roadmap-0001-roadmap-canon (FastAPI + MySQL + Vanilla JS)** por alinhamento total com RNFs explícitos, menor complexidade, adequação acadêmica e prazo de 30 dias.

A migração para **Nvidia NIM Nemotron 3 Ultra 550B A55B** exige exceção CCB ao Art. 1.2 da Constitution (zero cloud), mas oferece contexto 128k e capacidades superiores para o desenvolvimento SDD assistido por IA.

Todos os artefatos, configs e arquitetura estão mapeados neste relatório. A execução pode começar **imediatamente após decisão do CCB**.

---

**Fim do Relatório**  
*Preparado para tomada de decisão do CCB — COBECO MVP*