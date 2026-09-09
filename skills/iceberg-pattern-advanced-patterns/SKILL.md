---
name: iceberg-pattern-advanced-patterns
description: Master advanced Iceberg Pattern techniques including multi-repository signal composition, in-flight mutation guards, atomic batch rollback state machines, and cross-screen reactive state synchronization. Use when building complex multi-stream Flutter architectures.
license: MIT
metadata:
  category: advanced-architecture
---

# Advanced Iceberg Pattern Techniques

Advanced Iceberg Pattern implementations handle multi-repository composition, re-entrant mutation guards, offline mutation queues, and multi-step state machine reconciliation.

```
┌─────────────────────────────────────────────────────────────┐
│                 ADVANCED REACTIVE COMPOSITION               │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ UserRepository       │       │ TaskRepository       │   │
│   │ ReadonlySignal<User> │       │ ReadonlySignal<Tasks>│   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Composite computed│                     │
│                   │ (Screen Facade)   │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Patterns Checklist

- [ ] Implement `Set<String>` in-flight guards in repositories to block rapid double-taps.
- [ ] Wrap multi-repository signal inputs inside composite `computed()` signals inside CubitSignal facades.
- [ ] Enforce atomic `batch()` calls during state reconciliation and rollback phases.
- [ ] Run `python3 scripts/verify_iceberg_advanced_patterns.py lib/` to audit advanced pattern compliance.

For detailed state machine diagrams and multi-repository snippets, see:
- [State Machine Reconciliation Reference](references/state-machine-reconciliation.md)
- [Multi-Repository Signal Composition Reference](references/multi-repo-composition.md)
