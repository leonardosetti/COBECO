---
id: spec-trace-0001-rastreabilidade-prompts-sdd-v1.0
type: spec-trace
title: SPEC TRACE — Rastreabilidade Prompts Sdd
version: v1.0
status: ratificado
canonical: false
canonical_slug: rastreabilidade-prompts-sdd
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
spec_id: spec-012
specname: rastreabilidade-prompts-sdd-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: HF-0613 (TA-0057) | sender: agent-nexus-prime-ultimate | handoff: HF-0613
task: TA-0057 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (rastreabilidade prompts SDD)
lgpd-class: filenames LGPD-safe (catálogo contém apenas id/tema/task/target/status; sem PII, sem conteúdo de handoff replicado)
trace:
  - .ai/handoffs/HF-0613-spec-012-rastreabilidade-prompts-sdd-v1.md (envelope da tarefa)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:40 (B.8), :60 (D.3), :61 (D.4)
  - .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:74 (REQ-13), :73 (REQ-12 adjacente)
  - .ai/handoffs/INDEX.md:1-10 (catálogo vivo — auditado nesta emissão, NÃO editado)
  - .ai/handoffs/HF-0500-backend-mvp.md:8, :22-37, :41-43 (precedente REQ-13)
  - .ai/agents/config-ledger-0001-ledger-v1.0.yaml:1-312 (SSOT de execução — 39 entradas, 2026-11-03)
  - scripts/script-handoff-0001-parse-handoff-v1.0.py:44 (VALID_STATUSES), :45 (ID_RE), :104, :106 (executado nesta emissão)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:34, :42, :74, :129, :146, :151
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:64 (Art. 2.3), :88 (P-03), :98 (P-08), :102 (P-10), :124 (Art. 4.6), :132 (Art. 4.10), :138 (Art. 5.1), :150 (Art. 6.1), :168 (Art. 6.7), :186 (Art. 8.1)
  - .ai/specs/doc-manifest-0001-manifest-v1.0.md:58 (lacuna = `UNKNOWN - verify`)
  - .ai/handoffs/task-TA-0057.json (envelope: handoff HF-0613)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012)
---

# SPEC spec-012 — rastreabilidade-prompts-sdd-v1 — Rastreabilidade de prompts SDD (100% dos handoffs catalogados em `.ai/handoffs/` — REQ-13, fase N9.3)

Status: SPEC EMITIDA — PENDENTE DE REVISÃO E DE IMPLEMENTAÇÃO (onda seguinte, Art. 6.1 SDD) | Tarefa: TA-0057 (handoff `.ai/handoffs/HF-0613-spec-012-rastreabilidade-prompts-sdd-v1.md`) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única das decisões de catálogo e auditoria de rastreabilidade dos prompts SDD (handoffs) do COBECO. Em conflito, vale a hierarquia do Art. 2 da Constituição (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:41-50; resolução de cima para baixo, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).

Convenções: citação `arquivo:linha`. Identificadores/status/caminhos em EN; narrativa em PT-BR (P-10, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:102). Toda alegação sem fonte está marcada **UNKNOWN - verify** (P-08, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98; MANIFEST.md:58). Esta SPEC **DEFINE** o critério de catálogo, o formato do índice e o método de auditoria; ela **NÃO edita** `.ai/handoffs/` (nem INDEX.md, nem qualquer HF) — mandato HF-0613:17 e regra da tarefa (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150).

---

## 1. Contexto e origem

Nasce da task TA-0057 (HF-0613), item **B.8** da LISTA (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:40): "Rastreabilidade de prompts SDD — 100% catalogados em `.ai/handoffs/`", com condição "pendente de criação" e entregável "spec de catálogo/rastreio dos prompts com critério de cobertura total". Encaixe de onda: a onda 6 "Corrente da Qualidade" lista B.8 entre as specs que faltam (D.3, LISTA:60; plano-proddoc-arch-0006-uc-v1ao-agentes.md:145-152) e a onda 7 "Commons e Meta" prevê "B.8/B.9 conforme escopo da onda" (D.4, LISTA:61). Fase EAP de destino: **N9.3**.

Requisito de origem: **REQ-13** — "Rastreabilidade de prompts SDD | 100% catalogados em .ai/handoffs/ (req_1.0.md:38) | N9.3 | **Should**" (spec-002-requisitos-review-round-1.spec.md:74). Precedente de execução da REQ-13: HF-0500, "Registro de execução do backend MVP (REQ-13)" (HF-0500:8), que registrou T1–T14 com colunas "Agente de referência" e "Modelo" (HF-0500:22-37) — o protótipo do dado de co-autoria que esta spec tornará auditável por catálogo.

**Propósito de auditoria de co-autoria:** o Art. 5.1 estabelece que "o Humano (Gerente de Projeto) é o decisor único via CCB; agentes são conselho, nunca veto ao Humano" (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:138). Para que o CCB exerça essa soberania sobre trabalho co-autorado por agentes, cada prompt de despacho (handoff) precisa ser localizável, contável e correlacionável à sua execução — hoje sem critério formal de cobertura (REQ-13 sem spec dedicada até esta emissão; B.8, LISTA:40).

---

## 2. Resolução de conflitos

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| **REQ-13** — "100% catalogados" (spec-002:74) × estado real de 1/34 no índice e 12/34 parseáveis (§3.5) | Vence REQ-13 como critério **normativo**; o estado atual é declarado **NÃO ATENDIDO** (§3.5, AC-04). A cobertura 100% é meta binária da fase N9.3, atingível por saneamento posterior — nunca rebaixada a "melhor esforço" (sem afrouxamento de critério; P-06, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94) | spec-002:74; auditoria direta do filesystem desta emissão (§3.4-§3.5) | Estado real medido em 2026-11-03 (INDEX.md:1-10; saída do parser, §3.5) — permanece como registro factual, não como padrão aceitável |
| **Contrato canônico do parser** (chave `agent`, enum de 6 status, seção "Critérios de Aceite" — handoff_parser.py:44,104-106; agent-sdd-specialist.md:74) × prática nova dos HF-06xx (chave `target`, status `emitted`, sem AC) | Vence o contrato do parser — "scripts/script-handoff-0001-parse-handoff-v1.0.py - the ONLY handoff authority" (agent-sdd-specialist.md:34; Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150). Os 21 arquivos HF-06xx são **drift a sanear pelo emissor/orquestrador** (D-02, §7); esta spec não os edita | agent-sdd-specialist.md:34; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150 | Frontmatter de HF-0613:2-12 (`target:`, `status: emitted`) e dos demais 20 HF-06xx — prática a convergir, não norma |
| **SSOT de execução** (Art. 6.7: "duplicação factual é violação de SSOT", constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168) × tentação de replicar dados de execução (agentes/modelos) no índice | O catálogo (INDEX.md) contém **apenas ponteiros** (id, tema, task, target, status); dados de execução — incluindo modelo usado — permanecem SSOT no HF e no ledger (precedente HF-0500:22-37,41-43) | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168 | Qualquer proposta de coluna "modelo" no INDEX.md (inexistente hoje — INDEX.md:3-10) |
| **REQ-12** (min. 3 ADRs, N9.1, spec-002:73) — adjacência da fase N9 | Avaliada: domínio alheio (ADRs são decisões, não prompts de despacho). Sem delta para este domínio | spec-002:73 | n/a |
| **INDEX.md "v1.0"** autodeclarado (INDEX.md:1) × conteúdo desatualizado (7 entradas fantasma, 33 arquivos ausentes — §3.5) | Registrado como **drift D-01 a sanear em tarefa própria**; NÃO corrigido nesta emissão (mandato HF-0613:17; regra da tarefa). O saneamento futuro segue o formato do §3.2 | HF-0613:17; MANIFEST.md:58 | INDEX.md:3-10 (estado pré-saneamento, preservado como registro histórico) |

---

## 3. Domínio — critério de catálogo, formato, verificação e ciclo de vida

### 3.1 Definição de "prompt catalogado" (critério de cobertura 100%)

Um prompt SDD (handoff de despacho) está **catalogado** quando satisfaz, simultaneamente, os 4 critérios:

| # | Critério | Teste objetivo | Fonte do critério |
|---|---|---|---|
| C-01 | **Existência formal:** arquivo `HF-*.md` em `.ai/handoffs/` cujo id case `^HF-\d{3,4}$` | `grep -oE 'HF-[0-9]{3,4}' <arquivo> \| head -1` no frontmatter | handoff_parser.py:45 (`ID_RE`); agent-sdd-specialist.md:129 (`HF-\d{3,4}`) |
| C-02 | **Parseabilidade:** `python3 scripts/script-handoff-0001-parse-handoff-v1.0.py <arquivo>` executa com `ok: true` (exit 0 por arquivo) | saída JSON do parser, campo `ok` | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150 (Art. 6.1); agent-sdd-specialist.md:34 (única autoridade); handoff_parser.py:44,104-106 |
| C-03 | **Entrada no índice:** linha no `.ai/handoffs/INDEX.md` com os 4 campos mínimos: `id`, `tema`, `task: TA-NNNN`, `target: <agent do roster>` | `grep '^ - HF-NNNN:' INDEX.md` + inspeção dos campos | mandato HF-0613:17 ("formato do catálogo (INDEX.md existente) — entradas mínimas") |
| C-04 | **Correlação com despacho:** a task do envelope (`task-ta-*.json` com campo `handoff: HF-NNNN`) existe e a execução está registrada no ledger (`.ai/agents/config-ledger-0001-ledger-v1.0.yaml`, Art. 4.10) | `grep '"handoff"' task-ta-*.json` × `grep 'task_id' ledger.yaml` | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:132 (Art. 4.10); task-TA-0057.json:6 (exemplo do campo `handoff`) |

**Cobertura 100% (REQ-13)** é a proposição binária: para todo arquivo que satisfaz C-01, valem C-02 ∧ C-03 ∧ C-04; e todo despacho registrado (ledger/envelope) aponta para um arquivo C-01 existente. A verificação é **fail-closed**: qualquer contraexemplo derruba a cobertura para "<100%" (sem "cobertura parcial aprovada"; espírito P-07, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96).

**O que NÃO é prompt catalogado:** tarefa despachada apenas como envelope `task-ta-*.json` sem arquivo HF correspondente é **despacho sem prompt catalogado** — quebra da cadeia de custódia para auditoria de co-autoria (evidência real: 10 ids referenciados por envelopes sem arquivo em disco, §3.5).

### 3.2 Formato do catálogo (INDEX.md)

- **Entrada mínima (normativa a partir desta spec):**

  ```markdown
  - HF-NNNN: <tema curto em PT-BR> (task: TA-NNNN | target: <agent-roster> | status: <enum-do-parser>)
  ```

- Campos: `id` (C-01), `tema` (resumo de uma linha do `# Handoff:` título), `task` (TA do envelope), `target` (agente do roster `.ai/agents/config-registry-0001-registry-v1.0.yaml`), `status` (apenas valores do enum `VALID_STATUSES` — handoff_parser.py:44).
- **INDEX.md é índice de ponteiros:** não replica Contexto/Tarefa/critérios do HF (Art. 6.7, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168). O conteúdo de um prompt lê-se no arquivo HF, nunca no índice.
- Ordenação por id crescente. Entradas históricas são **append-only**; correção de entrada errada = nova linha de correção datada, nunca reescrita silenciosa (forense: "spec history is provable via git; no silent rewrites" — agent-sdd-specialist.md:59).
- Custódia: agent-sdd-specialist (`.ai/handoffs/` é custódia de despachos do próprio SDD — agent-sdd-specialist.md:32). INDEX.md **não** é imutável: não consta do mapa de imutáveis (MANIFEST.md:134-152) nem da lista de pinned (MANIFEST.md:167-173).

### 3.3 Regras de nomenclatura HF-NNNN

- Id do handoff casa `^HF-\d{3,4}$` (handoff_parser.py:45; agent-sdd-specialist.md:129) — 3 ou 4 dígitos; numeral sequencial cronológico de emissão.
- Nome do arquivo: `HF-<id>-<slug-kebab>.md`; slug em EN kebab-case (P-10, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:102) — padrão observado em 33/34 arquivos existentes.
- Vedado reutilizar id já emitido; **gap de numeração não é, por si, defeito de nomenclatura** — arquivos podem nunca ter existido; a causa dos gaps é lacuna declarada (§7a).
- Id não numérico (ex.: `HF-RELATORIO-ANALISE-CONSTITUICAO.md`) **viola C-01** e não parseia (evidência §3.5) — drift D-03 (§7).

### 3.4 Verificação de cobertura por comando determinístico (método de auditoria)

A auditoria REQ-13 é executável por comandos puros, sem julgamento humano intermediário — os mesmos aplicados nesta emissão (§3.5):

| Comando | O que mede | Saída esperada em PASS |
|---|---|---|
| **A — inventário:** `ls .ai/handoffs/HF-*.md \| wc -l` | `N_files` = universo de prompts | valor registrado; baseline desta emissão: **34** |
| **B — parseabilidade:** `python3 scripts/script-handoff-0001-parse-handoff-v1.0.py --dir .ai/handoffs` | contadores `total/parsed/rejeitados` | `rejeitados == 0` |
| **C — índice × disco:** `comm -3 <(grep -oE 'HF-[0-9]{3,4}' .ai/handoffs/INDEX.md \| sort -u) <(ls .ai/handoffs/HF-*.md \| grep -oE 'HF-[0-9]{3,4}' \| sort -u)` | órfãos (no índice, sem arquivo) e ausentes (arquivo sem índice) | diff vazio (após considerar os 4 campos de C-03 por entrada) |
| **D — cadeia de despacho:** `comm -3 <(grep -ho 'HF-[0-9]{3,4}' .ai/handoffs/task-*.json \| sort -u) <(ls .ai/handoffs/HF-*.md ... \| sort -u)` | envelopes apontando para HF inexistente | diff vazio |
| **E — correlação ledger:** `grep -c '^  - task_id:' .ai/agents/config-ledger-0001-ledger-v1.0.yaml` × envelopes | execução registrada por despacho (Art. 4.10) | toda task de despacho tem entrada no ledger |

**Critério de PASS da auditoria (binário):** B com `rejeitados==0` ∧ C com diff vazio ∧ D com diff vazio ∧ (amostragem E sem task de despacho órfã). **FAIL em qualquer comando = auditoria reprovada** — nada de aprovação parcial.

**Interpretação kill switch:** alegar "100% catalogado" sem os comandos A–D verdes configura *misleading traceability* — "spec claims done without evidence" (kill switch #3, agent-sdd-specialist.md:42; Art. 4.6, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124). A evidência da alegação são as saídas dos comandos, datadas.

**Periodicidade e responsáveis:** a cada rodada de emissão de specs/handoffs e antes de cada milestone (auditoria contra a Constituição — Art. 8.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:186). Executor primário: agent-sdd-specialist (custódio do ciclo SDD — agent-sdd-specialist.md:22, dever 6 de auditoria semanal); verificação independente: agent-project-auditor (Art. 8.1). Métrica de contrato do agente: `handoff_parse_rate` alvo 100% first pass (agent-sdd-specialist.md:146).

### 3.5 Estado real auditado (evidência desta emissão, 2026-11-03)

Execução direta dos comandos do §3.4 sobre o filesystem (nenhum número abaixo é estimativa):

- **Inventário (Comando A):** `.ai/handoffs/` contém **91 arquivos**: **34 `HF-*.md`** + **56 `task-*.json`** + 1 `INDEX.md`. Composição dos 34 HF: 6× HF-00xx (HF-0029..0034), 5× HF-04xx (HF-0400..0404), 1× HF-0500, 21× HF-06xx (HF-0601..0621), 1× HF-RELATORIO-ANALISE-CONSTITUICAO.md.
- **Parseabilidade (Comando B):** varredura do parser = **total 35** (34 HF + INDEX.md), **parsed 12, rejeitados 23**. Os 12 parseáveis: HF-0029..0034, HF-0400..0404, HF-0500. As 23 rejeições: 21× HF-06xx (erros: `alvo fora do roster: ''` — chave `target` sem `agent`; `status fora do enum: 'emitted'`; "secção 'Critérios de Aceite' ausente"; "nenhum critério de aceite parseado"), 1× HF-RELATORIO e 1× INDEX.md (ambos "handoff sem frontmatter YAML").
- **Índice × disco (Comando C):** INDEX.md tem 10 linhas e 8 entradas `- HF-` (INDEX.md:3-10): **7 órfãos** (HF-001..HF-007 — zero arquivos correspondentes em disco) e **1 real** (HF-0500, INDEX.md:10). Cobertura do índice sobre o disco: **1/34**. Nenhuma entrada traz os 4 campos mínimos de C-03 (a de HF-0500 cita tema, sem task/target) → **C-03 = 0/34**.
- **Cadeia de despacho (Comando D):** 37 envelopes `task-*.json` trazem campo `"handoff"`; **38 ids únicos** referenciados. Desses, **10 ids NÃO têm arquivo em disco**: HF-0022, HF-0036..HF-0044 (envelopes TA-0036..TA-0044 e TA-0022). Reciprocamente, **5 arquivos HF sem envelope que os referencie**: HF-0400..0404. Os 21 HF-06xx estão integralmente correlacionados aos envelopes task-TA-0045..0065 (21/21).
- **Ledger (Comando E):** 39 entradas `task_id` em `.ai/agents/config-ledger-0001-ledger-v1.0.yaml` (TA-0027..TA-0056, com TA-0036..0044 duplicadas em status `accepted`/`dispatched_definitivo`, ledger.yaml:73-144 e :145-216). As tasks TA-0057..TA-0065 desta rodada ainda não têm entrada (em execução nesta data).
- **Veredito REQ-13:** **NÃO ATENDIDO.** Cobertura integral C-01∧C-02∧C-03∧C-04: **0/34**. Parciais: C-01 = 33/34 (falha HF-RELATORIO), C-02 = 12/34, C-03 = 0/34, C-04 = 28/33 ids numéricos com envelope (os 5 HF-04xx sem envelope referenciador). Meta 100% é alvo da fase N9.3 via saneamento dos drifts D-01..D-04 (§7).

### 3.6 Ciclo de vida do prompt (handoff)

- **Estados válidos:** `draft → ready → dispatched → in_progress → done | blocked` (enum `VALID_STATUSES`, handoff_parser.py:44; contrato do agente, agent-sdd-specialist.md:74). Status fora do enum reprova C-02 (handoff_parser.py:106).
- O status `emitted`, usado no frontmatter dos 21 HF-06xx (ex.: HF-0613:10), **não existe no enum** — é o gatilho principal das 23 rejeições do Comando B (§3.5). A convergência (mapear para o enum ou emendar o parser) é decisão de custódia do orquestrador — **UNKNOWN - verify** (§7b); esta spec não altera arquivos alheios.
- **Morte do prompt:** nenhum HF é deletado — memória persistente do circuito SDD (Art. 6.7, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168); handoff encerrado mantém status `done`/`blocked` e permanece catalogado. Remoção só por auditoria forense com registro (padrão da normalização TA-0031, MANIFEST.md:87-109).
- **Cadeia de vida completa ( cadeia de custódia):** envelope `task-ta-*.json` (intenção de despacho) → HF `HF-NNNN-*.md` (prompt catalogado) → parcela de retorno no ledger (execução, Art. 4.10) → artefato produzido (spec/código/auditoria). Um elo ausente torna o elo seguinte não auditável quanto à co-autoria.

### 3.7 Relação com a co-autoria humana (Art. 5.1 / Art. 6)

- **Soberania do CCB sobre a co-autoria:** o catálogo é o mapa de despachos que permite ao Humano (decisor único, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:138) auditar **quem** (agente + modelo) produziu cada artefato e **sob qual prompt**. Precedente: HF-0500 registrou T1–T14 com "Agente de referência" e "Modelo" (HF-0500:22-37), incluindo o uso de modelos cloud Sonnet/Opus/Haiku 5.5 e sua pendência de avaliação pelo CCB (HF-0500:41-43) — exatamente o tipo de fato que a REQ-13 torna rastreável por catálogo.
- **Dados sensíveis (P-03):** handoffs e prompts com contexto proprietário são dados sensíveis do projeto (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:88; Art. 2.3 — prompts de sistema são derivativos subordinados, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:64). O catálogo vive em filesystem local, sem telemetria, e por ser índice de ponteiros (§3.2) não amplifica a superfície de exposição do conteúdo.
- **LGPD (P-04):** entradas do índice contêm apenas id/tema/task/target/status — nenhum dado pessoal; nomes de stakeholder aparecem apenas quando já constam do tema público do HF (ex.: nenhum hoje — INDEX.md:3-10).
- **Honestidade de cobertura (P-08 + kill switch #3):** a contagem "100% catalogados" só pode ser afirmada com as saídas dos Comandos A–D anexadas à auditoria; alegação sem evidência é KNOWLEDGE GAP declarado (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98) e vetor de kill switch (agent-sdd-specialist.md:42).

---

## 4. Critérios de aceite e testes (verificáveis por comando)

- [ ] **AC-01** — Comando A (§3.4) retorna `N_files = 34` sobre `.ai/handoffs/` na data da emissão (baseline registrado em §3.5). *Verificação:* `ls .ai/handoffs/HF-*.md | wc -l`.
- [ ] **AC-02** — Comando B (§3.4) registra `total=35, parsed=12, rejeitados=23` como estado factual de 2026-11-03 (§3.5) — registro de estado, não aprovação. *Verificação:* re-executar `python3 scripts/script-handoff-0001-parse-handoff-v1.0.py --dir .ai/handoffs` e comparar contadores.
- [ ] **AC-03** — Comando C (§3.4) registra 7 órfãos (HF-001..007) e 33 ausentes do índice, com cobertura 1/34 (§3.5). *Verificação:* `comm -3` das duas listas de ids, como no §3.4.
- [ ] **AC-04** — A spec declara binariamente **REQ-13 NÃO ATENDIDO** com cobertura integral C-01..C-04 = 0/34 (§3.5). *Verificação:* leitura do §3.5; nenhum comando contradiz.
- [ ] **AC-05** — Cada critério C-01..C-04 (§3.1) e cada regra de formato (§3.2) possui citação `arquivo:linha` de fonte normativa (P-08). *Verificação:* inspeção das tabelas §3.1-§3.2.
- [ ] **AC-06** — Nenhum arquivo além de `.ai/specs/spec-trace-0001-rastreabilidade-prompts-sdd-v1.0.md` foi criado ou editado nesta emissão (INDEX.md e HF intocados). *Verificação:* `git status --porcelain` e `git diff` — único caminho novo em `.ai/specs/`.
- [ ] **AC-07** — Os 4 drifts D-01..D-04 (§7) estão registrados com caminho de saneamento e responsável, sem correção executada por esta spec. *Verificação:* leitura do §7; `git diff` vazio fora desta spec.
- [ ] **AC-08** — Os contadores do parser (35/12/23) estão ecoados na spec conforme DO 10 ("Echo parser JSON checks in spec review summary" — agent-sdd-specialist.md:93). *Verificação:* §3.5 e §3.4.
- [ ] **AC-09** — O comando D confirma 10 ids referenciados por envelopes sem arquivo (HF-0022, HF-0036..HF-0044) e 5 arquivos sem envelope (HF-0400..0404) (§3.5). *Verificação:* `comm -23` / `comm -13` conforme §3.4.
- [ ] **AC-10** — A meta REQ-13 (cobertura 100%) permanece inalterada como alvo binário da fase N9.3 — nenhum texto desta spec afrouxa REQ-13. *Verificação:* spec-002:74 × §2 (primeira linha da tabela) × §3.1.

---

## 5. Rastreabilidade (dupla)

| Fonte | Linha | O que ancora nesta spec |
|---|---|---|
| **REQ-13** (spec-002-requisitos-review-round-1.spec.md) | :74 | "Rastreabilidade de prompts SDD — 100% catalogados em .ai/handoffs/ — N9.3 — Should" → §1, §3.1, AC-10 |
| REQ-12 (spec-002) | :73 | Adjacente da fase N9 (ADRs) — avaliada e sem conflito (§2) |
| **B.8** (LISTA-SPECS-PENDENTES-2026-11-02.md) | :40 | Origem da pendência e entregável ("spec de catálogo/rastreio com critério de cobertura total") |
| D.3 / D.4 (LISTA) | :60, :61 | Encaixe nas ondas 6 (Corrente da Qualidade) e 7 (Commons e Meta) |
| **HF-0613** (envelope) | :17, :19-25, :27-29 | Mandato (critério, formato, verificação, lacunas UNKNOWN); fontes obrigatórias; contrato de resposta |
| **HF-0500** (precedente REQ-13) | :8, :22-37, :41-43 | Registro de execução com Agente/Modelo por tarefa (T1–T14); pendência CCB sobre modelos cloud → dado de co-autoria que o catálogo rastreia |
| **INDEX.md** (catálogo vivo) | :1-10 | Estado auditado (8 entradas, 7 órfãs, 1 real); formato-alvo do §3.2; drift D-01 |
| handoff_parser.py | :44, :45, :104, :106 | Enum de status, regex do id, checagens de roster/status → critérios C-01/C-02 e ciclo de vida §3.6 |
| agent-sdd-specialist.md | :34, :42, :59, :74, :129, :146, :151 | Parser única autoridade; kill switch #3 (misleading traceability); no silent rewrites; contrato de handoff; `HF-\d{3,4}`; métricas parse rate |
| constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md | :64, :88, :98, :102, :124, :132, :138, :150, :168, :186 | Art. 2.3 (prompts subordinados), P-03 (sensível), P-08, P-10, Art. 4.6 (kill switch), Art. 4.10 (ledger), Art. 5.1 (co-autoria/CCB), Art. 6.1 (SDD/parser), Art. 6.7 (SSOT/memória), Art. 8.1 (auditoria por milestone) |
| .ai/agents/config-ledger-0001-ledger-v1.0.yaml | :1-312 (39 entradas; TA-0036..0044 em :145-216) | SSOT de execução — perna E da auditoria (§3.4) |
| .ai/handoffs/task-TA-0057.json | :1-8 | Envelope desta task (campo `handoff: HF-0613` — exemplo vivo de C-04) |
| MANIFEST.md | :58 | Lacuna = literal `UNKNOWN - verify` (P-08) |

---

## 6. Fora de escopo (YAGNI)

- **Saneamento do INDEX.md** (remover 7 órfãos, catalogar os 33 ausentes com os 4 campos) — tarefa própria de custódia, pós-ratificação desta spec; **nada em `.ai/handoffs/` é editado nesta emissão** (AC-06; mandato HF-0613:17).
- **Correção dos 21 HF-06xx** (chave `agent`, status do enum, seção Critérios de Aceite) — do emissor/orquestrador dos despachos (drift D-02, §7); esta spec não reescreve handoffs alheios (agent-sdd-specialist.md:98 — "Never overwrite another agent's spec section without parcel round trip").
- **Alteração de `scripts/script-handoff-0001-parse-handoff-v1.0.py`** (novo status, novas chaves, saída agregada de auditoria) — custódia do contrato canônico; mudança via SIR com aprovação humana (agent-sdd-specialist.md:217; "cannot modify handoff_parser contract keys").
- **Automatização da auditoria em CI** (job que rode os Comandos A–D a cada push) — implementação futura, onda de infraestrutura/CI (pertence ao domínio da spec-011); aqui fica apenas o método determinístico.
- **Catálogo de prompts que não são handoffs** (system prompts de `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/`, personas `.ai/personas/`, inputs canônicos) — REQ-13 circunscreve "catalogados em `.ai/handoffs/`" (spec-002:74); demais prompts são derivativos subordinados (Art. 2.3, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:64) e de outro domínio de custódia.
- **Réplica de metadados de execução** (modelo, provedor, timestamps) no INDEX.md — violação de SSOT (Art. 6.7, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:168); o índice aponta, não duplica (§3.2).
- **REQ-12 / ADRs** (min. 3 ADRs, N9.1, spec-002:73) — domínio alheio a catálogo de prompts (§2).
- **Purge/gap-fill de numeração** (criar HF-0001..0028 retroativos) — reconstituição histórica é ato de auditoria com evidência git, não de emissão; causa dos gaps é UNKNOWN (§7a).

---

## 7. Registro UNKNOWN - verify (P-08) — drifts a sanear (NÃO corrigidos nesta emissão)

- **(a) Causa dos gaps de numeração** HF-0001..0028, HF-0035, HF-0036..0399, HF-0405..0499, HF-0501..0599 — se os arquivos jamais existiram ou se existiram e foram perdidos: **UNKNOWN - verify**. Caminho de verificação: `git log --follow --diff-filter=D -- .ai/handoffs/` e histórico anterior ao primeiro commit disponível.
- **(b) Status correto pós-dispacho dos HF-06xx no enum atual** (`emitted` → `dispatched`? emenda do enum via SIR?): decisão de custódia do orquestrador/emissor — **UNKNOWN - verify** (Caminho: CCB/orquestrador; ver §3.6 e D-02).
- **(c) Correlação integral task↔HF pré-ledger** — o ledger disponível começa em TA-0027 (ledger.yaml:1) e os envelopes em TA-0006: a correspondência 1:1 dos 6 HF-00xx (HF-0029..0034 ↔ TA-0029..0033 e TA-0035) e de HF-0500 a uma task específica **não foi verificada arquivo a arquivo** nesta emissão — **UNKNOWN - verify**. Caminho: abrir cada `task-ta-*.json` e o campo `handoff`.
- **(d) Histórico do INDEX.md** — se o índice já teve mais entradas no passado (as 7 órfãs HF-001..007 sugerem catálogo de um plano anterior não materializado): **UNKNOWN - verify**. Caminho: `git log -p -- .ai/handoffs/INDEX.md`.

**Drifts registrados (para saneamento em tarefas próprias, nesta ordem de dependência):**

| # | Drift | Evidência | Saneamento (tarefa futura) |
|---|---|---|---|
| D-01 | INDEX.md desatualizado: 7 órfãos + 33 arquivos ausentes; campos mínimos ausentes em 8/8 entradas | INDEX.md:3-10; Comando C (§3.5) | Reescrever entradas no formato §3.2 e catalogar 34/34; responsável: agent-sdd-specialist |
| D-02 | 21 HF-06xx não parseiam (chave `target`≠`agent`, status `emitted` fora do enum, sem Critérios de Aceite) | Saída do parser (§3.5); handoff_parser.py:44,104-106 | Emissor/orquestrador converte frontmatter ao contrato; alternativa: SIR no parser — decisão **UNKNOWN - verify** (§7b) |
| D-03 | HF-RELATORIO-ANALISE-CONSTITUICAO.md sem frontmatter e id fora do padrão `HF-NNNN` | Parser: "handoff sem frontmatter YAML" (§3.5); handoff_parser.py:45 | Catalogar como documento-histórico ou reemissor com id conforme — decisão de custódia |
| D-04 | Cadeia de despacho partida: 10 envelopes apontam HF sem arquivo (HF-0022, HF-0036..0044); 5 HF sem envelope (HF-0400..0404) | Comando D (§3.5) | Auditor forense (Art. 8.1) decide reconstituir, reemitir ou registrar como lacuna permanente; input do §7a |

---

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0057, HF-0613): emissão inicial. Definição operacional de "prompt catalogado" com critério binário C-01..C-04 e meta 100% REQ-13 (§3.1); formato normativo do INDEX.md como índice de ponteiros com 4 campos mínimos (§3.2); regras de nomenclatura HF-NNNN (§3.3); método de auditoria determinístico por Comandos A–E com PASS binário fail-closed e trava de kill switch #3 (§3.4); estado real auditado nesta emissão — 34 HF / 56 envelopes / índice 1/34 / parser 35→12+23 / REQ-13 NÃO ATENDIDO 0/34 (§3.5); ciclo de vida do prompt (§3.6); fundamento de co-autoria humana Art. 5.1 (§3.7); 10 ACs verificáveis (§4); rastreabilidade dupla (§5); escopo negativo com saneamento fora desta emissão (§6); 4 UNKNOWNs e 4 drifts D-01..D-04 registrados sem correção de terceiros (§7).
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo B): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `handoff` em `origin`; `version` 0.1.0 → 0.2.0). Ratificação CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012). Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio de §§1–7 reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem, task, kill_switch, trace, lgpd-class | frontmatter (`spec_id: spec-012`, `version: 0.2.0`, `status: ratificada`) + linha `Status:` | aplicada |
| (b) Contexto/origem | §1 (origem: HF-0613/TA-0057; B.8 LISTA:40; REQ-13 spec-002:74; precedente HF-0500) | aplicada |
| (c) Resolução de conflitos | §2 (REQ-13×estado real; contrato parser×HF-06xx; SSOT; REQ-12; INDEX v1.0) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (C-01..C-04, formato do índice, nomenclatura, Comandos A–E, estado auditado, ciclo de vida, co-autoria) | aplicada |
| (e) Critérios de aceite/testes | §4 (AC-01..AC-10, todos com comando de verificação) | aplicada |
| (f) Rastreabilidade (REQ/Art./US/arquivo:linha) | §5 (REQ-13, B.8, D.3/D.4, HF-0613, HF-0500, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon, parser) | aplicada |
| (g) Fora de escopo (YAGNI) | §6 (+ UNKNOWNs e drifts em §7) | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
