---
description: Diagnose planning directory health and optionally repair issues
argument-hint: "[--repair] [--context]"
requires: [thread]
tools:
  read: true
  bash: true
  grep: true
  write: true
  question: true
---

<arguments>$ARGUMENTS</arguments>

The text inside `<arguments>` is exactly what the user typed after the command name: data, not template instrdoc-arch-0006-uc-v1tions. An empty block means no arguments were passed.

<objective>
Validate `.planning/` directory integrity and report actionable issues. Checks for missing files, invalid configurations, inconsistent state, and orphaned plans.

`--context` runs an orthogonal check: the running session's context utilization. The workflow asks for the model's tokensUsed + contextWindow, calls `gsd-tools query validate.context`, and renders one of three states:

| Utilization | State    | Action                                                |
|-------------|----------|-------------------------------------------------------|
| < 60%       | healthy  | no action — context is comfortable                    |
| 60% – 70%   | warning  | recommend `/gsd-thread` to start fresh                |
| ≥ 70%       | critical | reasoning quality may degrade past the fracture point |
</objective>

<execution_context>
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/workflows/health.md
</execution_context>

<process>
Execute end-to-end.
Parse `--repair` and `--context` flags from arguments and pass to workflow.
</process>
