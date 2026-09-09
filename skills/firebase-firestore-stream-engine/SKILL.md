---
name: firebase-firestore-stream-engine
description: Submerge Cloud Firestore snapshots() streams beneath the Iceberg repository waterline using streamSignal and signals_core. Integrates Firestore offline caching and 0ms optimistic updates. Use when integrating Cloud Firestore in Flutter.
license: MIT
metadata:
  category: firestore-sync
---

# Firebase Firestore Real-Time Stream Engine

Cloud Firestore provides native real-time collection `snapshots()` streams. Submerging Firestore snapshot streams beneath the repository waterline isolates presentation widgets from SDK listener lifecycle management.

```
┌─────────────────────────────────────────────────────────────┐
│                 FIRESTORE SNAPSHOT ENGINE                   │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Firestore Collection │       │ Local Optimistic     │   │
│   │ .snapshots() Stream  │       │ Overrides Map        │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ streamSignal()    │                     │
│                   │ Submerged Repository│                   │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Checklist

- [ ] Wrap Firestore `.snapshots()` streams in repository `streamSignal()`.
- [ ] Map Firestore `DocumentSnapshot` objects to Pure Dart 3 Records.
- [ ] Run `python3 scripts/audit_firestore_subscriptions.py lib/` to check layer purity.

For document mapping patterns and code snippets, see:
- [Firestore Stream Patterns Reference](references/firestore-stream-patterns.md)
