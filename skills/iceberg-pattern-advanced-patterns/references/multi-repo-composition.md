# Multi-Repository Signal Composition

When a screen requires derived data across multiple submerged repositories (e.g. `UserRepository` and `TaskRepository`), combine their exposed `ReadonlySignal` streams inside a composite `computed()` signal.

```
┌───────────────────────────┐         ┌───────────────────────────┐
│     UserRepository        │         │      TaskRepository       │
│  ReadonlySignal<User?>    │         │ ReadonlySignal<List<Task>>│
└─────────────┬─────────────┘         └─────────────┬─────────────┘
              │                                     │
              └──────────────────┬──────────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │  Composite computed() │
                     │  (Screen Facade)      │
                     └───────────────────────┘
```

## Implementation Pattern

```dart
class DashboardCubit extends CubitSignal<DashboardState> {
  DashboardCubit({
    required UserRepository userRepository,
    required TaskRepository taskRepository,
  }) : super(initialState: ...) {

    final compositeState = computed(() {
      final user = userRepository.currentUser.value;
      final tasks = taskRepository.tasks.value;

      final userTasks = user == null
          ? <Task>[]
          : tasks.where((t) => t.assigneeId == user.id).toList();

      return (
        userName: user?.name ?? 'Guest',
        assignedTasks: userTasks,
        hasSyncError: userRepository.hasSyncError.value || taskRepository.hasSyncError.value,
      );
    });

    _disposeEffect = compositeState.subscribe(emit);
  }
}
```
