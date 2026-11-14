---
id: ai-handoffs-index
title: CATÁLOGO DE HANDOFFS - COBECO v1.0
type: handoff
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/handoffs/INDEX.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- handoffs
- docs
- adequado-a-norma
---
# CATÁLOGO DE HANDOFFS - COBECO v1.0

# Catálogo de prompts SDD (handoffs de despacho) — REQ-13, fase N9.3

Este índice é um **índice de ponteiros**: não replica Contexto/Tarefa/critérios do HF
(Art. 6.7, constitution.md:168). O conteúdo de um prompt lê-se no arquivo HF,
nunca no índice.

Formato de entrada: `- HF-NNNN: <tema> (task: TA-NNNN | target: <agent> | status: <enum>)`

## Entradas

- HF-0010: HF-0010 (task: N/A | target: agent-sdd-specialist | status: ready)
- HF-0022: HF-0022 (task: TA-0022 | target: agent-architect | status: ready)
- HF-0029: SPEC de camadas de containers para a produção ortogonal do COBECO (task: TA-0029 | target: agent-sdd-specialist | status: done)
- HF-0030: Amenda Nginx aceito-e-mantido + comunicação integrada para demo local (TA-0030) (task: TA-0030 | target: agent-sdd-specialist | status: ready)
- HF-0031: Normalização integral do corpus de specs — slug, versionamento, corpo canônico, realocação e pendentes (TA-0031) (task: TA-0031 | target: agent-sdd-specialist | status: ready)
- HF-0032: Auditoria dedicada de registry.yaml e ledger.yaml — circuito de agentes, regras de roteamento, subutilização e desvio de função (TA-0032) (task: TA-0032 | target: agent-project-auditor | status: ready)
- HF-0033: Levantamento de artefatos com status draft para aprovação CCB (TA-0033) (task: TA-0033 | target: agent-project-analyst | status: ready)
- HF-0034: Enriquecimento da lista de specs pendentes com dados propositivos + rodapé com hora e ratificação CCB (TA-0035) (task: TA-0035 | target: agent-sdd-specialist | status: ready)
- HF-0036: HF-0036 (task: TA-0036 | target: agent-sdd-specialist | status: ready)
- HF-0037: HF-0037 (task: TA-0037 | target: agent-architect | status: ready)
- HF-0038: HF-0038 (task: TA-0038 | target: agent-pm | status: ready)
- HF-0039: HF-0039 (task: TA-0039 | target: agent-pm | status: ready)
- HF-0040: HF-0040 (task: TA-0040 | target: agent-project-auditor | status: ready)
- HF-0041: HF-0041 (task: TA-0041 | target: agent-project-auditor | status: ready)
- HF-0042: HF-0042 (task: TA-0042 | target: agent-architect | status: ready)
- HF-0043: HF-0043 (task: TA-0043 | target: agent-pm | status: ready)
- HF-0044: HF-0044 (task: TA-0044 | target: agent-ai-llm-rag-dag-mcp-roster-master-specialist | status: ready)
- HF-0100: HF-0100 (task: TA-0100 | target: agent-project-analyst | status: ready)
- HF-0101: HF-0101 (task: TA-0101 | target: agent-sdd-specialist | status: ready)
- HF-0102: HF-0102 (task: TA-0102 | target: agent-compliance-governance | status: ready)
- HF-0103: HF-0103 (task: TA-0103 | target: agent-devops | status: ready)
- HF-0104: HF-0104 (task: TA-0104 | target: agent-python-specialist | status: ready)
- HF-0105: HF-0105 (task: TA-0105 | target: agent-sldc-process-specialist | status: ready)
- HF-0106: HF-0106 (task: TA-0106 | target: agent-python-specialist | status: ready)
- HF-0107: HF-0107 (task: TA-0107 | target: agent-digital-security | status: ready)
- HF-0108: HF-0108 (task: TA-0108 | target: agent-qa-sdet | status: ready)
- HF-0109: HF-0109 (task: TA-0109 | target: agent-project-auditor | status: ready)
- HF-0110: HF-0110 (task: TA-0110 | target: agent-backend-dev | status: ready)
- HF-0111: HF-0111 (task: TA-0111 | target: agent-backend-dev | status: ready)
- HF-0400: SDDAI Data Loader — Ingestão de Dados (task: N/A | target: agent-sddai-loader | status: ready)
- HF-0401: SDDAI Memory Optimizer — Otimização de Memória (task: N/A | target: agent-sddai-memory | status: ready)
- HF-0402: SDDAI Feature Engineer — Engenharia de Features (task: N/A | target: agent-sddai-engineer | status: ready)
- HF-0403: SDDAI Model Trainer — Treinamento de Modelo (task: N/A | target: agent-sddai-trainer | status: ready)
- HF-0404: SDDAI CLI Orchestrator — Pipeline Unificado (task: N/A | target: agent-sddai-cli | status: ready)
- HF-0500: Scheduler de auditoria de compliance (REQ-13) (task: TA-0100 | target: agent-devops | status: ready)
- HF-0601: HF-0601 — Consulta de dominio: modelo de dados da invoice (B.4/GAP-04) (task: TA-0045 | target: agent-dba | status: emitted)
- HF-0602: HF-0602 — Consulta de dominio: frontend web responsivo (B.1/REQ-06) (task: TA-0046 | target: agent-ui-ux-advisor | status: emitted)
- HF-0603: HF-0603 — Consulta de dominio: UAT de produto e destino de evidencias (B.5/C.5) (task: TA-0047 | target: agent-qa-sdet | status: emitted)
- HF-0604: HF-0604 — Consulta de dominio: CI/CD, drift G-05 e camada CI (B.7/B.10/C.4) (task: TA-0048 | target: agent-devops | status: emitted)
- HF-0605: HF-0605 — Consulta de dominio: qualidade PDCA + Ishikawa 6M (B.6/REQ-10) (task: TA-0049 | target: agent-quality-architect-specialist | status: emitted)
- HF-0606: HF-0606 — Consulta de dominio: LGPD de produto — fundamentos para CCB (B.3/GAP-08) (task: TA-0050 | target: agent-compliance-governance | status: emitted)
- HF-0607: HF-0607 — Emissao spec-006-nfr-consolidados-v1 (B.2/GAP-02) (task: TA-0051 | target: agent-sdd-specialist | status: emitted)
- HF-0608: HF-0608 — Emissao spec-007-invoice-data-model-v1 (B.4/GAP-04) — insumo TA-0045 (task: TA-0052 | target: agent-sdd-specialist | status: emitted)
- HF-0609: HF-0609 — Emissao spec-008-frontend-web-responsive-v1 (B.1/REQ-06) — insumo TA-0046 (task: TA-0053 | target: agent-sdd-specialist | status: emitted)
- HF-0610: HF-0610 — Emissao spec-009-uat-produto-v1 (B.5/REQ-09) — insumo TA-0047 (task: TA-0054 | target: agent-sdd-specialist | status: emitted)
- HF-0611: HF-0611 — Emissao spec-010-qualidade-pdca-ishikawa-v1 (B.6/REQ-10) — insumo TA-0049 (task: TA-0055 | target: agent-sdd-specialist | status: emitted)
- HF-0612: HF-0612 — Emissao spec-011-cicd-pipeline-v1 (B.7/REQ-11) — insumo TA-0048 (task: TA-0056 | target: agent-sdd-specialist | status: emitted)
- HF-0613: HF-0613 — Emissao spec-012-rastreabilidade-prompts-sdd-v1 (B.8/REQ-13) (task: TA-0057 | target: agent-sdd-specialist | status: emitted)
- HF-0614: HF-0614 — Emissao spec-013-documentacao-tecnica-v1 (B.9/REQ-14) (task: TA-0058 | target: agent-sdd-specialist | status: emitted)
- HF-0615: HF-0615 — Emissao spec-014-runtime-agentes-ci-layers-v1 (B.10) — escopo CONFIRMADO pelo orquestrador (task: TA-0059 | target: agent-sdd-specialist | status: emitted)
- HF-0616: HF-0616 — Emissao spec-015-lgpd-produto-proposta-v1 (B.3/GAP-08) — PROPOSTA draft condicionada a CCB (task: TA-0060 | target: agent-sdd-specialist | status: emitted)
- HF-0617: HF-0617 — Emendas C.1+C.2 em spec-004 e C.4+C.5 em spec-005 (lacunas de conteudo) (task: TA-0061 | target: agent-sdd-specialist | status: emitted)
- HF-0618: HF-0618 — Auditoria de integridade da rodada de specs (fechamento) (task: TA-0062 | target: agent-project-auditor | status: emitted)
- HF-0619: HF-0619 — Repovoar .ai/specs/tap.md (A.2) — transcricao da baseline congelada TAP v3 (task: TA-0063 | target: agent-sdd-specialist | status: emitted)
- HF-0620: HF-0620 — Repovoar .ai/specs/eap.md (A.3) — fases N1..N11 com rastreabilidade (task: TA-0064 | target: agent-sdd-specialist | status: emitted)
- HF-0621: HF-0621 — Repovoar .ai/specs/requisitos.md (A.1) (task: TA-0065 | target: agent-sdd-specialist | status: emitted)

## Total: 56 handoffs catalogados

## Regras de manutenção
- Entradas são append-only; correção de entrada errada = nova linha de correção datada,
  nunca reescrita silenciosa (forense: spec history is provable via git).
- Ordenação por id crescente.
- Campos mínimos: id, tema, task, target, status (C-03, spec-012 §3.2).
