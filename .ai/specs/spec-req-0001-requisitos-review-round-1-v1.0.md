---
id: spec-req-0001-requisitos-review-round-1-v1.0
type: spec-req
title: SPEC REQ — Requisitos Review Round 1
version: v1.0
status: ratificado
canonical: false
canonical_slug: requisitos-review-round-1
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
spec_id: spec-002
specname: requisitos-review-round-1
version: 0.1.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-10-25
updated: 2026-11-05
origin: TA-0004 | handoff: N/A (analyze; sem HF emitido nesta rodada) | sender: agent-nexus-prime-ultimate
task: TA-0004
kill_switch: inherited
lgpd-class: n/a (zero PII neste artefato; P-04)
wave: WS-3 | Rodada 1 de revisao de requisitos base para definicao de specs + user stories
trace:
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md v1.0.0 (Art. 1.2/1.3/2/3/5.1/6.1/6.2/9.1; P-01..P-10)
  - docs/planos/plano-escopo.md v1.1 (Tabela 1; secoes 2.3-2.6)
  - docs/planos/plano-integral-tap-1-2-3-4-5.md (Tabela 3, REQ-01..15; TAP v3 congelado)
  - docs/planos/COBECO.pdf (texto extraido pdftotext -layout; PDF:N = linha N do dump /tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/cobeco.txt)
  - LEGADO: docs/archive/legacy-md-artifact/rf_rnf_qwen.md, rf_rnf_deepseek.md, review_rf_rfn.md; docs/archive/tap-sections/req_1.0.md
  - docs/auditorias/AUD-2610-03.md (F-01..F-12; KG-01..KG-04; R-00..R-07; BLOCK)
  - .ai/specs/spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md (E-01..E-08 — PENDENTES de CCB, nao sao lei)
  - doc-readme-0001-readme-canon.md:151-165 (espelho REQ-01..15)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012)
---

# req-func-0001-requisitos-funcionais-canon REVIEW — ROUND 1 (WS-3 · COBECO)

**Natureza:** auditoria + proposta. Nada aqui decide (Art. 5.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:53); stories
candidatas NAO sao compromisso de escopo — cabem ao backlog Kanban e ao Humano/PO via CCB.

## 0. METODO E CONVENCOES

- Convencao PDF:N = linha N do texto extraido de docs/planos/COBECO.pdf via pdftotext -layout
  (mesmo padrao de AUD-2610-03.md:18 e spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:26-29).
- Estados de inventario (EN tokens): `canonical-mirror` (linha de base TAP congelada, espelhada),
  `duplicate-mirror`, `legacy-input` (insumo historico valido), `legacy-contradicts` (legado
  contradiz camada superior), `out-of-scope`, `orphan` (sem pai canonico).
- Estado de governanca no momento desta emissao: camada ADR VAZIA (AUD-2610-03.md:26, F-01);
  emendas E-01..E-08 PENDENTES (spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:190); especificacao formal
  de produto = BLOCK (secao E deste documento).

## A. INVENTARIO DA BASE DE req-func-0001-requisitos-funcionais-canon

### A.1 Estado da custodia canonica

| Artefato (Art. 2) | Estado | Evidencia |
|---|---|---|
| docs/requisitos/requisitos.md (camada 4) | VAZIO (0 B) | ls -la nesta sessao (25/10); AUD-2610-03.md:43 (T3, commit 7892561 = 0B) |
| .ai/specs/requisitos.md (camada 5) | VAZIO (0 B) | ls -la nesta sessao; spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:132-141 (G-08) |
| .ai/specs/tap.md / eap.md (camada 5) | VAZIO (0 B) | idem (G-08) |
| docs/tap/TAP.md (camada 4) | VAZIO (0 B) | ls -la nesta sessao; TAP sobrevive em plano-integral-tap-1-2-3-4-5.md:10 |
| docs/decisoes/ADR-001..005 (camada 3) | VAZIO (0 B x5) | AUD-2610-03.md:26,59 (F-01) |

**Conclusao A.1:** a "base canonica" citada no envelope NAO EXISTE como artefato; o conteudo
sobrevive em 4 espelhos do TAP v3 congelado. KG-R-01 declarado (secao F).

### A.2 Inventario canonico REQ-01..REQ-15 (linha de base TAP §5)

Fontes: req_1.0.md:11-50 (=TAP §5 era); plano-integral-tap-1-2-3-4-5.md:67-85 (Tabela 3);
COBECO.pdf:807-851 (Tabela 6); doc-readme-0001-readme-canon.md:151-165. Distribuicao por entrega: plano-escopo.md:33-45.
Priorizacao MoSCoW (Must: REQ-01..09,11,15; Should: REQ-10,12,13,14): plano-escopo.md:57;
plano-integral:310. Estado unico: `canonical-mirror` (todos rastreaveis a TAP §3 + fase EAP).

| ID | Sintese | Critério de aceite (fonte) | Fase EAP | MoSCoW |
|---|---|---|---|---|
| REQ-01 | Simulacao cambial tempo real USD/EUR→BRL | latencia cotação ≤2s (req_1.0.md:11) | N5.2 | Must |
| REQ-02 | 5 regimes de contratacao (hora,dia,semana,mes,valor fixo) | 100% regimes em UAT (req_1.0.md:12) | N5.1 | Must |
| REQ-03 | Encargos financeiros (spread+IOF) | calculo auditavel, 2 casas decimais (req_1.0.md:13) | N5.1 | Must |
| REQ-04 | Emissao invoice PDF | WeasyPrint ≤3s/documento (req_1.0.md:14) | N5.4 | Must |
| REQ-05 | Tempo de resposta da aplicacao | ≤3s em 95% (req_1.0.md:15) | N5.1 | Must |
| REQ-06 | Interface web responsiva FOSS | Chrome/Firefox/Edge ult. 2 versoes (req_1.0.md:16) | N5.3 | Must |
| REQ-07 | Cache de cotacoes (SQLite) | reddoc-arch-0006-uc-v1ao ≥50% chamadas API (req_1.0.md:17) | N5.2 | Must |
| REQ-08 | Cobertura de testes | ≥80% (pytest+coverage) (req_1.0.md:23) | N6.1 | Must |
| REQ-09 | UAT | 100% fluxos criticos, zero defeitos criticos/bloqueantes (req_1.0.md:24) | N6.2 | Must |
| REQ-10 | Ferramentas da qualidade (PDCA+Ishikawa 6M) | 12 PDCAs + diagrama (req_1.0.md:25) | N6.3 | Should |
| REQ-11 | Pipeline CI | lint+testes ≤5min/push (req_1.0.md:31) | N7.1 | Must |
| REQ-12 | ADRs para decisoes criticas | min. 3 ADRs (req_1.0.md:37) | N9.1 | Should |
| REQ-13 | Rastreabilidade de prompts SDD | 100% catalogados em .ai/handoffs/ (req_1.0.md:38) | N9.3 | Should |
| REQ-14 | Documentacao tecnica (arquitetura+APIs) | revisada/aprovada (req_1.0.md:44) | N11.1 | Should |
| REQ-15 | Licenciamento 100% FOSS | dependencias OSI-approved (req_1.0.md:50) | N1.5+N4.4 | Must |

RNF canonicos estao EMBUTIDOS como criterios de aceite de REQ-05 (performance), REQ-08
(qualidade), REQ-11 (CI), REQ-15 (FOSS) — nao existe registro NFR separado (ver GAP-02).
Matriz SMART→EAP→REQ: COBECO.pdf:860-879 (Tabela 7); req_1.0.md:52-62.

### A.3 Inventario LEGADO (marcado como tal — insumo historico, NAO linha de base)

| Corpus | Conteudo | Estado |
|---|---|---|
| rf_rnf_qwen.md (RF-01..10, RNF-01..08, RN-01..04) | auth/JWT/PostgreSQL/Redis/GBP; fórmula por DEDUCAO (rf_rnf_qwen.md:44) | `legacy-contradicts` (RF-01..04, RNF-04/07, moedas GBP); `legacy-input` (RN-01 formula, RNF-08 UTC, RF-05 fallback) |
| rf_rnf_deepseek.md (RF-01..18, RNF-01..08) | auth, 18 RFs, keep-alive, warmup /warmup (:70), fórmula por MULTIPLICACAO (:50) | `legacy-contradicts` (RF-01..04, RNF-04/06, formula); `legacy-input` (RF-15 lista, RF-17 WYSIWYG, RF-18 warmup) |
| review_rf_rfn.md (RN-01..04, RF-01..10, RNF-01..08) | fusao corrigida: fórmula DEDUCAO "taxas sao subtraidas, nunca somadas" (:16), 2 modalidades (:17) | `legacy-input` (RN-01..03, RF-05..10); `legacy-contradicts` (RN-02/RF-04 2 modalidades vs REQ-02 5 regimes; RF-01..02 auth) |
| req_1.0.md | TAP §5 v1.0 (REQ-01..15) | `duplicate-mirror` do canonico (verificado linha a linha em A.2) |

Colisao de IDs: RF-01..10 possuem CONTEUDOS DIFERENTES nos 3 corpora com MESMOS IDs
(ex.: RF-04 qwen:19 vs deepseek:39 vs review:30) — todo uso de ID legado exige citacao do corpus.

## B. AUDITORIA

### B.1 Gaps (requisito ausente que o escopo canonico exige ou vazios estruturais)

| ID | Gap | Evidencia |
|---|---|---|
| GAP-01 | Artefato canonico de requisitos nao existe (0 B); camada 5 sem conteudo executavel | secao A.1; spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:132-141 |
| GAP-02 | Sem registro NFR consolidado; EAP previa fase N2.2 "Requisitos Nao Funcionais" (PDF:645) sem artefato; P-06/P-07/P-04 sem criterio de produto mapeado | req_1.0.md (sem secao NFR); constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:34,36 (P-06/P-08) |
| GAP-03 | Formula de spread/IOF nao fixada no canonico: REQ-03 exige "calculo auditavel" sem formula; legado diverge (DEDUCAO review:16/qwen:44 vs MULTIPLICACAO deepseek:50) — resultado financeiro distinto | req_1.0.md:13; corpora citados |
| GAP-04 | Modelo de dados da invoice (campos: dados bancarios, CPF/CNPJ, periodo) nao canonico — legado apenas (deepseek:58; qwen:18) | req_1.0.md:14 (REQ-04 generico) |
| GAP-05 | API externa de cotação nao nomeada no canonico ("API externa"); Frankfurter existe so no legado (qwen:20; deepseek:48) — nomeacao = decisao de stack → ADR-001 BLOCK | req_1.0.md:11; AUD-2610-03.md:87-116 |
| GAP-06 | Parametros de cache nao canonicos (TTL/invalidacao): REQ-07 da so o criterio ≥50%; Redis TTL 300s e legado | req_1.0.md:17; qwen:47; deepseek:49 |
| GAP-07 | Conversao REQ→User Story prevista ate M2 (plano-escopo.md:49; fase N2.3) nao executada; backlog de stories inexistente | plano-escopo.md:47-49 |
| GAP-08 | Sem criterio LGPD de produto: invoice carrega dados pessoais/financeiros (legado deepseek:58) e REQ-01..15 nao contemplam minimizacao/tratamento LGPD (P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:36) — requer decisao CCB/PO | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:36; corpora |

### B.2 Duplicatas

- REQ-01..15 declarados em 4 espelhos (A.2) = 60 declaracoes para 15 requisitos reais;
  risco de drift entre espelhos (espelho doc-readme-0001-readme-canon e plano-integral verificados iguais em spot-check;
  comparacao integral pendente — KG-R-01).
- ID-collision legada: RF-01..10 triplo (A.3).

### B.3 Contradicoes entre fontes

| ID | Contradicao | Resoldoc-arch-0006-uc-v1ao proposta (Art. 2 — constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:25) |
|---|---|---|
| C-01 | REQ-02 = 5 regimes (req_1.0.md:12) vs legado 2 modalidades, rejeitando dia/semana (review:17; qwen:19) | Canonico prevalece: 5 regimes; RN-02/RF-04 legados = `legacy-contradicts` |
| C-02 | IN = USD/EUR (plano-escopo.md:71; PDF Tabela 40:2197+) vs legado inclui GBP (qwen:19; deepseek:39,48; review:30) | GBP/JPY/CHF = OUT (Tabela 1:71) |
| C-03 | Legado auth/multiusuario core (qwen:16-18; deepseek:29-32; review:27-28) vs OUT "Cadastro multiusuario ou autenticacao" (plano-escopo.md:72) | OUT — rejeitado (OS-01) |
| C-04 | Legado PostgreSQL+Redis+Sequence (qwen:35,38; deepseek:49,58; review:47) vs OUT PostgreSQL e IN SQLite (plano-escopo.md:76; REQ-07) | SQLite prevalece; numeracao unica de invoice precisa soldoc-arch-0006-uc-v1ao sem PostgreSQL Sequence (GAP-04/06, ver doc-user-story-017-us-017) |
| C-05 | Formula: DEDUCAO (qwen:44; review:16) vs MULTIPLICACAO (1+spread)(1+IOF) (deepseek:50) | Gap financeiro real (GAP-03); proposta tecnica = deddoc-arch-0006-uc-v1ao (correcao historica review:75), DECISAO = CCB/PO |
| C-06 | WIP ≤3 total (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60) vs 3/pessoa ≤9 (PDF:1677,1817-1818) | Ja registrada: AUD-2610-03.md:66 (F-08); emenda E-08 pendente CCB |
| C-07 | Latencia cotação ≤2s (REQ-01) vs aplicacao ≤3s P95 (REQ-05) — camadas nao explicitadas | Leitura provavel: 2s=chamada API, 3s=E2E; requer explicitacao na spec (nao contradicao, ambiguidade) |
| C-08 | Capacidade: legado "equipe de 2 pessoas" (qwen:3; deepseek:5) vs Tabela 32 "3×3 pessoas" (PDF:1817) | Legado desatualizado; capacidade regida por plano vigente |
| C-09 | Modelo SDD: qwen30b-moe (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:30) vs "Qwen 32B" (PDF:2156; plano-escopo.md:53) | Constituicao prevalece (G-12, spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:168-173) |

### B.4 Itens fora do escopo congelado — REJEITADOS como OUT-OF-SCOPE (Art. 1.3, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:14)

| ID | Item (fonte legada) | Justificativa da rejeicao |
|---|---|---|
| OS-01 | Autenticacao/cadastro multiusuario (qwen:16-18) | Tabela 1 OUT (plano-escopo.md:72); ausente do Art. 1.2 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:13) |
| OS-02 | PostgreSQL/Redis (qwen:35,38; deepseek:49) | Tabela 1 OUT (plano-escopo.md:76); REQ-07 canonico = SQLite |
| OS-03 | Moedas GBP/JPY/CHF (qwen:19; deepseek:48) | Tabela 1 OUT (plano-escopo.md:71) |
| OS-04 | Integracao com plataformas de transferencia | Tabela 1 OUT (plano-escopo.md:73) |
| OS-05 | NF-e/NFS-e | Tabela 1 OUT (plano-escopo.md:74) |
| OS-06 | App mobile nativo | Tabela 1 OUT (plano-escopo.md:75) |
| OS-07 | Testes de carga/estresse 20 usuarios k6/Locust (qwen:33; review:45) | Tabela 1 OUT (plano-escopo.md:77) |
| OS-08 | Hospedagem publica + keep-alive /health 14min (deepseek:83; review:48) | Infra = "ambiente local/homologacao (sem cloud paga)" (PDF:~2530 Tabela 44, via spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:160-162); P-02 veta nuvem (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:30) |
| OS-09 | Graficos de evoldoc-arch-0006-uc-v1ao cambial, export DOCX, comparador de plataformas, painel admin (deepseek:19) | Fora do Art. 1.2; YAGNI (E-04 pendente, mas Tabela 1 OUT por analogia — KG-R-03) |
| OS-10 | Regime de jornada "por ano" (rejeitado ja no legado qwen:19) | Art. 1.2/REQ-02 enumeram 5 regimes sem "ano" (req_1.0.md:12) |

Nenhum destes itens entra em story; entrada futura exige emenda constitdoc-arch-0006-uc-v1ional previa (Art. 1.3).

## C. USER STORIES CANDIDATAS

**NOTA OBRIGATORIA (Art. 5.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:53):** estas stories sao CANDIDATAS de backlog.
Nao constituem compromisso de escopo, ordem de execdoc-arch-0006-uc-v1ao ou entregaveis garantidos. O Humano
(GP/PO) decide via CCB e refinement semanal (plano-escopo.md:57,110). YAGNI: cada story nasce
de requisito citado; nenhuma capacidade especulativa foi criada. Cobertura REQ→US: 15/15.

### C.1 Stories com origem canonica (REQ-01..15)

| ID/slug | Origem | Narrativa (PT-BR) | Criterios de aceite candidatos (Given/When/Then) |
|---|---|---|---|
| doc-user-story-001-us-001 realtime-currency-simulation | REQ-01, REQ-05 (req_1.0.md:11,15) | Como profissional que fatura em moeda estrangeira, quero simular em tempo real a conversao de USD/EUR para BRL, para saber o valor recebivel. | Given cotaçao valida disponivel; When submeto um valor em USD ou EUR; Then o sistema exibe o equivalente em BRL com latencia ≤3s (95% das requisicoes; cotaçao ≤2s — C-07 a explicitar). |
| doc-user-story-002-us-002 five-engagement-regimes | REQ-02 (req_1.0.md:12; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:13) | Como prestador, quero simular minha remuneracao em 5 regimes de contratacao (hora, dia, semana, mes, valor fixo) e compara-los, para escolher o melhor modelo. | Given a tela de simulacao; When seleciono cada um dos 5 regimes com parametros validos; Then todos calculam resultado e sao comparaveis, com 100% dos regimes operacionais em UAT. |
| doc-user-story-003-us-003 spread-iof-net-calculation | REQ-03 (req_1.0.md:13) | Como prestador, quero que a simulacao aplique spread e IOF com precisao de 2 casas decimais, para estimar o liquido real a receber. | Given valor bruto e percentuais de spread/IOF; When o calculo executa; Then o liquido segue a formula ratificada pelo CCB (GAP-03/C-05 pendente) com 2 casas decimais e trilha auditavel do calculo. |
| doc-user-story-004-us-004 invoice-pdf-generation | REQ-04 (req_1.0.md:14) | Como prestador, quero emitir uma invoice em PDF via WeasyPrint, para documentar formalmente o servico prestado. | Given uma invoice com dados validos (modelo de dados pendente — GAP-04); When aciono a emissao; Then o PDF e gerado em ≤3s por documento com os dados da invoice. |
| doc-user-story-005-us-005 responsive-foss-web-ui | REQ-06 (req_1.0.md:16) | Como usuario, quero acessar o sistema por interface web responsiva 100% FOSS, para trabalhar a partir de qualquer desktop. | Given navegadores Chrome/Firefox/Edge (ultimas 2 versoes); When acesso as telas do MVP; Then o layout responde sem quebra funcional em todos eles. |
| doc-user-story-006-us-006 sqlite-quote-cache | REQ-07 (req_1.0.md:17) | Como operador do sistema, quero cache SQLite de cotacoes, para reduzir a dependencia da API externa. | Given uma cotaçao ja consultada; When comparo as chamadas a API externa com e sem cache; Then a reduçao de chamadas e ≥50% (parametros TTL pendentes — GAP-06). |
| doc-user-story-008-us-008 test-coverage-gate | REQ-08 (req_1.0.md:23; P-06) | Como QA, quero cobertura de testes ≥80% validada por CI, para garantir qualidade minima por design. | Given a suite de testes; When o pipeline executa; Then o report de cobertura e ≥80% ou o merge e bloqueado. |
| doc-user-story-009-us-009 uat-critical-flows | REQ-09 (req_1.0.md:24) | Como PO, quero UAT cobrindo 100% dos fluxos criticos, para validar o MVP sem defeitos criticos. | Given o plano de UAT; When executo os fluxos criticos; Then 100% passam e existem zero defeitos criticos/bloqueantes. |
| doc-user-story-010-us-010 quality-tools-pdca-ishikawa | REQ-10 (req_1.0.md:25) | Como GP, quero 12 PDCAs consolidados e diagrama Ishikawa 6M, para evidenciar melhoria continua academica. | Given os ciclos PDCA por fase da EAP; When consolido a fase N6.3; Then 12 PDCAs e o diagrama de causa e efeito estao documentados. |
| doc-user-story-011-us-011 ci-pipeline | REQ-11 (req_1.0.md:31) | Como dev, quero pipeline CI com lint e testes em ≤5min por push, para feedback rapido de qualidade. | Given um push em feature branch; When o pipeline executa; Then lint+testes concluem em ≤5min e falha bloqueia merge. |
| doc-user-story-012-us-012 adr-records [BLOCKED] | REQ-12 (req_1.0.md:37) | Como arquiteto, quero ADRs para decisoes arquiteturais criticas, para rastreabilidade de decisao (P-05). | Given uma decisao critica; When documento o ADR; Then ≥3 ADRs com CONTEUDO nao-vazio estao versionados em docs/decisoes/. BLOCK: re-emissao ADR-001..006 pendente CCB (AUD-2610-03.md:85,240). |
| doc-user-story-013-us-013 sdd-prompt-traceability | REQ-13 (req_1.0.md:38) | Como custodio SDD, quero 100% dos prompts SDD catalogados em .ai/handoffs/, para auditoria de co-autoria. | Given um handoff emitido; When rodo handoff_parser.py; Then o payload parseia (PASS) e 100% dos prompts ficam catalogados. |
| doc-user-story-014-us-014 tech-docs-openapi | REQ-14 (req_1.0.md:44) | Como dev, quero documentacao tecnica (arquitetura + APIs OpenAPI) revisada, para manutenibilidade. | Given as APIs do MVP; When gero e reviso a documentacao; Then arquitetura e especificacao OpenAPI estao aprovadas em Code Review. |
| doc-user-story-015-us-015 foss-license-compliance | REQ-15 (req_1.0.md:50; P-01) | Como GP, quero 100% das dependencias com licenca OSI-approved, para conformidade FOSS absoluta. | Given uma release; When audito as licencas; Then o relatorio aponta 100% OSI-approved e licença restritiva bloqueia o merge. |

### C.2 Stories com origem LEGADO (candidatas condicionais — requerem ratificacao de pertencimento)

| ID/slug | Origem (LEGADO) | Narrativa (PT-BR) | Criterios candidatos | Condicao |
|---|---|---|---|---|
| doc-user-story-007-us-007 api-failure-fallback | review_rf_rfn.md:31 (RF-05); qwen:20; corrobora REQ-07 | Como usuario, quero fallback para a ultima cotaçao valida com aviso de defasagem quando a API externa falhar, para continuar operando. | Given API externa indisponivel; When tento simular; Then a ultima cotaçao valida e exibida com aviso visual "dados com defasagem". | KG-R-02: comportamento ausente do canonico; PO/CCB ratifica antes de Ready |
| doc-user-story-016-us-016 invoice-lifecycle-draft-finalize | review_rf_rfn.md:34 (RF-08) | Como prestador, quero invoice com estados Rascunho (editavel) e Finalizada (somente leitura), para garantir imutabilidade do documento emitido. | Given invoice em Rascunho; When finalizo; Then todos os campos ficam travados e ediçao e bloqueada. | KG-R-03: "emissao de invoice PDF" (Art. 1.2) implica criacao, mas ciclo de estados nao esta na Tabela 1 IN; CCB decide |
| doc-user-story-017-us-017 invoice-clone-new-number | review_rf_rfn.md:35 (RF-09) | Como prestador, quero clonar uma invoice finalizada em novo rascunho com novo numero unico, para corrigir sem violar a imutabilidade. | Given invoice Finalizada; When clono; Then novo rascunho com numero unico (soldoc-arch-0006-uc-v1ao sem PostgreSQL Sequence — C-04) e data de emissao atual. | Depende de doc-user-story-016-us-016 ratificada; KG-R-03 |

**Notas:** doc-user-story-012-us-012 permanece BLOCKED (gate E). Warmup do WeasyPrint (deepseek:70) entra como
criterio opcional de doc-user-story-004-us-004, marcado legacy-input, se CCB ratificar. Regra RN-03 legada
(sem calculo de dias uteis/feriados — review:17) sobrevive como insumo de doc-user-story-002-us-002/doc-user-story-003-us-003
apenas na clausula "sem calendario corporativo"; a clausula de 2 modalidades esta morta (C-01).

## D. PROPOSTA DE DoR (definition of ready) — alinhada ao Art. 6.2 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60)

Fluxo: Backlog → Ready (DoR) → In Progress (WIP ≤3) → Code Review → Done (DoD).
Base: plano-escopo.md §2.6 (:110-112); Padrão B (OKB §9.3, via plano-escopo.md:114); P-08/P-04/P-10.

A story entra em **Ready** somente com TODOS os itens:
1. [ ] Titulo padrao `N{X}.{Y} — <slug EN>` vinculado a pacote EAP (plano-escopo.md:110);
2. [ ] Contexto ubíquo autocontido em PT-BR (sem dependencia de sessao/memoria);
3. [ ] ≥1 criterio de aceite testavel Given/When/Then (contrato DO #2; AUD: "nao vago");
4. [ ] Rastreabilidade tripla: REQ-NN + fase EAP + objetivo SMART (req_1.0.md:5; plano-escopo.md:110);
5. [ ] Fonte citada por arquivo:linha para TOTAIS as alegacoes (P-08, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:36);
6. [ ] Screen de escopo congelado: story mapeia a REQ-01..15 OU possui deliberaçao CCB registrada (Art. 1.3); item OUT-OF-SCOPE (B.4) = rejeicao imediata;
7. [ ] Estimativa ≤8h (plano-escopo.md:110); card maior → decomposicao por tasklist (ADR-004 draft, AUD-2610-03.md:162-178 — so apos CCB);
8. [ ] Dependencias identificadas, INCLUINDO marcacao de gate pendente (ex.: "blocked-by: ADR-001 re-issuance");
9. [ ] ≥3 labels (tipo, macro-fase MF1..3, area) + milestone vinculada (plano-escopo.md:110);
10. [ ] Screen LGPD: sem PII no card/artefato de agente; dados de produto minimizados (P-04);
11. [ ] Slugs/IDs em EN, narrativa PT-BR (P-10, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:38);
12. [ ] Passagem por Refinement semanal (plano-escopo.md:110).

**WIP ≤3:** aplica-se a coluna In Progress conforme Art. 6.2; se o CCB ratificar E-08
(3/pessoa), a leitura muda — ate la, vale a redacao literal da Constituicao (C-06).

## E. GATES E BLOQUEIOS EXPLICITOS

**GATE-BLOCK (fail-closed, herdado de AUD-2610-03.md:29,249 e contrato §11.5):** a ESPECIFICACAO
FORMAL de produto (spec drafting em .ai/specs/ com criterios de aceite para implementacao,
handoffs para dev, e qualquer codigo) fica **BLOCK** ate que AMBAS as condicoes se cumpram:

1. **Re-emissao/ratificacao CCB das ADRs 001-006** — a camada 3 do Art. 2 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:20)
   esta oca (F-01); qualquer spec que assuma stack, freeze ou fluxo de mudanca cita camada vazia
   (P-08 violado por referencia circular — F-03). Roteiro: AUD-2610-03.md:85,240 (R-00..R-02).
2. **Decisao CCB sobre E-01..E-08** — pendentes (spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md:193-334);
   criticas para requisitos: E-07 (ancora do freeze do Art. 1.3), E-08 (WIP), E-05 (fluxo
   CR→ADR→CCB), E-04 (YAGNI codificado).

**Tambem BLOCKED enquanto o gate durar:** doc-user-story-012-us-012 (ADRs); qualquer escolha de dependencia/stack
(inclusive nomear a API externa de cotaçao — GAP-05); spec de implementacao de doc-user-story-001-us-001..017;
repovoacao de docs/requisitos/requisitos.md, .ai/specs/{tap,eap,requisitos}.md (escrita fora da
custodia desta tarefa e dependente das decisoes 1-2).

**PODE avancar SEM violar o gate** (artefatos de ANALISE, nao de implementacao):
- este review e suas atualizacoes (rastreabilidade, matriz REQ→US);
- backlog DRAFT com as 17 stories candidatas em status `candidate` (nunca `ready`), sem estimativas
  de compromisso e com a nota do Art. 5.1;
- proposta de DoR (secao D) para apreciacao do PO;
- assumptions ledger e interrogacao a PM/PO (spec ladder step 2, contrato §1);
- saneamento de vocabulario no glossario; preparo de templates de handoff (sem dispatch);
- plano de testes conceitual desacoplado de stack (nenhuma ferramenta nomeada como decisão).

**Rationale:** estes artefatos nao contradizem camada superior, nao implementam codigo, nao
escolhem dependencia e mantem kill_switch limpo; adiantam o ciclo SDD (Art. 6.1: especifica →
especifica → implementa → valida) ate a fronteira do gate, sem saltar-la (contrato DON'T #04).

**Rota de escalonamento:** orchestrator (agent-nexus-prime-ultimate) → Humano CCB (Art. 5.1).

## F. KNOWLEDGE GAPS, VALIDACAO E CONFORMIDADE

- **KG-R-01:** igualdade integral entre os 4 espelhos de REQ-01..15 assumida por spot-check
  (REQ-01, REQ-02, REQ-15 conferidos em req_1.0.md, plano-integral:71-85, PDF:809-851,
  doc-readme-0001-readme-canon:151-165); diff integral pendente de ferramenta local (sem nuvem, P-01/P-02).
- **KG-R-02:** pertencimento de fallback/defasagem de cotaçao ao escopo congelado (doc-user-story-007-us-007).
- **KG-R-03:** pertencimento do ciclo de vida/clone de invoice ao Art. 1.2 (doc-user-story-016-us-016/doc-user-story-017-us-017) e
  analogia YAGNI para OS-09 sem norma ratificada.
- **KG-R-04:** parametros operacionais de cache (TTL, limite de API) e do warmup — legado apenas.
  (KGs estruturais herdados: KG-01..KG-04 de AUD-2610-03.md:76-81.)
- **Validacao (quem valida e DoD):** agent-reviewer audita as citaçoes linha-a-linha e a
  testabilidade dos GWT; agent-project-auditor emite parecer se acionado; o Humano decide o
  que vira backlog (Art. 5.1). **DoD deste artefato:** (i) inventario A com origem+estado+
  rastreabilidade por item; (ii) auditoria B com gaps/duplicatas/contradicoes/OUT-OF-SCOPE
  justificados; (iii) 17 stories candidatas com GWT e REQ→US; (iv) DoR proposta (D);
  (v) gates explicitos (E); (vi) arquivo ≤400 linhas; (vii) zero escrita fora deste arquivo.
- **Conformidade:** escrita APENAS em .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md (kill switch
  herdado); nenhum arquivo de lei/plano/TAP/ADR tocado; 100% local, sem nuvem paga (P-01/P-02);
  sem PII (P-04); slugs/IDs EN + narrativa PT-BR (P-10); YAGNI — nenhuma story sem origem
  citada; self-delegation ausente (escalonamento apenas via orchestrator).

## CHANGELOG

- 0.1.0 — 2026-10-25 (WS-3, TA-0004): emissao inicial R1. 15 REQ canonicos inventariados
  (4 espelhos) + 70 itens legados mapeados (3 corpora); 8 gaps, 9 contradicoes, 10 OUT-OF-SCOPE;
  17 stories candidatas (14 canonicas + 3 legacy-informadas; cobertura REQ→US 15/15); DoR
  12 itens; 2 condicoes de BLOCK + 4 KGR declarados.
- 0.1.0 — 2026-11-05 (refinamento de ratificação, Grupo B): frontmatter atualizado ao
  padrão TA-0031 ratificado (adicionado `handoff` em `origin`; `updated` 2026-10-25 →
  2026-11-05; `status: draft` → `ratificada`). Ratificação CCB 05/11/2026 (instrumento
  RAT-2026-11-05-A16, ADR-LOG-012). Aderência ao padrão de nomenclatura
  `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de
  negócio das §0–§F reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

Normalização estrutural (TA-0031, hf-exec-0031): `spec_id` atualizado de `requisitos-review-round-1-1` para `spec-002` (slug `spec_id-specname.spec.md`); conteúdo das §0–§F e do CHANGELOG preservado; nenhuma linha anterior renumerada (referências `arquivo:linha` históricas permanecem válidas).

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-002`, `version: 0.1.0`, `status: ratificada`, `created: 2026-10-25`, `updated: 2026-11-05`, `origin: TA-0004 | handoff: N/A (analyze)`) | aplicada |
| (b) Contexto/origem | parágrafo "Natureza: auditoria + proposta" + §0 (método e convenções) | aplicada |
| (c) Resolução de conflitos | §B.3 (contradições entre fontes) + §B.4 (itens OUT-OF-SCOPE rejeitados) | aplicada |
| (d) Corpo de decisões/requisitos | §A (inventário REQ-01..15 e legado), §B (auditoria), §C (stories), §D (DoR) | aplicada |
| (e) Critérios de aceite/testes | §E (gates e bloqueios explícitos) + critérios de conformidade do §F (lista i–vii) | aplicada |
| (f) Rastreabilidade | §C.1 (REQ → US, cobertura 15/15) + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §B.4 (10 itens fora do escopo congelado, rejeitados) | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
