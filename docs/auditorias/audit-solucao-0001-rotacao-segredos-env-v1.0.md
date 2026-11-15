---
id: audit-solucao-0001-rotacao-segredos-env-v1.0
type: audit-solucao
title: AUDIT SOLUCAO — Rotacao de segredos do .env (incidente leak d9cc5db)
version: v1.1
status: rascunho
canonical: false
canonical_slug: solucao-rotacao-segredos-env
created: '2026-11-15'
updated: '2026-11-15T04:39:33Z'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:ffd5261c03ee84415ef8644b66e1dd09a46850f6de35bc910aa7eccd63c2c634
ratified_at: '2026-11-15T04:39:33Z'
supersedes: null
superseded_by: null
trace:
  constitution: [Art. 6.3, Art. 7.7, Art. 17.7, Art. 9.9, Art. 17.5]
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: [commit 770e504, PR #67, PR #68, c852fcc, d5cffa5, c5fdbeb]
  tests: []
domain: operation
layer: solucao
tags: [solucao, rotacao, segredos, env, seguranca, SEV-2, incidente]
lgpd_class: n/a (zero valores de segredos registrados; apenas confirmacao de rotacao)
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: ffd5261c03ee84415ef8644b66e1dd09a46850f6de35bc910aa7eccd63c2c634
  board_url: null
---

# MEDIDA SOLUTIVA — Rotacao de segredos do .env (incidente leak commit d9cc5db)

## 1. Contexto

Incidente SEV-2: arquivo `.env` commitado e rastreado pelo git na migracao P1/P2/P3 (commits `e639a0a` / mescla `d9cc5db`), expondo credenciais no remote `origin` (branch `stage`).

Fix aplicado (PR #67, mergado em `stage` via `d5cffa5`): `.env` removido do rastreamento do git e adicionado ao `.gitignore` (`.env` e `.*`). Arquivo local mantido.

Incidente registrado (PR #68, mergado em `stage` via `c5fdbeb`): `docs/auditorias/audit-incident-0001-env-secret-leak-v1.0.md`, assinado com hash (`gh-sig:owner:leonardosetti:67f30b8d…cf6e241`).

Como o `.env` ja estava no remote, todos os segredos nele constantes estao considerados **comprometidos** e devem ser rotacionados.

## 2. Escopo da rotacao

| Variavel | Tratamento | Quem rotaciona | Status |
|----------|------------|----------------|--------|
| `GITHUB_TOKEN` | Segredo da conta GitHub (possivelmente compartilhado com outros projetos) | Usuario (prioridade 0) | ROTACIONADO |
| `CR_PAT` | Segredo da conta GitHub (possivelmente compartilhado com outros projetos) | Usuario (prioridade 0) | ROTACIONADO |
| `MYSQL_ROOT_PASSWORD` | Segredo local COBECO | Esta acao | ROTACIONADO |
| `MYSQL_PASSWORD` | Segredo local COBECO | Esta acao | ROTACIONADO |
| `SECRET_KEY` | Segredo local COBECO (FastAPI) | Esta acao | ROTACIONADO |
| `DATABASE_URL` | Segredo local COBECO (contem senha MySQL) | Esta acao | ROTACIONADO |
| `MYSQL_DATABASE` | Config (nao segredo) | — | mantido (`cobeco`) |
| `MYSQL_USER` | Config (nao segredo) | — | mantido (`cobeco`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Config (nao segredo) | — | mantido (`30`) |
| `NGINX_PORT` | Config (nao segredo) | — | mantido (`8380`) |
| `VITE_API_BASE_URL` | Config (nao segredo) | — | mantido (`http://localhost:8380/api`) |
| `TZ` | Config (nao segredo) | — | mantido (`America/Sao_Paulo`) |

## 3. Acao executada

- Gerados novos valores fortes para `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, `SECRET_KEY` (via `openssl rand`) por este agente.
- `DATABASE_URL` reconstruido com a nova senha (`mysql+pymysql://cobeco:<nova>@db:3306/cobeco`).
- `GITHUB_TOKEN` e `CR_PAT` rotacionados pelo **usuario** (prioridade 0), conforme comunicado em 15/11/2026.
- Arquivo `.env` local reescrito com os novos valores (segredos locais) e os tokens rotacionados pelo usuario injetados.
- Valores de segredos **nao sao registrados neste documento** (zero segredos em texto claro).
- `.env` permanece **nao rastreado** pelo git (ignorado via `.gitignore`).

## 4. Acao pendente (usuario — prioridade 0)

Nenhuma. `GITHUB_TOKEN` e `CR_PAT` foram rotacionados pelo usuario em 15/11/2026. Todos os segredos do `.env` estao rotacionados.

Considerar revisao de acesso: verificar se `GITHUB_TOKEN` e `CR_PAT` sao dedicados a COBECO ou compartilhados com outros projetos da conta GitHub; se compartilhados, garantir que todos os projetos consumam os novos valores.

## 5. Medidas solutivas complementares (ja aplicadas)

| Medida | Local | Status |
|--------|-------|--------|
| `.env` fora do rastreamento git | `.gitignore` + `git rm --cached .env` | CONCLUIDO (PR #67) |
| `.env` e `.*` no `.gitignore` | `.gitignore` linha 10-11 | CONCLUIDO |
| Incidente registrado + RCA | `docs/auditorias/audit-incident-0001-env-secret-leak-v1.0.md` | CONCLUIDO (PR #68) |
| Rotacao de segredos locais COBECO (`MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, `SECRET_KEY`, `DATABASE_URL`) | `.env` (local) | CONCLUIDO (este agente) |
| Rotacao de `GITHUB_TOKEN` / `CR_PAT` | conta GitHub | CONCLUIDO (usuario, prioridade 0) |
| Consertar hook `pre-commit` (script ausente) | `scripts/script-security-0001-secret-scan-v1.0.py` | CONCLUIDO |
| Consertar/remover hook `pre-push` (`ci_green_check.py` inexistente) | `scripts/script-ci-0001-ci-green-check-v1.0.py` | CONCLUIDO |
| Auditar outros arquivos sensiveis rastreados (`.pem`, `.key`, `secrets/`) | `git ls-files` | PENDENTE |

## 6. Avaliacao de impacto em outros projetos

Nenhuma evidencia de shared secrets com outros projetos encontrada no repositorio COBECO (sem referencias a `shared.*`, `common.*env`, infraestrutura compartilhada ou multiplos projetos). `GITHUB_TOKEN` e `CR_PAT` foram rotacionados pelo usuario; se forem tokens da conta GitHub reutilizados em outros repositorios, garantir que todos esses projetos consumam os novos valores (janela de manutenção coordenada). Impacto transversal mitigapos apos confirmacao de injecao dos novos valores.

## 7. Rastreabilidade

- **Incidente vinculado:** `docs/auditorias/audit-incident-0001-env-secret-leak-v1.0.md`
- **Runbook relacionado:** `docs/operacao/runbook-incident-0001-incident-v1.0.md`
- **Fix do leak:** PR #67 (`fix/env-leak` → `stage`), commit `770e504`, mesclado em `d5cffa5`
- **Registro do incidente:** PR #68 (`fix/incident-env-leak-report` → `stage`), commit `c852fcc`, mesclado em `c5fdbeb`
- **Constitution:** Art. 6.3 (branch protegido), Art. 7.7 / 17.7 (secret scanner), Art. 9.9 / 17.5 (CI green check)

---
**Fim da medida solutiva — rotacao de todos os segredos do .env concluida.**
