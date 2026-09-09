# Advanced State Machine Reconciliation in the Iceberg Pattern

In complex real-time applications, optimistic updates must handle nested entity state transitions and multi-step server reconciliation.

```
                  ┌────────────────────────┐
                  │   INITIAL SERVER TRUTH │
                  │   Task { status: open }│
                  └───────────┬────────────┘
                                │
                  [ User Action: Complete Task ]
                                │
                  ┌───────────▼────────────┐
                  │ 0ms OPTIMISTIC STATE   │
                  │ Task { status: done }  │
                  └───────────┬────────────┘
                                │
                  [ Background Server Write ]
                                │
             ┌──────────────────┴──────────────────┐
             ▼                                     ▼
   [ Server ACK Received ]                [ Server Error / Collision ]
   Clear Local Override                   Atomic batch():
   Retain Server Snapshot                 1. Revert to Server Truth
                                          2. Set Sync Error Flag
```

## Atomic `batch()` Reconciliation Flow

To prevent torn UI frames during state transitions, always execute patch clearing and error status updates within a single `batch()` block:

```dart
try {
  await _updateCloudTask(id, newStatus);
  batch(() {
    _hasSyncError.value = false;
    final updated = Map<String, bool>.from(_optimisticPatches.value)..remove(id);
    _optimisticPatches.value = updated;
  });
} catch (error, stackTrace) {
  batch(() {
    final updated = Map<String, bool>.from(_optimisticPatches.value)..remove(id);
    _optimisticPatches.value = updated;
    _hasSyncError.value = true;
  });
  Error.throwWithStackTrace(
    SyncRollbackException('Failed to update task $id. Reverted.', error),
    stackTrace,
  );
}
```
