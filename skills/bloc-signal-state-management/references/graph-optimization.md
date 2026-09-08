# Signal Graph Optimization Strategies

To ensure 60/120 FPS UI performance in real-time Flutter apps, follow these signal reactivity graph optimization guidelines.

## 1. Granular Signals over Giant State Objects

Avoid placing the entire screen state inside a single mutable `signal(State())`. Instead, split state into independent atomic signals:

```dart
// ❌ Poor Pattern: Giant signal forces re-evaluation of all fields
final _screenState = signal(ScreenState(tasks: [], filter: null, loadingId: null));

// ✅ Recommended Pattern: Fine-grained atomic signals
final _activeFilterTag = signal<String?>(null);
final _isDeletingTaskId = signal<String?>(null);
```

## 2. Dynamic Subscription Pruning in `computed()`

`computed()` functions automatically track which signals are read during execution. If a branch is skipped, dependency subscriptions are dynamically pruned:

```dart
final _computedTasks = computed(() {
  final baseTasks = _cloudStreamSignal.value.value ?? const [];
  final overrides = _optimisticPatches.value;

  // If overrides is empty, _computedTasks will NOT subscribe to individual item signals
  if (overrides.isEmpty) return baseTasks;

  return baseTasks.map((task) {
    final override = overrides[task.id];
    return override != null ? task.copyWith(isCompleted: override) : task;
  }).toList();
});
```

## 3. Custom Structural Record Equality

Pass a custom equality function to `CubitSignal` to prevent BLoC re-emissions when records or lists contain identical values:

```dart
TaskBoardCubit({required TaskRepository repository})
    : super(
        initialState: ...,
        equals: (prev, curr) {
          return prev.activeFilterTag == curr.activeFilterTag &&
              prev.isDeletingTaskId == curr.isDeletingTaskId &&
              prev.hasSyncError == curr.hasSyncError &&
              _listEquals(prev.tasks, curr.tasks);
        },
      );
```
