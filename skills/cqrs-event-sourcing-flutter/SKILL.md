---
name: cqrs-event-sourcing-flutter
description: Architect CQRS (Command-Query Responsibility Segregation) and Event Sourcing patterns in Flutter and Dart using reactive signal read-model projections and command dispatchers. Use when designing event-driven architectures or CQRS systems in Dart.
license: MIT
metadata:
  category: architecture-cqrs
---

# CQRS & Event Sourcing in Flutter

Command-Query Responsibility Segregation (CQRS) decouples write operations (Commands) from read model projections (Queries), allowing client applications to project real-time event streams into synchronous reactive state graphs (`computed`).

```
┌─────────────────────────────────────────────────────────────┐
│                      CQRS ARCHITECTURE                      │
│                                                             │
│                 ┌────────────────────────┐                  │
│                 │      FLUTTER UI        │                  │
│                 └───────────┬────────────┘                  │
│                             │                               │
│            ┌────────────────┴────────────────┐              │
│            ▼                                 ▼              │
│   [ COMMAND DISPATCH ]             [ QUERY PROJECTION ]     │
│   Future<void> execute(Cmd)        ReadonlySignal<ReadModel>│
│            │                                 │              │
│            ▼                                 ▼              │
│   [ Write Side Engine ]            [ Reactive Signal Engine]│
└─────────────────────────────────────────────────────────────┘
```

## Principles

1. **Commands Return `Future<void>`**: Command methods express intent and return `Future<void>`. They do not return updated entities.
2. **Queries Are Synchronous Projections**: Read models are projected synchronously via `computed()` signals derived from event streams.
3. **Eventual & Optimistic Consistency**: Read models project optimistic overrides instantly (0ms) and reconcile when server events arrive.

---

## Workflow Checklist

- [ ] Separate command methods from query getters in repository interfaces.
- [ ] Project event streams into read-model signals using `streamSignal` and `computed`.
- [ ] Run `python3 scripts/audit_cqrs_separation.py lib/` to check CQRS compliance.

For detailed CQRS patterns and read-model code snippets, see:
- [CQRS Patterns Reference](references/cqrs-patterns.md)
