---
id: execute-phase-response--language
type: execute-phase
title: 'EXECUTE PHASE — '
version: language
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
# Execute-Phase Response-Language Directive (#2402)

**If `response_language` is set:** User-facing orchestrator output (questions, narration, report-template prose) in `{response_language}`; technical terms, code, file paths, and subagent prompts stay in English. Pass `response_language: {value}` into every spawned subagent prompt so any user-facing output they produce stays in the configured language.

**The `gsd-verifier` subagent has no workflow file of its own (#2529):** the shared verification step (`workflows/execute-phase/steps/verify-phase-goal.md`, included by execute-phase's `verify_phase_goal` and by verify-work, #5118) reaches it by dispatch, not by reading a workflow, so there is no file in which to place a directive — the dispatch prompt is the only place its coverage can live. That prompt MUST carry this line verbatim, immediately after `Create VERIFICATION.md.` (the shared step's prompt carries it inline, so both callers inject it):

`Use response_language {response_language} for all user-facing prose — narration between tool calls, status updates, progress notes, and findings included; preserve code and paths.`

It lives here rather than inline in `workflows/execute-phase.md` for the same reason the rest of this file does — that workflow is held under the frozen byte ceiling named below, and this `@-reference` is eager, so the orchestrator loads this instruction with the workflow either way.

The literal report templates embedded in this workflow (`## Execution Plan`, `## Phase {X}: {Name} Execution Complete`, `## ⚠ Phase {X}: {Name} — Gaps Found`, etc.) are a structural source, not literal output to copy verbatim — render their prose translated into `{response_language}` while keeping headings' structural markers, table columns, IDs, commands, and file paths unchanged.

This directive was extracted from `workflows/execute-phase.md` to keep that file under the frozen pre-phase-6 byte ceiling (ADR-857 Phase 6 capstone, `tests/claude-orchestration.test.cjs`). The `@-reference` is eager, so the runtime still loads this content alongside the workflow — the extraction is purely a file-size discipline, not a lazy-load optimization.
