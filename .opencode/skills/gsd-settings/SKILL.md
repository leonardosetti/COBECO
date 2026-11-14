---
name: gsd-settings
description: "Configure GSD workflow toggles and model profile"
---

<objective>
Interactive configuration of GSD workflow agents and model profile via multi-question prompt.

Routes to the settings workflow which handles:
- Config existence ensuring
- Current settings reading and parsing
- Interactive multi-question prompt covering model profile and workflow toggles (research, plan_check, verifier, drift guard, TDD, code review, worktrees, compact content, and more — see `gsd-core/workflows/settings.md` for the current set)
- Config merging and writing
- Confirmation display with quick command references
</objective>

<execution_context>
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/workflows/settings.md
</execution_context>

<process>
Execute end-to-end.
</process>
