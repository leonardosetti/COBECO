---
id: spec-nfr-0001-nfr-consolidados-v1.0
type: spec-nfr
title: SPEC NFR — Nfr Consolidados
version: v1.0
status: ratificado
canonical: false
canonical_slug: nfr-consolidados
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
spec_id: spec-006
specname: nfr-consolidados-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: HF-0607 (.ai/handoffs/HF-0607-spec-006-nfr-consolidados-v1.md)
task: TA-0051 | handoff: HF-0607 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (NFR consolidados)
lgpd-class: n/a (zero PII neste artefato; P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90 — precedente lgpd-class: spec-002-requisitos-review-round-1.spec.md:19)
trace:
  - .ai/handoffs/HF-0607-spec-006-nfr-consolidados-v1.md:17-29 (tarefa, fontes obrigatórias, contrato de resposta)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:34 (item B.2 — origem desta emissão)
  - .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:78-79,101,105,107,126,249 (RNF embutidos nos REQ; GAP-02/GAP-06/GAP-08; C-07; KG-R-04)
  - docs/planos/plano-granular/plano-integral-tap-1-2-3-4-5.md:30,37,71-85,96,97,520,528,573,595 (EAP 12/37; fase N2.2; REQ-01..15; marcos M2/M3; whitelist de licenças; stack FOSS; métricas de qualidade; PDCA-N7)
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md v1.2.1:78,84-98,102,104,154,156,160,174-180,213-219 (Art. 2.5; P-01..P-08, P-10, P-11; Art. 6.3/6.4/6.5; Art. 7; Art. 10)
  - .ai/specs/spec-tech-0001-backend-mvp-v1.0.md:25,64,107,114,122,134 (contrato API; /v1/health; TTL; orçamento REQ-01; fx_quotes; fail-closed e scanner)
  - .ai/specs/spec-arch-0001-container-layers-v1.0.md:77,81,191,202-212,266-293,315-342,346-352 (cache; camadas L1/CI fora de escopo; healthcheck; §8 CI; US-020/US-021; §12 UAT; YAGNI)
  - docs/planos/plano-granular/plano-escopo.md:71-80 (Tabela 1 IN/OUT)
  - .ai/specs/doc-manifest-0001-manifest-v1.0.md:20-61 (template canônico obrigatório §1)
  - .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:83-103,127-133,180-203 (custódia .ai/specs/; DOs/DON'Ts; template de spec)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)
---

# SPEC spec-006 — nfr-consolidados-v1 — Requisitos Não Funcionais consolidados (registro canônico da fase N2.2 da EAP)

## 1. Contexto e origem

Esta spec nasce da tarefa TA-0051, via handoff HF-0607 emitido por agent-nexus-prime-ultimate
(.ai/handoffs/HF-0607-spec-006-nfr-consolidados-v1.md:17-25), e implementa o item **B.2** da
LISTA-SPECS-PENDENTES-2026-11-02.md:34. Ela fecha o **GAP-02** (spec-002-requisitos-review-round-1.spec.md:101):
a EAP previa a fase **N2.2 "Requisitos Não Funcionais"** (N2.2 integrada a N2. Levantamento de Requisitos,
MF1 — plano-integral-tap-1-2-3-4-5.md:37; referência PDF:645 sob a convenção PDF:N do dump pdftotext,
spec-002-...spec.md:29, forwarding via spec-002-...spec.md:101 e LISTA...:34) **sem artefato**.

A fonte da lacuna é explícita: "RNF canonicos estao EMBUTIDOS como criterios de aceite de REQ-05
(performance), REQ-08 (qualidade), REQ-11 (CI), REQ-15 (FOSS) — nao existe registro NFR separado"
(spec-002-...spec.md:78-79). O objetivo desta emissão é registrar esses critérios dispersos — e os
princípios P-01..P-08 da constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84-98 — como **fonte única de verificação não funcional**
(HF-0607:17), mapeando **P-04, P-06 e P-07 a critérios de produto** (HF-0607:17; LISTA...:34).

Limites declarados: (i) este é um **registro NFR**, não spec executiva de domínio — UAT de produto
(B.5, LISTA...:37), CI/CD executiva (B.7, LISTA...:39) e LGPD de produto executiva (B.3, LISTA...:35)
têm specs próprias pendentes; (ii) nada aqui decide: em conflito, vale a hierarquia Art. 2.1/2.5
(resolução de cima para baixo, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78); (iii) ausência de métrica citável = literal
`UNKNOWN - verify` (P-08, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98; MANIFEST.md:58).

## 2. Resolução de conflitos

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| Latência REQ-01 ≤2s × REQ-05 ≤3s sem camadas explícitas | Sem decisão nova nesta spec: ambiguidade registrada como C-07, com "leitura provável: 2s=chamada API, 3s=E2E; requer explicitação na spec (não contradição, ambiguidade)" — confirmação PO/CCB pendente; NF-01 e NF-02 adotam a leitura declarada pela fonte, marcada como tal | spec-002-...spec.md:126 (registro C-07) | "latencia cotação ≤2s" × "aplicacao ≤3s P95" sem camadas (req_1.0.md:11,15, via spec-002-...spec.md:62,66) |
| Persistência do cache: REQ-07 rotulado "SQLite" (plano-integral...:77; Tabela 1 OUT PostgreSQL, plano-escopo.md:76) × stack canônica PostgreSQL + cache em memória + tabela `fx_quotes` | Hierarquia resolve de cima para baixo (Art. 2.5, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78): constituição v1.2.0+ declara PostgreSQL canônico (Art. 10.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213); estado já consagrado por spec-004-backend-mvp-v1.spec.md:107,122 e camada de cache separada recusada por YAGNI (spec-005...:77). O critério numérico REQ-07 (redução ≥50%) permanece íntegro (NF-04) | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 + spec-005-container-layers-v1.spec.md:77 | plano-integral-tap-1-2-3-4-5.md:77; plano-escopo.md:76 |
| G-05 "`ci.yml` vazio" × arquivo real com 189 linhas e 6 jobs, porém sem build Docker e com `timeout-minutes: 15` no `test-suite` | Prevalece o estado verificado (P-08): o delta de G-05 está declarado e não contornado na spec-005 §8; NF-19 herda o delta como meta não atendida | spec-005-container-layers-v1.spec.md:202,208 | docs/planos/plano-granular/plano-proddoc-arch-0006-uc-v1ao-agentes.md:33 |
| Drift de citação constitdoc-arch-0006-uc-v1ional: spec-002 cita P-06/P-08 em constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:34,36 e P-04 em :36 | Prevalece o layout atual verificado da constituição v1.2.1 (restauração de 29/10/2026, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:21): P-04=:90, P-06=:94, P-07=:96, P-08=:98. As citações de spec-002 são tratadas como forwarding histórico; esta spec cita o arquivo:linha atual em toda alegação | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90,94,96,98 (v1.2.1) | spec-002-requisitos-review-round-1.spec.md:101,107 |

Nenhum outro conflito normativo conhecido entre as fontes citadas nesta emissão; se surgir tensão
não registrada acima, marcar `UNKNOWN - verify` e escalar ao arquiteto (Art. 2.5, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).

## 3. Requisitos não funcionais consolidados (NF-01..NF-25)

Convenção: cada NF carrega descrição, métrica mensurável (quando a fonte a fornece; lacuna =
`UNKNOWN - verify`) e rastreabilidade `arquivo:linha`. Categorias conforme o mandato da tarefa
(HF-0607:17; LISTA...:34).

### 3.1 Desempenho

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-01 | Latência de cotação cambial externa — REQ-01; leitura de camada por C-07: ≤2s aplica-se à chamada à API externa (pendência de confirmação PO/CCB) | ≤2s (plano-integral...:71; spec-002...:62,126); orçamento interno já fixado: 1,9s total por requisição com timeouts por provedor (spec-004...:114) | REQ-01, fase N5.2 (plano-integral...:71); spec-004-backend-mvp-v1.spec.md:114 |
| NF-02 | Tempo de resposta da aplicação (E2E, por C-07) — REQ-05 | ≤3s em 95% das requisições, ambiente homologação, marco M3; p95 (plano-integral...:75,573) | REQ-05, fase N5.1 (plano-integral...:75); spec-002...:66 |
| NF-03 | Geração de invoice PDF via WeasyPrint — REQ-04 | ≤3s por documento (plano-integral...:74); verificação binária em UAT F-03, sem PII em logs (spec-005...:325) | REQ-04, fase N5.4 (plano-integral...:74); spec-002...:65 |
| NF-04 | Eficiência de chamadas externas: cache de cotações reduz a dependência da API — REQ-07 (rótulo "SQLite" superado — §2) | redução ≥50% das chamadas à API externa (plano-integral...:77); TTL 3600s fixado (`COBECO_RATE_TTL_SECONDS`, spec-004...:107); parâmetros além do TTL: GAP-06/KG-R-04 — legado apenas (spec-002...:105,249) → `UNKNOWN - verify` | REQ-07, N5.2 (plano-integral...:77); spec-004...:107,122; spec-005...:77 |

### 3.2 Usabilidade

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-05 | Interface web responsiva 100% FOSS sem quebra funcional — REQ-06 (US-005) | "o layout responde sem quebra funcional" em Chrome/Firefox/Edge últimas 2 versões (plano-integral...:76; spec-002...:67,162) | REQ-06, fase N5.3 (plano-integral...:76) |
| NF-06 | Protótipo UX/UI aprovado e artefatos de modelagem versionados — fase N3.2 | aprovação no marco M2 ("Pipeline CI 'verde' e artefatos de modelagem versionados", plano-integral...:96) | fase N3.2 (plano-integral...:38); M2 (plano-integral...:96) |

### 3.3 Segurança — P-07/OWASP (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96) + Art. 7

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-07 | Baseline OWASP com falha por padrão (fail-closed): ausência de `COBECO_DATABASE_URL` impede startup; `db` indisponível degrada em erro canônico 503, sem crash/traceback | binário: fail-closed verificável no startup (spec-004...:134) e no fluxo F-05 da UAT (spec-005...:327, que cita spec-004-backend-mvp-v1.spec.md:89-93) | P-07 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96); spec-004...:134 |
| NF-08 | Nenhuma credencial real versionada; credencial real em repositório é incidente; apenas chaves dummy (ex.: `sk-local-dummy-key`) para serviços locais; scanner do CI rejeita `password=` literal em `.py`/`.yml`/`.yaml` | zero credencial real no repositório — gate de CI (ci.yml:50-59, via spec-005...:204; spec-004...:134) | P-07 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96); Art. 7.2 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:176) |
| NF-09 | Zero Trust e menor privilégio em secrets/scopes; serviços externos (cloud free tier) apenas para dados não sensíveis, com whitelist registrada, transporte cifrado, ausência de PII e rota de reversão local | métrica quantitativa: `UNKNOWN - verify` (a fonte é norma, não métrica) | Art. 7.1/7.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:174,180); Art. 10.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:217); P-02 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86) |
| NF-10 | Hardening de containers: non-root, `no-new-privileges`, `cap_drop ALL`, `read_only`+tmpfs, portas do host em `127.0.0.1`, imagens por digest; segredo/PII nunca em camada de imagem | 100% dos controles presentes por camada — UAT F-07 binário (spec-005...:274,329; Art. 10.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215) | US-020 (spec-005...:266-278); P-07 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96) |

### 3.4 Portabilidade e FOSS — P-01/P-02 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84,86)

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-11 | Licenciamento 100% FOSS — REQ-15: toda dependência OSI-approved; licença restritiva bloqueia o merge | 100% OSI-approved em relatório de auditoria (US-015, spec-002...:171); whitelist fechada: MIT, Apache 2.0, BSD 2/3-clause, GPL v2/v3, LGPL, ISC, PSF, Public Domain (plano-integral...:520) | REQ-15, fases N1.5+N4.4 (plano-integral...:85); P-01 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84) |
| NF-12 | FOSS-ZERO-COST: dependência FOSS e custo recorrente zero; exceção proprietária somente via Bypass Protocol de 3 pilares registrado | custo recorrente R$ 0,00 — alerta preventivo em qualquer valor > 0 (plano-integral...:535) | P-01 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84); Tabela 1 OUT "serviços pagos" (plano-escopo.md:80) |
| NF-13 | Soberania computacional local: inferência primária 100% local (`Qwen3-30B-A3B Q4_K_M` via llama.cpp, 8700G); cloud free tier da whitelist apenas para tarefas não sensíveis; em falha/risco prevalece o local | configurável/auditável; métrica quantitativa: `UNKNOWN - verify` | P-02 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86); L1 (Art. 6.5, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:160) |
| NF-14 | Portabilidade do produto: acesso desktop web em ambiente local/homologação; app mobile nativo e hospedagem pública/keep-alive são OUT | ambiente-alvo: desktop (REQ-06, plano-integral...:76); OUT binário (OS-06/OS-08, spec-002...:139,141) | P-02 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86); OS-08 "sem cloud paga" (spec-002...:141) |

### 3.5 LGPD — P-04 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90) — mapeamento a critérios de produto

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-15 | LGPD primária: mínimo necessário, sem PII em artefatos técnicos de agentes, direito ao esquecimento por design (texto literal de P-04 aplicado ao produto) | `UNKNOWN - verify` (P-04 é norma; métrica de produto pendente da spec B.3) | P-04 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90); GAP-08 (spec-002...:107) |
| NF-16 | Dados demonstrativos sem dados reais de terceiros sem consentimento documentado; sem PII em logs/volumes (inclui logs da emissão de PDF e da degradação 503) | binário: varredura de logs/artefatos sem PII (US-020 AC 2, spec-005...:275; F-03/F-05 "sem PII", spec-005...:325,327) | Art. 7.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:178); Art. 10.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:217) |
| NF-17 | Export externo sem PII: nenhum dado pessoal/financeiro trafega para serviço de terceiros; cloud free tier somente dados não sensíveis | binário: auditoria de whitelist + ausência de PII (Art. 7.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:180) | P-03 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:88); Art. 7.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:180) |

**Fronteira LGPD:** o mapeamento desta seção registra os critérios constitdoc-arch-0006-uc-v1ionais; a
especificação executiva de LGPD de produto (minimização/tratamento em invoice e logs) é o item
B.3 (LISTA...:35), condicionada a decisão prévia de CCB/PO (GAP-08, spec-002...:107) — não emitida
aqui por ausência de decisão citável (P-08).

### 3.6 Manutenibilidade

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-18 | Cobertura de testes automatizados — REQ-08 (US-008); merge sem rastreabilidade proibido; portões reviewer → gatekeeper compulsórios | ≥80% (`pytest`+`coverage.py`, plano-integral...:78); fail-closed: `--cov-fail-under=80` (ci.yml:170, via spec-005...:204,289) | P-06 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94); Art. 10.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219); spec-002...:69,164 |
| NF-19 | Feedback de CI: lint+testes por push com falha bloqueando merge — REQ-11 (US-011); taxa de sdoc-arch-0006-uc-v1esso do pipeline ≥95% semanal | ≤5min por push (plano-integral...:81,595); **estado hoje não atende**: `test-suite` com `timeout-minutes: 15` (ci.yml:111) — delta G-05 declarado, não contornado (spec-005...:208) | REQ-11, fase N7.1 (plano-integral...:81); spec-002...:72,167 |
| NF-20 | Documentação técnica consolidada (arquitetura + OpenAPI) revisada e aprovada em Code Review — REQ-14; documentação acompanha código | aprovação em Code Review (US-014, spec-002...:170); OpenAPI já coberta por spec-004 §3 (LISTA...:41) | REQ-14, fase N11.1 (plano-integral...:84); Art. 6.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:156) |
| NF-21 | Toda decisão não trivial gera ADR/registro; mínimo 3 ADRs — REQ-12; silêncio documental é defeito | ≥3 ADRs com conteúdo não vazio versionados (US-012, spec-002...:168) — **BLOCKED** pelo gate E (spec-002...:208-224) | P-05 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:92); plano-integral...:82 |
| NF-22 | Dívida técnica controlada: código sem teste correspondente é Technical Debt declarado em backlog; análise estática via SonarQube Free Tier | Technical Debt Ratio <5% por marco (plano-integral...:573); Art. 6.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:154) | Art. 6.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:154); plano-integral...:573 |

### 3.7 Observabilidade e auditabilidade

| ID | NFR | Métrica mensurável (fonte) | Rastreabilidade |
|---|---|---|---|
| NF-23 | Healthcheck da aplicação: `GET /v1/health` → 200; `front` alcança `back:8000/v1/health` (topologia local; sem hospedagem pública — OS-08 rejeitado) | binário 200 (spec-004...:64; spec-005...:191) | spec-004-backend-mvp-v1.spec.md:64; OS-08 (spec-002...:141) |
| NF-24 | Evidências de qualidade nativas, sem dashboard próprio (decisão GMV): GitHub Actions + coverage.py como fonte de evidência para o avaliador | evidência = runs do Actions + relatórios de cobertura (plano-integral...:573) | plano-integral...:573 (GMV) |
| NF-25 | Auditabilidade do cálculo financeiro — REQ-03: cálculo auditável com precisão de 2 casas decimais e trilha auditável (US-003); fórmula fixada em spec-004 §2, ratificada via ADR-016 (RAT-2026-11-05-A16) | 2 casas decimais + trilha do cálculo (plano-integral...:73; US-003, spec-002...:160); fórmula ratificada via ADR-016 (RAT-2026-11-05-A16) | REQ-03, fase N5.1 (plano-integral...:73); spec-002...:160 |

## 4. Critérios de aceite e testes

Critérios verificáveis desta emissão (formato checkbox, contrato DO #2 —
.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:85):

- [ ] AC-01: o arquivo `.ai/specs/spec-nfr-0001-nfr-consolidados-v1.0.md` existe com frontmatter conforme MANIFEST §1.1 (spec_id, specname, version, status, custody, created/updated, origin, task/sender, kill_switch, trace, lgpd-class — .ai/specs/doc-manifest-0001-manifest-v1.0.md:27-44) e ≤400 linhas (contrato DO #3, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:86).
- [ ] AC-02: a fase N2.2 da EAP passa a ter artefato NFR canônico correspondente — verificação: existência deste arquivo + citação direta plano-integral-tap-1-2-3-4-5.md:37 + referência ao GAP-02 (spec-002...:101) — fecha o item B.2 (LISTA...:34).
- [ ] AC-03: P-04, P-06 e P-07 estão mapeados a ≥1 NF cada, com citação do arquivo:linha atual (P-04=constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90; P-06=:94; P-07=:96) — seções 3.5, 3.6 (NF-18) e 3.3.
- [ ] AC-04: 100% dos NF-01..NF-25 possuem rastreabilidade `arquivo:linha`; todo NF sem métrica mensurável em fonte traz o literal `UNKNOWN - verify` (NF-09, NF-13, NF-15; parâmetros de cache além do TTL em NF-04).
- [ ] AC-05: nenhum NF contradiz camada superior (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md > TAP congelado > ADRs — Art. 2.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:43-45); tensões conhecidas registradas na tabela §2 com fonte vencedora (Art. 2.5, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).
- [ ] AC-06: zero PII neste artefato (P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90); kill_switch herdado sem instrução de bypass de gate (kill switch vetos 3-4, .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md:42-43).
- [ ] AC-07: validação — **quem valida:** agent-reviewer audita citações linha-a-linha e a testabilidade dos ACs (padrão de validação declarado em spec-002...:251-256); **DoD desta spec:** (i) 25 NFRs categorizados em 7 categorias; (ii) tabela §2 preenchida com fontes; (iii) AC-01..AC-06 verificáveis; (iv) arquivo único criado sob .ai/specs/, nenhum outro arquivo editado, nada commitado.

## 5. Rastreabilidade

| NF(s) | REQ/Princípio/Fase EAP | Fonte primária |
|---|---|---|
| NF-01..NF-04 | REQ-01 (N5.2), REQ-05 (N5.1), REQ-04 (N5.4), REQ-07 (N5.2) | plano-integral-tap-1-2-3-4-5.md:71,75,74,77 |
| NF-05..NF-06 | REQ-06 (N5.3); fase N3.2 | plano-integral...:76,38 |
| NF-07..NF-10 | P-07; Art. 7; Art. 10.2 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96,174-180,215 |
| NF-11..NF-14 | REQ-15 (N1.5+N4.4); P-01/P-02; Tabela 1 OUT | plano-integral...:85,520; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84,86; plano-escopo.md:80 |
| NF-15..NF-17 | P-04; P-03; Art. 7.3/7.4; GAP-08 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90,88,178,180; spec-002...:107 |
| NF-18..NF-22 | REQ-08 (N6.1), REQ-11 (N7.1), REQ-14 (N11.1), REQ-12 (N9.1); P-05/P-06; Art. 6.3/6.4 | plano-integral...:78,81,84,82; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:92,94,154,156 |
| NF-23..NF-25 | REQ-03 (N5.1); GMV; healthcheck | plano-integral...:73,573; spec-004...:64 |

Rastreabilidade da emissão: tarefa TA-0051 ← HF-0607 (.ai/handoffs/HF-0607-spec-006-nfr-consolidados-v1.md:17) ← item B.2 (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:34) ← GAP-02 (spec-002...:101) ← RNF embutidos nos REQ (spec-002...:78-79). Covização REQ→US que ancora NF-01..NF-25: spec-002 §C.1 (spec-002...:158-171). Adjacências NÃO cobertas aqui: fase N2.3 (conversão REQ→User Story — GAP-07, spec-002...:106; E.4, LISTA...:70) e fases N6.x/N7.1 (specs B.5/B.7, LISTA...:37,39).

## 6. Fora de escopo (YAGNI)

- Testes de carga/estresse (20 usuários k6/Locust) — OS-07 rejeitado (spec-002...:140); "Testes de carga ou estresse" OUT na Tabela 1 (plano-escopo.md:77).
- Hospedagem pública + keep-alive `/health` — OS-08 rejeitado (spec-002...:141).
- App mobile nativo — OS-06 rejeitado (spec-002...:139); OUT na Tabela 1 (plano-escopo.md:75).
- Dashboard próprio de métricas de qualidade — decidido GMV: GitHub Insights + coverage.py + pytest bastam (plano-integral...:573).
- Continuous deployment para produção — OUT na Tabela 1 (plano-escopo.md:78).
- Especificação executiva de LGPD de produto (B.3) — condicionada a CCB/PO (LISTA...:35; GAP-08, spec-002...:107); aqui há apenas o mapeamento constitdoc-arch-0006-uc-v1ional (§3.5).
- Specs executivas de UAT de produto (B.5) e CI/CD (B.7) — LISTA...:37,39; esta spec apenas mapeia os critérios (NF-10, NF-19, NF-23..NF-25).
- Novas métricas/limiares NFR sem fonte citável — vedado por P-08 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:98); lacunas marcadas `UNKNOWN - verify` (NF-09, NF-13, NF-15).
- Qualquer código, compose, workflow ou ADR alterado por esta emissão (Art. 6.1 — implementação é onda seguinte; padrão spec-005...:348).

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0051 / HF-0607): emissão inicial. Registro canônico de NFR (item B.2, LISTA...:34): 25 NFRs (NF-01..NF-25) em 7 categorias (desempenho, usabilidade, segurança P-07/OWASP, portabilidade/FOSS P-01/P-02, LGPD P-04, manutenibilidade, observabilidade); GAP-02 coberto — fase N2.2 (plano-integral...:37) com artefato; P-04/P-06/P-07 mapeados a critérios de produto (AC-03); 4 tensões registradas na §2; lacunas de métrica marcadas `UNKNOWN - verify` (NF-09, NF-13, NF-15, cache além do TTL em NF-04). Arquivo único; nada commitado.
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo A): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `trace`; `version` 0.1.0 → 0.2.0). ADR-016 D4 (RAT-2026-11-05-A16-D4) incorporada: NF-25 menciona fórmula spread/IOF ratificada. NFR de cotação (NF-01..NF-04) alinhadas com spec-004 v1.2.0 e spec-005 v0.4.0. Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio de §§1–6 reescrita. **Ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)**.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-006`, `version: 0.2.0`, `status: draft`, `created/updated: 2026-11-03`/`2026-11-05`, `origin: HF-0607`, `task: TA-0051`) | aplicada |
| (b) Contexto/origem | §1 Contexto e origem | aplicada |
| (c) Resolução de conflitos | §2 (tabela tema→decisão→fonte vencedora→texto superado) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (NF-01..NF-25 em 3.1–3.7) | aplicada |
| (e) Critérios de aceite/testes | §4 (AC-01..AC-07 com validação/DoD) | aplicada |
| (f) Rastreabilidade | §5 + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §6 | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
