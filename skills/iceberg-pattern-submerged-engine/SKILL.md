---
name: iceberg-pattern-submerged-engine
description: Construct the Submerged Repository Engine tier of the Iceberg Pattern. Quarantines asynchronous streams using streamSignal, tracks un-ACKed optimistic client overrides, and merges data into unified computed signals. Use when building repository data engines.
license: MIT
metadata:
  category: iceberg-engine
---

# Submerged Repository Engine Architecture

The Submerged Repository Engine is Tier 2 of the Iceberg Pattern. It resides beneath the Waterline and submerges raw asynchronous streams into synchronous, memoized reactive signals (`ReadonlySignal<T>`).

```
┌─────────────────────────────────────────────────────────────┐
│                 SUBMERGED REPOSITORY ENGINE                 │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Real-time Stream     │       │ Local Optimistic     │   │
│   │ streamSignal(cloud)  │       │ Override Map Signal  │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ computed()        │                     │
│                   │ Engine Merging    │                     │
│                   └─────────┬─────────┘                     │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ ReadonlySignal<T> │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Engine Checklist

- [ ] Submerge raw asynchronous streams inside `streamSignal()` in repository initialization.
- [ ] Track un-ACKed optimistic client overrides in a private `signal<Map<String, Patch>>`.
- [ ] Merge cloud stream data and overrides into a memoized `computed()` signal.
- [ ] Enforce in-flight `Set<String>` operation guards to block double-taps.
- [ ] Run `python3 scripts/verify_submerged_engine.py lib/` to audit engine construction.

For complete engine architecture code snippets, see:
- [Engine Architecture Reference](references/engine-architecture.md)
