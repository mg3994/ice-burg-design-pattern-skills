# Riverpod to BlocSignal Migration Mapping

Migrating from Riverpod (`StateNotifierProvider`, `AsyncNotifierProvider`) to `BlocSignal` simplifies state dependency graphs and eliminates `ref.watch` lifecycle memory leaks.

## Mapping Equivalencies

| Riverpod Primitive | BlocSignal Primitive |
| :--- | :--- |
| `StateProvider<T>` | `signal<T>(initialValue)` |
| `StateNotifierProvider` / `NotifierProvider` | `CubitSignal<State>` |
| `StreamProvider<T>` | `streamSignal(() => stream)` |
| `ref.watch(provider)` | `computed(() => dependencySignal.value)` |
| `AsyncValue<T>` | `ReadonlySignal<AsyncState<T>>` or Stale-While-Revalidate caching |

## Migration Code Example

```dart
// ❌ Legacy Riverpod StateNotifier
class TaskNotifier extends StateNotifier<AsyncValue<List<Task>>> {
  TaskNotifier(this._repository) : super(const AsyncValue.loading());
  final TaskRepository _repository;
}

// ✅ Migrated BlocSignal CubitSignal
class TaskBoardCubit extends CubitSignal<TaskBoardState> {
  TaskBoardCubit({required TaskRepository repository})
      : super(initialState: (tasks: repository.tasks.value, ...)) {
    final computedState = computed(() => ...);
    _disposeEffect = computedState.subscribe(emit);
  }
}
```
