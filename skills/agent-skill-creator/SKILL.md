---
name: agent-skill-creator
description: Meta-skill for authoring, structuring, and validating production-ready Agent Skills according to agentskills.io specifications. Features progressive disclosure patterns, frontmatter schema rules, gotchas, and validation scripts. Use when creating new agent skills or auditing existing skill packages.
license: MIT
metadata:
  author: RandalSchwartz
  category: meta-skills
---

# Agent Skill Creation & Specification Guide

Agent Skills are a standardized, lightweight format (`agentskills.io`) for equipping AI agents with specialized domain knowledge, workflows, and executable scripts.

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + core instructions (<500 lines)
├── scripts/          # Optional: Executable code (Python, Bash, JS)
├── references/       # Optional: On-demand documentation (markdown)
└── assets/           # Optional: Static resources (templates, schemas)
```

## Progressive Disclosure Rules

1. **Discovery (Startup)**: Agents load only skill `name` and `description` (~100 tokens).
2. **Activation**: When a task prompt matches the `description`, the agent loads `SKILL.md` into context (<5,000 tokens).
3. **Execution**: The agent reads files in `references/` or executes code in `scripts/` only when needed.

---

## Best Practices Checklist

- [ ] Folder name matches `name` frontmatter field exactly.
- [ ] Description states *what* the skill does AND *when* to activate it (including keywords).
- [ ] Keep `SKILL.md` concise (<500 lines). Move deep documentation to `references/`.
- [ ] Run `python3 scripts/validate_workspace_skills.py` to validate frontmatter schemas.

For frontmatter rules and specifications, see:
- [Frontmatter Specification Reference](references/frontmatter-spec.md)
