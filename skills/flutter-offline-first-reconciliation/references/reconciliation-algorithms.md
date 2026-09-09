# Offline-First Database Reconciliation Algorithms

Reconciling un-synced offline mutations with fresh server snapshot streams upon network reconnection requires deterministic merge rules.

```
┌─────────────────────────────────────────────────────────────┐
│                 OFFLINE RECONCILIATION                      │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Offline Local DB     │       │ Fresh Server Snapshot│   │
│   │ (Pending Mutations)  │       │ Stream               │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Reconciliation    │                     │
│                   │ Merge Engine      │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Three-Way Merge Protocol

1. **Base Snapshot**: Last known server state before disconnect.
2. **Local Offlines**: Queue of client mutation payloads recorded while offline.
3. **Remote Snapshot**: Fresh server state received upon reconnect.
4. **Merge Execution**: Re-apply un-ACKed local mutations on top of the remote snapshot in sequential timestamp order.
