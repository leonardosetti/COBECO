---
id: ai-specs-manifest
title: MANIFEST — corpus `.ai/specs/` (TA-0031, HF-0031)
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/MANIFEST.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
id: MANIFEST
title: MANIFEST do corpus .ai/specs/ — normalização TA-0031
status: active
version: 1.0.0
created: 2026-11-02
owner: agent-sdd-specialist (.ai/specs/)
task: TA-0031 | handoff: HF-0031 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
---

# MANIFEST — corpus `.ai/specs/` (TA-0031, HF-0031)

Normalização integral decretada pelo GP/Humano (2026-11-02, constitution.md Art. 5.1 —
outorga registrada em ledger no entry TA-0030). Este arquivo é a fonte única do
mapeamento old→new do corpus: referências antigas em arquivos imutáveis
(`.ai/agents/ledger.yaml`, `.ai/handoffs/*`, `docs/decisoes/*`, `docs/auditorias/*`)
resolvem-se por aqui, nunca por edição daqueles arquivos (HF-0031:55-68).

## 1. Template canônico de corpo (camadas fundamentais a–h)

Derivado do estilo de `spec-004-backend-mvp-v1.spec.md` e `spec-005-container-layers-v1.spec.md`
+ ciclo Art. 6 (especifica → implementa → valida → registra). O mapa de aplicação
camada→seção, com estado por spec, está no fim de cada spec (seção
`CAMADAS FUNDAMENTAIS — MAPA (TA-0031)`).

### 1.1 Camada (a) — cabeçalho (frontmatter YAML)

| Campo | Obrigatório | Regra |
|---|---|---|
| `spec_id` | sim | `spec-NNN` (kebab; ver §2.1) |
| `specname` | sim | slug kebab do domínio (ex.: `backend-mvp-v1`) |
| `version` | sim | semver explícita (ver §2.2) |
| `status` | sim | `draft` \| `in_progress` \| `approved` (mapeado do texto prévio; nunca inventado) |
| `custody` | sim | `agent-sdd-specialist (.ai/specs/)` |
| `created` / `updated` | sim | datas ISO (YYYY-MM-DD) |
| `origin` | sim | commit/handoff de origem; lacuna = `UNKNOWN - verify` |
| `task` / `sender` | sim | TA-NNNN + handoff; desconhecido = `UNKNOWN - verify` |
| `kill_switch` | sim | `inherited` |
| `trace` | sim | lista de fontes (Art./ADR/arquivo) |
| `lgpd-class` | opcional | presente quando aplicável (precedente: spec-002) |
| `wave` | opcional | onda de emissão (ex.: `WS-1`, `WS-3`); útil para rastreabilidade de rodadas; usado em spec-001 e spec-002 |

Logo após o frontmatter: H1 no padrão `# SPEC <spec_id> — <specname> — <título>` e
linha `Status:` (quando o texto prévio já a possuía — preservada, não reescrita).

### 1.2 Camadas (b)–(h) — corpo

| Camada | Seção canônica | Regra de conteúdo |
|---|---|---|
| (b) Contexto/origem | `## N. Contexto e origem` | de onde nasce a spec (task/handoff/commit); sem invenção |
| (c) Resolução de conflitos | `## N. Resolução de conflitos` | tabela tema→decisão→fonte vencedora→texto superado (quando aplicável; inexistente = `UNKNOWN - verify`) |
| (d) Corpo de decisões/requisitos/contratos | `## N. …` (domínio) | TODO conteúdo pré-existente preservado; decisões nunca reescritas |
| (e) Critérios de aceite/testes | `## N. Critérios de aceite e testes` | AC verificáveis; ausência prévia = seção declarada `UNKNOWN - verify` (nunca critério inventado) |
| (f) Rastreabilidade | `## N. Rastreabilidade` | REQ/ADR/Art./US/`arquivo:linha` |
| (g) Fora de escopo (YAGNI) | `## N. Fora de escopo (YAGNI)` | escopo negativo já declarado; novas exclusões = `UNKNOWN - verify` |
| (h) Changelog | `## CHANGELOG` | entrada por bump, com task/handoff e o que mudou |

Lacuna de qualquer camada = texto literal `UNKNOWN - verify` (P-08 — sem invenção de
status, datas, métricas ou critérios). Narrativa PT-BR; identificadores/caminhos EN;
citação `arquivo:linha`.

## 2. Regras de nomenclatura e versionamento

### 2.1 Slug e `spec_id`

- Padrão de arquivo: **`spec_id-specname.spec.md`** (kebab-case), decretado em HF-0031:35. Norma geral de nomenclatura de arquivos de artefato: `tipo_artefato-id_artefato-nome_artefato.{ext}` (ADR-018, RAT-2026-11-05-A18). As specs são o caso particular `tipo_artefato=spec` com extensão `.spec.md`.
- `spec_id` sequencial `spec-NNN` (lowercase kebab): precedente dos prefixos NNN do
  repo — `HF-NNNN`, `TA-NNNN`, `ADR-NNN`, `VIO-NNN` (HF-0031:36-37) — com a exigência
  de kebab-case no frontmatter de `.opencode/agents/agent-sdd-specialist.md:127`
  (imutável). O frontmatter anterior usava `<nome>-1` (ex.: `constitution-round-1-proposta-1`),
  incompatível com o slug de arquivo decretado.
- Numeração **cronológica de emissão**: 001 = TA-0002 (25/10), 002 = TA-0004 (25/10),
  003 = run `CANON-20261029-01`/commit `149067f` (30/10), 004 = commit `f6e0455` (01/11),
  005 = TA-0029/TA-0030 (02/11). A ordem de emissão preserva a precedência lógica
  (001/002 são insumos de 004/005).

### 2.2 Versões (bump inicial nas sem versão; preservar as existentes)

| spec | versão | justificativa |
|---|---|---|
| spec-001 | 0.1.0 | já declarada no frontmatter original (AUD-2610-04.md:10) — mantida |
| spec-002 | 0.1.0 | já declarada no frontmatter original (AUD-2610-04.md:12) — mantida |
| spec-003 | 3.1.0 | versão do run `CANON-20261029-01` (H1 original `v3.1.0`) — mantida, sem bump |
| spec-004 | 1.0.0 | **bump inicial** (linha `Status:` original sem versão semver) |
| spec-005 | 0.2.0 | pós-TA-0030 (HF-0031:20, HF-0030) — **mantida, sem regressão da amenda** |

## 3. Inventário e classificação (11 arquivos → 11 arquivos; 0 realocações)

Evidência de refs = `grep` em 2026-11-02. "Refs vivas" = ocorrências em arquivos
editáveis apontando para o slug novo; "imutáveis" = resolvidas pelo mapa do §4.

| Arquivo original (pré-TA-0031) | Class. | Nome novo | Versão | Delta (linhas) | Refs vivas atualizadas | Imutáveis resolvidas via §4 |
|---|---|---|---|---|---|---|
| `constitution-round-1-proposta.md` | spec | `spec-001-constitution-round-1-proposta.spec.md` | 0.1.0 | 396 → 413 (edição in-place do `spec_id` + caminho próprio; +17 anexados ao final; deslocamento 0 → refs `arquivo:linha` históricas seguem válidas) | 8 em `spec-002` (linhas 17, 30, 35, 45, 100, 128, 141, 217) | `AUD-2610-03.md:11,18,34,63,79,240,247`; `AUD-2610-04.md:10,57,73,109,247`; `HF-RELATORIO-ANALISE-CONSTITUICAO.md:43`; `HF-0031:21` |
| `requisitos-review-round-1.md` | spec | `spec-002-requisitos-review-round-1.spec.md` | 0.1.0 | 267 → 282 (in-place: `spec_id` + 9 linhas de ref; deslocamento 0) | 15 em `spec-005` | `vio-register.md:31`; `AUD-2610-04.md:12,65,75`; `HF-0029:53`; `HF-RELATORIO:42`; `HF-0031:21` |
| `000-SDD_CONF-memory.spec.md` | spec | `spec-003-sdd-conf-memory.spec.md` | 3.1.0 | 1127 → 1179 (+12 frontmatter; corpo das Partes 0–10 idêntico byte a byte, deslocamento +12; +40 anexados = PARTE 11 + MAPA) | 2 em `docs/analise/RELATORIO_MEMORIA_PERSISTENTE_SDDAI.md:13,88` | `AUD-2610-03-RESULTADOS.md:7`; `HF-0031:19` |
| `backend-mvp-v1.spec.md` | spec | `spec-004-backend-mvp-v1.spec.md` | 1.0.0 (bump inicial) | 207 → 262 (título substituído por frontmatter+título = +13 de deslocamento; corpo `f6e0455` idêntico; +42 anexados = §§10–14 + MAPA) | 25 em `spec-005` + 1 em `docs/planos/plano-granular/desenvolvimento.md:13` | `ADR-016:18,127`; `HF-0029:16,30,49,61`; `HF-0500:12`; `HF-0031:19` |
| `container-layers-v1.spec.md` | spec | `spec-005-container-layers-v1.spec.md` | 0.2.0 (mantida) | 378 hoje (arquivo nunca commitado — criado em TA-0029; `HF-0030:18` atesta 344 l no dispatch da amenda; +12 frontmatter + MAPA/anotação anexados em TA-0031) | 0 externas (2 auto-referências) | `ledger.yaml:24,32`; `HF-0030:18,26,57`; `HF-0031:19` |
| `afa-changelog.md` | **pinned** | (sem rename) | — | — | — | — (canon AFA §15, ver §5) |
| `requisitos.md` (0 B) | **pinned** | (sem rename) | — | — | — | — (ver §5) |
| `tap.md` (0 B) | **pinned** | (sem rename) | — | — | — | — (ver §5) |
| `eap.md` (0 B) | **pinned** | (sem rename) | — | — | — | — (ver §5) |
| `kb-taxonomy.md` | **pinned** | (sem rename) | — | — | — | — (ver §5) |
| `input-canonico-v4.1.1.md` | **pinned/ambiguous** | (sem rename — HF-0031:44-45) | — | — | — | `ADR-011:56` (ver §5) |

Totais verificáveis: 51 linhas de refs vivas atualizadas em 4 arquivos editáveis
(`spec-002` ×8, `spec-005` ×40, `RELATORIO_MEMORIA_PERSISTENTE_SDDAI.md` ×2,
`plano-granular/desenvolvimento.md` ×1) + auto-referências internas dos próprios specs;
64 ocorrências dos slugs novos em arquivos editáveis no total (`grep -o`, 2026-11-02).

### 3.1 Fronteira de integridade verificada

`grep` repo-wide pelos 5 slugs antigos (forma de caminho e forma nua) fora de
`.ai/specs/`: **zero** ocorrências em arquivos editáveis — todas remanescentes estão
exclusivamente em imutáveis (`docs/auditorias/*`, `docs/decisoes/*`, `.ai/handoffs/*`,
`.ai/agents/ledger.yaml`) e nas linhas de CHANGELOG "slug antigo → novo" dos próprios
specs (intencionais, para leitura do histórico). Verificado também que
`python3 -m pytest tests/agents/ -q` = 4 failed / 149 passed / 1 skipped (baseline
exata, mesmas 4 falhas preexistentes de report/wiring) e
`python3 scripts/sync_agent_registry.py --check` = exit 0.

## 4. Mapa de redirecionamento old→new

### 4.1 Specs renomeadas (5)

| Slug antigo (`.ai/specs/…`) | Slug novo |
|---|---|
| `constitution-round-1-proposta.md` | `spec-001-constitution-round-1-proposta.spec.md` |
| `requisitos-review-round-1.md` | `spec-002-requisitos-review-round-1.spec.md` |
| `000-SDD_CONF-memory.spec.md` | `spec-003-sdd-conf-memory.spec.md` |
| `backend-mvp-v1.spec.md` | `spec-004-backend-mvp-v1.spec.md` |
| `container-layers-v1.spec.md` | `spec-005-container-layers-v1.spec.md` |

### 4.2 Referências históricas em IMUTÁVEIS (resolvidas por este mapa — nunca editar o fonte)

| Fonte imutável (arquivo:linha) | Slug antigo citado | Resolve para |
|---|---|---|
| `.ai/agents/ledger.yaml:24` (TA-0029) | `container-layers-v1.spec.md` (344 l) | `spec-005-container-layers-v1.spec.md` (hoje 378 l; "344 l" é o valor histórico do dispatch) |
| `.ai/agents/ledger.yaml:32` (TA-0030) | `container-layers-v1.spec.md` (Status 0.2.0) | `spec-005-container-layers-v1.spec.md` (0.2.0 mantida) |
| `.ai/handoffs/HF-0029-container-layers-spec.md:16,30,49,61` | `backend-mvp-v1.spec.md` | `spec-004-backend-mvp-v1.spec.md` |
| `.ai/handoffs/HF-0029-container-layers-spec.md:53` | `requisitos-review-round-1.md` | `spec-002-requisitos-review-round-1.spec.md` |
| `.ai/handoffs/HF-0030-nginx-aceito-demo.md:18,26,57` | `container-layers-v1.spec.md` (344 l) | `spec-005-container-layers-v1.spec.md` |
| `.ai/handoffs/HF-0031-specs-normalizacao.md:19,21,30` | os 5 antigos | §4.1 (HF descreve o estado pré-normalização) |
| `.ai/handoffs/HF-0500-backend-mvp.md:12` | `backend-mvp-v1.spec.md` | `spec-004-backend-mvp-v1.spec.md` |
| `.ai/handoffs/HF-RELATORIO-ANALISE-CONSTITUICAO.md:42` | `requisitos-review-round-1.md` | `spec-002-requisitos-review-round-1.spec.md` |
| `.ai/handoffs/HF-RELATORIO-ANALISE-CONSTITUICAO.md:43` | `constitution-round-1-proposta.md` | `spec-001-constitution-round-1-proposta.spec.md` |
| `docs/decisoes/ADR-016-backend-mvp.md:18,127` | `backend-mvp-v1.spec.md` | `spec-004-backend-mvp-v1.spec.md` |
| `docs/auditorias/AUD-2610-03.md:11,18,34,63,79,240,247` | `constitution-round-1-proposta.md` | `spec-001-constitution-round-1-proposta.spec.md` |
| `docs/auditorias/AUD-2610-03-RESULTADOS.md:7` | `000-SDD_CONF-memory.spec.md` | `spec-003-sdd-conf-memory.spec.md` |
| `docs/auditorias/AUD-2610-04.md:10,57,73,109` | `constitution-round-1-proposta.md` | `spec-001-constitution-round-1-proposta.spec.md` |
| `docs/auditorias/AUD-2610-04.md:12,65,75` | `requisitos-review-round-1.md` | `spec-002-requisitos-review-round-1.spec.md` |
| `docs/auditorias/vio-register.md:31` | `requisitos-review-round-1.md` (refs `:44-51`, `:100`, `:210-224`) | `spec-002-requisitos-review-round-1.spec.md` — deslocamento 0, mesmo `arquivo:linha` |

Observações de continuidade de linha: para spec-001, spec-002 e spec-003 o deslocamento
de linhas do corpo é 0/+12 respectivamente apenas no bloco de frontmatter novo; as
citações numéricas existentes em imutáveis para spec-001/spec-002 (deslocamento 0)
permanecem exatas. Para spec-004 o corpo deslocou +13 (frontmatter) — nenhuma fonte
imutável cita linha numérica de `backend-mvp-v1.spec.md` (só §/seções), e as 25+4 citações
numéricas vivas em `spec-005` foram reposicionadas (+13) com verificação forense
(linha antiga == linha nova +13 para todos os números citados). `ledger.yaml:24` e
`HF-0030:18` citam "344 linhas" = valor histórico, agora resolvido por este mapa.

## 5. Justificativas — pinned, ambiguous e realocações

### 5.1 Pinned (não mover, não renomear) — referenciados por prompts/imutáveis

| Arquivo | Evidência de referência (grep) | Destino/justificativa |
|---|---|---|
| `afa-changelog.md` (317 B) | **43 arquivos** de `.opencode/agents/*` (forja AFA imutável, Art. 4.1) apontam `.ai/specs/afa-changelog.md` como log SIR — ex.: `agent-sdd-specialist.md:217`, `agent-architect.md:89,210`, `agent-compliance-governance.md:33`, `agent-factory-architect-ultimate.md:648`, `agent-nexus-prime-ultimate.md:232`; canon AFA §15 | Renomear/mover quebraria o contrato de log de 43 agentes imutáveis (fail-closed HF-0031:64-65) |
| `requisitos.md` (0 B) | `.opencode/agents/agent-business-analysis-specialist.md:31,67,144` ("REQ SSOT", "REQ ids from … only", "re-read … first"); `agent-project-design-specialist.md:32,166` | Placeholder canônico da camada 5 (Art. 2) sob custódia BA/design; conteúdo vazio = pendência declarada (G-08/GAP-01, ver LISTA-SPECS-PENDENTES). Repovoamento é ato de outra custódia, pós-gate E |
| `tap.md` (0 B) | `agent-business-analysis-specialist.md:32`; `agent-sldc-process-specialist.md:31` ("TAP/EAP scope baseline") | idem — baseline de escopo referenciada por prompts imutáveis |
| `eap.md` (0 B) | `agent-business-analysis-specialist.md:32`; `agent-sldc-process-specialist.md:31` | idem |
| `kb-taxonomy.md` (13.383 B) | `agent-business-analysis-specialist.md:33` ("taxonomy classes for requirement classification"); `agent-project-patterns-standards-specialist.md:32` ("taxonomy for pattern classification") | Taxonomia viva usada por 2 agentes imutáveis; renomear quebraria o contrato |

### 5.2 `input-canonico-v4.1.1.md` — `pinned/ambiguous` (NÃO movido, conforme HF-0031:44-45)

- **A favor do move** (papel de input, não de spec): o próprio arquivo se declara input
  canônico (título/frontmatter) e o HF-0031:22-23 o lista como "input canônico".
- **Contra o move** (fail-closed): `docs/decisoes/ADR-011-Ecossistema-SDDAI.md:56`
  (imutável, canon de decisão Art. 2) o classifica literalmente como
  "**Specs imutáveis** (`.ai/specs/*.md`): `tap.md`, `eap.md`, `requisitos.md`,
  `input-canonico-v4.1.1.md`. Once written, never modified without new version file."
  Mover para `docs/analise/` violaria o texto da ADR ratificada; editar a ADR é vedado.
- **Veredito:** papel incerto no ciclo SDD (input × spec) com conflito entre a
  autodeclaração e o cano decisional → classe `pinned/ambiguous`, permanece em
  `.ai/specs/` sem rename. Nenhuma viva o referencia (grep repo-wide: só `ADR-011:56` e
  `HF-0031:23`, ambos imutáveis) — portanto zero refs a atualizar e zero link quebrado.

### 5.3 Realocações de não-specs — NENHUMA (justificativa)

Os 6 não-specs do diretório são integralmente cobertos por §5.1 (5 pinned por
referência em prompts imutáveis) e §5.2 (1 ambiguous por cano imutável). Não há arquivo
restante com conteúdo correspondente a `docs/planos/`, `docs/analise/`, `docs/decisoes/`
ou `docs/conhecimento/` que possa ser movido sem quebrar link canônico em imutável —
regra fail-closed de HF-0031:67-68 ("nunca quebre link canônico"). Consequentemente,
`pending_rename` também está vazio: nenhum rename viável foi adiado.

## 6. Critérios de aceite (HF-0031:70-81) — verificação

| # | AC | Evidência | Estado |
|---|---|---|---|
| 1 | Template canônico (a–h) no MANIFEST | §1 (frontmatter §1.1 + camadas §1.2) | ✅ |
| 2 | TODAS as specs renomeadas + versão explícita | §3 (5/5 renomeadas; versões §2.2) | ✅ |
| 3 | Camadas aplicadas; conteúdo pré-exervado; lacunas `UNKNOWN - verify` | Mapa no fim de cada spec; diff forense §3.1 (corpos idênticos; deslocamentos 0/+12/+13); `UNKNOWN - verify` presente em todas | ✅ |
| 4 | Amenda TA-0030 preservada (proxy aceito, 0.2.0+) | `spec-005:4` (`version: 0.2.0`), `:15` (Status ACEITO E MANTIDO), `:46`, `:363` | ✅ |
| 5 | Não-specs tratados com refs vivas atualizadas; nenhum link quebrado | §5 (0 moves; 51 refs vivas atualizadas; grep §3.1 = zero old-name vivo) | ✅ |
| 6 | Imutáveis intocados | `git status`/`git diff --cached`: nenhum diff em constitution/registry/.opencode/handoffs/ledger/ADRs/auditorias (ledger `M` é pré-existente, entrada TA-0031 do dispatcher) | ✅ |
| 7 | MANIFEST com inventário, mapa old→new e justificativas | §§3, 4, 5 deste arquivo | ✅ |
| 8 | `docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md` emitido, cada pendência com citação | emitido em 2026-11-02 (resumo na parcela TA-0031) | ✅ |
| 9 | `pytest tests/agents/ -q` sem NOVAS falhas (baseline 4F/149P/1S) | execução 2026-11-02: `4 failed, 149 passed, 1 skipped` — mesmas 4 falhas preexistentes | ✅ |
| 10 | `sync_agent_registry.py --check` exit 0 | execução 2026-11-02: `[OK] registry em sincronia com o disco`, exit 0 | ✅ |

## 7. Fora do escopo desta normalização

- Nenhum arquivo de código/compose/Dockerfile/workflow alterado (HF-0031:90-92).
- Realocação humana não-commitada em `docs/planos/` (legacy/ + plano-granular/ preservados, unstaged).
- Repovoamento dos placeholders 0 B (`requisitos.md`, `tap.md`, `eap.md`) — pós-gate E,
  listado como pendência em `docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md`.
- Nada stageado; nada commitado.
