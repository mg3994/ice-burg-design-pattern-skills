# The Submerged Repository Engine Architecture

The Submerged Repository Engine is the core data engine of the Iceberg Pattern. It resides beneath the **Waterline** and quarantines asynchronous streams (Firestore, WebSockets, gRPC) away from the UI.

```
┌─────────────────────────────────────────────────────────────┐
│                 SUBMERGED REPOSITORY ENGINE                 │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Real-time Stream     │       │ Local Optimistic     │   │
│   │ streamSignal(cloud)  │       │ Patch Signal         │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ computed()        │                     │
│                   │ Engine Merging    │                     │
│                   └─────────┬─────────┘                     │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ ReadonlySignal<T> │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Submerged Engine Construction Pattern

```dart
class TaskRepository {
  TaskRepository({
    required Stream<List<Task>> cloudSnapshotStream,
    required Future<void> Function(String id, bool status) updateCloudTask,
    required Future<void> Function(String id) deleteCloudTask,
    List<Task> initialTasks = const [],
  })  : _updateCloudTask = updateCloudTask,
        _deleteCloudTask = deleteCloudTask {
    _initEngine(cloudSnapshotStream, initialTasks);
  }

  final Future<void> Function(String id, bool status) _updateCloudTask;
  final Future<void> Function(String id) _deleteCloudTask;
  final _inFlightToggles = <String>{};

  late final StreamSignal<List<Task>> _cloudStreamSignal;
  final _optimisticPatches = signal<Map<String, bool>>({});
  final _hasSyncError = signal(false);
  late final Computed<List<Task>> _computedTasks;

  void _initEngine(Stream<List<Task>> cloudSnapshotStream, List<Task> initialTasks) {
    _cloudStreamSignal = streamSignal(
      () => cloudSnapshotStream,
      options: AsyncSignalOptions<List<Task>>(initialValue: initialTasks),
    );

    _computedTasks = computed(() {
      final baseTasks = _cloudStreamSignal.value.value ?? const [];
      final overrides = _optimisticPatches.value;
      if (overrides.isEmpty) return baseTasks;

      return baseTasks.map((task) {
        final override = overrides[task.id];
        return override != null ? task.copyWith(isCompleted: override) : task;
      }).toList();
    });
  }

  ReadonlySignal<List<Task>> get tasks => _computedTasks;
  ReadonlySignal<bool> get hasSyncError => _hasSyncError;
}
```
