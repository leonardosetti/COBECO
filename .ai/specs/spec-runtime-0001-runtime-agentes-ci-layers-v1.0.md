---
id: spec-runtime-0001-runtime-agentes-ci-layers-v1.0
type: spec-runtime
title: SPEC RUNTIME — Runtime Agentes Ci Layers
version: v1.0
status: ratificado
canonical: false
canonical_slug: runtime-agentes-ci-layers
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
spec_id: spec-014
specname: runtime-agentes-ci-layers-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: HF-0615 (TA-0059) | sender: agent-nexus-prime-ultimate | handoff: HF-0615 | incorpora parcela de consulta TA-0048 (agent-devops, HF-0604:33-46)
task: TA-0059 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (runtime agentes + camada CI)
lgpd-class: zero PII (gates de CI e runtime sem dados pessoais por design; única credencial do CI é dummy efêmera, ci.yml:120,130)
trace:
  - .ai/handoffs/HF-0615-spec-014-runtime-agentes-ci-layers-v1.md:17 (envelope com a CONFIRMAÇÃO DO ORQUESTRADOR)
  - .ai/handoffs/HF-0604-consulta-de-dominio.md:33-46 (parcela de consulta TA-0048, agent-devops, 2026-11-03)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:42 (B.10)
  - .ai/specs/spec-arch-0001-container-layers-v1.0.md:81 (UNKNOWN - verify), :211 (Bypass registrado), :352 (follow-up)
  - .ai/specs/spec-infra-0001-cicd-pipeline-v1.0.md:80-83 (R-01..R-04), :96 (D-06), :112-117 (gates), :168 (reserva B.10 → spec-014)
  - .ai/specs/spec-sdd-0001-sdd-conf-memory-v1.0.md:3-4,16-17 (memória persistente do runtime — cross-ref)
  - .github/workflows/config-ci-0001-github-actions-v1.0.yml (189 linhas — auditado diretamente no filesystem em 2026-11-03)
  - .github/workflows/sddai-verify.yml (44 linhas — auditado diretamente no filesystem em 2026-11-03)
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84 (P-01), :94 (P-06), :104 (P-11), :122 (Art. 4.5), :124 (Art. 4.6), :130 (Art. 4.9), :132 (Art. 4.10), :150 (Art. 6.1), :158-164 (Art. 6.5), :168 (Art. 6.7), :174 (Art. 7.1), :176 (Art. 7.2), :213 (Art. 10.1), :215 (Art. 10.2)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-nexus-prime-ultimate.md:59-65 (BYPASS_PROTOCOL — 3 pilares)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:14 (hardware L1), :33-35 (personas/handoff_parser/sdd-cycle.sh), :39-46 (KILL_SWITCH), :48 (BYPASS_PROTOCOL), :74 (contrato de handoff)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-devops.md:6 ("Automation serves gates, never bypasses them")
  - docs/decisoes/ADR-011-Ecossistema-SDDAI.md:65-68 (MCPs nexus-*), docs/decisoes/ADR-006-inteligencia-sdd.md:57 (symlink active.md)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012)
---

# SPEC spec-014 — runtime-agentes-ci-layers-v1 — Camada CI e runtime de agentes SDD (L1/L3) como camadas do Art. 10.1

Status: SPEC EMITIDA — PENDENTE DE REVISÃO (nada a implementar nesta onda — spec de definição de camadas) | Tarefa: TA-0059 (handoff `.ai/handoffs/HF-0615-spec-014-runtime-agentes-ci-layers-v1.md`, item **B.10** da LISTA) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única da definição das camadas do Art. 10.1 que ficaram FORA da `spec-005` (runtime de agentes SDD e CI). Em conflito, vale a hierarquia do Art. 2 da Constituição (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:41-50; resolução de cima para baixo, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).

Convenções: citação `arquivo:linha`. Identificadores/status/caminhos em EN; narrativa em PT-BR (P-10). Toda alegação sem fonte está marcada **UNKNOWN - verify** (P-08). Esta SPEC **define camadas e fronteiras**; ela **não implementa** código nem edita workflows (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150 — especifica → implementa → valida → registra).

---

## 1. Contexto e origem

Nasce da task **TA-0059** (HF-0615), item **B.10** da LISTA (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:42): "Camadas L1 (runtime de agentes) e CI como camadas do Art. 10.1" — com condição de emissão "escopo a confirmar pelo orquestrador antes de emitir".

Fundamento da pendência: `spec-005-container-layers-v1.spec.md:81` declara, ao fechar o escopo nas camadas de aplicação: "o runner de CI é GitHub Actions Free Tier sob Bypass registrado (P-01, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84) e o runtime de agentes é L1/L3 conforme Art. 6.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:160-162) — **UNKNOWN - verify** se o orquestrador deseja SPEC própria para elas"; o follow-up está listado em spec-005:352 ("SPEC das camadas L1 (runtime de agentes) e CI como camadas do Art. 10.1 — escopo a confirmar"). A auditoria de normalização TA-0031 inventariou o corpus integral (11 arquivos — MANIFEST:92-104) sem nenhuma spec própria dessas camadas, confirmando a inexistência registrada no envelope.

**CONFIRMAÇÃO DO ORQUESTRADOR (nexus-prime-ultimate, 2026-11-03, HF-0615:17):** "**CONFIRMACAO DO ORQUESTRADOR (nexus-prime-ultimate, 2026-11-03): escopo CONFIRMADO.** Fundamento: spec-005:81 declara `UNKNOWN - verify` quanto a spec propria das camadas L1/L3 (runtime de agentes SDD, Art. 6.5) e camada de CI (GitHub Actions Free Tier sob Bypass registrado, P-01); follow-up em spec-005:352. Nenhuma spec propria existe (verificado por auditoria TA-0031). Cobrir: definicao dessas camadas segundo Art. 10.1, limites com spec-005, e o regime de Bypass registrado para CI free-tier. INCORPORE a parcela TA-0048 (agent-devops, camada CI)."

**Insumo de domínio:** a parcela de consulta **TA-0048** (agent-devops, 2026-11-03, HF-0604:33-46) recomendou para este item: "(d) B.10 — recomendo spec-014 cobrir SO a camada CI (workflows como camada Art. 10.1, Bypass P-01, boundaries: gates como contratos de fronteira, zero secrets) e desagregar L1 runtime de agentes para spec propria" (HF-0604:42). A parte CI é incorporada integralmente nesta spec (§3); a divergência sobre a desagregação do L1 está resolvida em §2 e registrada como UNKNOWN em §9d.

---

## 2. Resolução de conflitos

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| **Especiação do B.10** — spec única (CI + runtime L1/L3) × desagregar L1 em spec própria | **Spec ÚNICA (esta)**, cobrindo ambas as camadas, conforme confirmação expressa do orquestrador | **HF-0615:17** (CONFIRMAÇÃO DO ORQUESTRADOR — autoridade L0, Art. 4.5, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:122) | Recomendação da parcela TA-0048 "desagregar L1 runtime de agentes para spec propria" (HF-0604:42, item (d)) — superada quanto à desagregação; a parte CI da mesma parcela ("workflows como camada Art. 10.1, Bypass P-01, boundaries: gates como contratos de fronteira, zero secrets") é **incorporada** (§3). Eventual spec futura dedicada ao L1: **UNKNOWN - verify** (§9d) |
| **Delimitação com spec-005** | Esta spec cobre as camadas do Art. 10.1 que a spec-005 NÃO cobre (runtime de agentes SDD, CI); a spec-005 permanece SSOT de Dados/Back/Front e aderentes (cross-ref apenas, §5) | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 (enumeração das camadas) + spec-005:81 | spec-005:81 ("UNKNOWN - verify se o orquestrador deseja SPEC própria para elas") e spec-005:352 (follow-up "escopo a confirmar") — a dúvida está **resolvida por esta emissão**; textos históricos da spec-005 permanecem intocados |
| **Delimitação com spec-011** | A spec-011 permanece SSOT do **PIPELINE** (requisitos R-01..R-04, deltas D-01..D-06, job `contract-network` — spec-011:80-98,102-110); esta spec define a **CAMADA CI** (natureza de camada do Art. 10.1, contratos de fronteira, regime P-01) sem redefinir requisitos de pipeline | spec-011:168 — reserva expressa: "Camada CI como camada do Art. 10.1 e runtime L1 de agentes — item B.10, destinado à **spec-014**" | Qualquer leitura que atribua à spec-011 a definição da camada CI, ou a esta spec a definição de requisitos de pipeline (≤5 min, deltas do ci.yml) — cada permanece na sua spec |
| **Alcance "L1/L3" × Art. 6.5 (L1/L2/L3)** | O runtime aqui definido abrange **L1 e L3** (alcance confirmado no HF-0615:17 e no rótulo do B.10); **L2 (Personas, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:161) fica fora do escopo** — nota de delimitação em §4.5 | HF-0615:17 + constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:158-164 | Leitura que estendesse esta spec ao conteúdo das personas (`.ai/personas/`) — camada distinta por definição constitdoc-arch-0006-uc-v1ional |

---

## 3. Domínio — Camada CI como camada do Art. 10.1

### 3.1 Definição e base constitdoc-arch-0006-uc-v1ional

O Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213) enumera as camadas de execução do projeto: "**runtime de agentes SDD, aplicação, dados, CI**" — e manda que rodem ortogonais: "cada camada é abrigada em container Docker próprio ou em **ambiente isolado equivalente** e pode ser construída, versionada, reiniciada ou substituída independentemente; comunicação entre camadas ocorre **apenas por interface declarada** (porta, volume ou API), nunca por estado implícito compartilhado".

**Definição da camada CI (norma desta spec):** o conjunto dos workflows GitHub Actions versionados em `.github/workflows/`, executados em runner GitHub-hosted efêmero — o "ambiente isolado equivalente" do Art. 10.1 (constituído por run, descartado ao fim, sem estado compartilhado entre runs). Estado real verificado no filesystem (2026-11-03):

- `.github/workflows/config-ci-0001-github-actions-v1.0.yml` — "COBECO CI/CD Pipeline" (ci.yml:1), **189 linhas, 6 jobs**: `kill-switch-check` (:17), `foss-compliance` (:36), `sdd-validation` (:69), `agent-health` (:91), `test-suite` (:108), `final-status` (:176).
- `.github/workflows/sddai-verify.yml` — "SDDAI Verify Pipeline" (sddai-verify.yml:1), **44 linhas**, job único `verify` (:15) com `workflow_dispatch` (:8) e verificação de kill switch (:25).

Ortogonalidade em relação às camadas de aplicação (spec-005): a camada CI não compartilha estado com `db`/`back`/`front` — interage apenas por interfaces declaradas (checkout do repositório, compose do job `test-suite`, artefatos de relatório). Versão e substituição independente: os workflows são versionados no git e alteráveis por PR isolado, sem tocar as demais camadas (Art. 10.1).

### 3.2 Workflows como contratos de fronteira

Incorporação da parcela TA-0048 (HF-0604:42 — "workflows como camada Art. 10.1", "boundaries: gates como contratos de fronteira"): cada workflow é um **contrato de fronteira** entre o repositório (código + specs) e a camada CI. Interfaces declaradas verificadas:

| Contrato de fronteira | Interface declarada | Fato (linha real) |
|---|---|---|
| Entrada repo → CI | trigger `push`/`pull_request` em `main` | ci.yml:3-7; sddai-verify.yml:3-8 (inclui `workflow_dispatch` em :8) |
| Sequenciamento de runs | `concurrency` com `cancel-in-progress: true` | ci.yml:9-11; sddai-verify.yml:10-12 |
| Leitura de estado | `actions/checkout` (única forma de acesso ao repo) | ci.yml:23,43,76,98,133,183; sddai-verify.yml:21 |
| Saída CI → humano/auditoria | logs do run; cobertura no stdout | ci.yml:170 (`--cov-report=term-missing`) |
| **Regra de fronteira (norma desta spec)** | **A camada CI lê o repositório; a camada CI nunca muta o repositório** | derivação do Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 — "nunca por estado implícito compartilhado") + Art. 4.10 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:132 — o ledger só é modificado "por script ou MCP validado") |

**Violação conhecida da regra de fronteira (fato, não silenciada — P-05):** o job `final-status` faz append em `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` (ci.yml:185-189, appends em :187-189) — escrita perdida no runner efêmero, nunca pushed. A remediação **já está normatizada na spec-011** (D-06, spec-011:96; AC-06, spec-011:138 — substituição por `GITHUB_STEP_SUMMARY` + run URL). Esta spec **adota** a regra de fronteira e registra o cross-ref, sem re-normar o delta (duplicação factual é violação de SSOT — Art. 6.7, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168).

**Gates como contratos de fronteira (intransferíveis):**

| Gate | Função | Fundamento | Fato (linha real) |
|---|---|---|---|
| `kill-switch-check` — **primeiro job, intransferível** | veta o pipeline se `kill_switch.trigger` existir | Art. 4.6 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124); KILL_SWITCH herdado por todo agente (agent-sdd-specialist.md:39-46) | ci.yml:17 (1º job; `exit 1` em :25-31); sddai-verify.yml:23-28 |
| Cobertura pytest ≥80% **fail-closed** | qualidade fechada | P-06 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94) | ci.yml:170 (`pytest tests/ -q ... --cov=src --cov-fail-under=80`) |
| Scanner de credenciais | zero credencial real versionada | P-07 e Art. 7.2 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96,176) | ci.yml:50-59 (`grep` de padrões de credencial, `exit 1` em :57) |
| Validações SDD/DAG/health | contratos do roster e do DAG | Art. 4.3/4.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:118,122) | ci.yml:80-81 (`validate_nexus_yaml.py`, `rejeitados == 0`), :85 (`dag_validator.py --strict`), :102 (`agent_health_check.py --strict`) |
| SDDAI verify | pipeline SDDAI strict | circuito SDDAI (SSOT: spec-003) | sddai-verify.yml:43 (`sddai_verify_pipeline.py --strict`) |

Regra de ordem: nenhum gate é removível, pulável (label/`continue-on-error`/re-run seletivo) nem reordenável para baixo do `kill-switch-check` (consistente com spec-011 §3.5, spec-011:112-117; R-03, spec-011:82) — "Automation serves gates, never bypasses them" (agent-devops.md:6).

### 3.3 Zero secrets na camada CI

Incorporação da parcela TA-0048 (HF-0604:42 — "zero secrets"):

1. **Nenhuma credencial real versionada** (Art. 7.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:176; P-07, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96) — a própria camada opera o scanner que falha o pipeline em caso de detecção (ci.yml:50-59).
2. **Única credencial do CI:** PostgreSQL efêmero do `test-suite` com valor **dummy** (ci.yml:120 `dummy-ci-efemero`, :130), imagem **digest-pinned** (ci.yml:117 — Art. 10.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215).
3. **Menor privilégio** (Art. 7.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:174): a chave `permissions:` está **AUSENTE** do ci.yml (grep sem matches, 2026-11-03) — correção normatizada como **D-03** na spec-011 (spec-011:93), com SHA-pin de actions como **D-04** (spec-011:94; hoje `checkout@v4` ci.yml:23 etc., `setup-python@v5` ci.yml:136). Cross-ref — a correção é execução da spec-011, não desta spec.
4. **Sem self-hosted runners com secrets** (disciplina Free Tier, §3.4; parcela HF-0604:42).

### 3.4 Regime Free Tier sob Bypass REGISTRADO (P-01)

**Base:** P-01 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84) — "toda dependência é FOSS e de custo recorrente zero. Dependência proprietária exige Bypass Protocol com 3 pilares... **Ficam reconhecidos como Bypass registrados, sujeitos a auditoria: GitHub Actions Free Tier para CI/CD** e provedores cloud de inferência em free tier da whitelist, exclusivamente para dados não sensíveis, nos termos das ADRs 001, 006, 010 e 011."

**Os 3 pilares do Bypass** (diretiva do orquestrador, agent-nexus-prime-ultimate.md:59-63): (1) **Force majeure** — "verifiable, time-bounded, evidenceful" (:60); (2) **FOSS exit strategy** — "named alt, migration steps, sdoc-arch-0006-uc-v1cess criteria" (:61); (3) **Human CCB ratification** — constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 5.1 (:62; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:138). "Missing ANY pillar → immediate refusal" (agent-nexus-prime-ultimate.md:63); anti-meta-bypass: o próprio Bypass não pode ser bypassado (agent-nexus-prime-ultimate.md:65). Precedente no contrato do especialista SDD: "[BYPASS_PROTOCOL] - refuse default; 3 pillars (force majeure, FOSS exit, human CCB) or nothing" (agent-sdd-specialist.md:48).

**Registro existente (mantido, não recriado):** spec-005:211 — "GitHub Actions Free Tier é Bypass registrado (P-01, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84) — não veta, mas exige registro." Esta spec **ratifica o registro no âmbito da camada CI**: toda a camada (§3.1) opera sob este Bypass registrado e sujeito a auditoria (P-01).

**Rota de fuga FOSS (pilar 2, verificável):** todos os gates são scripts FOSS do próprio repositório, executáveis localmente — `scripts/security_scan.py` (ci.yml:47), `scripts/validate_nexus_yaml.py` (:80), `scripts/dag_validator.py` (:85), `scripts/agent_health_check.py` (:102), `pytest` (:170), `scripts/sddai_verify_pipeline.py` (sddai-verify.yml:43) — em hardware local P-02 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86). A substituição do runner GitHub-hosted por execução local **não altera os contratos de fronteira** da §3.2 (as interfaces — triggers, leitura por checkout, gates — são independentes do runner).

**Disciplina Free Tier** (incorporada da parcela TA-0048, HF-0604:42, "FREE TIER P-01"): triggers mínimos (ci.yml:3-7), `cancel-in-progress` (ci.yml:9-11), **sem matriz** de versões/OS, **sem self-hosted com secrets**, **auditoria mensal de minutes**. Norma completa: spec-011 §3.7 (spec-011:125) — cross-ref, sem duplicação (executor da auditoria mensal: **UNKNOWN - verify**, §9e).

---

## 4. Domínio — Runtime de agentes SDD (L1/L3, Art. 6.5)

### 4.1 Definição e base constitdoc-arch-0006-uc-v1ional

O Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213) lista o "runtime de agentes SDD" como camada de execução; o Art. 6.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:158-164) define sua separação ortogonal:

- **L1 — Infraestrutura** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:160): "motor de inferência, hardware, systemd, modelos GGUF, configuração OpenCode base e imagens base. Muda raramente. **Agentes não modificam L1 diretamente; violação é blocker.**"
- **L3 — Metodologia** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:162): "especificações, handoffs, ledger, ADRs, planos, lições aprendidas e artefatos de governança. Muda por tarefa."
- Regra de ortogonalidade (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:164): "Mudanças em uma camada não exigem mudanças nas demais. Violação dessa separação é defeito operacional e pode acionar aborto controlado."

**Definição (norma desta spec):** o runtime de agentes SDD é a camada onde o ciclo "**especifica → implementa → valida → registra**" (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150) executa — especificação, validação e registro vivem em **L3** (specs, handoffs, ledger, ADRs); a implementação executa sobre **L1** (inferência local: `Qwen3-30B-A3B Q4_K_M` via `llama.cpp`, hardware 8700G, sem CUDA/cloud — P-02, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86; motor de referência da forja: agent-sdd-specialist.md:14). O Art. 10.1 é atendido por "ambiente isolado equivalente": camadas L1/L3 separadas por regime de mudança e por fronteiras declaradas (§4.2), não por container — **UNKNOWN - verify** se o orquestrador exigir containerização própria (§9c).

Estado real verificado (2026-11-03): pipeline do ciclo = `.ai/workflows/sdd-cycle.sh` (agent-sdd-specialist.md:35); personas = `.ai/personas/` com `active.md` como symlink trocado pelo ciclo (agent-sdd-specialist.md:33; fato: `active.md → coder.md`, `ls -la`); autoridade de handoffs = `scripts/script-handoff-0001-parse-handoff-v1.0.py` (agent-sdd-specialist.md:35; Art. 6.1); artefatos L3 = `.ai/specs/`, `.ai/handoffs/`, `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` (Art. 4.10, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:132; Art. 6.7, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168).

### 4.2 Fronteiras declaradas do runtime (Art. 10.1 aplicado)

| # | De | Para | Interface declarada | Base |
|---|---|---|---|---|
| 1 | Orquestrador (L0) | especialistas | dispatch com AGENT_TOPOLOGY, half-duplex, sem delegação circular | Art. 4.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:122); `nexus_dispatcher.py` |
| 2 | L3 (handoffs) | agentes | handoff parseável por `scripts/script-handoff-0001-parse-handoff-v1.0.py` — a única autoridade de handoff | Art. 6.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150); contrato agent-sdd-specialist.md:74 |
| 3 | Agentes | ledger (estado L3) | **somente script ou MCP validado** | Art. 4.10 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:132); `nexus-ledger` (ADR-011:65) |
| 4 | Agentes | `.ai/specs/` | leitura/escrita sob custódia declarada (camada 7 da hierarquia — constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:49) | Art. 2.1 |
| 5 | Runtime | motor de inferência (L1) | llama.cpp local, sem cloud para dados sensíveis | P-02/P-03 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86,88) |

Regra: **nenhuma comunicação por estado implícito** — o estado do ciclo vive nos artefatos L3 (memória persistente, §4.3); conhecimento não registrado é dívida (Art. 8.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:188 — "conhecimento tribal morto no cérebro é dívida colonial"). Violação de camada L1/L2/L3 é aborto operacional definido (Art. 4.6, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124; Art. 6.5, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:164).

### 4.3 Memória persistente como parte do runtime (cross-ref spec-003)

Art. 6.7 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168): "o circuito SDD opera com memória persistida em `ledger.yaml`, `handoffs/`, `specs/`, ADRs, lições aprendidas e `transversais.md`. Informação já processada e registrada não deve ser reprocessada sem necessidade; duplicação factual é violação de SSOT." A memória persistente é **componente do runtime** (estado do ciclo), e o SSOT do seu desenho é a **spec-003** (`spec-003-sdd-conf-memory.spec.md`, v3.1.0 — frontmatter spec-003:3-4; "Segunda Brain · Memória Persistente · MCPs · Prompt Ubíquo", spec-003:14, com guarda de integridade e rollback, spec-003:16-17). Componentes reais verificados (2026-11-03): pacotes SDDAI em `.ai/sddai/` (`cobeco_sddai_loader|memory|engineer|trainer|cli`). **Esta spec não redefine o desenho da memória — cross-ref apenas** (ver §5).

### 4.4 MCPs como interfaces declaradas do runtime (Art. 4.9) — estado real

Art. 4.9 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:130): MCPs "são **interfaces declaradas de contexto, estado e validação**. Devem ser versionados, auditáveis, determinísticos e subordinados ao roster. MCPs não criam agentes, não promovem delegação circular, não compartilham estado implícito entre camadas e **não possuem autoridade normativa autônoma**."

Estado real verificado (2026-11-03): os 4 MCPs canônicos existem como scripts — `scripts/mcp_nexus_ledger.py`, `scripts/mcp_nexus_dispatch.py`, `scripts/mcp_nexus_validate.py`, `scripts/mcp_nexus_kb.py` — com atribuições registradas em ADR-011:65-68 (ledger: leitura/escrita validada do `ledger.yaml`; dispatch: roteamento com AGENT_TOPOLOGY; validate: schemas de agentes/handoffs/specs; kb: consulta OKB/Glossário). O `nexus-dispatch` gerencia o roteamento com o mecanismo do symlink `active.md` (ADR-006:57).

**Papel nesta spec:** os MCPs integram o conjunto de interfaces declaradas do runtime (tabela §4.2, linha 3) — nunca fonte de norma (Art. 4.9). A atribuição formal dos MCPs a uma camada específica (L1 × L3) não é feita pela Constituição (que os define como interfaces, não como camada) — **UNKNOWN - verify** (§9b).

### 4.5 Limite com L2 (delimitação)

**L2 — Personas** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:161): "comportamento do modelo via contexto, residindo em `.ai/personas/`. Muda por agente ou papel." O **conteúdo** das personas não é objeto desta spec (§2, linha 4): o B.10 e a confirmação do orquestrador delimitam o alcance a L1/L3. O mecanismo de troca (symlink `active.md`) é citado apenas como fronteira observada (§4.1).

---

## 5. Fronteiras entre camadas e specs vizinhas (cross-refs)

| Camada do Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213) | SSOT normativo | Regime de leitura |
|---|---|---|
| aplicação — Dados (`db`) | spec-005 §3.1 (spec-005:60) | cross-ref apenas — nada redefinido aqui |
| aplicação — Back | spec-005 §3.1 (spec-005:61) + spec-004 §3 (contrato `/v1`) | cross-ref apenas |
| aplicação — Front | spec-005 §3.1 (spec-005:62) | cross-ref apenas |
| **CI** | **esta spec §3** (definição de camada) + spec-011 (requisitos do pipeline R-01..R-04, deltas D-01..D-06, job `contract-network`) | norma dividida por delimitação §2 |
| **runtime de agentes SDD — L1/L3** | **esta spec §4** (definição de camada) + spec-003 (memória persistente e circuito SDDAI) | idem |

Regra de não-duplicação (Art. 6.7, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168): esta spec declara **camada e fronteiras**; requisitos operacionais do CI permanecem na spec-011; o desenho da memória permanece na spec-003.

---

## 6. Critérios de aceite e testes

Critérios binários desta emissão (spec de definição — verificação por leitura/inspeção, não por implementação):

- [ ] **AC-01** — a camada CI está definida como camada do Art. 10.1 com a regra de fronteira "CI lê o repositório; CI nunca muta o repositório", citando constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 e o estado real dos 2 workflows (§3.1-§3.2). *Verificação:* leitura da §3 contra ci.yml/sddai-verify.yml.
- [ ] **AC-02** — `kill-switch-check` identificado como **primeiro job intransferível** com linha real. *Verificação:* `grep -n "kill-switch-check:" .github/workflows/config-ci-0001-github-actions-v1.0.yml` = 1 match (ci.yml:17), primeiro job da seção `jobs`; homólogo em sddai-verify.yml:25.
- [ ] **AC-03** — gate de cobertura pytest ≥80% fail-closed citado com linha real. *Verificação:* `grep -n "cov-fail-under=80" .github/workflows/config-ci-0001-github-actions-v1.0.yml` = 1 match (ci.yml:170).
- [ ] **AC-04** — regime Free Tier declarado como **Bypass registrado P-01**, com os 3 pilares citados (agent-nexus-prime-ultimate.md:59-63) e o registro existente da spec-005:211 ratificado, sem recriação. *Verificação:* leitura da §3.4.
- [ ] **AC-05** — runtime L1/L3 definido conforme Art. 6.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:158-164) com o ciclo especifica→implementa→valida→registra (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150), limite com L2 declarado (§4.5) e memória persistente em cross-ref com spec-003 (§4.3). *Verificação:* leitura da §4.
- [ ] **AC-06** — zero secrets: nenhuma credencial real nos workflows (única credencial dummy efêmera, ci.yml:120,130); lacuna `permissions:` e SHA-pin referenciadas como deltas da spec-011 (§3.3). *Verificação:* `grep -rEn "sk_live|AKIA[0-9A-Z]{16}" .github/workflows/ | grep -v "ci.yml:53"` = zero matches (o único match existente é o padrão regex do próprio scanner, ci.yml:53 — exclusão análoga à do scanner, ci.yml:55).
- [ ] **AC-07** — tabela de fronteiras §5 mapeia as 5 camadas do Art. 10.1 aos seus SSOTs sem redefinir conteúdo de spec-005/spec-011/spec-003/spec-004. *Verificação:* leitura da §5.
- [ ] **AC-08** — todos os UNKNOWNs registrados em §9 com caminho de verificação (a..e). *Verificação:* contagem = 5 itens.
- [ ] **AC-09** — esta emissão não altera nenhum arquivo além de `.ai/specs/spec-runtime-0001-runtime-agentes-ci-layers-v1.0.md` (workflows, specs vizinhas e constituição intocados). *Verificação:* `git status`/`git diff`.

---

## 7. Rastreabilidade (dupla)

| Fonte | Linha | O que ancora nesta spec |
|---|---|---|
| **Art. 10.1** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :213 | Enumeração das camadas (runtime de agentes SDD, aplicação, dados, CI); "ambiente isolado equivalente"; comunicação só por interface declarada → §§3.1, 4.1, 4.2, 5 |
| **Art. 6.5** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :158-164 | Separação ortogonal L1/L2/L3 → §4 |
| **P-01** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :84 | GitHub Actions Free Tier como Bypass registrado, sujeito a auditoria → §3.4 |
| Art. 6.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :150 | Ciclo especifica→implementa→valida→registra; handoffs parseados → §4.1, §4.2 |
| Art. 4.6 / Art. 4.9 / Art. 4.10 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :124, :130, :132 | Kill switch herdado → §3.2; MCPs como interfaces declaradas → §4.4; ledger só por script/MCP validado → §3.2 |
| P-06 / P-07 / P-11 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :94, :96, :104 | Gates de qualidade → §3.2; segurança/zero credenciais → §3.3; YAGNI → §8 |
| Art. 2.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md) | :49 | Specs como camada 7 da hierarquia → §4.2 |
| **B.10** (LISTA-SPECS-PENDENTES) | :42 | Origem da task; condição de confirmação do orquestrador |
| CONFIRMAÇÃO DO ORQUESTRADOR (HF-0615) | :17 | Escopo CONFIRMADO; fonte spec-005:81/352; mandato de incorporar a parcela TA-0048 |
| Parcela TA-0048 (HF-0604) | :42 | "workflows como camada Art. 10.1, Bypass P-01, boundaries: gates como contratos de fronteira, zero secrets" + disciplina Free Tier + UNKNOWNs |
| spec-005 | :81, :211, :352 | Pendência original (UNKNOWN - verify); registro do Bypass; follow-up fechado por esta emissão |
| spec-011 | :80-83, :96, :112-117, :125, :168 | Delimitação pipeline×camada; D-06 (regra de fronteira); gates intransferíveis; disciplina Free Tier; reserva expressa do B.10 para esta spec |
| spec-003 | :3-4, :14, :16-17 | SSOT da memória persistente do runtime (cross-ref, §4.3) |
| agent-nexus-prime-ultimate.md | :59-65 | BYPASS_PROTOCOL — os 3 pilares e o anti-meta-bypass |
| agent-sdd-specialist.md | :14, :33-35, :39-46, :48, :74 | Hardware L1; personas/sdd-cycle.sh/handoff_parser; KILL_SWITCH; BYPASS; contrato de handoff |
| agent-devops.md | :6 | "Automation serves gates, never bypasses them" → §3.2 |
| ADR-011 / ADR-006 | :65-68 / :57 | MCPs nexus-* e roteamento por symlink — §4.4 |

---

## 8. Fora de escopo (YAGNI — P-11, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:104)

- **Implementação de workflows** (`.github/workflows/*`) — custódia `agent-devops`; os deltas do CI já normatizados na spec-011 (D-01..D-06, job `contract-network`, spec-011:89-110) são **execução da spec-011**, não desta spec (Art. 6.1; precedente de não-implementação: spec-005:348).
- **Requisitos do pipeline** (lint+testes ≤5 min, merge-blocking, R-01..R-04) — SSOT spec-011 (§2, linha 3).
- **Camadas Dados/Back/Front e aderentes** (`migrate`, `proxy`) — SSOT spec-005 (cross-ref apenas, §5; §2, linha 2).
- **Conteúdo de L2** (`.ai/personas/`) — outra camada do Art. 6.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:161; §4.5).
- **Redesenho da memória persistente, MCPs e prompt ubíquo** — SSOT spec-003 (§4.3, §4.4).
- CD/deploy contínuo, self-hosted runners, matriz de versões/OS, cache remoto — vedados pela disciplina Free Tier (spec-011:125; §3.4).
- Configuração de branch protection (GitHub Admin) — fora do filesystem (§9a).
- Emenda constitdoc-arch-0006-uc-v1ional — o Art. 10.1 permanece como está; nenhuma emenda é proposta nesta emissão (Art. 9.1).

## 9. Registro UNKNOWN - verify (P-08)

- **(a) required status checks / branch protection** — configuração do GitHub, não versionada no filesystem (parcela TA-0048, HF-0604:42 "(a)"; precedente spec-011:177). Caminho de verificação: UI Admin → Settings → Branches.
- **(b) Atribuição formal dos MCPs a L1 ou L3** — Art. 4.9 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:130) os define como interfaces, não como camada; os 4 scripts existem (scripts/, ADR-011:65-68), mas nenhuma fonte atribui camada. Caminho: decisão de arquiteto/CCB.
- **(c) Containerização própria do runtime L1/L3** — hoje o runtime opera como "ambiente isolado equivalente" (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213) local, P-02 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86); pacotes SDDAI são Python em `.ai/sddai/` (inspeção, 2026-11-03). Se o orquestrador exigir container própria, caminho: ADR específica (Art. 9.3.ii, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:203).
- **(d) Spec futura dedicada ao detalhamento operacional do L1** — a recomendação de desagregação da parcela TA-0048 (HF-0604:42, item "(d)") foi superada nesta emissão pela confirmação do orquestrador (HF-0615:17, §2); a abertura de spec própria permanece decisão do orquestrador (backlog).
- **(e) Executor e registro da auditoria mensal de minutes Free Tier** — disciplina registrada (spec-011:125; HF-0604:42) sem executor designado no filesystem.

## Conformidade desta emissão

- Arquivo único editado: `.ai/specs/spec-runtime-0001-runtime-agentes-ci-layers-v1.0.md` (custódia `.ai/specs/`, Art. 6.1). Nenhum outro arquivo alterado; nada commitado.
- Kill switch herdado (Art. 4.6, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124); zero PII (P-04); 100% local nas derivações (P-02); slugs/IDs EN + narrativa PT-BR (P-10); alegações com `arquivo:linha` ou **UNKNOWN - verify** (P-08); nenhuma capacidade especulativa (P-11); nenhuma instrução de bypass de gate (kill switch #4, agent-sdd-specialist.md:43).

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0059, HF-0615): emissão inicial (item B.10 da LISTA). Confirmação do orquestrador citada (HF-0615:17); delimitações com spec-005 e spec-011 e superação da recomendação de desagregação da parcela TA-0048 registradas na tabela de conflitos (§2); camada CI definida como camada do Art. 10.1 com workflows como contratos de fronteira, regra "CI lê, nunca muta", gates intransferíveis (kill-switch-check primeiro, cobertura ≥80 fail-closed) e zero secrets (§3); regime Free Tier ratificado como Bypass registrado P-01 com os 3 pilares e rota de fuga FOSS (§3.4); runtime de agentes L1/L3 definido conforme Art. 6.5 com fronteiras declaradas, memória persistente em cross-ref spec-003 e MCPs do Art. 4.9 como interfaces (§4); mapa de camadas×SSOTs (§5); 9 AC binários (§6); rastreabilidade dupla (§7); escopo negativo (§8); 5 UNKNOWNs registrados (§9).
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo B): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `handoff` em `origin`; `version` 0.1.0 → 0.2.0). Ratificação CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012). Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio de §§1–9 reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem, task, kill_switch, trace, lgpd-class | frontmatter (`spec_id: spec-014`, `version: 0.2.0`, `status: ratificada`) + linha `Status:` | aplicada |
| (b) Contexto/origem | §1 (B.10; UNKNOWN - verify de spec-005:81; follow-up :352; confirmação do orquestrador HF-0615:17; parcela TA-0048) | aplicada |
| (c) Resolução de conflitos | §2 (especiação única × desagregação; delimitações spec-005/spec-011; alcance L1/L3 × L2) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §§3–5 (camada CI; runtime L1/L3; fronteiras e cross-refs) | aplicada |
| (e) Critérios de aceite/testes | §6 (AC-01..AC-09, binários com método de verificação) | aplicada |
| (f) Rastreabilidade (REQ/Art./US/arquivo:linha) | §7 (Art. 10.1, Art. 6.5, P-01, B.10 + fontes) | aplicada |
| (g) Fora de escopo (YAGNI) | §8 (+ UNKNOWNs em §9) | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
