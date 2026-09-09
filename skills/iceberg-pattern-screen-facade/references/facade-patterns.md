# The Visible Screen Facade Layer

The Screen Facade (Tier 3 of the Iceberg Pattern) sits directly above the Waterline. It extends `CubitSignal<State>` and serves as a screen-scoped controller.

```
┌─────────────────────────────────────────────────────────────┐
│                   VISIBLE SCREEN FACADE                     │
│                                                             │
│   Submerged Repository Signal  ──>   CubitSignal Facade     │
│   ReadonlySignal<List<Task>>         TaskBoardCubit         │
│                                            │                │
│                                  [ Screen Filters ]         │
│                                  [ Row-level Spinners ]     │
│                                  [ Exception Routing ]      │
│                                            │                │
│                                            ▼                │
│                                  Synchronous Presentation   │
└─────────────────────────────────────────────────────────────┘
```

## Facade Implementation Pattern

```dart
class TaskBoardCubit extends CubitSignal<TaskBoardState> {
  TaskBoardCubit({required TaskRepository repository})
      : _repository = repository,
        super(
          initialState: (
            tasks: repository.tasks.value,
            activeFilterTag: null,
            isDeletingTaskId: null,
            hasSyncError: repository.hasSyncError.value,
          ),
          equals: _tasksStateEquals,
        ) {
    _initFacade();
  }

  final TaskRepository _repository;
  final _activeFilterTag = signal<String?>(null);
  final _isDeletingTaskId = signal<String?>(null);
  late final void Function() _disposeEffect;

  void _initFacade() {
    final computedState = computed(() {
      final allTasks = _repository.tasks.value;
      final filter = _activeFilterTag.value;

      final filteredTasks = filter == null
          ? allTasks
          : allTasks.where((t) => t.tags.contains(filter)).toList();

      return (
        tasks: filteredTasks,
        activeFilterTag: filter,
        isDeletingTaskId: _isDeletingTaskId.value,
        hasSyncError: _repository.hasSyncError.value,
      );
    });

    _disposeEffect = computedState.subscribe(emit);
  }

  void toggleTask(String id, bool currentStatus) {
    unawaited(
      _repository.toggleTask(id, currentStatus).catchError((Object error, StackTrace st) {
        onError(error, st);
      }),
    );
  }

  Future<void> deleteTask(String id) async {
    _isDeletingTaskId.value = id;
    try {
      await _repository.deleteTask(id);
    } catch (error, stackTrace) {
      onError(error, stackTrace);
    } finally {
      if (!isClosed) _isDeletingTaskId.value = null;
    }
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
