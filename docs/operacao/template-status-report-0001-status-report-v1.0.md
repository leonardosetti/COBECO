---
id: template-status-report-0001-status-report-v1.0
type: template-status
title: TEMPLATE STATUS — 0001 Status Report
version: v1.0
status: rascunho
canonical: false
canonical_slug: 0001-status-report
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:14863508
ratified_at: '2026-11-14'
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
domain: general
layer: artifact
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Status Report Semanal — <NOME DO PROJETO>

**Semana:** <N> (DD/MM/AAAA a DD/MM/AAAA)  
**Sprint Atual:** S<X> (Dia <Y> de <Z>)  
**Data do Relatório:** DD/MM/AAAA  
**Autor:** Proddoc-arch-0006-uc-v1t Owner  
**Distribuição:** Equipe + Orientador + Coordenação (conforme Plano de Comunicação)  
**Classificação:** Interno — Dados Sintéticos Apenas (LGPD)

---

## 1. Resumo Executivo (TL;DR)

| Indicador | Status | Tendência | Comentário |
|-----------|--------|-----------|------------|
| **Saúde Geral do Projeto** | 🟢 Verde / 🟡 Amarelo / 🔴 Vermelho | ⬆️ Melhorando / ➡️ Estável / ⬇️ Piorando | <Uma frase> |
| **Cronograma (Schedule)** | 🟢 No prazo / 🟡 Risco / 🔴 Atrasado | | <Dias de avanço/atraso vs baseline> |
| **Escopo (Scope)** | 🟢 Estável / 🟡 Mudanças controladas / 🔴 Scope creep | | <CRs aprovados/pendentes> |
| **Qualidade (Quality)** | 🟢 ≥80% cov / 🟡 60-79% / 🔴 <60% | | `pytest --cov` atual: XX% |
| **Riscos (Risks)** | 🟢 Controlados / 🟡 Atenção / 🔴 Críticos | | <Riscos ALTA exposição abertos> |
| **Equipe (Team)** | 🟢 Completa / 🟡 1 ausência / 🔴 >1 ausência | | <Disponibilidade da semana> |

**Status Geral:** 🟢 **VERDE** — Projeto no trilho, riscos mitigados, equipe completa.

---

## 2. Progresso da Sprint Atual (S<X>)

### 2.1 Backlog da Sprint (Issues no GitHub Projects)

| Issue ID | Título | Status | % Concluído | Responsável | Comentário |
|----------|--------|--------|-------------|-------------|------------|
| #<NNN> | <Título da US/Task> | ✅ Done / 🔨 In Progress / 👀 Review / 📋 Backlog | 100% / 50% / 0% | <Nome> | <Bloqueio? Próximo passo?> |

### 2.2 Burndown / Velocity

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| **Story Points Planejados (Sprint)** | <SP> | — | — |
| **Story Points Concluídos** | <SP> | 100% planejado | 🟢/🟡/🔴 |
| **Velocity da Sprint (SP/dia)** | <SP/dia> | ≥ <meta> | 🟢/🟡/🔴 |
| **Dias Restantes na Sprint** | <N> | — | — |
| **Projeção de Conclusão** | <Data> | Fim da Sprint | 🟢/🟡/🔴 |

> **Gráfico Burndown:** *(Inserir imagem ou link para GitHub Projects Insights)*

---

## 3. Entregas da Semana (Done)

| Entregável | RF/UC | Spec/Handoff | Branch/PR | Testes | Deploy Tag |
|------------|-------|--------------|-----------|--------|------------|
| <Ex.: UC09 Cadastrar Usuário> | RF01/UC09 | spec-004/HF-0500 | `feat/UC-09` / PR#12 | Unit: 92% | v0.1.0-rc1 |

---

## 4. Próximos Passos (Próxima Semana)

| Atividade | RF/UC | Responsável | Prazo | Dependência |
|-----------|-------|-------------|-------|-------------|
| <Ex.: UC10 Login JWT> | RF02/UC10 | Dev Back 1 | DD/MM | UC09 Done |

---

## 5. Impedimentos / Bloqueios (Issues Abertos no RAID)

| RAID ID | Descrição | Severidade | Desde | Ação Necessária | Dono | Ajuda Precisa? |
|---------|-----------|------------|-------|-----------------|------|----------------|
| I-<NNN> | <Descrição> | 🔴 Crítica / 🟡 Alta / 🟢 Média | DD/MM | <Ação> | <Nome> | Sim/Não |

---

## 6. Riscos Atualizados (Top 5 da Semana)

| Risco ID | Risco | Exposição | Mudança vs Semana Passada | Mitigação Ativa |
|----------|-------|-----------|---------------------------|-----------------|
| R-001 | Atraso Sprint 1 | ALTA | ➡️ Estável | Pair programming Auth, docs paralelas |
| R-002 | Cobertura < 80% | ALTA | ⬆️ Aumentou (era MÉDIA) | TDD obrigatório, meta intermediária 60% fim S2 |

---

## 7. Decisões Tomadas (CRs / ADRs / RFCs da Semana)

| ID | Título | Tipo | Decisão | Impacto |
|----|--------|------|---------|---------|
| CR-<NNN> | <Título> | Change Request | Aprovado / Rejeitado / Em análise | <Escopo/Prazo/Custo> |
| ADR-<NNN> | <Título> | Architecture Decision | Ratificado | <Arquitetura> |

---

## 8. Métricas de Qualidade (Quality Gates)

| Métrica | Valor Atual | Meta | Gate | Status |
|---------|-------------|------|------|--------|
| Cobertura Testes Unitários | XX% | ≥ 80% | Gate 3 | 🟢/🟡/🔴 |
| Testes E2E Passando | XX/YY | 100% críticos | Gate 3 | 🟢/🟡/🔴 |
| CI Pipeline Tempo | XXXs | < 300s | Contínuo | 🟢/🟡/🔴 |
| Lint (ruff) | 0 erros | 0 | Contínuo | 🟢/🟡/🔴 |
| Type Check (mypy) | 0 erros | 0 | Contínuo | 🟢/🟡/🔴 |
| Segurança (bandit/secrets) | 0 achados | 0 | Contínuo | 🟢/🟡/🔴 |

---

## 9. Comunicação e Stakeholders

| Stakeholder | Contato da Semana | Assunto | Próximo Contato |
|-------------|-------------------|---------|-----------------|
| Orientador | Reunião 30min DD/MM | Sprint Review S<X> | DD/MM (próxima) |
| Coordenação | Email DD/MM | Status Report Semana <N> | DD/MM (mensal) |
| Equipe | Daily standup 15min | Progresso, impedimentos | Amanhã |

---

## 10. Aprovação / Ciência

| Papel | Nome | Ciência (✓) | Comentário | Data |
|-------|------|-------------|------------|------|
| Proddoc-arch-0006-uc-v1t Owner | | | | DD/MM/AAAA |
| Tech Lead | | | | DD/MM/AAAA |
| Orientador | | | | DD/MM/AAAA |

---

## Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | DD/MM/AAAA | PO | Criação — Semana <N> |

---

**Fim do Status Report Semana <N>**  
*Enviar por email + commit no repo `docs/operacao/STATUS-REPORT-S<N>-<YYYYMMDD>.md`*