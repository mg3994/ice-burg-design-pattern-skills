---
name: supa-base-realtime-engine
description: Submerge Supabase Realtime Postgres Changes (postgres_changes) streams beneath the Iceberg repository waterline using streamSignal and signals_core. Use when integrating Supabase Realtime in Flutter applications.
license: MIT
metadata:
  category: supabase-sync
---

# Supabase Realtime Postgres Engine Architecture

Supabase Realtime listens to Postgres database changes (`postgres_changes`) via WebSockets. Submerging Supabase realtime streams beneath the Iceberg repository waterline isolates presentation widgets from channel lifecycle management.

```
┌─────────────────────────────────────────────────────────────┐
│                 SUPABASE REALTIME ENGINE                    │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Supabase Postgres    │       │ Local Optimistic     │   │
│   │ Realtime Channel     │       │ Overrides Map        │   │
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

- [ ] Wrap Supabase `.stream(primaryKey: [...])` in repository `streamSignal()`.
- [ ] Map PostgreSQL JSON rows to Pure Dart 3 Records.
- [ ] Run `python3 scripts/audit_supabase_subscriptions.py lib/` to audit layer purity.

For stream code templates and mapping idioms, see:
- [Supabase Stream Patterns Reference](references/supabase-stream-patterns.md)
