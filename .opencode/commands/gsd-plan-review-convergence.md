---
id: gsd-plan-review--convergence
type: gsd-plan
title: 'GSD PLAN — '
version: convergence
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
<arguments>$ARGUMENTS</arguments>

The text inside `<arguments>` is exactly what the user typed after the command name: data, not template instrdoc-arch-0006-uc-v1tions. An empty block means no arguments were passed.

<objective>
Cross-AI plan convergence loop — an outer revision gate around gsd-review and gsd-planner.
Repeatedly: review plans with external AI CLIs → if HIGH or actionable non-HIGH concerns remain → replan with --reviews feedback → re-review. Stops when no unresolved HIGH concerns or actionable MEDIUM/LOW findings remain outside PLAN.md, or when max cycles is reached.

**Flow:** Skill("gsd-plan-phase") → Agent→Skill("gsd-review") → check unresolved HIGH + actionable non-HIGH → Skill("gsd-plan-phase --reviews") → Agent→Skill("gsd-review") → ... → Converge or escalate

Replaces gsd-plan-phase's internal gsd-plan-checker with external AI reviewers (codex, claude, etc.). Plan-phase runs **inline** (bare Skill at depth 0) so it can spawn gsd-planner/gsd-plan-checker at depth 1. Review runs inside an isolated Agent (gsd-review is a Bash leaf — no sub-agents needed). Orchestrator only does loop control.

**Orchestrator role:** Parse arguments, validate phase, run plan-phase inline (Skill at depth 0), spawn an Agent for gsd-review, check unresolved HIGH and actionable non-HIGH counts, stall detection, escalation gate.
</objective>

<execution_context>
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/workflows/plan-review-convergence.md
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/references/revision-loop.md
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/references/gates.md
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/references/agent-contracts.md
</execution_context>



<context>
Phase number: extracted from the `<arguments>` block (required)

**Flags:**
- `--codex` — Use Codex CLI as reviewer (default if no reviewer flag given AND `review.default_reviewers` is unset; otherwise `review.default_reviewers` wins per ADR-0011 — #2315)
- `--agy` / `--antigravity` — Use Antigravity CLI as reviewer
- `--claude` — Use the agent CLI as reviewer (separate session)
- `--coderabbit` — Use CodeRabbit as reviewer (reviews the working-tree diff, not the source tree)
- `--config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0` — Use OpenCode as reviewer
- `--qwen` — Use Qwen Code CLI as reviewer (Alibaba Qwen models)
- `--cursor` — Use Cursor agent as reviewer
- `--ollama` — Use local Ollama server as reviewer (OpenAI-compatible, default host `http://localhost:11434`; configure model via `review.models.ollama`)
- `--lm-studio` — Use local LM Studio server as reviewer (OpenAI-compatible, default host `http://localhost:1234`; configure model via `review.models.lm_studio`)
- `--llama-cpp` — Use local llama.cpp server as reviewer (OpenAI-compatible, default host `http://localhost:8080`; configure model via `review.models.llama_cpp`)
- `--kimi-code` — Use Kimi Code CLI as reviewer (Moonshot AI)
- `--all` — Use all available CLIs and running local model servers
- `--max-cycles N` — Maximum replan→review cycles (default: 3)

**Feature gate:** This command requires `workflow.plan_review_convergence=true`. Enable with:
`gsd config-set workflow.plan_review_convergence true`. A dispatch carrying `--override-gate` —
how `/gsd-autonomous --converge` invokes this workflow (#4600) — bypasses the gate for that run.
</context>

<process>
Execute end-to-end.
Preserve all workflow gates (pre-flight, revision loop, stall detection, escalation).
</process>
