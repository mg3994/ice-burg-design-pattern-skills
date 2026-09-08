# Stale-While-Revalidate Caching & Error Recovery

The Iceberg Pattern implements stale-while-revalidate UX to ensure users never experience blank screens or disruptive full-page error widgets during cloud stream connection loss or mutation failures.

## 1. Dual-State Architecture

The Submerged Engine maintains two reactive signals for synchronization:
1. `_cloudStreamSignal`: Holds the latest server snapshot or cached stream emission.
2. `_hasSyncError`: A boolean signal indicating whether the last background mutation failed or stream connection was lost.

```dart
class TaskRepository {
  late final StreamSignal<List<Task>> _cloudStreamSignal;
  final _hasSyncError = signal(false);

  ReadonlySignal<List<Task>> get tasks => _computedTasks;
  ReadonlySignal<bool> get hasSyncError => _hasSyncError;
}
```

## 2. Silent Rollback & Banner Notification

When an optimistic mutation fails:
1. `batch()` silently removes the optimistic override from `_optimisticPatches`.
2. `batch()` sets `_hasSyncError.value = true`.
3. The computed state automatically reverts to the last verified cloud snapshot state.
4. The UI displays an amber top warning banner without destroying current user scroll position or view context.

```dart
AppBar(
  title: const Text('Task Board'),
  bottom: state.hasSyncError
      ? const PreferredSize(
          preferredSize: Size.fromHeight(28),
          child: ColoredBox(
            color: Colors.amber,
            child: Center(
              child: Text(
                'Offline / Sync Error — Showing Cached Data',
                style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
              ),
            ),
          ),
        )
      : null,
)
```
