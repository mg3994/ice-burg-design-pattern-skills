# Cross-Screen State Synchronization & Single Source of Truth

When an item is updated or deleted on one Flutter screen (e.g. `TaskDetailScreen`), all other active routes (e.g. `TaskBoardScreen`, `DashboardScreen`) must reflect the change instantly in 0ms without requiring global event buses or manual route pop callbacks.

```
┌─────────────────────────────────────────────────────────────┐
│                 SINGLE SOURCE OF TRUTH                      │
│                                                             │
│                ┌──────────────────────┐                     │
│                │ Submerged Repository │                     │
│                │ ReadonlySignal<Tasks>│                     │
│                └──────────┬───────────┘                     │
│                           │                                 │
│        ┌──────────────────┴──────────────────┐              │
│        ▼                                     ▼              │
│ ┌───────────────┐                   ┌───────────────┐       │
│ │ TaskBoardCubit│                   │ TaskDetailCubit│      │
│ └──────┬────────┘                   └──────┬────────┘       │
│        ▼                                   ▼                │
│ TaskBoardScreen                    TaskDetailScreen         │
└─────────────────────────────────────────────────────────────┘
```

## Pattern Implementation

Instead of duplicating item state inside individual screen controllers, screens consume computed signals derived from a shared single-source-of-truth repository signal:

```dart
class TaskDetailCubit extends CubitSignal<TaskDetailState> {
  TaskDetailCubit({
    required String taskId,
    required TaskRepository repository,
  }) : super(initialState: ...) {
    final computedState = computed(() {
      final tasks = repository.tasks.value;
      final task = tasks.firstWhere(
        (t) => t.id == taskId,
        orElse: () => null,
      );
      return (task: task, isNotFound: task == null);
    });

    _disposeEffect = computedState.subscribe(emit);
  }
}
```
