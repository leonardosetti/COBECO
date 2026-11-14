---
id: research-only-early--exit
type: research-only
title: 'RESEARCH ONLY — '
version: exit
status: rascunho
canonical: false
canonical_slug: ''
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
### Research-Only Early Exit (`--research-phase`)

**Skip if:** `RESEARCH_ONLY` is `false` (the default).

**If `RESEARCH_ONLY=true`:** the user invoked `/gsd-plan-phase --research-phase <N>` for research-only mode. Do **not** continue to Section 5.5+ (validation strategy, planner, plan-checker, verification, gaps, bounce, post-planning-gaps). Print the research-complete summary and exit cleanly:

```text
✓ Research-only mode complete (#3042)

  Phase:       ${PHASE}
  RESEARCH.md: ${research_path}

Re-run /gsd-plan-phase ${PHASE} to plan the phase using this research,
or /gsd-plan-phase ${PHASE} --research to refresh research and plan.
```

This exits the workflow. The planner / plan-checker / verifier blocks below are skipped.
