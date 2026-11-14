---
id: runbook-sprint-0001-sprint1-dev-v1.0
type: runbook-sprint
title: RUNBOOK SPRINT — Sprint1 Dev
version: v1.0
status: ratificado
canonical: false
canonical_slug: sprint1-dev
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
domain: operation
layer: runbook
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Runbook — Sprint 1 Development Workflow (COBECO MVP)

**Documento:** Runbook Operacional — Sprint 1  
**Versão:** 1.0  
**Status:** Ativo  
**Data:** 14/11/2026  
**Autor:** Leonardo Setti (Tech Lead)  
**Aplica-se a:** dev | homolog  
**Sprint:** S1: Setup, Docs e Auth  
**Classificação:** Interno

---

## 1. Propósito

Procedimento padronizado para execução da Sprint 1 (Setup, Docs e Auth), cobrindo:
- Ambiente de desenvolvimento
- Schema MySQL + Migrations + Seed
- Autenticação (Cadastro, Login JWT, Logout, Recuperação Senha)
- Frontend Auth Pages
- Documentação ABNT
- Validação contínua (hooks, CI, testes)

---

## 2. Pré-requisitos

| Item | Verificação | Comando |
|------|-------------|---------|
| Docker rodando | `docker ps` | `docker ps` |
| `config-env-0001-env-example-v1.0` configurado | `ls config-env-0001-env-example-v1.0` | `ls -la config-env-0001-env-example-v1.0` |
| Portas livres | 8380, 8000, 3306 | `make ports-free` |
| Git hooks ativos | pre-commit, pre-push, commit-msg | `ls -la .git/hooks/` |
| Branch correta | `feat/UC-XX-*` | `git branch --show-current` |

---

## 3. Sprint 1 Scope (Itens Ready)

| Item | Título | Responsável | Estimativa |
|------|--------|-------------|------------|
| #13 | UC09: Cadastrar Usuário (RF01) | Backend 1 | 1.5 dias |
| #14 | UC10: Login JWT (RF02) | Backend 1 | 1.5 dias |
| #15 | UC11: Logout (RF03) | Backend 1 | 0.5 dia |
| #16 | UC12: Recuperar Senha (RF04) | Backend 1 | 1 dia |
| #17 | Frontend: Páginas Auth | Frontend | 2 dias |
| #18 | Schema MySQL (8 Tabelas) | Backend 2 | 1 dia |
| #19 | Seed Script (<10s) | Backend 2 | 1 dia |
| #20 | Docker Compose Produção | DevOps | 1 dia |
| #21 | Documentação ABNT | PO + Equipe | 3 dias |
| #48 | Documentos Arquiteturais C4 | Arquiteto | 1 dia |
| #49 | RAID Log Inicial | Tech Lead | 0.5 dia |
| #50 | Test Plan | QA | 0.5 dia |
| #51 | Post-Mortem + Lessons Learned | Tech Lead | 0.5 dia |
| #58 | Épicos do COBECO MVP | PO | 1 dia |

---

## 3. Procedimento de Início de Sprint (Day 0)

### 3.1 Setup do Ambiente

```bash
# 1. Clonar/atualizar repo
git checkout main
git pull origin main

# 2. Criar branch da Sprint 1 (ex: auth)
git checkout -b feat/UC-09-cadastrar-usuario

# 3. Subir ambiente
make up
make health

# 4. Validar banco
make migrate
make seed

# 5. Validar hooks
git add . && git commit -m "test: hook verification" --no-verify
# Deve passar secret_scan + commit-msg
```

### 3.2 Validação Inicial

```bash
# Testes rápidos
make test
make test-cov

# Validação cross-refs
python scripts/script-validate-0001-validate-refs-v1.0.py

# Lint
make lint
```

---

## 4. Procedimentos Diários (Daily Workflow)

### 4.1 Início do Dia (Pull + Sync)

```bash
# 1. Atualizar main
git checkout main && git pull origin main

# 2. Rebase feature branch
git checkout feat/UC-XX-*
git rebase main

# 3. Subir ambiente
make up
make health
```

### 4.2 Durante Desenvolvimento

```bash
# Commits frequentes (Conventional Commits)
git add .
git commit -m "feat(auth): add bcrypt hash validation"
# Hooks: pre-commit (secret_scan) + commit-msg (conventional)

# Testes contínuos
make test          # Unitários rápidos
make test-cov      # Com cobertura (deve passar ≥80% no final)
```

### 4.3 Fim do Dia (Push + Sync)

```bash
# Push da feature branch
git push origin feat/UC-XX-*

# Verificar CI (GitHub Actions)
gh run list --branch $(git branch --show-current) --limit 1
```

---

## 5. Procedimentos Específicos por Item

### 5.1 Schema MySQL + Migrations (#18)

```bash
# 1. Verificar models em backend/src/domain/entities/
# 2. Gerar migration
make migrate-create MSG="create_initial_schema"

# 3. Aplicar
make migrate

# 4. Verificar
docker compose exec backend alembic current
docker compose exec backend alembic history
```

### 5.2 Seed Script (#19)

```bash
# 1. Executar seed
make seed

# 2. Validar performance (< 10s)
time make seed

# 3. Verificar contagens
docker compose exec backend python -c "
from src.infrastrdoc-arch-0006-uc-v1ture.database import SessionLocal
from src.domain.entities import Categoria, Fornecedor, Produto, Preco
db = SessionLocal()
print(f'Categorias: {db.query(Categoria).count()}')
print(f'Fornecedores: {db.query(Fornecedor).count()}')
print(f'Produtos: {db.query(Produto).count()}')
print(f'Preços: {db.query(Preco).count()}')
db.close()
"
# Esperado: 11 cat, 10 forn, 50 prod, ~300 preços
```

### 5.3 Auth Backend (#13, #14, #15, #16)

```bash
# Estrutura esperada:
# backend/src/api/routers/auth.py
# backend/src/usecases/auth/
# backend/src/adapters/auth.py

# Testes
make test-cov  # Deve cobrir auth usecases ≥80%
```

### 5.4 Frontend Auth (#17)

```bash
# Estrutura esperada:
# frontend/modules/auth.js
# frontend/components/autocomplete.js (reutilizado)

# Testes E2E
cd frontend/tests/e2e && npm test
```

### 5.4 Docker Compose (#20)

```bash
# Validação completa
make down
make up
make health
make test
make test-cov
```

### 5.5 Documentação ABNT (#21)

```bash
# Pair writing: PO + Dev
# Revisão semanal com orientador
# Template: docs/strategy/TEMPLATE-CLOSURE.md
```

### 5.5 Diagramas C4 (#48)

```bash
# Arquivos: docs/arquitetura/doc-arch-0010-c4-context-v1.0.md, C4-Containers.md, C4-Components-*.md
# Renderizar no GitHub/VS Code para validação visual
```

### 5.6 RAID Log (#49)

```bash
# Atualização diária no standup
# Arquivo: docs/operacao/doc-raid-log-0001-raid-log-v1.0.md
```

### 5.7 Test Plan (#50)

```bash
# Arquivo: docs/operacao/doc-test-plan-0001-test-plan-v1.0.md
# Estratégia: Unit + Integration + E2E
```

---

## 6. Validação Contínua (Quality Gates)

### 6.1 Pre-commit (Automático via Hook)

- Secret Scanner (`scripts/script-security-0001-secret-scan-v1.0.py`)
- Conventional Commits (`commit-msg` hook)

### 6.2 Pre-push (Automático via Hook)

- CI Green Check (`ci_green_check.py`)
- Branch Protection (main/stage bloqueadas)

### 6.3 CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/config-ci-0001-github-actions-v1.0.yml
# Jobs: lint (ruff) + type-check (mypy) + test (pytest --cov≥80) + build Docker
# Deve passar em < 5 min
```

### 6.4 Validação Local (Antes de PR)

```bash
# Checklist pré-PR
make ci          # Pipeline local completo
make test-cov    # Coverage ≥80%
python scripts/script-validate-0001-validate-refs-v1.0.py  # Cross-refs OK
make lint        # ruff + mypy OK
```

---

## 7. Definition of Done (DoD) por Item

| Critério | Verificação |
|----------|-------------|
| Código limpo | Clean Architecture (4 camadas), sem vazamento framework→Domain |
| Segurança | Queries parameterizadas, validação Pydantic, bcrypt salt=12 |
| Nomenclatura | PT-BR (DB, variáveis, comentários, erros) |
| Testes | Unitários ≥80% nos módulos tocados (`pytest --cov`) |
| Contrato | OpenAPI (`/docs`) atualizado |
| Infra | `docker compose up` funciona sem config manual |
| Revisão | Code review aprovado (R-01..R-07) + CI verde |
| Governança | Aprovação CCB + merge em `main` → kanban "Done" |

---

## 8. Troubleshooting Comum

| Problema | Solução |
|----------|---------|
| `secret_scan` bloqueia commit | Verificar `config-env-0001-env-example-v1.0.example` não tem segredos reais; usar `--no-verify` só emergência |
| CI falha coverage < 80% | Adicionar testes nos módulos novos; `make test-cov` local |
| `pre-push` bloqueia | CI não verde; aguardar CI ou corrigir falhas |
| Migration falha | `alembic downgrade -1`, corrigir, `upgrade head` |
| Seed > 10s | Verificar `bulk_save_objects` + índices pós-carga |
| Porta 8380 ocupada | `make ports-free` |

---

## 9. Checklist de Fim de Sprint (Gate 2)

- [ ] Todos 16 itens **Done** (Status = Done no board)
- [ ] Cobertura testes ≥ 80% (`make test-cov`)
- [ ] CI verde na `main` (último run sdoc-arch-0006-uc-v1cess)
- [ ] Documentação ABNT aprovada (orientador)
- [ ] PRD aprovado (Gate 2 CCB)
- [ ] Diagramas C4 validados
- [ ] RAID Log atualizado
- [ ] Test Plan validado
- [ ] PRs merged com CI verde + Code Review + CCB approval
- [ ] Kanban: todos itens S1 em **Done**

---

## 9. Contatos e Escalação

| Nível | Papel | Contato | SLA |
|-------|-------|---------|-----|
| L1 | Dev de Plantão | Discord @nathony | Imediato |
| L2 | Tech Lead | Discord @leosetti | 15 min |
| L3 | CCB Chair / PO | Discord @leosetti | 30 min |

---

## Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | 14/11/2026 | Leonardo Setti | Criação inicial Sprint 1 |

---

**Fim do Runbook — Sprint 1 Development Workflow**  
*Seguir rigorosamente. Ratificado CCB 14/11/2026.*