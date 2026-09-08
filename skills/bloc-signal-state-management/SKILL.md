---
name: bloc-signal-state-management
description: Implement reactive state management in Flutter and Dart using bloc_signals and signals_core. Features CubitSignal, streamSignal, computed, signal, and batch() for zero-lag fine-grained reactive state graphs. Use when implementing state management with BlocSignal or signals in Dart/Flutter.
license: MIT
metadata:
  author: RandalSchwartz
  category: state-management
---

# BlocSignal Reactive State Management

`bloc_signals` bridges the BLoC ecosystem with Solid/Preact-style fine-grained signals (`signals_core`). It enables synchronous, frame-0 state emissions, atomic state updates, and stream quarantining.

```
┌─────────────────────────────────────────────────────────────┐
│                       REACTIVE GRAPH                        │
│                                                             │
│   ┌─────────────────────┐       ┌───────────────────────┐   │
│   │ streamSignal(cloud) │       │ signal(optimistic)    │   │
│   └──────────┬──────────┘       └───────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ computed(tasks)   │                     │
│                   └─────────┬─────────┘                     │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ CubitSignal state │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Essential Primitives

### 1. `signal<T>(initialValue)`
Creates a mutable reactive state container.
```dart
final _activeFilterTag = signal<String?>(null);
_activeFilterTag.value = 'work'; // Updates reactive dependents instantly
```

### 2. `streamSignal<T>(() => stream, {options})`
Converts an asynchronous Dart `Stream` into a synchronous, cached reactive signal. Quarantines stream subscriptions away from the UI.
```dart
final _cloudStreamSignal = streamSignal(
  () => cloudSnapshotStream,
  options: AsyncSignalOptions<List<Task>>(initialValue: initialTasks),
);
```

### 3. `computed<T>(() => expression)`
Creates a derived, memoized signal computed synchronously from other signals. Recalculates automatically when dependency signals change.
```dart
final _computedTasks = computed(() {
  final baseTasks = _cloudStreamSignal.value.value ?? const [];
  final overrides = _optimisticPatches.value;
  if (overrides.isEmpty) return baseTasks;

  return baseTasks.map((task) {
    final override = overrides[task.id];
    return override != null ? task.copyWith(isCompleted: override) : task;
  }).toList();
});
```

### 4. `batch(() { ... })`
Executes multiple signal mutations atomically within a single transaction. Dependents re-compute only once after the batch finishes, eliminating intermediate torn UI states.
```dart
batch(() {
  _hasSyncError.value = false;
  final updated = Map<String, bool>.from(_optimisticPatches.value)..remove(id);
  _optimisticPatches.value = updated;
});
```

### 5. `CubitSignal<State>`
Extends traditional BLoC `Cubit` to accept reactive signals and sync with `computed` expressions via subscriptions.
```dart
class TaskBoardCubit extends CubitSignal<TaskBoardState> {
  TaskBoardCubit({required TaskRepository repository})
      : super(
          initialState: ...,
          equals: customEqualityCheck,
        ) {
    final computedState = computed(() { ... });
    _disposeEffect = computedState.subscribe(emit);
  }
}
```

---

## Workflow Checklist

- [ ] Wrap raw streams with `streamSignal` in the repository layer.
- [ ] Represent transient state and local patches with `signal()`.
- [ ] Derive view-ready data models using `computed()`.
- [ ] Use `batch()` for all multi-signal updates and rollback handlers.
- [ ] Pass custom `equals` comparator function to `CubitSignal` to prevent unnecessary re-renders.
- [ ] Always call `.dispose()` on created signals/effects when closing the Cubit or Repository.

For exact code templates and equality check strategies, see [State Management Reference Guide](references/signals-guide.md).
