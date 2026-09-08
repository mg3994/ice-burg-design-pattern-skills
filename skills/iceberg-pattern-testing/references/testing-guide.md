# Declarative Testing Reference Guide (`blocSignalTest`)

This guide provides full runnable examples for testing Iceberg Pattern architectures with `bloc_signals_test`.

```dart
import 'dart:async';
import 'package:bloc_signals_test/bloc_signals_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:iceberg_pattern_example/application/task_board_cubit.dart';
import 'package:iceberg_pattern_example/data/task_repository.dart';
import 'package:iceberg_pattern_example/domain/task.dart';

void main() {
  group('The Iceberg Pattern Architecture Test Suite', () {
    late StreamController<List<Task>> cloudController;
    late TaskRepository repository;

    setUp(() {
      cloudController = StreamController<List<Task>>.broadcast();
    });

    tearDown(() {
      repository.dispose();
      cloudController.close();
    });

    // 1. Initial Stream Sync Test
    blocSignalTest<TaskBoardCubit, TaskBoardState>(
      'emits updated task list synchronously upon cloud stream emission',
      build: () {
        repository = TaskRepository(
          cloudSnapshotStream: cloudController.stream,
          updateCloudTask: (_, __) async {},
          deleteCloudTask: (_) async {},
        );
        return TaskBoardCubit(repository: repository);
      },
      act: (_) {
        cloudController.add([
          (id: '1', title: 'Write Article', isCompleted: false, tags: ['work']),
        ]);
      },
      wait: const Duration(milliseconds: 10),
      expect: () => [
        equalsTaskBoardState((
          tasks: [(id: '1', title: 'Write Article', isCompleted: false, tags: ['work'])],
          activeFilterTag: null,
          isDeletingTaskId: null,
          hasSyncError: false,
        )),
      ],
    );

    // 2. The 0ms Optimistic Test (emits before cloud completes)
    blocSignalTest<TaskBoardCubit, TaskBoardState>(
      'emits optimistic completed status in 0ms before cloud write finishes',
      build: () {
        final completer = Completer<void>();
        repository = TaskRepository(
          cloudSnapshotStream: cloudController.stream,
          updateCloudTask: (_, __) => completer.future, // Hanging future
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

    // 3. The Rollback & Error Test (reverts state and routes to onError)
    blocSignalTest<TaskBoardCubit, TaskBoardState>(
      'silently rolls back state and triggers onError on cloud rejection',
      build: () {
        repository = TaskRepository(
          cloudSnapshotStream: cloudController.stream,
          updateCloudTask: (_, __) async => throw Exception('Cloud network timeout'),
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
  });
}
```
