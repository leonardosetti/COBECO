---
id: template-test-plan-0001-test-plan-v1.0
type: template-test
title: TEMPLATE TEST — 0001 Test Plan
version: v1.0
status: rascunho
canonical: false
canonical_slug: 0001-test-plan
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
# Test Plan — <Nome da Funcionalidade / Release>

**Documento:** Test Plan / QA Sign-off  
**Versão:** 1.0  
**Status:** Draft | Aprovado | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome> (QA / SDET)  
**Release:** <versão> | **Sprint:** S<X>

---

## 1. Objetivo

Validar que os requisitos funcionais e não funcionais atendem aos critérios de aceite antes do deploy.

---

## 2. Estratégia de testes

| Tipo | Ferramenta | Cobertura alvo | Ambiente |
|---|---|---|---|
| Unitário | pytest | ≥ 80% nos módulos tocados | Local / CI |
| Integração | pytest + MySQL | Cenários críticos | Local / CI |
| E2E | Playwright | Fluxo demo (cadastro → comparação → PDF) | Local |

---

## 3. Cenários de teste

| ID | Requisito (RF) | Cenário | Resultado esperado | Status |
|---|---|---|---|---|
| TC-01 | RF01 | Cadastrar usuário com senha válida | Usuário criado, JWT emitido |  |
| TC-02 | RF02 | Login com credenciais corretas | Access token (15m) + refresh cookie |  |
| TC-03 | RF15 | Calcular orçamento com 2+ fornecedores | Tabela flat, preço total |  |
| TC-04 | RF17 | Exportar PDF | `lista_YYYYMMDD.pdf` válido, A4 |  |

---

## 4. Critérios de aceitação (DoD)

- [ ] Testes unitários escritos; cobertura não diminuiu
- [ ] CI verde (`ruff` + `pytest --cov` + `mypy`)
- [ ] E2E verde em `docker compose up`
- [ ] Code review rubrica R-01..R-07 aprovado
- [ ] Aprovação humana do CCB

---

## 5. Rastreabilidade

- **req-func-0001-requisitos-funcionais-canon.md:** RF-XX
- **req-use-case-0001-casos-de-uso-canon.md:** UC-YY
- **SPEC:** `.ai/specs/spec-<NNN>.spec.md`
- **Handoff:** `.ai/handoffs/HF-<NNNN>.md`

---

## 6. QA Sign-off

| Papel | Nome | Decisão | Data | Assinatura |
|---|---|---|---|---|
| QA / SDET |  |  |  |  |
| Tech Lead |  |  |  |  |

---

**Fim do Test Plan**
