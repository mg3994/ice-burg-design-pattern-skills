---
name: offline-first-persistence-layer
description: Build resilient offline-first persistence layers using SQLite, Hive, or Drift integrated with Iceberg streamSignals for instant 0ms app boot times and stale-while-revalidate data access. Use when implementing offline local persistence in Flutter.
license: MIT
metadata:
  category: offline-first
---

# Offline-First Persistence Layer Architecture

An offline-first persistence layer ensures that application state is loaded from local storage (SQLite, Hive, Drift) in 0ms on startup, while background streams silently revalidate cloud state.

```
┌─────────────────────────────────────────────────────────────┐
│                OFFLINE-FIRST ARCHITECTURE                   │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Local Cache (Hive)   │       │ Cloud Stream         │   │
│   │ 0ms Startup          │       │ Async Revalidation   │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ streamSignal()    │                     │
│                   │ Submerged Engine  │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Checklist

- [ ] Load cached local records into initial `streamSignal` options.
- [ ] Implement write-through caching on server ACKs.
- [ ] Run `python3 scripts/verify_persistence_adapters.py lib/` to audit persistence configuration.

For cache invalidation rules and strategies, see:
- [Cache Invalidation & Persistence Reference](references/cache-invalidation.md)
