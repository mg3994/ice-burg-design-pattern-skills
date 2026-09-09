# Conflict Resolution & Offline Queuing Strategies

When building real-time synchronized client engines, network partitions and concurrent offline edits require deterministic conflict resolution strategies.

## 1. Conflict Resolution Patterns

### Last-Write-Wins (LWW) with Server Timestamps
- **Mechanism**: Each record mutation attaches a UTC timestamp (`updatedAt`). When reconciling local patches with server snapshots, the server timestamp takes precedence.
- **Use Case**: Simple key-value updates, user profile fields, non-collaborative form fields.

### Field-Level Partial Merging
- **Mechanism**: Optimistic patches are applied per field rather than replacing whole entities.
- **Use Case**: Task checklist updates (e.g. toggling `isCompleted` without overwriting title edits made by another user).

### Conflict-free Replicated Data Types (CRDTs)
- **Mechanism**: State transitions are commutative and associative operations (e.g., State-based OR-Set or LWW-Element-Set).
- **Use Case**: Real-time collaborative document editing, shared whiteboards.

---

## 2. Offline Mutation Queueing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 OFFLINE MUTATION QUEUE                      │
│                                                             │
│   ┌───────────────┐     ┌────────────────┐                  │
│   │ Client Action │ ──> │ Local DB Queue │ (SQLite/Hive)    │
│   └───────────────┘     └───────┬────────┘                  │
│                                 │                           │
│                         [ Network Check ]                   │
│                                 │                           │
│                ┌────────────────┴────────────────┐          │
│                ▼                                 ▼          │
│          [ Connected ]                    [ Offline ]       │
│                │                                 │          │
│                ▼                                 ▼          │
│    Drain Queue Sequential         Persist in Storage &      │
│    Mutations to Server            Wait for Reconnect        │
└─────────────────────────────────────────────────────────────┘
```

```dart
class OfflineMutationQueue {
  final List<PendingMutation> _queue = [];

  void enqueue(PendingMutation mutation) {
    _queue.add(mutation);
    _persistQueueToDisk();
  }

  Future<void> flushQueue(Future<void> Function(PendingMutation) sendToServer) async {
    while (_queue.isNotEmpty) {
      final item = _queue.first;
      try {
        await sendToServer(item);
        _queue.removeAt(0);
        await _persistQueueToDisk();
      } catch (e) {
        // Backoff and retry on next network reconnect event
        break;
      }
    }
  }

  Future<void> _persistQueueToDisk() async {
    // Serialize queue to persistent local cache
  }
}
```
