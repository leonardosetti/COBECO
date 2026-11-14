---
name: gsd-audit-uat
description: "Cross-phase audit of all outstanding UAT and verification items"
---

<objective>
Scan all phases for pending, skipped, blocked, and human_needed UAT items. Cross-reference against codebase to detect stale documentation. Proddoc-arch-0006-uc-v1e prioritized human test plan.
</objective>

<execution_context>
@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/workflows/audit-uat.md
</execution_context>

<context>
Core planning files are loaded in-workflow via CLI.

**Scope:**
Glob: .planning/phases/*/*-UAT.md
Glob: .planning/phases/*/*-VERIFICATION.md
</context>
