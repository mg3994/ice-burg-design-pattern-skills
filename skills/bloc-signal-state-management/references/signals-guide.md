# BlocSignal & Signals Core Usage Guide

This reference provides detailed code snippets and techniques for `bloc_signals` and `signals_core`.

## 1. Custom State Equality Comparator

Because Dart 3 record states and nested list comparison can trigger unnecessary BLoC emissions, define a custom equality function:

```dart
static bool _tasksStateEquals(TaskBoardState prev, TaskBoardState curr) {
  if (prev.activeFilterTag != curr.activeFilterTag) return false;
  if (prev.isDeletingTaskId != curr.isDeletingTaskId) return false;
  if (prev.hasSyncError != curr.hasSyncError) return false;
  if (prev.tasks.length != curr.tasks.length) return false;
  for (var i = 0; i < prev.tasks.length; i++) {
    final a = prev.tasks[i];
    final b = curr.tasks[i];
    if (a.id != b.id ||
        a.title != b.title ||
        a.isCompleted != b.isCompleted ||
        a.tags.length != b.tags.length) {
      return false;
    }
    for (var j = 0; j < a.tags.length; j++) {
      if (a.tags[j] != b.tags[j]) return false;
    }
  }
  return true;
}
```

## 2. Resource Disposal Pattern

All created signals and computed subscriptions must be disposed when the enclosing Cubit or Repository is disposed:

```dart
class TaskBoardCubit extends CubitSignal<TaskBoardState> {
  // ...
  late final void Function() _disposeEffect;

  void _initFacade() {
    final computedState = computed(() => ...);
    _disposeEffect = computedState.subscribe(emit);
  }

  @override
  Future<void> close() async {
    _disposeEffect();
    _activeFilterTag.dispose();
    _isDeletingTaskId.dispose();
    await super.close();
  }
}
```

## 3. Error Forwarding Pattern

In BLoC, async background failures inside unawaited optimistic calls must be routed through `onError`:

```dart
void toggleTask(String id, bool currentStatus) {
  unawaited(
    _repository.toggleTask(id, currentStatus).catchError(
      (Object error, StackTrace st) {
        onError(error, st);
      },
    ),
  );
}
```
