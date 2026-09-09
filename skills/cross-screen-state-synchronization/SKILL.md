---
name: cross-screen-state-synchronization
description: Synchronize state across multiple Flutter screens and routes using single-source-of-truth repository signals. Eliminates torn UI states and global event buses. Use when building multi-screen Flutter applications.
license: MIT
metadata:
  category: cross-screen-sync
---

# Cross-Screen State Synchronization

Sharing reactive state across multiple Flutter routes requires deriving screen view states from shared single-source-of-truth repository signals (`ReadonlySignal<T>`).

```
┌─────────────────────────────────────────────────────────────┐
│                 SINGLE SOURCE OF TRUTH                      │
│                                                             │
│                ┌──────────────────────┐                     │
│                │ Submerged Repository │                     │
│                │ ReadonlySignal<Tasks>│                     │
│                └──────────┬───────────┘                     │
│                           │                                 │
│        ┌──────────────────┴──────────────────┐              │
│        ▼                                     ▼              │
│ ┌───────────────┐                   ┌───────────────┐       │
│ │ TaskBoardCubit│                   │ TaskDetailCubit│      │
│ └──────┬────────┘                   └──────┬────────┘       │
│        ▼                                   ▼                │
│ TaskBoardScreen                    TaskDetailScreen         │
└─────────────────────────────────────────────────────────────┘
```

## Synchronization Checklist

- [ ] Derive screen-scoped Cubits from shared repository signals.
- [ ] Handle entity deletion across secondary screens cleanly (`isNotFound`).
- [ ] Run `python3 scripts/audit_cross_screen_signals.py lib/` to audit single-source-of-truth adherence.

For single-source patterns, see:
- [Cross-Screen Synchronization Reference](references/cross-screen-patterns.md)
