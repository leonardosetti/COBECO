---
id: ai-specs-requisitos
title: REQ-SPEC-001 — Requisitos COBECO — SSOT RF/RNF da camada 5
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
confirmed_by: gh-sig:owner:leonardosetti:14863508
confirmed_at: '2026-11-16T04:58:00-03:00'
derived-from:
- .ai/specs/requisitos.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-16'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
- ssot-confirmed-ccb-001
---
---
id: REQ-SPEC-001
title: "Requisitos COBECO — SSOT RF/RNF da camada 5"
status: draft
version: 1.0.0
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
task: TA-0065
sender: agent-nexus-prime-ultimate
kill_switch: inherited
lgpd-class: n/a (zero PII neste artefato; P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90 — precedente: spec-002:19, spec-006:12)
trace:
  - .ai/handoffs/hf-exec-0621-requisitos-repovoar-v1.0.md:16-31 (envelope TA-0065; condição de desbloqueio; regra de ouro P-08)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:25 (item A.1 — origem)
  - .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:53-79,149-179,208-224,243-249 (fonte primária RF: REQ-01..15, US, gates, KGs)
  - docs/planos/plano-granular/plano-integral-tap-1-2-3-4-5.md:67-87,310 (Tabela 3 — baseline textual dos REQ; MoSCoW)
  - .ai/specs/tap.md:96-121 (Tabela 3 transcrita — fonte alternativa de conferência)
  - .ai/specs/spec-nfr-0001-nfr-consolidados-v1.0.md:61-130,147-155 (fonte canônica NFR — cross-ref, não duplicação)
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226,245 (ratificação CCB E-01..E-08); :90 (P-04); :213,215 (Art. 10.1/10.2)
  - .ai/specs/spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:193-334 (texto das emendas E-01..E-08)
  - .ai/specs/doc-manifest-0001-manifest-v1.0.md:100,170 (§3/§5.1 — requisitos.md pinned, sem rename)
  - docs/conhecimento/KB-INDEX.md:53-54 (REQ-SPEC-001 draft 1.0.0; docs/requisitos/requisitos.md é ponteiro)
---

# REQ-SPEC-001 — Requisitos COBECO — SSOT RF/RNF da camada 5

Status: draft — transcrição rastreável de fontes ratificadas. NENHUM requisito foi criado,
alterado ou promovido a aprovado nesta emissão (P-08; hf-exec-0621:35).

## 1. Regime — fontes e precedência

- **Natureza:** este arquivo é o SSOT (single source of truth) de RF/RNF da camada 5
  (KB-INDEX:53 — "SSOT RF/RNF declarado; docs/requisitos/requisitos.md é ponteiro"). Seu
  conteúdo é TRANSCRIÇÃO rastreável das fontes sobreviventes ratificadas — nenhum requisito
  novo é inventado (P-08; hf-exec-0621:22).
- **Fonte primária de RF:** `spec-002` (REQ-01..REQ-15, tabela A.2 + corpo, incl. US
  associadas doc-user-story-0001-us-001..doc-user-story-0017-us-017). **Fonte da baseline textual:** `plano-integral` Tabela 3
  (plano-integral:67-87), transcrita com conferência em `tap.md` §8 (tap.md:96-121).
- **Fonte canônica de RNF:** `spec-006` (NF-01..NF-25). Este arquivo REFERENCIA os NFR por
  cross-ref (§6) e não os duplica: métricas, conflitos e `UNKNOWN - verify` residem na fonte.
- **Fonte de emendas:** `spec-001` (texto E-01..E-08, spec-001:193-334) + ratificação CCB em
  `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` (CHANGELOG constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226; co-assinatura constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:245).
- **Precedência (Art. 2):** constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md > TAP congelado/plano-integral > ADRs > planos >
  specs > código; resolução de cima para baixo (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78; spec-006:54). Em
  divergência entre este arquivo e uma fonte citada, a FONTE vence e aqui registra-se
  `UNKNOWN - verify` (padrão tap.md:31).
- **Imutabilidade pós-escrita:** `.ai/specs/*.md` são "Specs imutáveis… never modified without
  new version file" (ADR-011:56, via MANIFEST §5.2). Alteração futura = novo arquivo de versão.
- **Documento ponteiro:** `docs/requisitos/requisitos.md` aponta para cá (KB-INDEX:54) — não
  editar (hf-exec-0621:37).
- **Consulta TA-0050 (compliance):** decisões D1-D7 em docs/uat/ são condicionantes, não
  requisitos aprovados (hf-exec-0621:36).
- **Nota de execução (2026-11-03):** MANIFEST:100 registrava `requisitos.md` (0 B); no momento
  desta task o arquivo inexistia no diretório `.ai/specs/` (nem como 0 B). TA-0065 cria-o no
  caminho pinned, sem rename (MANIFEST §5.1, MANIFEST:170) — precedente idêntico: tap.md:34.

## 2. Contexto e origem

- Origem: task TA-0065 / handoff hf-exec-0621 (action: spec), item A.1 de LISTA:25 — "Repovoar
  `.ai/specs/requisitos.md` (0 B) para dar conteúdo executável à camada 5 e fechar o
  GAP-01/G-08" (GAP-01: spec-002:100; G-08: spec-001:132-141).
- **Condição de desbloqueio VERIFICADA (gate E):** "constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226 — '1.1.0 — 2026-10-26:
  CCB ratifica as emendas E-01..E-08 da Rodada 1'; tabela de co-assinatura constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:245.
  Portanto o gate E foi DECIDIDO; a condição 're-emissão de ADRs + CCB' da spec-002:208-224
  para E-01..E-08 está satisfeita na parte constitdoc-arch-0006-uc-v1ional. O orquestrador autoriza a emissão"
  (hf-exec-0621:17-22). A ratificação v1.1.0 registra instrumento "CCB 26/10/2026, emendas
  E-01..E-08" (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:245).
- O gate de spec-002 (§E, spec-002:208-224) condicionava esta escrita às decisões do gate E;
  a parte constitdoc-arch-0006-uc-v1ional satisfeita + autorização do orquestrador (hf-exec-0621:21-22) desbloqueiam
  esta emissão nos termos declarados no envelope. Nenhuma decisão adicional é assumida aqui.
- Legado do item: spec-002 §E listava esta repovoação entre os BLOCKED (spec-002:223-224);
  o estado atual de desbloqueio parcial é o declarado em hf-exec-0621:17-22.

## 3. Resolução de conflitos (divergências registradas — conferência spec-002 × plano-integral/tap.md)

| # | Tema | Leitura A | Leitura B | Fonte vencedora | Registro |
|---|---|---|---|---|---|
| 1 | Conferência REQ-01..15: tabela A.2 (spec-002:62-76) × Tabela 3 (plano-integral:71-85; transcrição tap.md:102-116) | síntese spec-002 (abreviada) | baseline textual integral | conteúdo idêntico em síntese, critério e fase EAP nas 15 linhas — sem divergência material nesta conferência | KG-R-01 (diff integral entre os 4 espelhos) permanece pendente na fonte (spec-002:243-245) |
| 2 | Persistência do cache REQ-07: rótulo "SQLite" da baseline (plano-integral:77) | PostgreSQL canônico pós-emenda v1.2.0 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213; delta-v3.1.md:9, via tap.md:47,120) | leitura operacional = Delta Log; baseline textual atualizada para PostgreSQL 15+ (esta linha) | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 + spec-006:54 | já registrado na fonte (spec-006 §2, linha 54; tap.md §3 item 2) — aqui apenas referenciado; critério numérico ≥50% íntegro (spec-006:74) |
| 3 | Latência REQ-01 ≤2s × REQ-05 ≤3s sem camadas explícitas (C-07) | contradição | ambiguidade — "leitura provável: 2s=chamada API, 3s=E2E" | spec-002:126 (registro) | confirmação PO/CCB pendente (spec-006:53); NF-01/NF-02 adotam a leitura declarada pela fonte |
| 4 | Fórmula spread/IOF (GAP-03; C-05) | DEDUÇÃO (legado review:16/qwen:44) | MULTIPLICAÇÃO (legado deepseek:50) | decisão CCB/PO pendente (spec-002:102,124) | spec-006 NF-25 registra fórmula fixada em spec-004 §2, "pendente de ratificação via ADR-016" (spec-006:130) |
| 5 | Citações constitdoc-arch-0006-uc-v1ionais P-04/P-06/P-08: spec-002 cita constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:34,36 (layout antigo) | layout v1.2.1 atual: P-04=:90, P-06=:94, P-07=:96, P-08=:98 | resolução já declarada na fonte | spec-006:56 | este arquivo cita o layout v1.2.1 verificado |
| 6 | Estado do arquivo: MANIFEST:100 registra 0 B | arquivo inexistente no disco (verificação 2026-11-03) | observação direta | `UNKNOWN - verify` — divergência de inventário a consolidar pelo custodiante do MANIFEST |

## 4. Catálogo RF — REQ-01..REQ-15 (linha de base TAP §3/§5)

Fontes: spec-002:53-79 (tabela A.2, estado e MoSCoW) + plano-integral:67-87 (Tabela 3,
baseline textual) + conferência tap.md:102-116. Distribuição por entrega: spec-002:56.
MoSCoW: Must = REQ-01..09, 11, 15; Should = REQ-10, 12, 13, 14 (plano-integral:310; spec-002:57).
Estado de inventário único declarado: `canonical-mirror` — "todos rastreáveis a TAP §3 + fase
EAP" (spec-002:58). Trata-se de token de INVENTÁRIO da fonte, não de aprovação: nenhum
requisito é promovido a aprovado aqui (hf-exec-0621:35).

| ID | Requisito (transcrito) | Critério de aceite (transcrito) | Fase EAP | MoSCoW | Rastreabilidade |
|---|---|---|---|---|---|
| REQ-01 | Simulação de conversão cambial em tempo real (USD/EUR → BRL) | Cotação obtida via API externa com latência ≤ 2s | N5.2 | Must | spec-002:62; plano-integral:71; tap.md:102 |
| REQ-02 | Suporte a 5 regimes de contratação (hora, dia, semana, mês, valor fixo) | 100% dos regimes operacionais em UAT | N5.1 | Must | spec-002:63; plano-integral:72; tap.md:103 |
| REQ-03 | Aplicação de encargos financeiros simulados (spread + IOF) | Cálculo auditável com precisão de 2 casas decimais | N5.1 | Must | spec-002:64; plano-integral:73; tap.md:104 |
| REQ-04 | Emissão de invoice em formato PDF | Geração via WeasyPrint em ≤ 3s por documento | N5.4 | Must | spec-002:65; plano-integral:74; tap.md:105 |
| REQ-05 | Tempo de resposta da aplicação | ≤ 3s em 95% das requisições (ambiente homologação) | N5.1 | Must | spec-002:66; plano-integral:75; tap.md:106 |
| REQ-06 | Interface web responsiva (FOSS) | Compatível com Chrome/Firefox/Edge (últimas 2 versões) | N5.3 | Must | spec-002:67; plano-integral:76; tap.md:107 |
| REQ-07 | Cache de cotações (PostgreSQL 15+)¹ | Redução de ≥ 50% das chamadas à API externa | N5.2 | Must | spec-002:68; plano-integral:77; tap.md:108 |
| REQ-08 | Cobertura de testes automatizados | ≥ 80% do código (unitários + integração via pytest + coverage.py) | N6.1 | Must | spec-002:69; plano-integral:78; tap.md:109 |
| REQ-09 | Testes de aceitação (UAT) | 100% dos fluxos críticos passando, zero defeitos críticos/bloqueantes | N6.2 | Must | spec-002:70; plano-integral:79; tap.md:110 |
| REQ-10 | Aplicação de ferramentas da qualidade (PDCA + Ishikawa 6M) | 12 PDCAs consolidados + diagrama de causa e efeito documentado | N6.3 | Should | spec-002:71; plano-integral:80; tap.md:111 |
| REQ-11 | Pipeline CI funcional | Lint + testes rodando em ≤ 5 min por push | N7.1 | Must | spec-002:72; plano-integral:81; tap.md:112 |
| REQ-12 | ADRs para decisões arquiteturais críticas | Mínimo 3 ADRs registrados (stack, Kanban, métricas) | N9.1 | Should | spec-002:73; plano-integral:82; tap.md:113 |
| REQ-13 | Rastreabilidade de prompts SDD | 100% dos prompts catalogados em .ai/handoffs/ | N9.3 | Should | spec-002:74; plano-integral:83; tap.md:114 |
| REQ-14 | Documentação técnica consolidada | Arquitetura + APIs (OpenAPI) revisadas e aprovadas | N11.1 | Should | spec-002:75; plano-integral:84; tap.md:115 |
| REQ-15 | Licenciamento 100% FOSS | Todas as dependências com licenças OSI-approved | N1.5+N4.4 | Must | spec-002:76; plano-integral:85; tap.md:116 |

¹ Rótulo de persistência "PostgreSQL 15+" é a leitura operacional vigente (emenda REQ-07 no Delta Log, 2026-11-01; ADR-010 / ADR-001 v1.1.0). A baseline congelada "SQLite" permanece como histórico; o critério numérico (≥50%) não é afetado.

Notas da fonte (transcritas):

- "RNF canonicos estao EMBUTIDOS como criterios de aceite de REQ-05 (performance), REQ-08
  (qualidade), REQ-11 (CI), REQ-15 (FOSS) — nao existe registro NFR separado (ver GAP-02)"
  (spec-002:78-79). O registro NFR separado passou a existir em spec-006 (§6 abaixo), que
  fecha o GAP-02 (spec-006:32-35,138).
- Gaps abertos que condicionam requisitos: GAP-02 (NFR consolidado — FECHADO por spec-006),
  GAP-03 (fórmula spread/IOF — §3 nº 4), GAP-05 (API de cotação não nomeada — decisão de
  stack, spec-002:104), GAP-06 (TTL/invalidação de cache — legado apenas, spec-002:105),
  GAP-07 (conversão REQ→US até M2 não executada — spec-002:106), GAP-08 (sem critério LGPD de
  produto — requer decisão CCB/PO, spec-002:107).

## 5. Matriz REQ↔US (fonte: spec-002 §C)

As stories são CANDIDATAS de backlog: "Nao constituem compromisso de escopo, ordem de
execdoc-arch-0006-uc-v1ao ou entregaveis garantidos. O Humano (GP/PO) decide via CCB" (spec-002:149-152,
Art. 5.1). Cobertura REQ→US declarada: 15/15 (spec-002:152). Estado/condição transcritos da
fonte; nada promovido.

| REQ | US (id/slug) | Origem declarada | Estado/condição (transcrito) | spec-002 |
|---|---|---|---|---|
| REQ-01, REQ-05 | doc-user-story-0001-us-001 realtime-currency-simulation | REQ-01, REQ-05 (req_1.0.md:11,15) | candidate | :158 |
| REQ-02 | doc-user-story-0002-us-002 five-engagement-regimes | REQ-02 | candidate | :159 |
| REQ-03 | doc-user-story-0003-us-003 spread-iof-net-calculation | REQ-03 | candidate; fórmula pendente CCB (GAP-03/C-05) | :160 |
| REQ-04 | doc-user-story-0004-us-004 invoice-pdf-generation | REQ-04 | candidate; modelo de dados pendente (GAP-04) | :161 |
| REQ-06 | doc-user-story-0005-us-005 responsive-foss-web-ui | REQ-06 | candidate | :162 |
| REQ-07 | doc-user-story-0006-us-006 sqlite-quote-cache | REQ-07 | candidate; TTL pendente (GAP-06) | :163 |
| REQ-08 | doc-user-story-0008-us-008 test-coverage-gate | REQ-08; P-06 | candidate | :164 |
| REQ-09 | doc-user-story-0009-us-009 uat-critical-flows | REQ-09 | candidate | :165 |
| REQ-10 | doc-user-story-0010-us-010 quality-tools-pdca-ishikawa | REQ-10 | candidate | :166 |
| REQ-11 | doc-user-story-0011-us-011 ci-pipeline | REQ-11 | candidate | :167 |
| REQ-12 | doc-user-story-0012-us-012 adr-records | REQ-12; P-05 | **BLOCKED** — "re-emissao ADR-001..006 pendente CCB (AUD-2610-03.md:85,240)" | :168 |
| REQ-13 | doc-user-story-0013-us-013 sdd-prompt-traceability | REQ-13 | candidate | :169 |
| REQ-14 | doc-user-story-0014-us-014 tech-docs-openapi | REQ-14 | candidate | :170 |
| REQ-15 | doc-user-story-0015-us-015 foss-license-compliance | REQ-15; P-01 | candidate | :171 |
| (corrobora REQ-07) | doc-user-story-0007-us-007 api-failure-fallback | LEGADO review_rf_rfn.md:31 (RF-05) | condicional — KG-R-02: PO/CCB ratifica antes de Ready | :177 |
| (sem REQ canônico) | doc-user-story-0016-us-016 invoice-lifecycle-draft-finalize | LEGADO review_rf_rfn.md:34 (RF-08) | condicional — KG-R-03: CCB decide | :178 |
| (depende de doc-user-story-0016-us-016) | doc-user-story-0017-us-017 invoice-clone-new-number | LEGADO review_rf_rfn.md:35 (RF-09) | condicional — depende de doc-user-story-0016-us-016 ratificada; KG-R-03 | :179 |

Notas transcritas: doc-user-story-0012-us-012 permanece BLOCKED (gate E) conforme a fonte (spec-002:168,181);
warmup do WeasyPrint (deepseek:70) entra como critério opcional de doc-user-story-0004-us-004, marcado
legacy-input, se CCB ratificar (spec-002:181-182); regra RN-03 legada sobrevive como insumo
de doc-user-story-0002-us-002/doc-user-story-0003-us-003 apenas na cláusula "sem calendário corporativo" (spec-002:182-184). KGs
declarados: KG-R-02 e KG-R-03 (spec-002:246-248); KG-R-04 (parâmetros de cache/warmup —
legado apenas, spec-002:249).

## 6. Catálogo RNF — cross-ref a spec-006 (NF-01..NF-25)

Fonte canônica NFR: `.ai/specs/spec-nfr-0001-nfr-consolidados-v1.0.md` (registro da fase N2.2
da EAP; GAP-02 fechado — spec-006:32-35,138). Este arquivo NÃO duplica métricas nem
descrições: a linha viva de cada NFR está na fonte indicada.

| ID | Categoria (spec-006 §3) | Vínculo REQ/princípio declarado | Fonte (spec-006:linha) |
|---|---|---|---|
| NF-01 | Desempenho | REQ-01 (N5.2); C-07 | :71 |
| NF-02 | Desempenho | REQ-05 (N5.1); C-07 | :72 |
| NF-03 | Desempenho | REQ-04 (N5.4) | :73 |
| NF-04 | Desempenho | REQ-07 (N5.2); rótulo SQLite superado (§2 da fonte) | :74 |
| NF-05 | Usabilidade | REQ-06 (doc-user-story-0005-us-005) | :80 |
| NF-06 | Usabilidade | fase N3.2 / marco M2 | :81 |
| NF-07 | Segurança (P-07/OWASP) | P-07; fail-closed startup/db | :87 |
| NF-08 | Segurança | P-07; Art. 7.2; scanner CI | :88 |
| NF-09 | Segurança | Art. 7.1/7.4; Art. 10.3; P-02 (métrica: `UNKNOWN - verify`) | :89 |
| NF-10 | Segurança | doc-user-story-0020-us-020; P-07; Art. 10.2 — hardening de containers | :90 |
| NF-11 | Portabilidade e FOSS | REQ-15 (N1.5+N4.4); P-01 | :96 |
| NF-12 | Portabilidade e FOSS | P-01; FOSS-ZERO-COST | :97 |
| NF-13 | Portabilidade e FOSS | P-02; soberania local (métrica: `UNKNOWN - verify`) | :98 |
| NF-14 | Portabilidade e FOSS | P-02; OS-06/OS-08 OUT | :99 |
| NF-15 | LGPD | P-04; GAP-08 (métrica: `UNKNOWN - verify`) | :105 |
| NF-16 | LGPD | Art. 7.3; Art. 10.3; sem PII em logs/volumes | :106 |
| NF-17 | LGPD | P-03; Art. 7.4; export externo sem PII | :107 |
| NF-18 | Manutenibilidade | REQ-08 (N6.1); P-06; Art. 10.4 | :118 |
| NF-19 | Manutenibilidade | REQ-11 (N7.1); delta G-05 declarado | :119 |
| NF-20 | Manutenibilidade | REQ-14 (N11.1); Art. 6.4 | :120 |
| NF-21 | Manutenibilidade | REQ-12 (N9.1); P-05 — **BLOCKED** pelo gate E conforme a fonte | :121 |
| NF-22 | Manutenibilidade | Art. 6.3; dívida técnica | :122 |
| NF-23 | Observabilidade | healthcheck /v1/health; OS-08 rejeitado | :128 |
| NF-24 | Observabilidade | GMV — evidências nativas | :129 |
| NF-25 | Observabilidade | REQ-03 (N5.1); trilha auditável; ADR-016 pendente | :130 |

Fronteira LGPD transcrita: "o mapeamento desta seção registra os critérios constitdoc-arch-0006-uc-v1ionais; a
especificação executiva de LGPD de produto… é o item B.3 (LISTA…:35), condicionada a decisão
prévia de CCB/PO (GAP-08…)" (spec-006:109-112).

## 7. Emendas E-01..E-08 (Rodada 1) e impacto em requisitos

Ratificação: "1.1.0 — 2026-10-26: CCB ratifica as emendas E-01..E-08 da Rodada 1"
(constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226); co-assinatura v1.1.0 — instrumento "CCB 26/10/2026, emendas E-01..E-08"
(constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:245). Texto-fonte das emendas: spec-001:193-334. Impacto em requisitos
registrado SOMENTE onde a fonte o declara; onde não há declaração, marca-se `UNKNOWN - verify`.

| Emenda | Tema (transcrito do título) | Artigo alvo | Impacto em requisitos (declarado na fonte) |
|---|---|---|---|
| E-01 | Correção do slug do orquestrador | Art. 4.5 | `UNKNOWN - verify` — nenhum impacto em requisitos declarado nas fontes consultadas (spec-001:193; spec-002:218-219 omite E-01) |
| E-02 | Mecanismo de fechamento da co-assinatura — ratificador humano identificado "por papel… (sem nome civil — minimização LGPD, Art. 7.3)" (spec-001:214-216) | Art. 5.4 | Declarado: impacta requisitos de dados/LGPD (hf-exec-0621:27-28) — minimização LGPD em registros de governança; eco constitdoc-arch-0006-uc-v1ional P-04 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90); domínio afetado: NF-15/NF-16 (spec-006:105-106) |
| E-03 | Containers Docker e ortogonalidade de camadas — "segredo e PII nunca entram em camada de imagem (Arts. 7.2, 7.3)" (spec-001:238-239) | Art. 10 (10.2) | Declarado: impacta requisitos de dados/LGPD (hf-exec-0621:27-28); texto ratificado: constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215; herança: NF-10 (spec-006:90) |
| E-04 | Codificação de YAGNI e primeiros princípios (P-11, P-12) | Art. 3 | Declarado como "critica[s] para requisitos" (spec-002:218-219) |
| E-05 | Fluxo de mudança (CR → ADR → CCB → Emenda) | Art. 9.3 | Declarado como crítica para requisitos (spec-002:218-219) |
| E-06 | Precisão do gate de forja (Art. 4.7) | Art. 4.7 | `UNKNOWN - verify` — nenhum impacto em requisitos declarado nas fontes consultadas |
| E-07 | Re-ancoragem transitória do freeze (Art. 1.3) | Art. 1.3 | Declarado como crítica para requisitos (spec-002:218) |
| E-08 | WIP por pessoa (micro-emenda) | Art. 6.2 | Declarado como crítica para requisitos (spec-002:218-219); C-06 — leitura de WIP condicionada à ratificação de E-08 (spec-002:125,205-206) |

## 8. Rastreabilidade (deste artefato)

Legenda de caminhos: `spec-002` = `.ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md`;
`spec-001` = `.ai/specs/spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md`; `spec-006` =
`.ai/specs/spec-nfr-0001-nfr-consolidados-v1.0.md`; `tap.md` = `.ai/specs/tap.md`;
`plano-integral` = `docs/planos/plano-granular/plano-integral-tap-1-2-3-4-5.md`;
`LISTA` = `docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md`; `MANIFEST` = `.ai/specs/doc-manifest-0001-manifest-v1.0.md`;
`KB-INDEX` = `docs/conhecimento/KB-INDEX.md`; `hf-exec-0621` = `.ai/handoffs/hf-exec-0621-requisitos-repovoar-v1.0.md`.

| Seção deste arquivo | Fonte (arquivo:linha) |
|---|---|
| Frontmatter/ID | KB-INDEX:53 (REQ-SPEC-001, draft, 1.0.0, agent-sdd-specialist); MANIFEST:170 (custódia .ai/specs/); KB-INDEX:54 (docs/requisitos ponteiro) |
| §1 Regime | hf-exec-0621:22,35-37; MANIFEST:58,100,170; ADR-011:56 (via MANIFEST §5.2); constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78; KB-INDEX:53-54; tap.md:31,34 |
| §2 Contexto | hf-exec-0621:11,16-22; LISTA:25; spec-002:100,208-224; spec-001:132-141; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226,245 |
| §3 Conflitos | spec-002:62-76,102,104-107,126,243-245; plano-integral:71-77,310; tap.md:47,102-116,120; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213; spec-006:53-56,74 |
| §4 Catálogo RF | spec-002:53-79,100-107; plano-integral:67-87,310; tap.md:96-121; spec-006:32-35 |
| §5 Matriz REQ↔US | spec-002:149-184,246-249 |
| §6 Catálogo RNF | spec-006:26,61-130,138,147-155,173 |
| §7 Emendas | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226,245,90,215; spec-001:193-334 (E-02 :209-227; E-03 :228-252); hf-exec-0621:27-28; spec-002:125,205-206,218-219; spec-006:90,105-106 |
| Regra de ouro | hf-exec-0621:22 (transcrição rastreável; P-08); constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98 (P-08); MANIFEST:58 |

## 9. Critérios de aceite e testes (deste artefato)

- [ ] AC-01: arquivo não vazio no caminho pinned `.ai/specs/requisitos.md`, sem rename
      (MANIFEST:100, §5.1; LISTA:25; hf-exec-0621:25).
- [ ] AC-02: REQ-01..REQ-15 transcritos com rastreabilidade dupla (spec-002:62-76 +
      plano-integral:71-85, com conferência tap.md:102-116); ZERO requisito, valor ou métrica
      novo — tudo citado (P-08; hf-exec-0621:22,31).
- [ ] AC-03: RNF por cross-ref a spec-006 (NF-01..NF-25), sem duplicar métricas (§6).
- [ ] AC-04: matriz REQ↔US reflete spec-002 §C com cobertura 15/15 e condicionais
      KG-R-02/KG-R-03 marcadas (§5).
- [ ] AC-05: emendas E-01..E-08 com ratificação citada (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226,245) e impacto em
      requisitos apenas onde declarado; lacunas com `UNKNOWN - verify` (§7).
- [ ] AC-06: nenhum requisito/story promovido a aprovado — estados transcritos conforme a
      fonte (hf-exec-0621:35); `canonical-mirror` identificado como estado de inventário.
- [ ] AC-07: arquivo ≤400 linhas (contrato DO #3, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:86).
- [ ] AC-08: nenhum outro arquivo editado nesta task — docs/requisitos/requisitos.md,
      spec-002, spec-006, spec-001, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md, plano-integral e tap.md intocados;
      nada commitado (hf-exec-0621:34,37).
- Validação: agent-reviewer audita as citações linha-a-linha (padrão spec-002:251-252);
  agent-gatekeeper verifica gates. DoD desta task: parcela JSON
  `{"task_id":"TA-0065", "status":"accepted", "parcel":{...}, "kill_switch":"inherited"}`
  com dod/artifacts/notes (hf-exec-0621:38).

## 10. Fora de escopo (YAGNI)

- Criar, alterar, aprovar ou priorizar requisitos — locus exclusivo de CCB/PO (Art. 5.1;
  spec-002:149-152); P-08 veta invenção (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98).
- Editar o ponteiro `docs/requisitos/requisitos.md` (KB-INDEX:54; hf-exec-0621:37) ou qualquer
  fonte citada (spec-002, spec-006, spec-001, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md, plano-integral, tap.md).
- Especificação executiva de domínio (modelo de dados da invoice, frontend, UAT, CI/CD, LGPD
  de produto) — specs próprias já previstas (spec-007..spec-015; spec-006:109-112,166-167);
  este arquivo é catálogo de RF/RNF, não spec executiva.
- Conversão REQ→User Story executiva (fase N2.3 — GAP-07; plano-integral:306) — backlog do PO.
- Promover condicionais (doc-user-story-0007-us-007/016/017, KG-R-02/03) ou resolver gaps abertos (GAP-03/05/06/07/08)
  — decisão CCB/PO (spec-002:102-107; spec-002:246-249).
- Novas métricas NFR sem fonte citável — vedado (spec-006:168).
- Tratar decisões D1-D7 da consulta TA-0050 como requisitos aprovados — são condicionantes
  (hf-exec-0621:36).

## CHANGELOG

- **1.0.0 — 2026-11-03 — TA-0065 / hf-exec-0621** (sender: agent-nexus-prime-ultimate):
  repovoamento do arquivo pinned (item A.1, LISTA:25; inexistente no disco, cf. MANIFEST:100).
  Catálogo RF: REQ-01..REQ-15 transcritos (fonte primária spec-002:53-79; baseline textual
  plano-integral:67-87; conferência tap.md:96-121 — sem divergência material; KG-R-01 segue
  pendente na fonte). Matriz REQ↔US: 17 stories (15 mapeadas + doc-user-story-0007-us-007/016/017 condicionais,
  KG-R-02/03). RNF: NF-01..NF-25 por cross-ref a spec-006 (fonte canônica; GAP-02 fechado).
  Emendas E-01..E-08 ratificadas (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:226,245) com impacto em requisitos somente
  onde declarado (E-02, E-03, E-04, E-05, E-07, E-08); E-01/E-06 sem impacto declarado =
  `UNKNOWN - verify`. Divergências registradas: 6 (§3). Nenhum status promovido; nenhum outro
  arquivo editado; nada commitado.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

Adaptado a arquivo pinned (sem `spec_id spec-NNN`; MANIFEST §5.1 — requisitos.md sem rename;
padrão tap.md §20):

| Camada | Seção neste artefato | Estado |
|---|---|---|
| (a) Cabeçalho (frontmatter) | frontmatter YAML (id REQ-SPEC-001; custody; task/sender; kill_switch; trace; lgpd-class) | ✅ |
| (b) Contexto/origem | §2 Contexto e origem | ✅ |
| (c) Resolução de conflitos | §3 Resolução de conflitos (6 divergências; `UNKNOWN - verify` onde aplicável) | ✅ |
| (d) Corpo de decisões/requisitos/contratos | §4 Catálogo RF; §5 Matriz REQ↔US; §6 RNF (cross-ref); §7 Emendas | ✅ (transcrição; lacunas declaradas) |
| (e) Critérios de aceite e testes | §9 Critérios de aceite e testes (AC-01..AC-08 + validação/DoD) | ✅ |
| (f) Rastreabilidade | §8 Rastreabilidade + rastreabilidade por linha nas tabelas | ✅ |
| (g) Fora de escopo (YAGNI) | §10 Fora de escopo (YAGNI) | ✅ |
| (h) Changelog | CHANGELOG (1.0.0) | ✅ |
