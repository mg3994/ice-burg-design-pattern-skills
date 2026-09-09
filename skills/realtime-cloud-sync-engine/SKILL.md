---
name: realtime-cloud-sync-engine
description: Design resilient real-time cloud synchronization engines handling Firestore, WebSockets, SSE, and Supabase streams with 0ms optimistic updates, offline queuing, Last-Write-Wins conflict resolution, and exponential backoff. Use when building real-time sync engines or cloud data layers in Flutter/Dart.
license: MIT
metadata:
  author: RandalSchwartz
  category: cloud-sync
---

# Real-Time Cloud Synchronization Engine Architecture

Building real-time cloud sync engines for mobile and desktop applications requires handling intermittent network connections, packet loss, and concurrent mutations.

```
┌─────────────────────────────────────────────────────────────┐
│                 REAL-TIME SYNC ARCHITECTURE                 │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Incoming Cloud Stream│       │ Local Optimistic     │   │
│   │ (WebSocket/Firestore)│       │ Overrides (Map)      │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Synchronous Engine│                     │
│                   │ Reconciliation    │                     │
│                   └─────────┬─────────┘                     │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Unified Cache State│                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Core Synchronous Reconciliation Protocol

1. **Stream Submersion**: Wrap incoming WebSocket/Firestore snapshot streams inside a local cache container (`streamSignal`).
2. **Optimistic Overrides Map**: Track un-ACKed client mutations in an in-memory `Map<String, Patch>`.
3. **Atomic State Merging**: Expose a derived state projection merging the cloud stream value with local optimistic patches.
4. **Exponential Backoff Retry**: When network connections drop, queue pending mutations locally and retry with exponential backoff on reconnect.

---

## Engine Implementation Checklist

- [ ] Submerge raw asynchronous streams in repository initialization.
- [ ] Enforce in-flight operation guards (`Set<String>`) to block rapid double-taps.
- [ ] Implement atomic `batch()` calls on write acknowledgment or failure rollback.
- [ ] Use `scripts/simulate_sync_network.py` to test network loss resilience.

For conflict resolution strategies and offline queuing architecture, see:
- [Conflict Resolution & Offline Queuing Guide](references/conflict-resolution.md)
