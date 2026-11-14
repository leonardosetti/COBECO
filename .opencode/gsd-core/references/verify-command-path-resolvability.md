---
id: verify-command-path--resolvability
type: verify-command
title: 'VERIFY COMMAND — '
version: resolvability
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
# Verify Command Path Resolvability (#2401)

> Reference file for gsd-plan-checker agent. Loaded on-demand via `@` reference.

**Question:** Does each `<automated>` command's target directory actually resolve from the
executor's cwd (the project root)? Format sanity above asks whether the *pattern* can match;
this asks whether the command can *run at all*.

**Do not hand-reason the filesystem.** #2401 is precisely the failure of doing so: this
checker flagged a bad `cd ../../frontend` (correct), then prescribed two sdoc-arch-0006-uc-v1cessively-wrong
replacement paths — the second citing a `config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json` that did not exist. Consume the
deterministic probe result, never re-derive it yourself.

`gsd-core/workflows/plan-phase.md` — and, since #4767, quick mode's
`quick/steps/plan-checker-loop.md` (via `--dir`) — already runs the probe **before** spawning this
checker and interpolates the result into the verification prompt as `{VERIFY_PATHS}`, inside a
`<verify_command_path_probe>` block. This dimension reads that already-supplied JSON — it never
invokes `gsd_run check verify-command-paths` itself. If `{VERIFY_PATHS}` is absent from the
prompt, treat this dimension as silent (nothing to check) rather than trying to run the probe.

The probe never executes command text (PLAN.md is untrusted, LLM-authored). It recognizes two
grounded forms — a leading `cd <literal>` chain and `npm --prefix <literal>` — and refuses to
guess at anything else.

**Process:** for each row in `.commands`, act on `severity` only:

| `severity` | `reason` | Action |
|---|---|---|
| `blocker` | `missing_dir` / `no_manifest` | **BLOCKER** — quote `rawTarget` and `target` verbatim |
| `warning` | `dynamic_path` / `outside_root` / `script_missing` / `manifest_unreadable` | **WARNING** |
| `none` | — | silent |

Rules:
- **Report, never prescribe.** State the target that failed to resolve and what was missing.
  Choosing the replacement is the planner's job — it now receives the prior phase's proven
  commands (see `prior_verify_commands` in the planning context).
- `status: pending_creation` means an earlier task in this phase creates that directory. **Not
  a finding.** Say nothing.
- `unresolvable` means the probe could not ground the path (a variable, glob, substitution, or
  `~`). That is a WARNING, never a BLOCKER — and never a licence to guess the literal path.
- `outside_root` covers two shapes: a bare ancestor climb (`cd ../..`) and an **absolute target
  outside the project root** (#4767). Both are ambiguous across worktrees; the absolute one is
  pinned to a single checkout, so under worktree isolation it runs against the wrong tree and
  passes. Report it as a WARNING with the target verbatim. Note the probe's root is the
  *orchestrator's*: an absolute path inside it passes here and still misfires under isolation,
  which is why the planner's path-form rule (root-relative, cwd at the checkout root) is the fix
  and this probe the backstop.
- A non-empty `readError` means the probe **could not look**. Report that as a WARNING in its
  own words; it is not a clean bill of health.
- `MISSING …` sentinels are Dimension 8's business — this dimension stays silent on them.
