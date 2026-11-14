---
id: doc-runbook-survey-0001-levantamento-runbooks-hooks-sanitizacao-v1.0
type: doc-runbook-survey
title: DOC RUNBOOK SURVEY — Levantamento Runbooks Hooks Sanitizacao
version: v1.0
status: ratificado
canonical: false
canonical_slug: levantamento-runbooks-hooks-sanitizacao
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
layer: survey
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Levantamento: Runbooks, Hooks e Sanitização Contínua de Cross-References

**Documento:** Survey técnico para adequação de automação operacional  
**Versão:** 1.0  
**Data:** 14/11/2026  
**Autor:** Leonardo Setti (Tech Lead)  
**Base:** Constitution v2.0 (Arts. 7.7, 9.9, 17.5, 17.7) + PMBOK 7 (Monitoring & Controlling)  
**Status:** Para revisão e validação do CCB

---

## 1. Contexto Normativo (Constitution v2.0)

| Artigo | Requisito | Status Atual |
|--------|-----------|--------------|
| **Art. 7.7** | Sanitização antes de commit/push: `git diff --cached --name-only | grep -iE '\config-env-0001-env-example-v1.0$|secrets/|\.pem$|\.key$|\.secret$'` | ⚠️ Manual (não automatizado) |
| **Art. 9.9** | Custom hooks OpenCode: pre-commit (sanitização segredos), pre-push (CI verde) | ❌ Ausente |
| **Art. 17.5** | Custom hooks OpenCode: pre-commit (sanitização), pre-push (CI verde); webhooks GitHub para CI/CD e notificações PR | ❌ Ausente |
| **Art. 17.7** | Sanitização de projetos: antes de commit/push verificar arquivos de segredo; `.gitignore` atualizado para excluir segredos, build outputs, artefatos gerados (`graphify-out/`, `log_llama.txt`, `*.bkp` não solicitados) | ⚠️ Parcial (gitignore OK, verificação manual) |
| **Art. 17.1** | Scripts em `scripts/` — automação Python preferencial; versionados; execução determinística | ⚠️ Parcial (scripts GSD existentes, mas faltam `nexus_dispatcher.py`, `handoff_parser.py`) |
| **Art. 17.3** | Agents: roster `.ai/agents/config-registry-0001-registry-v1.0.yaml`; dispatch via L0 (`scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py`) | ❌ `nexus_dispatcher.py` ausente |
| **Art. 17.4** | RAG/DAG/Roster: roster canônico, indexação RAG specs/handoffs em `.planning/`, grafo DAG dependências `.planning/graphs/` | ⚠️ Parcial (registry.yaml existe, `.planning/` vazio) |
| **Art. 16.5 / 17.8** | Avaliação recorrente arquitetura/conformidade a cada sprint; resultado em `docs/auditorias/` | ✅ `docs/auditorias/audit-postmortem-0001-postmortem-v1.0.md`, `LESSONS-LEARNED.md` criados |

---

## 2. Estado Atual dos Runbooks

| Runbook | Arquivo | Status | Cobertura | Próxima Ação |
|---------|---------|--------|-----------|--------------|
| **Deploy Produção** | `docs/operacao/runbook-deploy-0001-deploy-v1.0.md` | ✅ Criado | Deploy, Rollback, Backup, Validação, Escalação | Testar em staging |
| **Seed/DB Reset** | `docs/operacao/template-runbook-0001-runbook-v1.0.md` (seção 3.2) | ⚠️ Template | Recriar DB, Migrations, Seed | Mover para `RUNBOOK-DB-RESET.md` |
| **Incident Response** | `docs/operacao/template-runbook-0001-runbook-v1.0.md` (seção 4) | ⚠️ Template | Troubleshooting tabela | Expandir para `RUNBOOK-INCIDENT.md` |
| **Release/Tag** | `docs/operacao/template-release-notes-0001-release-notes-v1.0.md` | ⚠️ Template | Release notes, Rollback, Links | Mover para `RUNBOOK-RELEASE.md` |
| **CI/CD Pipeline** | `.github/workflows/config-ci-0001-github-actions-v1.0.yml` | ✅ Executável | Lint, Test, Build, CD | Validar < 5 min |
| **Health Check** | `config-make-0001-makefile-v1` (`make health`) | ✅ Executável | nginx, backend, mysql | Validar endpoints |
| **Backup/Restore** | `docs/operacao/runbook-deploy-0001-deploy-v1.0.md` (seção 3.5) | ⚠️ Parcial | mysqldump + gzip, restore | Separar em `RUNBOOK-BACKUP.md` |

**Gap Crítico:** Runbooks existem como templates ou parciais, mas **não há runbooks executáveis/validados** para operações rotineiras (seed, migrate, backup, incident response).

---

## 3. Estado Atual dos Hooks (OpenCode + Git)

### 3.1 Hooks OpenCode Existentes (`.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/hooks/`)
- 30+ hooks GSD (agent isolation, context monitor, prompt guard, secret read guard, validate commit, etc.)
- **Faltando:** `pre-commit` (sanitização segredos), `pre-push` (CI verde)

### 3.2 Hooks Git (`.git/hooks/`) — Não Configurados
| Hook | Requisito Constitution | Status | Implementação Necessária |
|------|------------------------|--------|-------------------------|
| `pre-commit` | Art. 7.7, 17.5, 17.7 — Sanitização segredos antes de commit | ❌ Ausente | Script Python: `git diff --cached --name-only \| grep -iE '\config-env-0001-env-example-v1.0$|secrets/|\.pem$|\.key$|\.secret$'` + bloqueio |
| `pre-push` | Art. 9.9, 17.5 — CI verde antes de push | ❌ Ausente | Verificar `gh run list --limit 1 --workflow=CI` status sdoc-arch-0006-uc-v1cess |
| `commit-msg` | Conventional Commits (Art. 9.3) | ❌ Ausente | Validar formato `tipo(escopo): resumo` |
| `pre-receive` (server-side) | Bloquear push direto em `main`/`stage` | ❌ N/A (GitHub Branch Protection) | Configurar via GitHub Branch Protection Rules |

### 3.3 Webhooks GitHub — Não Configurados
| Webhook | Evento | Ação | Status |
|---------|--------|------|--------|
| **CI/CD** | `push`, `pull_request` | Trigger GitHub Actions | ✅ Via `.github/workflows/config-ci-0001-github-actions-v1.0.yml` |
| **PR Notifications** | `pull_request` (opened, review_requested, merged) | Notificar Discord/Slack/Email | ❌ Ausente |
| **Release** | `release` (published) | Trigger deploy staging/prod | ❌ Ausente |
| **Issue/PR Sync** | `issues`, `pull_request` | Sincronizar GitHub Projects (kanban) | ❌ Ausente |
| **Security** | `secret_scanning_alert` | Alerta segredo commitado | ❌ Ausente |

---

## 4. Sanitização Contínua de Cross-References

### 4.1 Referências Cruzadas Atuais (Verificadas via grep)
- **Total de arquivos `.md` em `docs/`:** 58
- **Referências internas (`docs/...`):** ~120 (todas íntegras)
- **Referências a specs (`.ai/specs/`):** ~30 (todas íntegras)
- **Referências a handoffs (`.ai/handoffs/`):** ~20 (todas íntegras)
- **Referências a código (`backend/`, `frontend/`):** ~15 (todas íntegras)

### 4.2 Riscos de Dériva (Drift)
| Fonte de Drift | Probabilidade | Impacto | Mitigação |
|----------------|---------------|---------|-----------|
| **Renomeação de arquivos** (ex: `doc-user-story-001-us-001-v1.0.md` → `US-01-cadastro.md`) | Média | Quebra links em PRD, TRACEABILITY, C4, WBS | Hook `pre-commit` validar refs |
| **Mudança de path** (ex: `docs/strategy/` → `docs/proddoc-arch-0006-uc-v1t/`) | Baixa | Quebra em massa | Não planejado |
| **Remoção de seção/âncora** (ex: `# 2. Critérios` removido) | Média | Links internos quebrados | Validação Markdown lint |
| **Atualização de versão sem atualizar refs** (ex: `spec-004` → `spec-005`) | Alta | Rastreabilidade perdida | Hook `pre-commit` cross-ref |

### 4.3 Ferramentas de Validação Atuais
| Ferramenta | Uso | Status |
|------------|-----|--------|
| `markdownlint` | Lint Markdown (headings, links, formatting) | ❌ Não configurado no CI |
| `lychee` / `markdown-link-check` | Verificar links internos/externos | ❌ Não configurado |
| `grep` manual | Verificação ad-hoc (feita hoje) | ✅ Funciona mas manual |
| `scripts/validate-refs.py` | Validação automatizada cross-refs | ❌ Não existe |

---

## 5. Scripts Obrigatórios Ausentes (Constitution Art. 17.1, 17.3)

| Script | Finalidade | Dependências | Prioridade |
|--------|------------|--------------|------------|
| `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py` | Dispatch L0 agents via roster `.ai/agents/config-registry-0001-registry-v1.0.yaml`; input: handoff JSON; output: `dod` + `kill_switch` | `PyYAML`, `httpx` (se HTTP) | **P0** (Art. 17.3) |
| `scripts/script-handoff-0001-parse-handoff-v1.0.py` | Parse `.ai/handoffs/HF-*.md` → extrai metadata (task_id, spec_id, origin, wave) → valida schema | `PyYAML`, `markdown-it-py` | **P0** (Art. 17.3, SDD flow) |
| `scripts/script-validate-0001-validate-refs-v1.0.py` | Valida cross-refs Markdown: `docs/...`, `.ai/specs/...`, `.ai/handoffs/...`, `backend/...`, `frontend/...` | `markdown-it-py`, `pathlib` | **P1** (Sanitização contínua) |
| `scripts/sync_github_projects.py` | Sincroniza GitHub Projects ↔ Issues ↔ Milestones ↔ Labels (bidirecional) | `PyGithub`, `gh` CLI | **P1** (Rastreabilidade) |
| `scripts/arch_audit.py` | Auditoria arquitetura: Clean Arch (Domain não importa FastAPI/SQLAlchemy), parameterized queries, PT-BR naming | `ast`, `sqlalchemy` | **P1** (Art. 17.8) |
| `scripts/script-security-0001-secret-scan-v1.0.py` | Pre-commit: scan staged files para segredos (regex `config-env-0001-env-example-v1.0`, `secrets/`, `*.pem`, `*.key`, `*.secret`, JWT, API keys) | `re`, `git` | **P0** (Art. 7.7, 17.7) |
| `scripts/script-ci-0001-ci-green-check-v1.0.py` | Pre-push: verifica último run CI (`gh run list`) = sdoc-arch-0006-uc-v1cess | `gh` CLI, `PyGithub` | **P0** (Art. 9.9, 17.5) |

---

## 6. Plano de Ação Proposto (Priorizado)

### Fase 0 — Imediato (Esta Semana) — **P0 Bloqueadores**
| # | Ação | Responsável | Entregável | Critério Done |
|---|------|-------------|------------|---------------|
| 1 | Criar `scripts/script-security-0001-secret-scan-v1.0.py` + hook `pre-commit` | DevOps | Script + `.git/hooks/pre-commit` | Commit com `config-env-0001-env-example-v1.0` bloqueado |
| 2 | Criar `scripts/script-ci-0001-ci-green-check-v1.0.py` + hook `pre-push` | DevOps | Script + `.git/hooks/pre-push` | Push sem CI verde bloqueado |
| 3 | Criar `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py` (stub MVP) | Backend | Script funcional | Dispatch handoff → L0 retorna `dod`+`kill_switch` |
| 4 | Criar `scripts/script-handoff-0001-parse-handoff-v1.0.py` (stub MVP) | Backend | Script funcional | Parse `HF-XXXX.md` → metadata válida |
| 5 | Configurar GitHub Branch Protection (`main`, `stage`) | Tech Lead | Regras ativas | Push direto bloqueado; PR + CI + 1 approval obrigatório |
| 6 | Configurar GitHub Secret Scanning + Push Protection | Tech Lead | Alertas ativos | Segredo commitado → alerta + bloqueio |

### Fase 1 — Sprint 1 (Próxima) — **P0/P1 Operacionais**
| # | Ação | Responsável | Entregável | Critério Done |
|---|------|-------------|------------|---------------|
| 7 | Mover runbooks templates → instâncias executáveis | DevOps | `RUNBOOK-DB-RESET.md`, `RUNBOOK-INCIDENT.md`, `RUNBOOK-BACKUP.md`, `RUNBOOK-RELEASE.md` | Cada runbook testado em staging |
| 8 | Criar `scripts/script-validate-0001-validate-refs-v1.0.py` + integrar no CI | QA | Script + job CI `validate-refs` | PR com link quebrado → CI falha |
| 9 | Adicionar `markdownlint` + `markdown-link-check` no CI | QA | CI job `lint-docs` | Link quebrado → CI falha |
| 10 | Configurar webhook GitHub → Discord (PR opened/merged, release) | DevOps | Webhook ativo | Notificação no canal `#cobeco-prs` |
| 11 | Criar `scripts/sync_github_projects.py` (unidirecional: Issues → Projects) | DevOps | Script + agendamento diário | Board sincronizado diariamente |

### Fase 2 — Sprint 2 — **P1/P2 Qualidade**
| # | Ação | Responsável | Entregável | Critério Done |
|---|------|-------------|------------|---------------|
| 12 | Implementar `scripts/arch_audit.py` (Clean Arch, param queries, PT-BR) | Arquiteto | Script + job CI `arch-audit` | Violação Clean Arch → CI falha |
| 13 | Popular `.planning/graphs/` com DAG dependências (specs → handoffs → code) | Arquiteto | Graph DAG JSON/GraphML | Visualização dependências |
| 14 | Indexação RAG specs/handoffs em `.planning/` (Art. 17.4) | Backend | Embeddings + busca semântica | Query "auth spec" → retorna spec-004 |
| 15 | Runbook "Game Day" mensal: testar rollback, restore, incident response | DevOps | Agenda + checklist | 0 falhas em simulação |

### Fase 3 — Contínuo (Pós-MVP) — **P2 Melhoria**
| # | Ação | Responsável | Entregável |
|---|------|-------------|------------|
| 16 | Dashboard cross-refs health (Grafana/Prometheus ou simples HTML) | DevOps | `/health/refs` endpoint |
| 17 | Auto-fix cross-refs simples (renomeação → update refs) | Backend | `scripts/fix_refs.py --dry-run` |
| 18 | Integração MCP GitHub Kanban (Art. 17.6) | Backend | MCP server funcional |

---

## 7. Decisões Necessárias do CCB (Para Validação)

| Decisão | Opções | Recomendação | Impacto |
|---------|--------|--------------|---------|
| **D1** | Hook `pre-commit`: bloquear commit se segredo detectado vs apenas warn | **Bloquear** (fail-fast) | Segurança > Velocidade |
| **D2** | Hook `pre-push`: exigir CI verde vs apenas warn | **Exigir CI verde** (Art. 9.9) | Qualidade > Velocidade |
| **D3** | `nexus_dispatcher.py`: implementação completa vs stub MVP | **Stub MVP** (dispatch HTTP local → L0 mock) | Desbloquear SDD flow sem depender de infra L0 completa |
| **D4** | `handoff_parser.py`: parse full markdown vs extração regex simples | **Regex simples** (frontmatter YAML + seções conhecidas) | MVP rápido, refatorar depois |
| **D5** | Runbooks: manter como Markdown executável vs migrar para ferramenta (RunDeck, etc.) | **Markdown + config-make-0001-makefile-v1** (simplicidade, versionado, zero dep) | Consistência Docs-as-Code |
| **D6** | Validação cross-refs: no CI (bloqueante) vs pre-commit (local) | **CI bloqueante** (garante porta de entrada) | CI é source of truth |
| **D7** | Webhook GitHub Projects sync: unidirecional (Issue→Project) vs bidirecional | **Unidirecional Issue→Project** (simplicidade) | GitHub Projects é view, Issue é truth |
| **D8** | Frequência sanitização cross-refs: a cada commit (pre-commit) vs diário (CI scheduled) | **CI diário + pre-commit** (dupla camada) | Cobertura total |

---

## 8. Métricas de Sdoc-arch-0006-uc-v1esso (KPIs)

| Métrica | Baseline Atual | Target Pós-Implementação | Frequência Medição |
|---------|----------------|--------------------------|-------------------|
| **Segredos commitados** | 0 (manual) | 0 (automatizado, bloqueado) | Cada commit |
| **Push sem CI verde** | Possível (manual) | 0 (bloqueado no pre-push) | Cada push |
| **Cross-refs quebrados** | 0 (verificação manual única) | 0 (CI contínuo) | Cada PR + diário |
| **Runbooks testados** | 1/7 (Deploy apenas) | 7/7 (todos testados em staging) | Mensal (Game Day) |
| **Tempo deploy → rollback** | ~10 min (manual) | < 3 min (runbook validado) | Cada deploy |
| **Tempo detecção segredo** | Pós-commit (manual) | Pré-commit (instantâneo) | Cada commit |
| **Sincronia GitHub Projects** | Manual (semanal) | Automática (diária + webhook) | Diária |
| **Conformidade Clean Arch** | Code review manual | CI automatizado | Cada PR |

---

## 9. Riscos de Implementação

| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|-----------|
| Hooks `pre-commit`/`pre-push` atrapalham fluxo (falsos positivos) | Média | Baixo | Testar em branch `chore/hooks-test` antes de merge; bypass `git commit --no-verify` documentado |
| `nexus_dispatcher.py` stub não atende SDD completo | Alta | Médio | Definir contrato mínimo (input handoff JSON → output `dod`/`kill_switch`); evoluir incrementalmente |
| Validação cross-refs no CI falha por links externos (GitHub, URLs) | Média | Baixo | `markdown-link-check` com `--exclude` para domínios externos; tolerar 404 temporário |
| GitHub Branch Protection impede hotfix emergencial | Baixa | Alto | Regra: `main`/`stage` protegidas; hotfix via `feat/hotfix-*` → PR → merge rápido |
| Webhook Discord expõe token | Baixa | Crítico | Token em GitHub Secrets; webhook apenas `repo:push`, `pull_request` events |

---

## 10. Próximos Passos Imediatos (Pós-Aprovação CCB)

1. **Aprovar decisões D1–D8** acima
2. **Criar branch `chore/operational-automation`** com:
   - `scripts/script-security-0001-secret-scan-v1.0.py` + `pre-commit`
   - `scripts/script-ci-0001-ci-green-check-v1.0.py` + `pre-push`
   - `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py` (stub)
   - `scripts/script-handoff-0001-parse-handoff-v1.0.py` (stub)
   - GitHub Branch Protection rules
3. **Testar em staging** (dia 1)
4. **Merge em `main`** via PR + CI verde + CCB approval (dia 2)
5. **Iniciar Fase 1** (Sprint 1) com runbooks executáveis + `validate_refs.py` no CI

---

## Anexos

- **Anexo A:** `.gitignore` atual (já conforme Art. 7.1)
- **Anexo B:** `config-make-0001-makefile-v1` targets existentes (`up`, `down`, `test`, `test-cov`, `ci`, `seed`, `migrate`, `health`, `backup`, `ports-free`)
- **Anexo C:** `.github/workflows/config-ci-0001-github-actions-v1.0.yml` (ruff + pytest --cov≥80 + mypy + build Docker < 5 min)
- **Anexo D:** `.ai/agents/config-registry-0001-registry-v1.0.yaml` (roster agents para `nexus_dispatcher.py`)

---

**Fim do Levantamento**  
*Aguardando revisão e validação do CCB para priorização e execução.*