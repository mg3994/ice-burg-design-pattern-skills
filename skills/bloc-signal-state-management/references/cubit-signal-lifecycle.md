# CubitSignal Lifecycle & Effect Management

Understanding the instantiation and teardown cycle of `CubitSignal` prevents memory leaks and stale subscriptions.

```
       [ Cubit Instantiation ]
                  │
                  ▼
       [ Define Private Signals ]
       (_activeFilterTag, _isDeletingTaskId)
                  │
                  ▼
       [ Construct computed() State ]
                  │
                  ▼
  [ Subscribe effect: state.subscribe(emit) ]
                  │
                  ▼
       [ Active Presentation Phase ]
                  │
                  ▼
         [ Cubit.close() Called ]
                  │
                  ▼
      [ Dispose computed Effect ]
                  │
                  ▼
     [ Dispose Private Signals ]
                  │
                  ▼
       [ super.close() Resolved ]
```

## Recommended Disposing Idiom

```dart
class TaskBoardCubit extends CubitSignal<TaskBoardState> {
  TaskBoardCubit({required TaskRepository repository})
      : _repository = repository,
        super(initialState: ...) {
    _initFacade();
  }

  final _activeFilterTag = signal<String?>(null);
  late final void Function() _disposeEffect;

  void _initFacade() {
    final computedState = computed(() {
      // Build view state synchronously
      return (...);
    });

    // Save dispose callback returned by subscribe()
    _disposeEffect = computedState.subscribe(emit);
  }

  @override
  Future<void> close() async {
    _disposeEffect(); // Teardown effect subscription first
    _activeFilterTag.dispose(); // Teardown private signals
    await super.close();
  }
}
```
