# Cache Invalidation & Persistence Policies

Offline-first reactive applications combine local persistent storage (SQLite/Hive/Drift) with real-time cloud streams.

## 1. Cache Invalidation Strategies

| Strategy | Trigger Condition | Behaviour |
| :--- | :--- | :--- |
| **Time-To-Live (TTL)** | Cache age > threshold (e.g., 24 hours) | Invalidate local sqlite cache; force fresh cloud stream snapshot fetch. |
| **Server Version Tag (ETag)** | ETag mismatch on reconnect | Evict stale rows and write fresh server payload. |
| **Stale-While-Revalidate** | Immediate startup | Load cached disk rows instantly in 0ms; revalidate asynchronously in background. |

---

## 2. Persistence Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 PERSISTENCE ADAPTER ENGINE                  │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Local SQLite / Hive  │       │ Cloud Stream Engine  │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ streamSignal()    │                     │
│                   │ (Disk + Network)  │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```
