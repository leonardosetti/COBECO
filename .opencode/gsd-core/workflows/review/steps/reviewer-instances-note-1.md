---
id: reviewer-instances-note--1
type: reviewer-instances
title: 'REVIEWER INSTANCES — '
version: '1'
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
**Reviewer instances (#1517, optional):** if `review.reviewer_instances` is configured,
instance names in `review.default_reviewers` run as independent identities. Resolution rules
are in `gsd-core/references/reviewer-instances.md` — load it lazily only when instances are
configured. Unconfigured → default path unchanged.
