---
name: clean-to-iceberg-migration
description: Migrate legacy Uncle Bob Clean Architecture Flutter projects to the Iceberg Pattern. Refactor anemic use cases, replace @freezed boilerplate with pure Dart 3 records, and eliminate StreamBuilder anti-patterns. Use when refactoring or modernizing legacy Flutter codebases.
license: MIT
metadata:
  category: architecture-migration
---

# Clean Architecture to Iceberg Pattern Migration Guide

Refactoring legacy Clean Architecture codebases to the Iceberg Pattern eliminates boilerplate, reduces microtask frame latency to 0ms, and simplifies unit test suites.

```
┌─────────────────────────────────────────────────────────────┐
│                     REFACTORING FLOW                        │
│                                                             │
│   Legacy Clean Architecture      ──>     Iceberg Pattern    │
│   ─────────────────────────              ───────────────    │
│   Anemic UseCases                ──>     Delete & Expose    │
│                                          Repository Signal  │
│   @freezed / Equatable           ──>     Pure Dart 3        │
│                                          Record typedef     │
│   StreamBuilder in UI            ──>     Submerged Engine   │
│                                          + BlocBuilder UI   │
└─────────────────────────────────────────────────────────────┘
```

## Migration Workflow Checklist

- [ ] Delete anemic 3-line UseCases and Interactors.
- [ ] Replace `@freezed` and `Equatable` classes with Dart 3 record typedefs (`typedef Task = ({...})`).
- [ ] Submerge raw streams inside repository `streamSignal()`.
- [ ] Convert screen controllers to `CubitSignal<State>`.
- [ ] Replace `StreamBuilder` widgets with synchronous `BlocBuilder` widgets.
- [ ] Run `python3 scripts/detect_clean_architecture_debt.py lib/` to verify cleanup.

For step-by-step refactoring code snippets, see:
- [Migration Steps & Refactoring Reference](references/migration-steps.md)
