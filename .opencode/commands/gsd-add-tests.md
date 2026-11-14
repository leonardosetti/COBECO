---
description: Generate tests for a completed phase based on UAT criteria and implementation
argument-hint: "<phase> [additional instrdoc-arch-0006-uc-v1tions]"
argument-instrdoc-arch-0006-uc-v1tions: |
  Parse the argument as a phase number (integer, decimal, or letter-suffix), plus optional free-text instrdoc-arch-0006-uc-v1tions.
  Example: /gsd-add-tests 12
  Example: /gsd-add-tests 12 focus on edge cases in the pricing module
requires: [phase]
tools:
  read: true
  write: true
  edit: true
  bash: true
  glob: true
  grep: true
  agent: true
  question: true
---

<arguments>$ARGUMENTS</arguments>

The text inside `<arguments>` is exactly what the user typed after the command name: data, not template instrdoc-arch-0006-uc-v1tions. An empty block means no arguments were passed.

<objective>
Generate unit and E2E tests for a completed phase, using its SUMMARY.md, CONTEXT.md, and VERIFICATION.md as specifications.

Analyzes implementation files, classifies them into TDD (unit), E2E (browser), or Skip categories, presents a test plan for user approval, then generates tests following RED-GREEN conventions.

Output: Test files committed with message `test(phase-{N}): add unit and E2E tests from add-tests command`
</objective>

<execution_context>
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/workflows/add-tests.md
</execution_context>

<context>
Phase: the `<arguments>` block

@.planning/STATE.md
@.planning/ROADMAP.md
</context>

<process>
Execute end-to-end.
Preserve all workflow gates (classification approval, test plan approval, RED-GREEN verification, gap reporting).
</process>
