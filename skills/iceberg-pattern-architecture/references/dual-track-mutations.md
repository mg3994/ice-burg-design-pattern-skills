# Dual-Track Mutation State Machine & Atomic Rollback Protocol

The Iceberg Pattern categorizes mutations into two distinct operational tracks based on user interaction ergonomics and operation reversibility.

```
                         ┌────────────────────────┐
                         │   USER INTENT ACTION   │
                         └───────────┬────────────┘
                                     │
                     [ Is operation destructive? ]
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
             [ NO: OPTIMISTIC ]               [ YES: PESSIMISTIC ]
                    │                                 │
          0ms Patch Signal Emission            Set Loading Spinner ID
          Synchronous Frame 0 Re-render        In Screen Facade State
                    │                                 │
          Background Server Write              Await Server Future
                    │                                 │
           ┌────────┴────────┐               ┌────────┴────────┐
           ▼                 ▼               ▼                 ▼
      [ Success ]       [ Failure ]     [ Success ]       [ Failure ]
      Clear Patch       Atomic batch()  Clear Spinner     Clear Spinner
      In batch()        Silent Revert   UI Refresh        Forward onError
                        + Sync Error
```

## 1. Optimistic Track (0ms Latency)

- **Target Operations**: Non-destructive, high-frequency user actions (e.g., checking a task, toggling a star, incrementing a counter).
- **Execution Flow**:
  1. Client applies patch to private `signal<Map<String, Patch>>` instantly in 0ms.
  2. UI re-renders synchronously in Frame 0.
  3. Client dispatches background write future to server.
  4. On server ACK: `batch()` clears the local override patch from the map.
  5. On server rejection: `batch()` silently removes the override patch, sets `hasSyncError = true`, and rethrows a `SyncRollbackException` to `onError`.

## 2. Pessimistic Track (Awaited Confirmation)

- **Target Operations**: Destructive or irreversible actions (e.g., permanently deleting a record, executing a financial transaction).
- **Execution Flow**:
  1. Client sets a row-level spinner ID in the screen facade state (`isDeletingTaskId = id`).
  2. UI displays a row-level spinner indicator without blocking the rest of the screen.
  3. Client awaits the server future.
  4. Upon completion or failure: `isDeletingTaskId` is cleared in the `finally` block.
