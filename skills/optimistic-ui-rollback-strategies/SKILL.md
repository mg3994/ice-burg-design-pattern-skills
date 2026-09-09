---
name: optimistic-ui-rollback-strategies
description: Implement robust 0ms optimistic UI updates with atomic batch() rollback state machines and stale-while-revalidate error recovery. Use when implementing optimistic mutations in Flutter/Dart.
license: MIT
metadata:
  category: optimistic-ui
---

# Optimistic UI Rollback Strategies

Optimistic UI updates give users instant 0ms feedback. If a background server request fails, the application must silently roll back state using atomic transactions (`batch()`).

```
┌─────────────────────────────────────────────────────────────┐
│                 OPTIMISTIC MUTATION ENGINE                  │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ 0ms Local Patch      │       │ Async Cloud Write    │   │
│   │ (signal override)    │       │ (Background Future)  │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Exception Catch   │                     │
│                   │ Atomic batch()    │                     │
│                   │ Rollback          │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Rollback Checklist

- [ ] Apply local optimistic patch map instantly.
- [ ] Wrap rollback eviction and `hasSyncError` updates inside `batch()`.
- [ ] Run `python3 scripts/verify_rollback_transactions.py lib/` to audit transaction safety.

For rollback state machine patterns, see:
- [Rollback Patterns Reference](references/rollback-patterns.md)
