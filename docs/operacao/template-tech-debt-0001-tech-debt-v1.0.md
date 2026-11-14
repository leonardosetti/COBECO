---
id: template-tech-debt-0001-tech-debt-v1.0
type: template-tech
title: TEMPLATE TECH — 0001 Tech Debt
version: v1.0
status: rascunho
canonical: false
canonical_slug: 0001-tech-debt
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
# Tech Debt Log — COBECO MVP

**Versão:** 1.0  
**Status:** Ativo  
**Data:** DD/MM/AAAA  
**Autor:** <Nome>

---

## Débitos técnicos identificados

| ID | Local (arquivo:linha) | Tipo (TODO / FIXME / Tech Debt) | Descrição | Data | Autor | Issue vinculada | Prioridade |
|---|---|---|---|---|---|---|---|
| TD-01 |  | TODO |  |  |  |  | P0/P1/P2 |
| TD-02 |  | FIXME |  |  |  |  | P0/P1/P2 |

---

## Regras

- Todo TODO/FIXME no código deve ter data, autor e link para issue.
- Tech Debt revisado a cada sprint; itens P0 são bloqueantes para merge.
- Nenhum "para depois" sem issue vinculada (YAGNI, Art. 3.7).

---

## Exemplo de marcação no código

```python
# TODO(TD-01, 13/11/2026, @dev): refatorar uso de asyncmy para aiomysql quando estabilizar (issue #XX)
pass
```

---

**Fim do Tech Debt Log**
