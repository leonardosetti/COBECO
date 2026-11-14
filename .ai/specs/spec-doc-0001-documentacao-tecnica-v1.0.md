---
id: ai-specs-spec-013-documentacao-tecnica-v1-spec
title: 'SPEC spec-013 — documentacao-tecnica-v1 — Documentação técnica: doc de arquitetura + revisão/aprovação da OpenAPI
  (REQ-14)'
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-doc-0001-documentacao-tecnica-v1.0.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-013
specname: documentacao-tecnica-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: HF-0614 (TA-0058) | sender: agent-nexus-prime-ultimate | handoff: HF-0614 | consulta de domínio incorporada (agent-iso-26514-specialist, autorizada em HF-0614:21)
task: TA-0058 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-7 | Onda 7 — Commons e Meta (documentação técnica)
lgpd-class: n/a (zero PII neste artefato; P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90 — precedente lgpd-class: spec-002-requisitos-review-round-1.spec.md:19)
trace:
  - .ai/handoffs/HF-0614-spec-013-documentacao-tecnica-v1.md:17-29 (tarefa, fontes obrigatórias, contrato de resposta meio-duplex)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:41 (B.9 — origem desta emissão), :62 (D.4 — onda 7), :68 (E.2 — ADR-016 proposta), :71 (E.5 — REQ-12)
  - .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:75 (REQ-14), :170 (US-014)
  - .ai/specs/spec-tech-0001-backend-mvp-v1.0.md:14 (H1 REQ-14), :58-93 (§3 contrato /v1), :230 (§11), :239 (§12 REQ-14 `UNKNOWN - verify`)
  - tests/integration/test_openapi.py:1-107 (10 testes `*_req14` — lidos integralmente em 2026-11-03)
  - docs/planos/plano-granular/plano-integral-tap-1-2-3-4-5.md:46 (N11.1/N11.2), :84 (REQ-14/N11.1), :599 (PDCA-N11)
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md v1.2.1:90 (P-04), :94 (P-06), :98 (P-08), :150 (Art. 6.1), :152 (Art. 6.2), :156 (Art. 6.4), :213 (Art. 10.1), :219 (Art. 10.4)
  - .ai/specs/spec-arch-0001-container-layers-v1.0.md:56-69 (§3.1 camadas), :87-92 (§4.1), :98-109 (§4.2), :111 (cadeia), :221 (OpenAPI FastAPI), :226 (compat /v1)
  - docs/conhecimento/Canon_Stack_SDD.md:27,41 (canon ratificado v2.0.0), :280-283 (docs/ = humanos; regra de ouro), :331-347 (ciclo SDD com review)
  - .ai/specs/doc-manifest-0001-manifest-v1.0.md:20-61 (template canônico obrigatório §1)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:42 (kill switch 3), :85-86 (DO #2/#3), :108 (DON'T #7)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-iso-26514-specialist.md:20-24,58,62,66-72,100,115-126,141,145-146,183-186 (consulta de domínio ISO/IEC 26514:2022)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-docker-specialist.md:6,22,209 (custódia documental; documented truth = running truth; never hand-restyled)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-reviewer.md:21,23,33,69 (vereditos pass|amend|block; rubrica R-01..R-07; risco docs=low)
  - docs/decisoes/ADR-016-backend-mvp.md:5 (status: proposta — não ratificada)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012)
---

# SPEC spec-013 — documentacao-tecnica-v1 — Documentação técnica: doc de arquitetura + revisão/aprovação da OpenAPI (REQ-14)

Status: SPEC EMITIDA — PENDENTE DE REVISÃO E DE IMPLEMENTAÇÃO (onda seguinte, Art. 6.1 SDD) | Tarefa: TA-0058 (handoff `.ai/handoffs/HF-0614-spec-013-documentacao-tecnica-v1.md`) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única das decisões de documentação técnica do COBECO. Em conflito, vale a hierarquia do Art. 2 da Constituição (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:41-50; resolução de cima para baixo, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).

Convenções: citação `arquivo:linha`; alegação sem fonte = literal `UNKNOWN - verify` (P-08, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98; MANIFEST.md:58). Identificadores/status/caminhos em EN; narrativa em PT-BR (P-10). Esta SPEC não implementa código nem escreve o doc de arquitetura (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150 — especifica → implementa → valida → registra).

## 1. Contexto e origem

Esta spec nasce da tarefa TA-0058, via handoff HF-0614 emitido por agent-nexus-prime-ultimate
(.ai/handoffs/HF-0614-spec-013-documentacao-tecnica-v1.md:17-21), e implementa o item **B.9** da
LISTA-SPECS-PENDENTES-2026-11-02.md:41, no quadro da onda 7 "Commons e Meta" (D.4, LISTA...:62).

REQ-14 — "Documentação técnica consolidada | Arquitetura + APIs (OpenAPI) revisadas e aprovadas |
TAP §3 (Produto) + N11.1" (plano-integral-tap-1-2-3-4-5.md:84; espelho spec-002-requisitos-review-round-1.spec.md:75)
— pertence à fase **N11.1 "Documentação Técnica (Arquitetura, APIs)"** (plano-integral...:46, MF3).
US-014 `tech-docs-openapi` fixa o critério: "arquitetura e especificação OpenAPI estão aprovadas em
Code Review" (spec-002...:170). A spec-004 declara REQ-14 no H1 (spec-004-backend-mvp-v1.spec.md:14),
mas a linha de rastreabilidade :239 registra a seção dedicada como `UNKNOWN - verify` — lacuna que
esta emissão endereça pelo lado do DOC e do PROCESSO de revisão, sem tocar na spec-004 (intocável
aqui: normalização TA-0031, .ai/specs/doc-manifest-0001-manifest-v1.0.md:97).

Estado verificado no filesystem (2026-11-03): **não existe** `docs/arquitetura/` no repositório
(`ls docs/`: analise, archive, auditorias, change-requests, compliance, conhecimento, decisoes,
dependencias, diagramas, especificacoes, evidencias, governanca, metricas, operacao, planos,
requisitos, slides_apresentacao, stakeholder, tap, troubleshooting.md, verification — nenhum
subdiretório de arquitetura; `docs/diagramas/` tem 9 subdiretórios sem "arquitetura" e um
`mermaid-config.json`). O destino do doc de arquitetura é, portanto, `UNKNOWN - verify` (§3.5).
A OpenAPI, em contraste, já está implementada e blindada: `tests/integration/test_openapi.py`
(107 linhas, 10 testes sufixados `*_req14`) verifica o documento servido pela aplicação.

Consulta de domínio incorporada (meio-duplex, autorizada em HF-0614:17,21): o contrato do
especialista ISO/IEC/IEEE 26514:2022 (.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-iso-26514-specialist.md) foi lido como
insumo normativo e está citado em cada regra que dele deriva (§3). Nenhum número de cláusula ISO é
afirmado aqui sem verificação — lacuna marcada `UNKNOWN - verify` (P-08; DON'T 7 do especialista
ISO, agent-iso-26514-specialist.md:100).

## 2. Resolução de conflitos

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| OpenAPI já coberta por spec-004 §3 | **Delimitação exata:** o CONTEÚDO do contrato `/v1` (rotas, schemas, erros) permanece normativo exclusivamente em spec-004-backend-mvp-v1.spec.md:58-93, verificado por tests/integration/test_openapi.py:1-107. Esta spec NÃO redeclara rota, schema, enum ou erro — cobre apenas (i) o doc de arquitetura, inexistente; (ii) o processo e os critérios de revisão/aprovação da OpenAPI em Code Review (US-014, spec-002...:170); (iii) a regra anti-restyle (§3.4) | spec-004-backend-mvp-v1.spec.md:58-93 + test_openapi.py:16,51-53 | Qualquer re-declaração de contrato `/v1` nesta spec (nunca feita; se surgir, é defeito desta spec) |
| REQ-14 sem seção dedicada na spec-004 (`UNKNOWN - verify`, spec-004:239) | A seção dedicada de REQ-14 para o lado DOCUMENTAÇÃO passa a ser esta SPEC (§3); a spec-004 permanece intocada — REQ-14 nela segue válido apenas pelo H1 (:14) e pela §3 (contrato) | HF-0614:17,24 + LISTA...:41 | Corrigir/editar spec-004-backend-mvp-v1.spec.md:239 nesta emissão (vedado — decisão TA-0031, MANIFEST.md:97) |
| Quem escreve e quem aprova | Escrita do doc de arquitetura = custódia documental **agent-docker-specialist** ("documentation custody. Owns doc-readme-0001-readme-canon + docs/ tree", agent-docker-specialist.md:6; "the sole documentation custodian", agent-iso-26514-specialist.md:24); revisão/aprovação = **agent-reviewer** em Code Review (vereditos pass\|amend\|block, agent-reviewer.md:21; portão Art. 6.2/6.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:152,156); QA documental = **agent-iso-26514-specialist** (parcela de conformidade, agent-iso-26514-specialist.md:66-67). O SDD custodian especifica e custodia esta spec, não escreve o doc | agent-docker-specialist.md:6,22 + agent-reviewer.md:21 + constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:152,156 | Qualquer leitura de que o SDD custodian é redator técnico do produto (ele não é — DON'T de fronteira, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:24) |
| ADR-016 como decisão de arquitetura no doc | O doc de arquitetura cita **apenas decisões ratificadas** como norma (ADR-001 v1.1.0, ADR-010 histórica, Constituição); ADR-016 está `status: proposta` (docs/decisoes/ADR-016-backend-mvp.md:5 — "não está ratificada... posição técnica proposta, não norma vigente") e deve ser citada somente com esse estado, jamais como decisão vigente | ADR-016-backend-mvp.md:5,13 + E.2 (LISTA...:68) | Citar ADR-016 como norma ratificada (P-08 — status inventado) |
| Arquitetura do PRODUTO × arquitetura do ecossistema SDD | REQ-14 exige o doc de arquitetura do PRODUTO COBECO (simulador cambial). A arquitetura do ecossistema SDD (L1/L2/L3, stack local) já tem canon ratificado v2.0.0: docs/conhecimento/Canon_Stack_SDD.md:27,41,64 — este canon NÃO é substituído nem duplicado | Canon_Stack_SDD.md:27,41 | Reescrever o canon SDD num eventual doc de arquitetura de produto (duplicação de SSOT — P-03, Canon_Stack_SDD.md:79) |
| Destino do doc no repositório | **Registro, não decisão:** `docs/arquitetura/` não existe (verificado 2026-11-03, §1). O destino é ato da custódia documental + arquiteto na implementação; candidatos registrados SEM decisão: `docs/arquitetura/` (novo), `docs/especificacoes/` (existe, 1 arquivo), `docs/conhecimento/`. `docs/` é o território de documentação humana (Canon_Stack_SDD.md:280,283 — regra de ouro de `.ai/`) | Estado verificado (P-08) + Canon_Stack_SDD.md:283 | Inventar caminho definitivo sem decisão da custódia (P-08) |

## 3. Domínio — documentação técnica (REQ-14, US-014)

### 3.1 Escopo do doc de arquitetura (visão de camadas, Art. 10.1)

Conteúdo mínimo obrigatório do doc de arquitetura de produto (cada item com rastreabilidade interna
ao doc; o doc cita fontes por `arquivo:linha`, nunca parafraseia sem fonte):

1. **Visão de camadas do Art. 10.1** — as camadas de execução ortogonais (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213):
   Dados/Back/Front + aderentes `migrate`/`proxy`, com fronteiras declaradas por camada
   (spec-005-container-layers-v1.spec.md:56-69) e a cadeia integrada
   usuário → `proxy` (`127.0.0.1:8080`) → `front` → `back` → `db` (+ `migrate` → `db` no boot),
   com healthchecks em cadeia (spec-005...:111).
2. **Matriz de interfaces declaradas** — quem-fala-com-quem, somente por porta/volume/API
   (spec-005...:98-109; redes `data` internal × `edge`, spec-005...:87-92) e o contrato de
   interoperabilidade (spec-005...:221-226).
3. **Diagramas Mermaid (FOSS)** — ferramenta de diagrama FOSS only: "Mermaid, Markdown; no
   proprietary suites" (agent-iso-26514-specialist.md:58); `docs/diagramas/mermaid-config.json`
   já existe no repo como base de render. Suites proprietárias de documentação vetadas
   (agent-iso-26514-specialist.md:98, DON'T 5).
4. **ADRs como decisões ratificadas** — cada decisão de stack citada pela ADR de origem
   (caminho + versão), nunca reescrita dentro do doc; ADR-016 citada apenas como `proposta`
   (ADR-016-backend-mvp.md:5; §2). O doc não é camada de decisão — ADRs novas são REQ-12/E.5
   (LISTA...:71), fora daqui.
5. **Referência ao contrato `/v1` por ponteiro** — o doc referencia spec-004 §3 e o render
   OpenAPI por caminho/seção (spec-004-backend-mvp-v1.spec.md:58-93; `/docs` Swagger UI,
   test_openapi.py:102-107), sem copiar tabelas de rotas (evita drift — §3.3).

### 3.2 Ciclo de vida da documentação (draft → revisão Code Review → aprovado)

Estado canônico do doc de arquitetura e da referência OpenAPI, em três estágios binários:

| Estágio | Regra | Evidência exigida |
|---|---|---|
| `draft` | Doc escrito pela custódia documental (agent-docker-specialist.md:6,22) com rastreabilidade por item (§3.1); frontmatter do doc com `status: draft` | Doc versionado no git; nenhuma alegação sem fonte (P-08) |
| `in_review` | Code Review obrigatória pelo **agent-reviewer**: veredito estruturado `pass\|amend\|block` citando rubrica R-01..R-07 e linhas do diff — "LGTM is not a verdict" (agent-reviewer.md:16,21); classificação de risco: docs/cosmetics = `low` (agent-reviewer.md:69); loop de amend ≤2 iterações (agent-reviewer.md:23, duty 6); veredito é evidência imutável no ledger (agent-reviewer.md:33) | Verdict packet no ledger citando diff + rubrica |
| `approved` | Aprovado somente após veredito `pass` do reviewer; portão reviewer → gatekeeper compulsório para merge (P-06, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94; Art. 10.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219); frontmatter do doc passa a `status: approved` com referência ao veredito | Merge com rastreabilidade (Art. 6.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:152; Canon_Stack_SDD.md:361-363) |

QA documental adicional (especialista ISO/IEC 26514 — agent-iso-26514-specialist.md:66-67): mapear
o doc à cláusula ISO; verificar completude + acurácia + rastreabilidade; screen LGPD (zero PII —
agent-iso-26514-specialist.md:81, DON'T 8); emitir parcela de conformidade
(`conforme|brecha|gap|pending_human`, agent-iso-26514-specialist.md:125). Metas de serviço herdadas
do contrato ISO: `doc_review_latency` ≤48h e `documentation_freshness` ≤1 ciclo de release
(agent-iso-26514-specialist.md:145-146) — adotadas aqui como alvos de processo, não como critério
binário de aceite do MVP (base normativa, não inventada como AC).

### 3.3 Relação doc↔código (documented truth = running truth)

Princípio normativo, com três âncoras citadas:

1. **Art. 6.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:156):** "Documentação acompanha código: drift documental é defeito
   tratado." PDCA-N11 (plano-integral-tap-1-2-3-4-5.md:599) operacionaliza: "Código + docs no mesmo
   PR + revisão de consistência antes de M4"; métrica "100% dos requisitos mapeados a docs; zero
   inconsistências TAP → código"; prazo M4 (15/12/2026, plano-integral...:599).
2. **Custódia documental (agent-docker-specialist.md:6,209):** "Documented truth equals running
   truth; fabricated docs are a crime against the chain" e "O que esta documentado precisa rodar; o
   que roda precisa estar documentado". O doc-drift audit (agent-docker-specialist.md:64) é o
   mecanismo contínuo de verificação contra repo/ledger.
3. **Anti-fabricação (P-08, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98; kill switch 3 do SDD — "misleading traceability",
   .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:42; especialista ISO: "treat every doc claim as
   unverified until traced to source", agent-iso-26514-specialist.md:60):** doc fabricado (afirmar
   no doc comportamento sem fonte citável ou sem correspondência executável) = violação kill switch
   + P-08. Toda alegação do doc deriva de REQ + spec + código (proveniência, não memória —
   agent-iso-26514-specialist.md:62).

Consequência prática para a OpenAPI: o doc NÃO PODE descrever rota, status code, schema ou erro que
o documento OpenAPI gerado não declare — a verdade executável é o schema servido, blindado por
testes (`EXPECTED_PATHS` exato, test_openapi.py:16,51-53; sem 422, test_openapi.py:56-59).

### 3.4 OpenAPI: fonte única de verdade, render nunca hand-restyled, critérios de revisão

- **Fonte única de verdade:** o documento OpenAPI **gerado pela própria aplicação** — endpoint
  `/openapi.json` (fixture do TestClient, test_openapi.py:22-26), servido pelo FastAPI
  (corroboração: spec-005-container-layers-v1.spec.md:221). O contrato normativo do conteúdo é
  spec-004 §3 (spec-004-backend-mvp-v1.spec.md:58-93): 4 rotas `/v1` (:62-67), schemas em
  `src/shared/schemas.py` SSOT `extra="forbid"` (:69-75), modelo de erro canônico 400/404/503/500
  (:79-93), sem 422 (:87). Título e versão do documento: "COBECO API" / "1.0.0"
  (test_openapi.py:45-48).
- **Render nunca hand-restyled:** nenhuma página de referência de API escrita à mão ("hand-copied
  or 'improved' beyond the render") pode substituir ou re-estilizar o render; a custódia documental
  só anota o render (agent-docker-specialist.md:6,22 — "only annotations of the render - never
  restyling"). Justificativa derivada de spec-004 §3: o par schema + testes de contrato
  (test_openapi.py) é a rede anti-drift (spec-005...:226); restyle manual criaria uma segunda fonte
  de verdade sujeita a drift documental (Art. 6.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:156).
- **Critérios de revisão/aprovação da OpenAPI (binários, executados na revisão Code Review):**
  1. Suite `tests/integration/test_openapi.py` 100% verde (10 testes `*_req14` — título/versão
     :45-48, 4 rotas exatas :51-53, sem 422 :56-59, schemas FastAPI removidos :62-66,
     `ErrorResponse` compartilhado :69-76, chaves canônicas nas descrições :79-84, PDF +
     `pdf_unavailable` :87-93, health sem erros :96-99, `/docs` 200 :102-107).
  2. Igualdade schema ↔ spec-004 §3 (nenhuma divergência de rota/campo/erro; evidência: docstrings
     dos testes citam a §3, test_openapi.py:1,46,52,57).
  3. Zero PII em descrições/exemplos do schema (P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90; "details nunca ecoa o
     valor enviado", spec-004-backend-mvp-v1.spec.md:93).
  4. Veredito `pass` do agent-reviewer registrado no ledger (agent-reviewer.md:21,33) — sem
     veredito, REQ-14 não está atendida ("revisada/aprovada", spec-002...:75; US-014
     "aprovadas em Code Review", spec-002...:170).
- **Estado atual verificado (2026-11-03):** os 10 testes existem no repo; o delta desta spec é
  formalizar a revisão/aprovação (veredito) e o doc de arquitetura — **não** alterar testes
  (custódia QA; DON'T #7, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:108).

### 3.5 Integração REQ-14/US-014, mapa de rastreabilidade documental e destino

Linha de rastreabilidade documental (formato do especialista ISO, agent-iso-26514-specialist.md:115-126;
matriz REQ → spec → doc → test é duty 4, :22):

| Campo | Valor | Fonte |
|---|---|---|
| doc_id | `DOC-001` reservado para o doc de arquitetura de produto (atribuição formal na implementação) | agent-iso-26514-specialist.md:119 |
| doc_type | `design` (enum :120 — arquitetura é documentação de design; mapeamento final na emissão do doc) | agent-iso-26514-specialist.md:120 |
| iso_clause | **`UNKNOWN - verify`** — o especialista ISO estabelece a cláusula ISO/IEC/IEEE 26514:2022 do doc_type `design` com o texto da norma em mãos; inventar cláusula é proibido (DON'T 7, :100; anti-halldoc-arch-0006-uc-v1ination :70-72) | agent-iso-26514-specialist.md:100 |
| traceability | REQ-14 (spec-002...:75; plano-integral...:84) → spec-013 (esta) → doc de arquitetura (destino `UNKNOWN - verify`) → test_openapi.py (lado OpenAPI) | agent-iso-26514-specialist.md:123 |
| verdict | `conforme\|brecha\|gap\|pending_human` na parcela de QA documental (:125) | agent-iso-26514-specialist.md:125 |

**Destino do doc de arquitetura — estado real registrado (P-08):** `docs/arquitetura/` **não
existe** (verificação de 2026-11-03, §1/§2). Decisão de destino = `UNKNOWN - verify`, ato da
custódia documental + arquiteto na onda de implementação; candidatos registrados sem decisão em §2.
Vinculação REQ-14↔US-014: o critério de aceite da US-014 ("arquitetura e especificação OpenAPI
estão aprovadas em Code Review", spec-002...:170) é atendido quando (i) o doc de arquitetura existir
com o conteúdo mínimo de §3.1 e estiver `approved` (§3.2) e (ii) os critérios §3.4 estiverem todos
verdes com veredito registrado.

## 4. Critérios de aceite e testes

Critérios verificáveis desta emissão (checkbox, DO #2 — .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:85):

- [ ] AC-01: o arquivo `.ai/specs/spec-doc-0001-documentacao-tecnica-v1.0.md` existe com frontmatter conforme MANIFEST §1.1 (spec_id, specname, version, status, custody, created/updated, origin, task/sender, kill_switch, trace, lgpd-class — .ai/specs/doc-manifest-0001-manifest-v1.0.md:27-44) e ≤400 linhas (DO #3, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:86).
- [ ] AC-02: o item B.9 (LISTA...:41) fecha-se declaradamente — doc de arquitetura especificado (§3.1, §3.5) + revisão/aprovação da OpenAPI especificada (§3.2, §3.4); o conteúdo do contrato `/v1` NÃO foi redeclarado (delimitação §2, linha 1).
- [ ] AC-03: o estado real do destino está registrado — `docs/arquitetura/` inexistente documentado com data da verificação (2026-11-03) e destino marcado `UNKNOWN - verify` (§2, §3.5).
- [ ] AC-04: o ciclo de vida draft → revisão Code Review → aprovado está especificado com revisor nomeado (agent-reviewer), formato de veredito (rubrica R-01..R-07, agent-reviewer.md:21) e portão reviewer → gatekeeper citado (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94,219) — §3.2.
- [ ] AC-05: a regra doc↔código (documented truth = running truth) está citada com as três âncoras (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:156; agent-docker-specialist.md:6,209; PDCA-N11 plano-integral...:599) e a proibição de doc fabricado declarada (P-08; kill switch 3, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:42) — §3.3.
- [ ] AC-06: a fonte única de verdade da OpenAPI está declarada (`/openapi.json` gerado pela aplicação, test_openapi.py:22-26; contrato spec-004 §3) e a regra "render nunca hand-restyled" está citada (agent-docker-specialist.md:6,22), com os 4 critérios binários de revisão (§3.4).
- [ ] AC-07: 100% dos itens do conteúdo mínimo do doc (§3.1) e das linhas da tabela de rastreabilidade documental (§3.5) possuem citação `arquivo:linha`; lacunas de decisão/cláusula marcadas `UNKNOWN - verify` (iso_clause, destino).
- [ ] AC-08: nenhum número de cláusula ISO/IEC 26514:2022 foi afirmado sem verificação (P-08; DON'T 7 do especialista ISO, agent-iso-26514-specialist.md:100) — o campo iso_clause está `UNKNOWN - verify` (§3.5).
- [ ] AC-09: zero PII neste artefato (P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90); kill_switch herdado sem instrução de bypass de gate (vetos 3-4, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:42-43); nenhum arquivo além deste criado/editado; nada commitado.
- [ ] AC-10: validação — **quem valida:** agent-reviewer (veredito pass|amend|block sobre esta spec, auditando citações linha a linha e testabilidade dos ACs — padrão spec-002...:251-256) e, quando acionado, agent-iso-26514-specialist (parcela de conformidade documental, agent-iso-26514-specialist.md:66-67). **DoD desta spec:** (i) AC-01..AC-09 verificáveis por inspeção do arquivo; (ii) delimitação §2 sem redeclaração de contrato; (iii) parcela JSON meio-duplex devolvida ao orquestrador (HF-0614:28-29).

## 5. Rastreabilidade

| Seção | Âncora normativa | Fonte |
|---|---|---|
| §1 | REQ-14 / fase N11.1 / US-014 | plano-integral...:46,84; spec-002...:75,170 |
| §2 (delimitação OpenAPI) | spec-004 §3 + testes de contrato | spec-004-backend-mvp-v1.spec.md:58-93,239; test_openapi.py:1-107 |
| §3.1 | Art. 10.1 (camadas ortogonais) | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213; spec-005...:56-69,87-92,98-111,221-226 |
| §3.2 | Art. 6.2/6.4 (Code Review; drift = defeito); P-06; Art. 10.4 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:152,156,94,219; agent-reviewer.md:16,21,23,33,69 |
| §3.3 | Art. 6.4; PDCA-N11; P-08; kill switch 3 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:156,98; plano-integral...:599; agent-docker-specialist.md:6,64,209; .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:42 |
| §3.4 | spec-004 §3; REQ-14 "revisada/aprovada"; US-014 | spec-004...:58-93; spec-002...:75,170; agent-docker-specialist.md:6,22 |
| §3.5 | Output schema ISO 26514; matriz REQ→spec→doc→test | agent-iso-26514-specialist.md:22,115-126 |

Cadeia da emissão: TA-0058 ← HF-0614 (.ai/handoffs/HF-0614-spec-013-documentacao-tecnica-v1.md:17)
← B.9 (LISTA...:41) / D.4 onda 7 (LISTA...:62) ← REQ-14 (spec-002...:75; plano-integral...:84) ←
US-014 (spec-002...:170). Consulta de domínio incorporada: agent-iso-26514-specialist (contrato lido
como insumo, HF-0614:21) — a custódia ISO não recebe dispatch nesta emissão; sua atuação (parcela de
QA documental) é pós-implementação do doc. Adjacências NÃO cobertas aqui: N11.2 "Consolidação da
Documentação Parcial" (plano-integral...:46, fase irmã); REQ-12/ADRs (E.5, LISTA...:71); spec-004 §12
permanece `UNKNOWN - verify` intocado (imutabilidade TA-0031).

## 6. Fora de escopo (YAGNI)

- Conteúdo do contrato HTTP `/v1` (rotas, schemas, enums, erros) — norma exclusiva da spec-004 §3 (spec-004-backend-mvp-v1.spec.md:58-93); duplicar aqui criaria segunda fonte de verdade (P-03, Canon_Stack_SDD.md:79).
- Editar `tests/integration/test_openapi.py` ou qualquer teste — custódia QA (DON'T #7, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:108); a suíte já existe e blinda o render.
- Escrever o doc de arquitetura nesta emissão — implementação é onda seguinte (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150); destino sem decisão (§2/§3.5).
- Editar spec-004 (inclui a linha :239 `UNKNOWN - verify`) — decisão TA-0031, MANIFEST.md:97; correção de :239, se algum dia cabível, é ato próprio de custódia com parcela.
- N11.2 "Consolidação da Documentação Parcial" (plano-integral...:46) — consolidação de documentação dispersa ≠ doc de arquitetura; fase irmã com escopo próprio.
- ADRs novas ou emendas (inclui emenda da ADR-010, spec-005...:349) — REQ-12/E.5 (LISTA...:71); ratificação da ADR-016 é ato humano CCB (E.2, LISTA...:68; ADR-016-backend-mvp.md:5).
- Suites proprietárias de documentação/API (registry pago, portal gerenciado) — veto FOSS (agent-iso-26514-specialist.md:58,98; P-01, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84).
- Página de referência de API hand-written fora do render (anti-restyle, §3.4) — proibida, não adiada.
- Diagrama de arquitetura do ecossistema SDD (L1/L2/L3) — canon ratificado v2.0.0 existente (Canon_Stack_SDD.md:27,41); re-doc = duplicação de SSOT.
- Template/norma interna de documentação além do necessário para REQ-14 (planejamento documental ISO completo por tipo de doc — user/operations/test/maintenance, agent-iso-26514-specialist.md:120) — YAGNI: esta spec cobre `design` + OpenAPI; demais tipos entram se REQ/US exigir.

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0058 / HF-0614): emissão inicial. Documentação técnica (item B.9, LISTA...:41): escopo do doc de arquitetura (visão de camadas Art. 10.1, matriz de interfaces, Mermaid FOSS, ADRs ratificadas — §3.1); ciclo de vida draft → revisão Code Review (agent-reviewer, rubrica R-01..R-07) → aprovado (§3.2); documented truth = running truth com proibição de doc fabricado (§3.3); OpenAPI com fonte única de verdade no schema gerado + render nunca hand-restyled + 4 critérios binários de revisão (§3.4); mapa de rastreabilidade documental ISO 26514 com iso_clause `UNKNOWN - verify` e destino do doc registrado como inexistente (`docs/arquitetura/`, verificado 2026-11-03) — §3.5. Delimitação exata com spec-004 §3 (§2). Arquivo único; nada commitado.
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo B): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-7`, `handoff` em `origin`; `version` 0.1.0 → 0.2.0). Ratificação CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012). Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio de §§1–6 reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-013`, `version: 0.2.0`, `status: ratificada`, `created/updated: 2026-11-03`/`2026-11-05`, `origin: HF-0614`, `task: TA-0058`) + linha `Status:` | aplicada |
| (b) Contexto/origem | §1 Contexto e origem | aplicada |
| (c) Resolução de conflitos | §2 (tabela tema→decisão→fonte vencedora→texto superado) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (3.1–3.5) | aplicada |
| (e) Critérios de aceite/testes | §4 (AC-01..AC-10 com validação/DoD) | aplicada |
| (f) Rastreabilidade | §5 + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §6 | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
