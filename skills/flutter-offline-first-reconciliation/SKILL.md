---
name: flutter-offline-first-reconciliation
description: Reconcile un-synced offline local mutations (SQLite, Drift, Hive) with real-time server streams upon network reconnection. Handles three-way merges and exponential sync retries. Use when implementing offline reconciliation in Flutter.
license: MIT
metadata:
  category: offline-reconciliation
---

# Offline-First Database Reconciliation

Reconciling offline client mutations with fresh server snapshot streams when network connections restore requires applying local un-ACKed patches on top of incoming server payloads.

```
┌─────────────────────────────────────────────────────────────┐
│                 OFFLINE RECONCILIATION                      │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Local Persistent DB  │       │ Incoming Cloud Stream│   │
│   │ (SQLite/Hive Cache)  │       │ Reconnection         │   │
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

## Reconciliation Checklist

- [ ] Re-apply un-ACKed offline patch queues on top of fresh server stream snapshots.
- [ ] Flush offline queues sequentially upon connection restore.
- [ ] Run `python3 scripts/verify_reconciliation_logic.py lib/` to audit reconciliation code.

For reconciliation algorithms, see:
- [Reconciliation Algorithms Reference](references/reconciliation-algorithms.md)
