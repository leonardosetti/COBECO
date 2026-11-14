---
id: execute-phase-requirement--revert
type: execute-phase
title: 'EXECUTE PHASE — '
version: revert
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
**Revert this phase's own requirement IDs out of `Complete` before rendering the gap report (#2388).** A shared requirement ID can already read `Complete` at this point (its first-declaring plan finished before this verification ran) — a `gaps_found` verdict must not leave that premature `Complete` sitting in REQUIREMENTS.md. Scoped strictly to `PHASE_REQ_IDS` (this phase's own citations from `init.execute-phase`), so another phase's `Complete` row is never todoc-arch-0006-uc-v1hed:

```bash
if [ -n "${PHASE_REQ_IDS}" ]; then
  gsd_run query requirements.revert-phase ${PHASE_REQ_IDS} >/dev/null 2>&1 || true
  gsd_run query commit "docs(phase-{X}): revert premature Complete requirements after gaps found" --files .planning/REQUIREMENTS.md >/dev/null 2>&1 || true
fi
```
