# Agent Skills Self-Load (Bootstrap)

> **Shared contract.** Every `agent_skills` consumer agent self-loads its configured
> skills in its mandatory init step, so a project's `.planning/config-planning-0001-planning-config-v1-planning-0001-planning-config-v1.0-planning-0001-planning-config-v1.0-planning-0001-planning-config-v1.0.json`
> `agent_skills.<agent-type>` mapping reaches the agent that actually does the work —
> even when the orchestrator did not run bash init (e.g. a runtime whose `Skill()`
> delegation does not reliably execute the delegated workflow's bash, such as Cursor;
> see open-gsd/gsd-core#1600 / #1601). This is the durable counterpart to the
> orchestrator-side injection documented under
> [Agent Skills Injection](../../docs/CONFIGURATION.md#agent-skills-injection).

## When to run

In your mandatory init step — right after `mandatory-initial-read.md` / the
`Project skills` discovery, before any other work.

## Steps

1. **Dedup guard (MANDATORY).** Look at your own prompt. If it already contains an
   `<agent_skills>` block, the orchestrator already injected one — **skip self-load
   entirely.** Loading a second copy wastes context on runtimes where orchestrator-side
   injection also runs (e.g. Claude Code). The guard is what keeps the two seams from
   doubling the block.

2. **Query your configured skills.** Use **your own agent type**: the one your agent
   file states on its `agent_skills:` pointer line, as `(agent type: \`gsd-executor\`)`.
   Do not read it from your frontmatter `name:` — Claude Code shows a subagent only the
   body, the Kimi converter drops frontmatter, and Codex keeps it in a TOML key. Run the
   query with `--skills-only`, in the **same bash call** as the launcher so `gsd_run` is
   defined when it runs. Substitute your type for `<your-agent-type>`:

   ```bash
   # 1. Launcher: paste the bash block from gsd-run-resolver.md here unless gsd_run
   #    is already defined in this shell (@/lab/FATEC/202602/ger_proj/COGME/.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/gsd-core/references/gsd-run-resolver.md).
   # 2. Query:
   _AGENT_SKILLS=$(gsd_run query agent-skills <your-agent-type> --skills-only)
   ```

   Not every agent file defines `gsd_run`, so supply it as above rather than assuming
   your init did. The query is read-only and idempotent. Its stderr and exit status stay
   visible, so a missing launcher or a failed query is never mistaken for "nothing
   configured".

3. **Read every listed skill.** The block emits entries as `@<path>/SKILL.md`
   includes — `Read` each one before starting work. If the block is empty, there is
   nothing to do (zero overhead).

## What the query returns, per runtime

| Call | the agent | Non-the agent (Codex, Kimi, OpenCode, Kilo, …) |
|---|---|---|
| `query agent-skills <type> --skills-only` (the self-load) | configured skills, or an empty block | configured skills, or an empty block |
| `query agent-skills <type>` (orchestrator-side `${AGENT_SKILLS_*}` injection) | configured skills, or an empty block | configured skills, or — when nothing is configured and the agent is installed — the agent's own **persona** (#2454, #4407) |

On a non-the agent runtime the plain query can answer with the agent's whole persona
(about 47 KB for the executor). `--skills-only` is what keeps the self-load from
reading your own persona back into your context as if it were a skills block. Never
run the query without it from inside an agent.

## What self-load does and does not cover

| Skill form | Self-loads? | Notes |
|---|---|---|
| Project-relative path (`skills/my-skill`) | ✅ everywhere | `Read` the `@`-include |
| Global personal (`global:<name>`) | ✅ everywhere | resolves to the runtime global skills dir, then `Read` |
| Plugin-provided (`global:<plugin>:<skill>`) | the agent only | emitted as a Skill-tool directive on the agent; **skipped with a warning on all other runtimes** — the plugin/Skill-tool model has no equivalent elsewhere (#1601, #1258). Not closeable on Cursor. |

## Notes

- **Idempotent and read-only.** `query agent-skills` never mutates state; calling it
  twice (once by the orchestrator, once by the agent) is harmless because the dedup
  guard suppresses the second load.
- **No new config keys.** This reuses the existing `agent_skills` map and the existing
  `buildAgentSkillsBlock` / `cmdAgentSkills` machinery (`src/init.cts`). The 22 consumer
  agent types are mirrored in `tests/agent-skills.test.cjs` (`CONSUMER_doc-agents-0001-agents-canon`) and
  guarded against drift by `tests/agent-skills-bootstrap.test.cjs`.
- **Checkers / read-only agents.** Bash is universal across consumer agents, so
  self-load works for plan-checkers, verifiers, and auditors too; the bootstrap assumes
  no tool an agent lacks.
