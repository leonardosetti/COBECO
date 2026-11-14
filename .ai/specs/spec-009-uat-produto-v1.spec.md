---
id: ai-specs-spec-009-uat-produto-v1-spec
title: SPEC spec-009 — uat-produto-v1 — Plano e roteiro de UAT de produto (fase N6.2)
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-009-uat-produto-v1.spec.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-009
specname: uat-produto-v1
version: 0.4.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: .ai/handoffs/HF-0610-spec-009-uat-produto-v1.md (envelope; item B.5 de docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:37)
task: TA-0054 | handoff: HF-0610 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (UAT produto)
lgpd-class: n/a neste artefato (zero PII); evidências de UAT exclusivamente sintéticas (P-04, constitution.md:90; parcela TA-0047, .ai/handoffs/HF-0603-consulta-de-dominio.md:40)
trace:
  - .ai/handoffs/HF-0610-spec-009-uat-produto-v1.md:14-29 (envelope — tarefa, fontes obrigatórias, contrato de resposta)
  - .ai/handoffs/HF-0603-consulta-de-dominio.md:31-44 (RESPOSTA — PARCELA DE CONSULTA TA-0047 / agent-qa-sdet — insumo normativo incorporado nos §§3.2, 3.3, 3.5-3.9)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:37 (item B.5), :52 (lacuna C.5), :60 (onda 6 — item D.3), :76 (GAP-03/ADR-016)
  - .ai/specs/spec-002-requisitos-review-round-1.spec.md:70 (REQ-09), :165 (US-009), :62-68 (REQ-01..REQ-07), :158-164 (US-001..US-008), :126 (C-07), :149-152 (nota Art. 5.1), :177-179 (US-007/016/017 — KG-R-02/KG-R-03)
  - .ai/specs/spec-005-container-layers-v1.spec.md:315-344 (§12 UAT de camadas; F-01..F-07 :323-329; critério binário :331; papéis :333-340; evidências `UNKNOWN - verify` :342), :47 (jobs do ci.yml), :117 (proxy 127.0.0.1:8080), :181 (e2e em backlog)
  - .ai/specs/spec-004-backend-mvp-v1.spec.md:29 (sem alíquota no código), :46-56 (§2 fórmula + exemplo sintético), :58-93 (§3 contrato), :107 (TTL 3600), :126 (LGPD), :130 (§6 invoice), :155 (sintético; ≥80%), :216 (T9)
  - .ai/specs/spec-006-nfr-consolidados-v1.spec.md:71-74 (NF-01..NF-04), :80 (NF-05), :87 (NF-07), :90 (NF-10)
  - .ai/specs/spec-007-invoice-data-model-v1.spec.md:26 (status), :38 (condicionante D1), :126-138 (§3.8 UNKNOWNs GAP-04)
  - .ai/specs/spec-008-frontend-web-responsive-v1.spec.md:161-163 (§8 browsers), :184-202 (§10 AC-1..AC-13), :202 (destino das evidências `UNKNOWN - verify`)
  - .ai/specs/MANIFEST.md:20-61 (template canônico camadas a–h), :58 (lacuna = literal `UNKNOWN - verify`)
  - constitution.md v1.2.1 (Art. 1.1 :27; Art. 5.1 :53; Art. 5.3 :142; P-02 :86; P-04 :90; P-08 :98; P-10 :102; P-11 :104; Art. 6.1 :150; Art. 10.1 :213)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)
---

# SPEC spec-009 — uat-produto-v1 — Plano e roteiro de UAT de produto (fase N6.2)

Status: SPEC EMITIDA — PENDENTE DE REVISÃO (agent-reviewer) E DE RATIFICAÇÃO CCB/PO DO DESTINO DAS EVIDÊNCIAS (condicionante, §2 e §3.8) | Tarefa: TA-0054 (handoff `.ai/handoffs/HF-0610-spec-009-uat-produto-v1.md`) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única do plano e do roteiro de UAT de produto da REQ-09. Em conflito, vale a hierarquia do Art. 2 (constitution.md:41-50; resolução de cima para baixo, constitution.md:78). Convenções: citação `arquivo:linha`; identificadores/paths/tokens de estado em EN; narrativa PT-BR (P-10, constitution.md:102); alegação sem fonte = **UNKNOWN - verify** (P-08, constitution.md:98; MANIFEST.md:58). Esta SPEC não implementa código e não executa a UAT (Art. 6.1, constitution.md:150) — ela norma a fase N6.2.

---

## 1. Contexto e origem

Emitida por TA-0054, via handoff HF-0610 (agent-nexus-prime-ultimate → agent-sdd-specialist, action: spec, 2026-11-03, `.ai/handoffs/HF-0610-spec-009-uat-produto-v1.md:17`), para fechar o item **B.5** da rodada 1 de specs pendentes (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:37): a REQ-09 exige "100% fluxos criticos, zero defeitos criticos/bloqueantes" na fase N6.2 da EAP (spec-002:70) e a US-009 (`uat-critical-flows`) materializa o critério (spec-002:165). O que existia era apenas a **proposta de UAT de camadas** da spec-005 §12 (spec-005:315-344), escopo restrito às camadas Dados/Back/Front + aderentes — a UAT de produto (fluxos de negócio) não tinha spec (LISTA-SPECS-PENDENTES-2026-11-02.md:37).

**Insumo normativo meio-duplex:** a parcela de consulta TA-0047 (agent-qa-sdet), retornada em `.ai/handoffs/HF-0603-consulta-de-dominio.md:31-44`, é incorporada nesta emissão como norma dos eixos: critério binário fail-closed (HF-0603:40, item 1), roteiro/matriz e reaproveitamento de F-01..F-07 por referência (:40, item 2), proposta de destino das evidências (:40, item 3) e lista de UNKNOWNs (:40, item 4). Recomendações dela que dependem de decisão de camada superior (destino/retenção das evidências, caráter bloqueante do relatório) entram apenas como **condicionantes CCB/PO, não como requisitos aprovados** (precedente de leitura: spec-007:32, que aplica `.ai/handoffs/HF-0621-requisitos-repovoar.md:36`).

**Specs irmãs da mesma rodada (cross-ref):** `spec-006` (NF-01..NF-10 ancoram as métricas dos critérios de passagem, spec-006:71-74,80,87,90), `spec-007` (modelo de dados da invoice — condicionante D1 condiciona UAT-04, spec-007:38,48), `spec-008` (camada `front` — AC-1..AC-13 e matriz de browsers alimentam UAT-05, spec-008:184-202). A spec-008 já declara: "UAT de produto: os fluxos de front integram F-02/F-03 (spec-005:324-325) e a UAT de produto B.5 (...); destino das evidências: **UNKNOWN - verify** (spec-005:342)" (spec-008:202).

**Estado das dependências nesta emissão:** o produto não está implementado (specs da rodada em `status: draft`, Art. 6.1) — este artefato é o **plano e o roteiro** que a fase N6.2 executará quando as histórias estiverem Done; a execução em si está fora do escopo desta emissão (§6). Esta spec está na onda 6 "Corrente da Qualidade" (A.19–A.22, docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:60).

---

## 2. Resolução de conflitos

| Tema | Decisão desta spec | Fonte vencedora | Texto superado / não promovido |
|---|---|---|---|
| Alcance da UAT | Esta spec cobre a **UAT de produto** (fluxos de negócio US-001..US-008, fase N6.2); a UAT de camadas F-01..F-07 da spec-005 §12 permanece vigente e é **reaproveitada por referência**, sem duplicação nem reescrita (§3.4) | LISTA-SPECS-PENDENTES-2026-11-02.md:37 + spec-005:315-317 | Leitura de que a spec-005 §12 esgotaria a REQ-09 ("parcial em spec-005-...spec.md:315-344, proposta restrita às camadas") |
| Critério de passagem | Binário fail-closed: 100% dos fluxos críticos PASS e zero defeitos críticos/bloqueantes abertos; qualquer reprovado = UAT reprovada (§3.2) | REQ-09 (spec-002:70) + US-009 (spec-002:165) + precedente spec-005:331 + parcela TA-0047 (HF-0603:40) | Qualquer leitura percentual ou "aprovada com ressalvas" |
| Destino das evidências | **Proposta** `docs/uat/N6.2/` com nomenclatura definida (§3.8); a RATIFICAÇÃO do destino final é do GP/CCB — reserva explícita da spec-005:342 ("a definir pelo GP"); até lá vale `UNKNOWN - verify` | Condicionante CCB: spec-005:342 + parcela TA-0047 (HF-0603:40, item 3) | Promoção de `docs/uat/` a decisão fechada nesta emissão (alternativa: `docs/auditorias/`) |
| Caráter bloqueante do relatório | O relatório de UAT aprovado como condição de release/merge é parte da ratificação CCB pendente — não decidido aqui | Parcela TA-0047 (HF-0603:40, item 3: "carater bloqueante do relatorio" a ratificar) | Assumir bloqueio automático de release sem ratificação |
| Fluxos condicionais | US-007, US-016, US-017 só entram no roteiro se ratificadas (KG-R-02/KG-R-03); enquanto não ratificadas, não computam no 100% nem como FAIL (§3.5) | Parcela TA-0047 (HF-0603:40) + spec-002:177-179 | Tratá-las como fluxos críticos vigentes |
| Defeitos não críticos | Major/minor vão ao backlog com severidade e decisão PO (Art. 5.1) — não reprovam a UAT | Parcela TA-0047 (HF-0603:40, item 1) + spec-005:331 + spec-002:149-152 | Reprovação da UAT por defeito não crítico |

---

## 3. Plano de UAT de produto (domínio)

### 3.1 Escopo

- **O quê:** UAT de produto da REQ-09 — validação binária dos fluxos críticos de negócio do MVP sobre a interface e o contrato `/v1`, na fase N6.2 (spec-002:70).
- **Onde:** ambiente local CPU-only (P-02, constitution.md:86), stack separada da spec-005 (`docker compose up --build`, usuário via `proxy` em `127.0.0.1:8080` — spec-005:117, roteiro F-01 spec-005:323).
- **Com o quê:** dados/fixtures 100% sintéticos (spec-004:155; parcela TA-0047, HF-0603:40 — "fixtures 100% sinteticas (P-04)").
- **Cobertura obrigatória:** 7 fluxos de produto (§3.3, US-001..US-006 e US-008) + 7 casos de camada por referência (§3.4, F-01..F-07 da spec-005 §12).
- **Fora do escopo UAT:** ver §6 (REQ-10/11/12/13/14/15, testes de carga, e2e automatizado, LGPD de produto).

### 3.2 Critério de passagem binário (fail-closed)

1. Cada fluxo crítico tem resultado **pass/fail** binário — não existe "passou com ressalva" (parcela TA-0047, HF-0603:40, item 1; precedente spec-005:331).
2. **UAT APROVADA** somente com **100% PASS** e **zero defeitos críticos/bloqueantes abertos** ("100% fluxos criticos, zero defeitos criticos/bloqueantes" — REQ-09, spec-002:70; US-009, spec-002:165).
3. **UAT REPROVADA** com qualquer caso FAIL ou qualquer defeito crítico/bloqueante aberto (fail-closed; HF-0603:40).
4. Defeitos major/minor → backlog com severidade e decisão PO (Art. 5.1, constitution.md:53; HF-0603:40).
5. **Proibido fake green:** nenhuma passagem declarada sem evidência com run id, exit code, timestamp e comando de repro (HF-0603:40; violação é misleading traceability — kill switch Art. 4.6, item 3 do contrato agent-sdd-specialist §0.2).

### 3.3 Matriz de fluxos críticos de produto × US × REQ (com trace ids)

Formato de trace id da parcela TA-0047: `REQ-x::UAT-nn::layer::case` (HF-0603:40, item 2); camada `product` nesta seção. Cobertura exigida: 7/7 linhas — 100% dos fluxos críticos de produto ratificados.

| Trace id | Fluxo crítico (produto) | US | REQ | Critério de passagem binário | Ancoras |
|---|---|---|---|---|---|
| `REQ-01::UAT-01::product::sim-realtime` | Simulação em tempo real USD/EUR→BRL | US-001 (spec-002:158) | REQ-01, REQ-05 (spec-002:62,66) | PASS: equivalente em BRL exibido com cotação ≤2s (chamada externa) e resposta E2E ≤3s P95 — leitura de camadas C-07 (spec-002:126); FAIL: estouro ou tela sem resultado | NF-01/NF-02 (spec-006:71-72); orçamento 1,9s (spec-004:114) |
| `REQ-02::UAT-02::product::regimes-5` | 5 regimes de contratação operacionais e comparáveis | US-002 (spec-002:159) | REQ-02 (spec-002:63) | PASS: 100% dos regimes (`hourly|daily|weekly|monthly|fixed`, spec-004:60) calculam e são comparáveis — "100% regimes em UAT" (spec-002:63); FAIL: qualquer regime ausente | F-02 por referência (§3.4) |
| `REQ-03::UAT-03::product::spread-iof-audit` | Encargos spread+IOF com trilha auditável e 2 casas | US-003 (spec-002:160) | REQ-03 (spec-002:64) | PASS: líquido segue a fórmula da spec-004 §2 (spec-004:46-53) com 2 casas, identidade `gross_brl − spread_brl − iof_brl == net_brl` (spec-004:53) e trilha auditável; fixture candidata: exemplo sintético canônico (rate 5.000000, spread 2, iof 0.38 → net_brl 23430.62, spec-004:55-56); alíquotas informadas pelo usuário, sem default (spec-004:29); fórmula ratificada via ADR-016 (RAT-2026-11-05-A16) | NF-04 parcial (spec-006:74) |
| `REQ-04::UAT-04::product::invoice-pdf` | Emissão de invoice em PDF | US-004 (spec-002:161) | REQ-04 (spec-002:65) | PASS: PDF válido em ≤3s/documento (NF-03, spec-006:73) com `Content-Disposition: attachment` (spec-004:130) e zero PII em logs (spec-004:126); invoice persistida na tabela `invoices` com modelo canônico (spec-007 §3.1; ADR-016 D4, RAT-2026-11-05-A16-D4); rota de erase obrigatória (LGPD art. 18) se D1-D6 da spec-007 ratificadas. | F-03 por referência (§3.4) |
| `REQ-06::UAT-05::product::ui-browsers` | Interface web responsiva sem quebra funcional | US-005 (spec-002:162) | REQ-06 (spec-002:67) | PASS: layout responde sem quebra funcional em Chrome/Firefox/Edge **últimas 2 versões** (versões exatas na data: `UNKNOWN - verify`, §3.10); método: matriz manual de browsers (AC-4 da spec-008, spec-008:191) | NF-05 (spec-006:80) |
| `REQ-07::UAT-06::product::cache-reduction` | Cache reduz dependência da API externa | US-006 (spec-002:163) | REQ-07 (spec-002:68) | PASS: redução ≥50% das chamadas à API externa com cache ativo; TTL fixado 3600s (`COBECO_RATE_TTL_SECONDS`, spec-004:107); demais parâmetros (GAP-06): `UNKNOWN - verify` (§3.10) | NF-04 (spec-006:74) |
| `REQ-08::UAT-07::product::coverage-gate` | Cobertura de testes ≥80% válida por CI | US-008 (spec-002:164) | REQ-08 (spec-002:69) | PASS: relatório de cobertura ≥80% sobre `src/` (spec-004:155) no run do CI citado como evidência (artefato de cobertura, ci.yml:170 via spec-005:342); run id citável: `UNKNOWN - verify` enquanto G-05 não auditado (§3.10) | NF-07 (spec-006:87) |

### 3.4 Reuso por referência dos casos de camada F-01..F-07 (spec-005 §12)

Os casos de UAT de camadas **não são redefinidos aqui** — reuso exclusivamente por referência (parcela TA-0047, HF-0603:40, item 2: "reaproveitar F-01..F-07 spec-005 SS12 POR REFERENCIA (sem duplicar)"):

| Caso (por referência) | Fluxo de camada | Fonte canônica |
|---|---|---|
| `container::F-01` | Reprodutibilidade: clone limpo → `.env` → `docker compose up --build` → `127.0.0.1:8080` | spec-005:323 |
| `container::F-02` | Simulação E2E: `POST /v1/simulate`, 5 regimes, identidade monetária | spec-005:324 |
| `container::F-03` | Invoice: `POST /v1/invoice`, PDF ≤3s, sem PII em logs | spec-005:325 |
| `container::F-04` | Isolamento: `front` não alcança `db:5432`; `db` sem porta no host | spec-005:326 |
| `container::F-05` | Degradação: `db` parado → 503 canônico sem crash | spec-005:327 |
| `container::F-06` | Migração: `alembic upgrade head` + `downgrade base` idempotentes | spec-005:328 |
| `container::F-07` | Segurança: 100% dos controles do bloco de segurança | spec-005:329 |

Regra anti-duplicação: cada caso executa-se **uma única vez** e alimenta o mesmo relatório (§3.8); onde um fluxo de produto dependa do comportamento de um F-0N, o trace id de produto o referencia sem reexecutá-lo (precedente declarado pela spec-008:202 — "os fluxos de front integram F-02/F-03"). Pares de sobreposição: UAT-02↔F-02 e UAT-04↔F-03.

### 3.5 Fluxos condicionais (não computam no 100% hoje)

| US | Fluxo | Condição de entrada no roteiro | Fonte |
|---|---|---|---|
| US-007 | Fallback de cotação com aviso de defasagem | KG-R-02 ratificado PO/CCB | spec-002:177; HF-0603:40 |
| US-016 | Ciclo de vida Rascunho/Finalizada | KG-R-03 ratificado CCB | spec-002:178; HF-0603:40 |
| US-017 | Clone de invoice com novo número | KG-R-03 ratificado CCB (depende de US-016) | spec-002:179; HF-0603:40 |

Enquanto não ratificadas, esses fluxos **não entram na contagem dos 100%** nem podem reprovar a UAT (condicional não é fluxo crítico vigente — §2, linha 5).

### 3.6 Papéis (RACI)

| Papel (RACI) | Exercido por | Base | Fonte |
|---|---|---|---|
| **R** — Executor (roteiro e execução) | agent-qa-sdet | Roster (Art. 2.2) | spec-005:337; HF-0603:40 (item 2) |
| **C** — Revisor de segurança e de código | agent-digital-security + agent-reviewer | precedente T9 do backend-mvp | spec-004:216; spec-005:338 |
| **A** — Aprovador do resultado (ato humano) | Humano — GP via CCB | merge/release é ato humano | Art. 5.3 (constitution.md:142); spec-005:339 |
| **C** — Stakeholder avaliador acadêmico | Prof. Dr. Nivaldo Carleto | canônico | Art. 1.1 (constitution.md:27); spec-005:340 |
| **I** — Decisão sobre defeitos major/minor (backlog) | PO | Art. 5.1 (stories decididas pelo Humano/PO) | spec-002:149-152; HF-0603:40 |
| **I** — Orquestrador (retorno meio-duplex da fase) | agent-nexus-prime-ultimate | contrato de resposta do envelope | HF-0610:26-29 |

### 3.7 Roteiro de execução (fase N6.2)

1. **Setup do ambiente:** máquina local CPU-only (P-02, constitution.md:86); stack separada da spec-005 no ar via `docker compose up --build` (F-01, spec-005:323) com todos os serviços healthy; `127.0.0.1:8080` responde (spec-005:117); fixtures exclusivamente sintéticas (spec-004:155; HF-0603:40).
2. **Congelamento da matriz de browsers:** registrar no relatório as versões exatas de Chrome/Firefox/Edge utilizadas na data (REQ-06 "últ. 2 versões", spec-002:67; spec-008:161) — versões exatas hoje: `UNKNOWN - verify` (§3.10).
3. **Execução por trace id:** para cada linha da §3.3 e cada caso da §3.4, o executor registra o resultado binário pass/fail com a evidência mínima — run id, exit code, timestamp e comando de repro (HF-0603:40, item 1). Proibido fake green (§3.2, item 5).
4. **Registro de defeitos:** todo FAIL gera `DEF-UAT-NNN` no registro de §3.9 com severidade; nada segue "aprovado com ressalva".
5. **Consolidação:** relatório `relatorio-UAT-<yyyymmdd>-run<nn>.md` (§3.8) com tabela pass/fail por trace id + registro de defeitos com severidade e status.
6. **Veredito binário fail-closed:** 100% PASS e zero defeitos críticos/bloqueantes abertos → UAT **APROVADA**; qualquer FAIL ou defeito crítico/bloqueante aberto → UAT **REPROVADA** (§3.2; spec-005:331; spec-002:70). Defeitos major/minor → backlog com decisão PO (Art. 5.1, constitution.md:53).
7. **Aprovação humana:** veredito levado ao GP via CCB (Art. 5.3, constitution.md:142) — a aprovação da UAT e a ratificação do destino das evidências (§3.8) são atos humanos; o resultado não se torna release sem esse gate.

### 3.8 Evidências — destino decidido (fecha C.5)

O destino das evidências de UAT é **docs/uat/**, classificado por rodada (ex.: `docs/uat/rodada-001/`), com relatório analítico por rodada contendo taxa de aceite, cobertura analizada e ciclo de implementação. Decisão GP/CCB fechada em 05/11/2026 (pendência #6 dos 7 bloqueantes resolvida). Não é mais condicionante.

- **Relatório:** `docs/uat/N6.2/relatorio-UAT-<yyyymmdd>-run<nn>.md` → normalizado para `docs/uat/rodada-NN/relatorio-analitico.md` — tabela pass/fail por trace id + registro de defeitos com severidade (§3.9).
- **Evidências por caso:** `docs/uat/rodada-NN/evidencias/<id>__US-<slug>__<yyyymmdd>__run<nn>.log\|.png` — para os fluxos de produto, `<id>` = `UAT-nn` (ex.: `UAT-04__US-004__20261103__run01.png`); para os casos de camada, `<id>` = `F-0N`. Padrão da parcela (HF-0603:40).
- **Evidência mínima por caso:** run id, exit code, timestamp, comando de repro (§3.2, item 5; HF-0603:40, item 1).
- **Retenção:** PERMANENTE, versionada em git como trilha de auditoria, sem exclusão; conteúdo exclusivamente sintético (P-04, constitution.md:90).
- **Caráter bloqueante do relatório:** o relatório de UAT aprovado é condição de release/merge (ato humano do GP via CCB, Art. 5.3, constitution.md:142).

### 3.9 Registro de defeitos e severidade

Cada defeito é uma linha do relatório (§3.8) com o schema:

| Campo | Valores (EN tokens) | Regra |
|---|---|---|
| id | `DEF-UAT-NNN` | sequencial por run |
| severity | `critical` \| `blocking` \| `major` \| `minor` | `critical`/`blocking` = reprovam a UAT; `major`/`minor` = backlog com decisão PO (§3.2, itens 2-4) |
| trace_id | `REQ-x::UAT-nn::product::case` ou `container::F-0N` | caso reprodutor |
| repro | comando + run id + exit code + timestamp | obrigatório (HF-0603:40, item 1) |
| status | `open` \| `backlog` \| `closed` | `open` em `critical`/`blocking` = UAT reprovada |
| decision | PO ou CCB (ato humano) | Art. 5.1 (constitution.md:53) |

Semântica de severidade (taxonomia proposta nesta emissão, sem precedente citado no corpus — sem contrafonte em spec-005:331 e HF-0603:40): `critical` = resultado financeiro incorreto, perda de dados ou violação LGPD (ex.: PII em log, spec-004:126); `blocking` = fluxo crítico impossível de completar; `major` = funcional com workaround; `minor` = cosmético/UX.

### 3.10 `UNKNOWN - verify` (P-08 — sem invenção)

Lista da parcela TA-0047 (HF-0603:40, item 4), completa:

1. **Destino das evidências** — decidido = `docs/uat/`, classificado por rodada (`docs/uat/rodada-NN/`), com relatório analítico por rodada (taxa de aceite, cobertura analizada, ciclo de implementação). Decisão GP/CCB fechada em 05/11/2026; não é mais condicionante. Retenção permanente, conteúdo exclusivamente sintético (P-04). | §2, §3.8 |
2. **Versões exatas dos browsers** na data da execução (REQ-06 "últ. 2 versões" é móvel — spec-002:67).
3. **Valores de spread/IOF dos casos de teste** (GAP-03, spec-002:102): alíquotas são informadas pelo usuário, nenhuma no código (spec-004:29); fórmula do MVP fixada em spec-004:46-53, ratificada via ADR-016 (RAT-2026-11-05-A16).
4. **Campos da invoice** além do contrato spec-004 §3: modelo canônico definido em spec-007 §3.1 (tabela `invoices`); GAP-04 fechado por ADR-016 D4 (RAT-2026-11-05-A16-D4).
5. **Parâmetros de cache além do TTL** (GAP-06, spec-002:105; TTL 3600s já fixado, spec-004:107).
6. **Run id de CI citável como evidência** enquanto G-05 não auditado (item B.7, LISTA-SPECS-PENDENTES-2026-11-02.md:39).
7. **Inclusão de US-016/US-017** (KG-R-03) e de US-007 (KG-R-02) no roteiro — condicionais (§3.5).

---

## 4. Critérios de aceite e testes

**Validador:** agent-reviewer (audita citações linha a linha e testabilidade) e agent-gatekeeper (gate). **DoD desta emissão:** arquivo único criado + parcela JSON retornada ao orquestrador (contrato HF-0610:26-29).

Critérios de spec (vigentes agora):

- [ ] O arquivo `.ai/specs/spec-009-uat-produto-v1.spec.md` existe, com frontmatter conforme MANIFEST §1.1 e ≤ 400 linhas (contrato agent-sdd-specialist §0.2 RESOURCE).
- [ ] Toda afirmação de domínio cita `arquivo:linha` OU está marcada literal `UNKNOWN - verify` (P-08, constitution.md:98; MANIFEST.md:58).
- [ ] A matriz §3.3 cobre 100% dos fluxos críticos de produto ratificados — 7/7 trace ids (`UAT-01..UAT-07`) mapeando US-001..US-006 e US-008 e REQ-01..REQ-08, sem lacuna contável.
- [ ] O critério binário fail-closed (§3.2) é idêntico em substância ao de spec-005:331 e à REQ-09/US-009 (spec-002:70,165) — sem afrouxamento.
- [ ] F-01..F-07 aparecem apenas POR REFERÊNCIA (§3.4): nenhuma definição nova de caso de camada neste arquivo.
- [ ] O destino das evidências (§3.8) está registrado como condicionante CCB, não como decisão — precedente de leitura spec-007:32; lacuna C.5 não declarada como fechada até ratificação.
- [ ] US-007/US-016/US-017 não computam no 100% (§3.5) — condicionais KG-R-02/KG-R-03.
- [ ] Nenhum critério introduz tracking/surveillance ou dado real (kill switch herdado, Art. 4.6; P-04).

Critérios de execução (fase N6.2 — NÃO executáveis nesta emissão; bloqueados até implementação das histórias, Art. 6.1):

- [ ] Para cada trace id da §3.3 e §3.4: resultado PASS com evidência mínima (run id, exit code, timestamp, comando de repro) armazenada no destino ratificado.
- [ ] Relatório `relatorio-UAT-<yyyymmdd>-run<nn>.md` emitido com tabela pass/fail completa (7 fluxos de produto + 7 casos de camada) e registro de defeitos §3.9.
- [ ] Veredito binário aplicado e registrado: UAT APROVADA (100% PASS + zero `critical`/`blocking` abertos) OU UAT REPROVADA — sem terceiro estado.
- [ ] Defeitos major/minor encaminhados ao backlog com severidade e decisão PO (Art. 5.1).
- [ ] Aprovação humana do veredito registrada (GP via CCB, Art. 5.3, constitution.md:142).
- [ ] Zero PII em qualquer evidência (fixtures sintéticas — spec-004:155; P-04, constitution.md:90).

---

## 5. Rastreabilidade

| Fonte | Onde nesta spec |
|---|---|
| B.5 / REQ-09 / US-009 (LISTA-SPECS-PENDENTES-2026-11-02.md:37; spec-002:70,165) | §1, §3.2, §3.3, §4 |
| Lacuna C.5 (LISTA-SPECS-PENDENTES-2026-11-02.md:52; spec-005:342) | §2, §3.8, §3.10.1 |
| Parcela TA-0047 agent-qa-sdet (HF-0603:31-44) | §2, §3.2, §3.3, §3.4, §3.5, §3.7, §3.8, §3.9, §3.10 |
| UAT de camadas F-01..F-07 (spec-005:315-344) | §3.1, §3.4 |
| Regras do produto (spec-004:29,46-56,58-93,107,126,130,155) | §3.3 (UAT-01..UAT-07), §3.7, §3.9 |
| NFR consolidados (spec-006:71-74,80,87,90) | §3.3 (coluna Ancoras) |
| Modelo de dados da invoice / D1 (spec-007:38,48,126-138) | §3.3 (UAT-04), §3.10.4 |
| Camada `front` (spec-008:161-163,184-202) | §3.3 (UAT-05), §3.4 (sobreposição), §3.10.2 |
| US-001..US-008 e condicionais (spec-002:158-164,177-179) | §3.3, §3.5 |
| C-07 (spec-002:126) | §3.3 (UAT-01) |
| GAP-03/ADR-016 E.2 (LISTA-SPECS-PENDENTES-2026-11-02.md:76; spec-002:102) | §3.3 (UAT-03), §3.10.3 |
| G-05 / B.7 (LISTA-SPECS-PENDENTES-2026-11-02.md:39) | §3.3 (UAT-07), §3.10.6 |
| Papéis (Art. 1.1/5.1/5.3, constitution.md:27,53,142; spec-005:337-340; spec-004:216) | §3.6, §3.7 (itens 6-7) |
| Onda 6 (LISTA-SPECS-PENDENTES-2026-11-02.md:60) | §1 |

---

## 6. Fora de escopo (YAGNI — P-11, constitution.md:104)

- **Execução da UAT nesta emissão** — este artefato é plano/roteiro; executar é tarefa futura da fase N6.2, pós-implementação (Art. 6.1, constitution.md:150).
- **UAT de camadas** — já norma da spec-005 §12 (spec-005:315-344); aqui apenas reuso por referência (§3.4), sem redefinição.
- **REQ-10 qualidade (PDCA+Ishikawa)** — item B.6, spec própria (LISTA-SPECS-PENDENTES-2026-11-02.md:38).
- **REQ-11 CI/CD** — item B.7/spec própria; aqui o CI aparece só como fonte de evidência de cobertura (UAT-07; LISTA-SPECS-PENDENTES-2026-11-02.md:39).
- **REQ-12/13/14** (ADRs, rastreabilidade de prompts, documentação) e **REQ-15** (auditoria FOSS — gate `foss-compliance` do CI, spec-005:47) — não são fluxos críticos de produto da matriz §3.3 (fora do roteiro da parcela TA-0047, HF-0603:40).
- **Testes de carga/estresse** (OS-07, spec-002:140) e **e2e automatizado de navegador nesta onda** (spec-005:181; spec-008:52) — UAT-05 usa matriz manual estruturada (spec-008:191).
- **Política LGPD de produto** — item B.3, condicionada a CCB/PO (LISTA-SPECS-PENDENTES-2026-11-02.md:35); aqui UAT-04 verifica apenas o critério vigente "sem PII em logs" (spec-004:126).
- **Ferramentas de automação de UAT** (nomear Playwright/Selenium etc.) — plano de testes conceitual desacoplado de stack, nenhuma ferramenta nomeada como decisão (precedente spec-002:233).
- **Novos endpoints ou alteração do contrato `/v1`** (spec-005:226) e qualquer código/compose/workflow alterado (Art. 6.1).

---

## Conformidade desta emissão

- Arquivo único criado: `.ai/specs/spec-009-uat-produto-v1.spec.md` (custódia `.ai/specs/`). Nenhum outro arquivo editado; nada commitado.
- Kill switch herdado (Art. 4.6); zero PII no artefato e nas evidências normadas (P-04, constitution.md:90); 100% local, sem cloud (P-02, constitution.md:86); slugs/paths/tokens EN + narrativa PT-BR (P-10, constitution.md:102); toda alegação com `arquivo:linha` ou `UNKNOWN - verify` (P-08, constitution.md:98); nenhuma capacidade especulativa (P-11, constitution.md:104).
- Hierarquia respeitada: Constituição > ADR-001 v1.1.0 > planos > specs (spec-002/004/005/006/007/008 preservadas, nenhuma editada) > código (Art. 2).

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0054, HF-0610): emissão inicial. Template canônico MANIFEST §1 (camadas a-h). Insumo normativo incorporado: parcela de consulta TA-0047 (agent-qa-sdet, HF-0603:31-44) — critério binário fail-closed, matriz fluxo×US×REQ com trace ids `REQ-x::UAT-nn::layer::case`, reuso por referência de F-01..F-07, papéis RACI, destino proposto `docs/uat/N6.2/` com nomenclatura e retenção (condicionante CCB — fecha C.5 somente após ratificação), roteiro de 7 passos, registro de defeitos com severidade `critical|blocking|major|minor` e 7 UNKNOWNs. 7 fluxos de produto (UAT-01..UAT-07) + 7 casos de camada por referência; 3 fluxos condicionais (US-007/016/017). Critérios de spec (8) + critérios de execução (6, não executáveis nesta emissão). Nenhum outro arquivo editado; nada commitado.
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo A): destino das evidências DECIDIDO = `docs/uat/`, classificado por rodada (`docs/uat/rodada-NN/`), com relatório analítico por rodada (taxa de aceite, cobertura analizada, ciclo de implementação). Decisão GP/CCB fechada em 05/11/2026 (pendência #6 resolvida). §3.8 reescrito — destino não é mais condicionante; `docs/uat/README.md` criado; `docs/uat/rodada-001/relatorio-analitico.md` criado (taxa de aceite 0% não executada, cobertura 0/14 casos, ciclo EM EXECUÇÃO). `unknown - verify` do destino removido. `version` 0.1.0 → 0.4.0 (salto para alinhar com refinamento do Grupo A). Nenhuma decisão de negócio de §§1–3 reescrita. **Ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)**.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-009`, `version: 0.4.0`, `status: draft`) + linha `Status:` | aplicada |
| (b) Contexto/origem | §1 (origem TA-0054/HF-0610; item B.5; insumo TA-0047; specs irmãs) | aplicada |
| (c) Resolução de conflitos | §2 (6 temas: alcance, critério, destino evidências, caráter bloqueante, condicionais, defeitos) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (§3.1-§3.10: escopo, critério binário, matriz com trace ids, reuso F-01..F-07, condicionais, RACI, roteiro, evidências, defeitos, UNKNOWNs) | aplicada |
| (e) Critérios de aceite/testes | §4 (critérios de spec + critérios de execução da fase N6.2) | aplicada |
| (f) Rastreabilidade | §5 (REQ/US/parcela/arquivo:linha) + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §6 | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
