---
id: reviewer-instances-note--2
type: reviewer-instances
title: 'REVIEWER INSTANCES — '
version: '2'
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
**Reviewer instances (#1517, optional):** instances resolve *through* a lane and are not lanes
themselves (ADR-2782 D8). Each selected instance invokes its base `cli` with its own `model`/`agent`
as opaque argv. Exact invocation in `gsd-core/references/reviewer-instances.md`.
