---
id: spec-infra-0001-cicd-pipeline-v1.0
type: spec-infra
title: SPEC INFRA — Cicd Pipeline
version: v1.0
status: ratificado
canonical: false
canonical_slug: cicd-pipeline
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
domain: specs
layer: spec
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
---
spec_id: spec-011
specname: cicd-pipeline-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: hf-exec-0612 (TA-0056) | sender: agent-nexus-prime-ultimate | incorpora parcela de consulta TA-0048 (agent-devops, hf-exec-0604:33-46)
task: TA-0056 | handoff: hf-exec-0612 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (CI/CD)
lgpd-class: filenames LGPD-safe (artefatos de CI sem PII; credenciais do banco dummy e efêmeras, ci.yml:120,130)
trace:
  - .ai/handoffs/hf-exec-0612-spec-011-cicd-pipeline-v1-v1.0.md (envelope da tarefa)
  - .ai/handoffs/hf-exec-0604-consulta-de-dominio-v1.0.md:33-46 (parcela de consulta TA-0048, agent-devops, 2026-11-03)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:39 (B.7), :51 (C.4), :59 (D.2)
  - .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:72 (REQ-11), :164 (doc-user-story-0008-us-008), :167 (doc-user-story-0011-us-011)
  - .ai/specs/spec-arch-0001-container-layers-v1.0.md:184-195 (§7.3), :198-212 (§8), :210 (C.4), :211, :352
  - .github/workflows/config-ci-0001-github-actions-v1.0.yml (189 linhas — auditado diretamente no filesystem em 2026-11-03)
  - .github/workflows/sddai-verify.yml (44 linhas — wc -l, 2026-11-03)
  - .ai/agents/config-ledger-0001-ledger-v1.0.yaml:24 (drift G-05 — registro HISTÓRICO, não editar)
  - docs/planos/plano-granular/plano-producao-agentes.md:33 (G-05)
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84 (P-01), :94 (P-06), :124 (Art. 4.6), :219 (Art. 10.4)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-devops.md:6 ("Automation serves gates, never bypasses them")
---

# SPEC spec-011 — cicd-pipeline-v1 — Pipeline CI/CD do COBECO (lint+testes ≤5 min por push, falha bloqueando merge)

Status: SPEC EMITIDA — PENDENTE DE REVISÃO E DE IMPLEMENTAÇÃO (onda seguinte, Art. 6.1 SDD) | Tarefa: TA-0056 (handoff `.ai/handoffs/hf-exec-0612-spec-011-cicd-pipeline-v1-v1.0.md`) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única das decisões de pipeline CI/CD do COBECO. Em conflito, vale a hierarquia do Art. 2 da Constituição (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:41-50; resolução de cima para baixo, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).

Convenções: citação `arquivo:linha`. Identificadores/status/caminhos em EN; narrativa em PT-BR (P-10). Toda alegação sem fonte está marcada **UNKNOWN - verify** (P-08). Esta SPEC **define** o pipeline; ela **não implementa** código nem edita workflows (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150 — especifica → implementa → valida → registra).

---

## 1. Contexto e origem

Nasce da task TA-0056 (hf-exec-0612), item **B.7** da LISTA (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:39): "Pipeline CI/CD — lint+testes ≤5 min/push, gates", parcialmente coberto pela `spec-005` §8 (fase única; spec-005:198-212), que deixou o nome exato do job de rede de contratos como **UNKNOWN - verify** (spec-005:210) — lacuna **C.4** (LISTA:51). Integra a onda 5 "Infraestrutura, Automação e Segurança" (D.2, LISTA:59; plano-producao-agentes.md:133-143).

Requisitos de origem: **REQ-11** — "Pipeline CI | lint+testes ≤5min/push (req_1.0.md:31) | N7.1 | **Must**" (spec-002-requisitos-review-round-1.spec.md:72) e **doc-user-story-0011-us-011** — "Given um push em feature branch; When o pipeline executa; Then lint+testes concluem em ≤5min e falha bloqueia merge" (spec-002:167).

**Insumo de domínio:** a parcela de consulta **TA-0048** (agent-devops, 2026-11-03, hf-exec-0604:33-46) auditou o estado REAL do `ci.yml` e recomendou 6 correções; esta spec incorpora essa parcela com citação por item (§3.1-§3.7) e resolve as duas pendências que a consulta fixou: **G-05 fechável por implementação preexistente** (drift descritivo) e **C.4 fecha com nome fixado** (`contract-network`, §3.4).

---

## 2. Resolução de conflitos

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| **G-05** — "`ci.yml` vazio" (plano-producao-agentes.md:33) × realidade de 189 linhas (ledger.yaml:24) | **FECHADO como drift descritivo.** O plano está obsoleto; o arquivo tem 189 linhas com 6 jobs (auditado diretamente, 2026-11-03, §3.1). A parcela TA-0048 registra: "DRIFT G-05 CONFIRMADO/FECHAVEL: plano-producao-agentes.md:33 ('ci.yml vazio') obsoleto; ledger.yaml:24 (TA-0029, HISTORICO nao editar) ja registrava 189 linhas; spec-011 registra G-05 como FECHADO por implementacao preexistente, delta only" (hf-exec-0604:42) | Auditoria direta do filesystem (ci.yml, 2026-11-03) + parcela TA-0048 (hf-exec-0604:42) | `docs/planos/plano-granular/plano-producao-agentes.md:33` ("G-05 \| `ci.yml` vazio") — registro histórico intocado; delta remanescente de G-05 declarado em §3.1 (nenhum job constrói as camadas Docker; timeout 15 min) |
| **doc-user-story-0011-us-011** — ≤5 min/push × `timeout-minutes: 15` do `test-suite` (ci.yml:111) | Vence REQ-11 (Must, spec-002:72) e doc-user-story-0011-us-011 (spec-002:167). doc-user-story-0011-us-011 está **NÃO ATENDIDO** hoje; a redução 15→≤5 e a paralelização são obrigação de implementação (delta D-01/D-02, §3.3), jamais contornada (sem skip — kill switch #1) | spec-002:72,167; spec-005:208 ("enquanto não reduzido, doc-user-story-0011-us-011 está não atendido"); parcela TA-0048 correção (1) | Estado atual do ci.yml:111 (timeout 15) e ci.yml:154-158 (flake8+mypy sequenciais dentro do test-suite) |
| **C.4** — nome do job `contract-network` como `UNKNOWN - verify` (spec-005:210) | **FECHADO: o nome é FIXADO como `contract-network`** nesta spec (§3.4), conforme recomendação da parcela TA-0048 ("spec-011 FIXA nome contract-network como job novo"; hf-exec-0604:42) e mandato do hf-exec-0612:17 | hf-exec-0612:17; hf-exec-0604:42; LISTA:51 | `spec-005-container-layers-v1.spec.md:210` ("nome exato: UNKNOWN - verify") — texto histórico da spec-005 preservado; resolvido por spec posterior |
| **C-07** (avaliada; NÃO relevante) | C-07 trata de ambiguidade de latência (cotação ≤2s × aplicação ≤3s P95, spec-002:126) — não toca CI/CD. Sem delta para este domínio | spec-002:126 | n/a |

---

## 3. Domínio — requisitos, estado auditado e contratos do pipeline

### 3.1 Estado atual auditado (evidência direta no filesystem, 2026-11-03)

`.github/workflows/config-ci-0001-github-actions-v1.0.yml` — **189 linhas**, nome "COBECO CI/CD Pipeline" (ci.yml:1); triggers `push`/`pull_request` em `main` (ci.yml:3-7); `concurrency` com `cancel-in-progress: true` (ci.yml:9-11). **6 jobs**, todos em `ubuntu-latest`:

| # | Job (id em ci.yml) | timeout | needs | Função verificada (linha real) |
|---|---|---|---|---|
| 1 | `kill-switch-check` (:17) | 5 (:20) | — | Verifica `kill_switch.trigger`; `exit 1` se ativo (:25-31). **Primeiro job** — Art. 4.6 |
| 2 | `foss-compliance` (:36) | 10 (:39) | kill-switch-check (:40) | `scripts/security_scan.py --strict` (:47); scanner de credenciais reais (:50-59); LGPD-safe declarado (:61-64) |
| 3 | `sdd-validation` (:69) | 10 (:72) | kill-switch-check (:73) | `validate_nexus_yaml.py` com `rejeitados == 0` (:80-81); `dag_validator.py --strict` (:85) |
| 4 | `agent-health` (:91) | 10 (:94) | kill-switch-check (:95) | `agent_health_check.py --strict` (:102) |
| 5 | `test-suite` (:108) | **15** (:111) | sdd-validation + agent-health (:112) | PostgreSQL efêmero **digest-pinned** (:117), credencial dummy (:120,130); flake8 (:154-155); mypy (:157-158); round-trip Alembic (:160-166); `pytest tests/ -q --cov=src --cov-report=term-missing --cov-fail-under=80` **fail-closed** (:170) |
| 6 | `final-status` (:176) | 5 (:179) | todos os 5 anteriores (:180) | **Appends efêmeros em `.ai/agents/config-ledger-0001-ledger-v1.0.yaml`** (:185-189 — a escrita ocorre em :187-189) |

Existe também `.github/workflows/sddai-verify.yml` com **44 linhas** (`wc -l`, 2026-11-03; coerente com spec-005:203).

**Deltas de G-05 que permanecem** (coerente com spec-005:202): (i) nenhum job constrói/sobe as camadas Docker; (ii) `test-suite` tem `timeout-minutes: 15` (ci.yml:111); (iii) não há job `contract-network` (leitura integral do arquivo, 2026-11-03). Além disso, verificado por grep: **não há chave `permissions:` em ci.yml** (zero matches, 2026-11-03).

### 3.2 Requisitos do pipeline (normativos)

- **R-01 — Feedback ≤5 min/push:** lint + testes concluem em ≤5 min por push (REQ-11, spec-002:72; doc-user-story-0011-us-011, spec-002:167). O orçamento aplica-se ao *feedback* de lint+testes; jobs paralelos podem excedê-lo isoladamente (leitura da spec-005:209).
- **R-02 — Falha bloqueia merge:** qualquer gate vermelho derruba o pipeline e o merge fica bloqueado (doc-user-story-0011-us-011, spec-002:167; doc-user-story-0008-us-008, spec-002:164).
- **R-03 — Gates nunca bypassados:** nenhum job pode ser pulado por label, `continue-on-error` ou re-run seletivo (spec-005:211; agent-devops.md:6 — "Automation serves gates, never bypasses them").
- **R-04 — Free Tier P-01:** uso do GitHub Actions Free Tier é **Bypass registrado** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84; spec-005:211) — não veta, mas exige disciplina (§3.7).

### 3.3 Delta requerido sobre o estado atual (doc-user-story-0011-us-011 NÃO ATENDIDO hoje)

As seis correções recomendadas pela parcela TA-0048 (hf-exec-0604:42, "CORRECOES RECOMENDADAS spec-011"), elevadas a delta normativo desta spec:

| # | Delta | Estado atual (linha real) | Alvo |
|---|---|---|---|
| D-01 | Reduzir `timeout-minutes` do `test-suite` de 15 para **≤5** | ci.yml:111 | ≤5 min (doc-user-story-0011-us-011, spec-002:167) |
| D-02 | **Paralelizar** lint (flake8) e mypy em **job próprio**, simultâneo à suíte de testes | sequenciais dentro do `test-suite` (ci.yml:154-155, :157-158) | job dedicado, sem alargar o caminho crítico |
| D-03 | Adicionar `permissions: contents: read` em nível de workflow (menor privilégio) | chave ausente (grep zero matches, 2026-11-03) | menor privilégio — o token do runner não ganha escrita que nenhum job usa |
| D-04 | **SHA-pin de actions** — fixar cada `uses:` por digest SHA do commit, não por tag mutável | `actions/checkout@v4` (ci.yml:23,43,76,98,133,183); `actions/setup-python@v5` (ci.yml:136) | kill switch #4 do contrato devops — "untrusted action unpinned (supply chain) - SHA-pin or BLOCK" (agent-devops.md:41); tag mutável pode ser trocada a jusante e injetar bypass de gate |
| D-05 | **Artifact upload** de `coverage.xml` + junit com **filenames LGPD-safe** | cobertura só em stdout (`term-missing`, ci.yml:170) | evidência auditável do gate ≥80% (doc-user-story-0008-us-008, spec-002:164) sem PII em nome/conteúdo |
| D-06 | **REMOVER o append efêmero em `.ai/agents/config-ledger-0001-ledger-v1.0.yaml`** (escrita perdida no runner efêmero, nunca pushed); substituir por `GITHUB_STEP_SUMMARY` + run URL — **CI lê, nunca muta o repo** | ci.yml:185-189 (appends em :187-189) | zero escrita em `.ai/` pelo CI; rastreabilidade via summary/URL do run |

D-01..D-06 são **obrigações de implementação** da onda seguinte (Art. 6.1) — ver Fora de escopo, §6.

### 3.4 Job `contract-network` (fecha C.4)

O nome é **FIXADO**: `contract-network` (resolve o `UNKNOWN - verify` de spec-005:210; mandato hf-exec-0612:17; recomendação parcela TA-0048, hf-exec-0604:42 — "stack efemera digest-pinned, casos SS7.3 spec-005, needs:[test-suite], timeout <=10, sem porta no host"). Contrato completo do job:

- **Nome do job (id YAML):** `contract-network` — literal, inalterável (chave de rastreabilidade entre spec-005 §8.3, LISTA:51 e o workflow).
- **Dependência:** `needs: [test-suite]` — só roda com a suíte verde (fail-closed).
- **Stack efêmera digest-pinned:** sobe a stack de compose por run e descarta ao fim; todo `image:` com digest (precedente do Postgres do CI, ci.yml:117; Art. 10.2).
- **Orçamento:** `timeout-minutes` ≤10 (parcela TA-0048, hf-exec-0604:42).
- **Rede/isolamento:** **nenhuma porta publicada no host**; comunicação só por rede interna de compose (Art. 10.1; análogo ao negativo de spec-005:190).
- **Casos executados:** os 5 casos binários da §7.3 da spec-005 (spec-005:186-192) — (1) `back` conecta em `db:5432` (positivo); (2) `front` NÃO alcança `db:5432` (negativo); (3) `db` sem porta no host, `docker compose port` vazio (negativo); (4) `front` alcança `back:8000/v1/health` com 200 (positivo); (5) rotas `/v1` compatíveis com spec-004 §3 (contrato HTTP). Marcador pytest sugerido: `compose` (proposta de spec-005:210) — a escolha final do marker é da implementação; **o nome do JOB não é**.
- **Fail-closed:** qualquer caso violado = job vermelho = pipeline vermelho = merge bloqueado (R-02).

### 3.5 Gates intransferíveis (nunca removidos, nunca reordenados abaixo do kill switch)

1. **`kill-switch-check` primeiro e obrigatório** em qualquer extensão do workflow (ci.yml:17; spec-005:212; Art. 4.6, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124; veto herdado por todos os agentes — contratos em agent-sdd-specialist.md:39-46).
2. **Cobertura ≥80% fail-closed:** `--cov-fail-under=80` permanece (ci.yml:170); cobertura <80% derruba o pipeline (REQ-08, spec-002:69; doc-user-story-0008-us-008, spec-002:164).
3. **Scanner de credenciais e validações SDD/DAG** permanecem (ci.yml:47,50-59,80-81,85 — P-07/Art. 7.2; Art. 4.5/6.1).
4. Nenhum bypass por label/`continue-on-error`/re-run seletivo (R-03; spec-005:211).

### 3.6 Merge-blocking como pré-condição (nunca substitui aprovação)

CI verde é **pré-condição** de merge — **nunca** é a aprovação em si. O merge exige reviewer → gatekeeper (P-06, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94; Art. 10.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219; spec-005:211). A parcela TA-0048 fixa: "merge-bloqueio: CI green = pre-condicao, nunca aprovacao (gatekeeper+Humano)" (hf-exec-0604:42). O mecanismo técnico de bloqueio (required status checks / branch protection) é configuração do GitHub, **não versionável no filesystem** — **UNKNOWN - verify** (§7a), declarado como AC-10 (condição pendente de verificação, não de invenção).

### 3.7 Disciplina Free Tier (P-01 — Bypass registrado)

Conforme constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84 e spec-005:211, o uso do Free Tier do GitHub Actions é Bypass **registrado** (este parágrafo é o registro em spec). Disciplina da parcela TA-0048 (hf-exec-0604:42, "FREE TIER P-01"): triggers mínimos (apenas `push`/`pull_request` em `main`, ci.yml:3-7), `cancel-in-progress` (ci.yml:9-11), **sem matriz** de versões/OS, **sem self-hosted runners com secrets**, auditoria mensal de minutes consumidos. O custo do job `contract-network` (compose no CI) no orçamento de minutes é **UNKNOWN - verify** (§7c).

---

## 4. Critérios de aceite e testes

Critérios binários, verificáveis na implementação (onda seguinte) — cada um com método de verificação:

- [ ] **AC-01** — o caminho lint+testes conclui em ≤5 min wall-clock num run real pós-implementação; `timeout-minutes` do(s) job(s) de lint+testes ≤5 (ci.yml:111 substituído). *Verificação:* URL do run no `GITHUB_STEP_SUMMARY` (D-06) + leitura do YAML. (O valor wall-clock prévio é UNKNOWN — §7b.)
- [ ] **AC-02** — flake8 e mypy executam em job próprio, paralelo ao restante da suíte (D-02). *Verificação:* leitura do YAML — `needs` não encadeia lint após testes.
- [ ] **AC-03** — `permissions: contents: read` presente no nível de workflow (D-03). *Verificação:* `grep -n "permissions" .github/workflows/config-ci-0001-github-actions-v1.0.yml` ≥1 match (hoje: zero).
- [ ] **AC-04** — todo `uses:` pinnado por SHA de commit; zero referências por tag mutável (`@v4`, `@v5`) (D-04; hoje ci.yml:23,43,76,98,133,183,136). *Verificação:* grep por `@v` = zero matches.
- [ ] **AC-05** — `coverage.xml` + relatório junit publicados como artifacts com filenames LGPD-safe (D-05). *Verificação:* `actions/upload-artifact` no YAML + inspeção dos nomes; conteúdo coberto pelo scanner de credenciais (ci.yml:50-59).
- [ ] **AC-06** — zero appends em `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` a partir de workflows (D-06). *Verificação:* `grep -rn ">> .ai/agents/config-ledger-0001-ledger-v1.0.yaml" .github/workflows/` = zero matches (hoje: ci.yml:187-189); resumo via `GITHUB_STEP_SUMMARY` com run URL.
- [ ] **AC-07** — job `contract-network` existe com **nome exato**, `needs: [test-suite]`, `timeout-minutes` ≤10, **zero portas no host**, e executa os 5 casos de spec-005:188-192 (§3.4). *Verificação:* leitura do YAML + run verde/vermelho coerente com violação proposital de um caso (teste do teste).
- [ ] **AC-08** — `kill-switch-check` permanece o primeiro job em qualquer extensão do workflow (§3.5.1; ci.yml:17). *Verificação:* ordem topológica no YAML.
- [ ] **AC-09** — `--cov-fail-under=80` permanece fail-closed (ci.yml:170); um run com cobertura <80% simulada derruba o pipeline. *Verificação:* run de sanidade.
- [ ] **AC-10** — required status checks / branch protection configurados de modo que pipeline vermelho bloqueie o merge. *Verificação:* UI/Admin do GitHub. **UNKNOWN - verify** (§7a) — condição de aceite pendente de verificação fora do filesystem; não bloqueia a emissão desta spec.
- [ ] **AC-11** — esta emissão não altera nenhum arquivo além de `.ai/specs/spec-infra-0001-cicd-pipeline-v1.0.md` (ci.yml e workflows intocados — Art. 6.1). *Verificação:* `git status`/`git diff`.

---

## 5. Rastreabilidade (dupla)

| Fonte | Linha | O que ancora nesta spec |
|---|---|---|
| REQ-11 (spec-002-requisitos-review-round-1.spec.md) | :72 | Pipeline CI — lint+testes ≤5min/push — Must, fase N7.1 → R-01 |
| doc-user-story-0011-us-011 (spec-002) | :167 | "lint+testes concluem em ≤5min e falha bloqueia merge" → R-01, R-02, AC-01 |
| REQ-08 / doc-user-story-0008-us-008 (spec-002) | :69, :164 | Cobertura ≥80% validada por CI, senão merge bloqueado → §3.5.2, AC-09 |
| spec-005 §8 (container-layers) | :198-212 | Delta base: fatos do CI (:200-204), proposta lint-and-unit ≤5min (:208), `contract-network` UNKNOWN (:210 — resolvido em §3.4), gates (:211), kill switch primeiro (:212) |
| spec-005 §7.3 | :184-195 | Os 5 casos binários de contrato de rede executados pelo job `contract-network` (§3.4) |
| G-05 (plano-producao-agentes.md × ledger.yaml) | :33 × :24 | Drift auditado e FECHADO (§2, §3.1); ledger histórico intocado |
| C.4 (LISTA-SPECS-PENDENTES) | :51 | Nome do job `UNKNOWN - verify` → FIXADO `contract-network` (§3.4, AC-07) |
| B.7 / D.2 (LISTA) | :39, :59 | Origem B.7; encaixe na onda 5 (A.14-A.18, plano:133-143) |
| Parcela TA-0048 (hf-exec-0604) | :33-46 | Estado real 189 l/6 jobs, 6 correções (D-01..D-06), Free Tier P-01, merge-blocking, UNKNOWNs §7 |
| constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md | :84, :94, :124, :219 | P-01 (Bypass registrado), P-06 (gates humanos), Art. 4.6 (kill switch), Art. 10.4 (ortogonalidade barrada por reviewer→gatekeeper) |
| agent-devops.md | :6 | "Automation serves gates, never bypasses them" — fundamento de R-03 |

---

## 6. Fora de escopo (YAGNI)

- **IMPLEMENTAÇÃO das correções D-01..D-06 e do job `contract-network` no `ci.yml`** — tarefa separada de devops, onda de implementação (Art. 6.1). Esta spec **DEFINE** o pipeline; **nenhum arquivo em `.github/workflows/` é editado nesta emissão** (AC-11; mandato hf-exec-0612; prática de hf-exec-0029/hf-exec-0030 registrada em spec-005:348).
- Camada CI como camada do Art. 10.1 e runtime L1 de agentes — item **B.10**, destinado à **spec-014** (LISTA:42; spec-005:352; parcela TA-0048 item (d), hf-exec-0604:42).
- CD/deploy contínuo, ambientes de staging/prod, gestão avançada de secrets, ambientes efêmeros por PR.
- Matriz de versões/OS, self-hosted runners, cache remoto de imagens — vedados pela disciplina Free Tier (§3.7).
- Configuração de branch protection (AC-10) — ato de configuração GitHub, não desta spec.
- C-07 (latência de API, spec-002:126) — domínio alheio (§2).
- Alteração de `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` (registro histórico — TA-0029; MANIFEST:15-18) — o ajuste é a REMOÇÃO da escrita pelo CI (D-06), nunca edição do arquivo.

## 7. Registro UNKNOWN - verify (P-08)

- **(a) Branch protection / required status checks** — configuração do GitHub, não versionada no filesystem; wall-clock de bloqueio real dependente dela (parcela TA-0048, hf-exec-0604:42, "UNKNOWN - verify: (a) required status checks/branch protection (config GitHub, nao filesystem)"). Caminho de verificação: UI Admin → Settings → Branches.
- **(b) Wall-clock real por run** — nenhum run histórico medido; AC-01 valida após a implementação (parcela item (b)).
- **(c) Budget Free Tier do compose no CI** — wall-clock/minutes do `docker compose build`/stack efêmera do `contract-network` no orçamento Free Tier (parcela item (c)).
- **(d) Verde do pipeline com o baseline atual de testes** — `pytest tests/` inclui `tests/agents` com baseline **4 failed / 149 passed / 1 skipped** (ledger.yaml:24; MANIFEST:118-120): **UNKNOWN - verify** se o CI fica verde hoje. Proibido skip de testes pelo CI — kill switch #1 do contrato devops ("gate bypass: CI skips, [skip ci] abuse, workflow disable", agent-devops.md:38), fonte da recomendação "proibido skip (kill switch #1)" da parcela TA-0048 (hf-exec-0604:42); a implementação deve declarar escopo explícito de suíte (unit+integration+agents).

---

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0056, hf-exec-0612): emissão inicial. Auditoria do estado real do ci.yml (189 linhas, 6 jobs — §3.1); drift G-05 declarado FECHADO por implementação preexistente (§2, §3.1); doc-user-story-0011-us-011 declarado NÃO ATENDIDO com 6 deltas normativos D-01..D-06 incorporados da parcela TA-0048 (hf-exec-0604:33-46) (§3.3); C.4 FECHADO — nome do job fixado como `contract-network` com contrato completo (§3.4); gates intransferíveis (§3.5); merge-blocking como pré-condição, nunca aprovação (§3.6); disciplina Free Tier P-01 registrada (§3.7); 11 AC binários (§4); rastreabilidade dupla (§5); escopo negativo com implementação do ci.yml fora desta spec (§6); 4 UNKNOWNs registrados (§7).
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo A): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `handoff` em `origin`; `version` 0.1.0 → 0.2.0). Deltas D-01..D-06 já implementados no `ci.yml` (commit `d657118`..`2765903`): timeout 15→5 min, job lint separado, `permissions: contents: read`, SHA-pin de actions, artifacts `coverage.xml`+`junit.xml`, remoção de append em `.ai/agents/config-ledger-0001-ledger-v1.0.yaml`. Job `contract-network` fixado (spec-011 §3.4). Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio de §§1–8 reescrita. **Ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)**.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem, task, kill_switch, trace, lgpd-class | frontmatter (`spec_id: spec-011`, `version: 0.2.0`) + linha `Status:` | aplicada |
| (b) Contexto/origem | §1 (origem: hf-exec-0612/TA-0056; parcela hf-exec-0604/TA-0048) | aplicada |
| (c) Resolução de conflitos | §2 (G-05, doc-user-story-0011-us-011, C.4; C-07 avaliada e não relevante) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (estado auditado, R-01..R-04, D-01..D-06, job `contract-network`, gates, Free Tier) | aplicada |
| (e) Critérios de aceite/testes | §4 (AC-01..AC-11, binários com método de verificação) | aplicada |
| (f) Rastreabilidade (REQ/Art./US/arquivo:linha) | §5 (REQ-11, doc-user-story-0011-us-011, G-05, C.4 + fontes) | aplicada |
| (g) Fora de escopo (YAGNI) | §6 (+ UNKNOWNs em §7) | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
