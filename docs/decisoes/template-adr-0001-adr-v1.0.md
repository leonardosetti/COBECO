---
id: template-adr-0001-adr-v1.0
type: template-adr
title: TEMPLATE ADR — Adr
version: v1.0
status: ratificado
canonical: false
canonical_slug: adr
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
domain: template
layer: template
tags: []
lgpd_class: n/a
workflow:
  stage: ratificado
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# ADR-<NNN> — <Título da Decisão>

**Status:** Proposto | Ratificado | Obsoleto | Substituído por ADR-<MMM>  
**Data:** DD/MM/AAAA  
**Decisores:** CCB (Change Control Board) — FATEC Taquaritinga ADS  
**Autor:** <Nome> (<Papel>)  
**Revisores:** <Nomes>

---

## Contexto

Descreva o problema ou decisão a ser tomada. Quais forças estão em jogo? Quais restrições existem (tempo, orçamento, stack, normas constitdoc-arch-0006-uc-v1ionais)?

---

## Decisão

Descreva a decisão tomada, de forma clara e direta.

### Stack / Tecnologia aprovada

| Camada | Tecnologia | Versão | Justificativa |
|---|---|---|---|
| <camada> | <tecnologia> | <versão> | <justificativa> |

---

## Alternativas consideradas

| Alternativa | Prós | Contras | Motivo da não escolha |
|---|---|---|---|
| <alt 1> |  |  |  |
| <alt 2> |  |  |  |

---

## Consequências

### Positivas
- <ponto positivo 1>
- <ponto positivo 2>

### Negativas (mitigadas)
- <ponto negativo 1> → mitigação: <como mitigar>
- <ponto negativo 2> → mitigação: <como mitigar>

---

## Conformidade com a Constitution

| Artigo | Requisito | Conforme? | Observação |
|---|---|---|---|
| Art. 3.x | Princípio (KISS/Clean Architecture/ACID/YAGNI) | Sim/Não |  |
| Art. 7.x | Segurança (segredos, rate limiting, erros) | Sim/Não |  |
| Art. 8.x | Qualidade (cobertura, testes, DoD) | Sim/Não |  |

---

## Rastreabilidade

- **Origem:** <documento fonte>
- **Requisitos:** RF-XX, UC-YY (req-func-0001-requisitos-funcionais-canon.md / req-use-case-0001-casos-de-uso-canon.md)
- **Especificações SDD:** `.ai/specs/spec-<NNN>.spec.md`
- **Constituição:** Art. X.Y

---

## Aprovação

| Papel | Nome | Assinatura | Data |
|---|---|---|---|
| CCB Chair / Proddoc-arch-0006-uc-v1t Owner |  |  |  |
| Tech Lead |  |  |  |
| Arquiteto de Software |  |  |  |

---

**Fim do ADR-<NNN>**
