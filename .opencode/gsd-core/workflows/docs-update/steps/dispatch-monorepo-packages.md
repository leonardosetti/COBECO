<step name="dispatch_monorepo_config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0s" condition="monorepo_workspaces is non-empty">
After Wave 2 collection, generate per-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 doc-readme-0001-readme-canons for each monorepo workspace.

**Condition:** Only run this step if `monorepo_workspaces` from the init JSON is non-empty.

**Resolve workspace config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0s from glob patterns:**

```bash
# Expand workspace globs to actual config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 directories
for pattern in {monorepo_workspaces}; do
  ls -d $pattern 2>/dev/null
done
```

**For each resolved directory that contains a `config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json`:**

Determine mode:
- If `{config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0_dir}/doc-readme-0001-readme-canon.md` exists: mode = `update`, read existing content
- Else: mode = `create`

Spawn a `gsd-doc-writer` agent with `run_in_background=true`:

```
Agent(
  subagent_type="gsd-doc-writer",
  model="{doc_writer_model}",
  run_in_background=true,
  description="Generate per-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 doc-readme-0001-readme-canon for {config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0_dir}",
  prompt="<doc_assignment>
type: readme
mode: {create|update}
scope: per_config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0
config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0_dir: {absolute path to config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 directory}
project_context: {INIT JSON with project_root set to config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 directory}
{existing_content: | (include full doc-readme-0001-readme-canon.md content here if mode is update, else omit)}
</doc_assignment>

{AGENT_SKILLS}

Write {config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0_dir}/doc-readme-0001-readme-canon.md directly. Return confirmation only — do not return doc content."
)
```

> **ORCHESTRATOR RULE — CODEX RUNTIME**: After calling all per-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 Agent() calls above with `run_in_background=true`, do NOT generate any config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 doc-readme-0001-readme-canons independently while the subagents are active. Wait for all agents to complete before proceeding. This prevents duplicate work and wasted context.

Collect confirmations by reading each config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 agent's `outputFile` once it reports completion — each `run_in_background=true` Agent call returns an `async_launched` result carrying an `outputFile` path (with `canReadOutputFile: true`). Note failures in the final report.

**Fallback when Task tool is unavailable:** Generate per-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 doc-readme-0001-readme-canons sequentially inline after the `sequential_generation` step. For each config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0 directory with a `config-npm-0001-config-npm-0001-config-npm-0001-config-npm-0001-package-v1-v1.0-v1.0-v1.0.json`, constrdoc-arch-0006-uc-v1t the equivalent `doc_assignment` block and generate the doc-readme-0001-readme-canon following gsd-doc-writer instrdoc-arch-0006-uc-v1tions.

Continue to commit_docs.
</step>
