# Optimistic UI Rollback Patterns & Atomic Isolation

When performing 0ms optimistic UI mutations, network errors or server validation rejections require reverting client state without producing intermediate torn UI frames.

```
┌─────────────────────────────────────────────────────────────┐
│                 ATOMIC ROLLBACK PROTOCOL                    │
│                                                             │
│   1. Apply Optimistic Override Map                          │
│      _optimisticPatches.value = { ...overrides, id: status} │
│                                                             │
│   2. Dispatch Async Background Mutation                     │
│      await _updateCloudTask(id, status);                    │
│                                                             │
│   3. Catch Exception & Execute Atomic batch():              │
│      batch(() {                                             │
│        _optimisticPatches.value = overrides..remove(id);    │
│        _hasSyncError.value = true;                          │
│      });                                                    │
└─────────────────────────────────────────────────────────────┘
```

## Rollback Principles

1. **Atomic Signal Batching**: Always combine patch map eviction and error flag setting inside `batch(() { ... })`.
2. **Silent State Recovery**: Revert the local override so the UI gracefully falls back to the server's snapshot truth.
3. **Non-Disruptive Notifications**: Display a top warning banner or SnackBar instead of replacing the screen with a full-page error widget.
