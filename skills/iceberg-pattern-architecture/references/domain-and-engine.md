# Domain Model & Submerged Repository Engine

This reference details the submerged engine implementation for the Iceberg Pattern.

## Domain Entity (Pure Dart 3 Record)

```dart
/// Pure Dart 3 record representation of a domain Task.
typedef Task = ({
  String id,
  String title,
  bool isCompleted,
  List<String> tags,
});
```

## Submerged Repository Engine

```dart
import 'dart:async';
import 'package:signals_core/signals_core.dart';
import '../domain/task.dart';

class SyncRollbackException implements Exception {
  SyncRollbackException(this.message, [this.cause]);
  final String message;
  final Object? cause;
  @override
  String toString() => 'SyncRollbackException: $message';
}

class TaskRepository {
  TaskRepository({
    required Stream<List<Task>> cloudSnapshotStream,
    required Future<void> Function(String id, bool isCompleted) updateCloudTask,
    required Future<void> Function(String id) deleteCloudTask,
    List<Task> initialTasks = const [],
  })  : _updateCloudTask = updateCloudTask,
        _deleteCloudTask = deleteCloudTask {
    _initEngine(cloudSnapshotStream, initialTasks);
  }

  final Future<void> Function(String id, bool isCompleted) _updateCloudTask;
  final Future<void> Function(String id) _deleteCloudTask;

  final _inFlightToggles = <String>{};

  late final StreamSignal<List<Task>> _cloudStreamSignal;
  final _optimisticPatches = signal<Map<String, bool>>({});
  final _hasSyncError = signal(false);
  late final Computed<List<Task>> _computedTasks;

  void _initEngine(
    Stream<List<Task>> cloudSnapshotStream,
    List<Task> initialTasks,
  ) {
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
        return override != null
            ? (
                id: task.id,
                title: task.title,
                isCompleted: override,
                tags: task.tags,
              )
            : task;
      }).toList();
    });
  }

  ReadonlySignal<List<Task>> get tasks => _computedTasks;
  ReadonlySignal<bool> get hasSyncError => _hasSyncError;

  /// OPTIMISTIC MUTATION (0ms Latency)
  Future<void> toggleTask(String id, bool currentStatus) async {
    if (_inFlightToggles.contains(id)) return;
    _inFlightToggles.add(id);

    final newStatus = !currentStatus;
    _optimisticPatches.value = {..._optimisticPatches.value, id: newStatus};

    try {
      await _updateCloudTask(id, newStatus);
      batch(() {
        _hasSyncError.value = false;
        final updated = Map<String, bool>.from(_optimisticPatches.value)
          ..remove(id);
        _optimisticPatches.value = updated;
      });
    } catch (error, stackTrace) {
      batch(() {
        final updated = Map<String, bool>.from(_optimisticPatches.value)
          ..remove(id);
        _optimisticPatches.value = updated;
        _hasSyncError.value = true;
      });
      Error.throwWithStackTrace(
        SyncRollbackException('Failed to update task $id. Reverted.', error),
        stackTrace,
      );
    } finally {
      _inFlightToggles.remove(id);
    }
  }

  /// PESSIMISTIC MUTATION
  Future<void> deleteTask(String id) async {
    await _deleteCloudTask(id);
  }

  void dispose() {
    _inFlightToggles.clear();
    _cloudStreamSignal.dispose();
    _optimisticPatches.dispose();
    _hasSyncError.dispose();
    _computedTasks.dispose();
  }
}
```
