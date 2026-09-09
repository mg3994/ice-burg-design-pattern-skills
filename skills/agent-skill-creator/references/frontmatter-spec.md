# Agent Skills Frontmatter & Specification Reference

The `agentskills.io` standard defines a lightweight format for extending AI agent capabilities using markdown files wrapped in YAML frontmatter.

## SKILL.md Frontmatter Rules

```yaml
---
name: skill-name-slug
description: Clear 1-2 sentence description of what the skill does and when to activate it. Include specific triggers and keywords.
license: MIT
metadata:
  author: example-org
  category: architecture
---
```

### Constraints Table

| Field | Required | Constraints |
| :--- | :--- | :--- |
| `name` | Yes | 1-64 chars. Lowercase `a-z`, `0-9`, and hyphens `-`. Must match parent folder name! |
| `description` | Yes | 1-1024 chars. Non-empty. Must describe capability + activation triggers. |
| `license` | No | Short license name (e.g. `MIT`, `Apache-2.0`). |
| `metadata` | No | Map of string keys to string values. |

## Progressive Disclosure Rules

1. **Discovery (Startup)**: Agents load only `name` and `description` (~100 tokens).
2. **Activation**: When prompt matches description, agent loads full `SKILL.md` (< 500 lines / 5,000 tokens).
3. **Resource Loading**: Move detailed documentation to `references/` and executable code to `scripts/`. Agents read these files on demand.
