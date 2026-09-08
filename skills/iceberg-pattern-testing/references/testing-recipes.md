# Iceberg Pattern Testing Recipes

Declarative unit tests for Iceberg Pattern applications leverage `blocSignalTest` to verify asynchronous cloud sync, 0ms optimistic UI emissions, and silent exception rollbacks in pure Dart.

## Recipe 1: 0ms Optimistic UI Verification

Verify that toggling a task emits state synchronously in Frame 1 *before* the async server future finishes:

```dart
blocSignalTest<TaskBoardCubit, TaskBoardState>(
  'emits optimistic completed status in 0ms before cloud write finishes',
  build: () {
    final completer = Completer<void>(); // Unresolved future simulates network flight
    repository = TaskRepository(
      cloudSnapshotStream: cloudController.stream,
      updateCloudTask: (_, __) => completer.future,
      deleteCloudTask: (_) async {},
      initialTasks: [
        (id: '1', title: 'Test Task', isCompleted: false, tags: const <String>[]),
      ],
    );
    return TaskBoardCubit(repository: repository);
  },
  act: (cubit) => cubit.toggleTask('1', false),
  expect: () => [
    equalsTaskBoardState((
      tasks: [(id: '1', title: 'Test Task', isCompleted: true, tags: const <String>[])],
      activeFilterTag: null,
      isDeletingTaskId: null,
      hasSyncError: false,
    )),
  ],
);
```

## Recipe 2: Silent Rollback & Exception Assertion

Verify that when a network request fails, the repository silently reverts local optimistic overrides and routes the exception to `onError`:

```dart
blocSignalTest<TaskBoardCubit, TaskBoardState>(
  'silently rolls back state and triggers onError on cloud rejection',
  build: () {
    repository = TaskRepository(
      cloudSnapshotStream: cloudController.stream,
      updateCloudTask: (_, __) async => throw Exception('Cloud timeout'),
      deleteCloudTask: (_) async {},
      initialTasks: [
        (id: '1', title: 'Test Task', isCompleted: false, tags: const <String>[]),
      ],
    );
    return TaskBoardCubit(repository: repository);
  },
  act: (cubit) => cubit.toggleTask('1', false),
  wait: const Duration(milliseconds: 15),
  expect: () => [
    // Frame 1: Optimistic toggle
    equalsTaskBoardState((
      tasks: [(id: '1', title: 'Test Task', isCompleted: true, tags: const <String>[])],
      activeFilterTag: null,
      isDeletingTaskId: null,
      hasSyncError: false,
    )),
    // Frame 2: Silent rollback to server truth + hasSyncError: true
    equalsTaskBoardState((
      tasks: [(id: '1', title: 'Test Task', isCompleted: false, tags: const <String>[])],
      activeFilterTag: null,
      isDeletingTaskId: null,
      hasSyncError: true,
    )),
  ],
  errors: () => [
    isA<SyncRollbackException>(),
  ],
);
```
