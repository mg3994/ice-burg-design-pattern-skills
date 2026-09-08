# Screen Facade & Flutter Presentation Layer

This reference details the screen-scoped facade (`CubitSignal`) and synchronous Flutter presentation UI.

## Visible Boundary: Screen Facade (`TaskBoardCubit`)

```dart
import 'dart:async';
import 'package:bloc_signals/bloc_signals.dart';
import 'package:signals_core/signals_core.dart';
import '../data/task_repository.dart';
import '../domain/task.dart';

typedef TaskBoardState = ({
  List<Task> tasks,
  String? activeFilterTag,
  String? isDeletingTaskId,
  bool hasSyncError,
});

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

  void setFilterTag(String? tag) => _activeFilterTag.value = tag;

  void toggleTask(String id, bool currentStatus) {
    unawaited(
      _repository.toggleTask(id, currentStatus).catchError(
        (Object error, StackTrace st) {
          onError(error, st);
        },
      ),
    );
  }

  Future<void> deleteTask(String id) async {
    _isDeletingTaskId.value = id;
    try {
      await _repository.deleteTask(id);
    } catch (error, stackTrace) {
      onError(error, stackTrace);
    } finally {
      if (!isClosed) {
        _isDeletingTaskId.value = null;
      }
    }
  }

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

  @override
  Future<void> close() async {
    _disposeEffect();
    _activeFilterTag.dispose();
    _isDeletingTaskId.dispose();
    await super.close();
  }
}
```

## Synchronous Flutter Presentation Screen

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../application/task_board_cubit.dart';

class TaskBoardScreen extends StatelessWidget {
  const TaskBoardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocListener<TaskBoardCubit, TaskBoardState>(
      listenWhen: (previous, current) => false,
      listener: (context, state) {},
      child: BlocBuilder<TaskBoardCubit, TaskBoardState>(
        builder: (context, state) {
          return Scaffold(
            appBar: AppBar(
              title: const Text('Iceberg Task Board'),
              bottom: state.hasSyncError
                  ? const PreferredSize(
                      preferredSize: Size.fromHeight(28),
                      child: ColoredBox(
                        color: Colors.amber,
                        child: Center(
                          child: Text(
                            'Offline / Sync Error — Showing Cached Tasks',
                            style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                          ),
                        ),
                      ),
                    )
                  : null,
            ),
            body: Column(
              children: [
                // Filter Chips
                Padding(
                  padding: const EdgeInsets.all(8),
                  child: Row(
                    children: [
                      FilterChip(
                        label: const Text('All'),
                        selected: state.activeFilterTag == null,
                        onSelected: (_) => context.read<TaskBoardCubit>().setFilterTag(null),
                      ),
                      const SizedBox(width: 8),
                      FilterChip(
                        label: const Text('Work'),
                        selected: state.activeFilterTag == 'work',
                        onSelected: (_) => context.read<TaskBoardCubit>().setFilterTag('work'),
                      ),
                    ],
                  ),
                ),
                // Task List (Zero Async Builders!)
                Expanded(
                  child: ListView.builder(
                    itemCount: state.tasks.length,
                    itemBuilder: (context, index) {
                      final task = state.tasks[index];
                      final isDeleting = state.isDeletingTaskId == task.id;

                      return ListTile(
                        leading: Checkbox(
                          value: task.isCompleted,
                          onChanged: isDeleting
                              ? null
                              : (_) => context
                                  .read<TaskBoardCubit>()
                                  .toggleTask(task.id, task.isCompleted),
                        ),
                        title: Text(
                          task.title,
                          style: TextStyle(
                            decoration: task.isCompleted ? TextDecoration.lineThrough : null,
                          ),
                        ),
                        trailing: isDeleting
                            ? const SizedBox.square(
                                dimension: 20,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              )
                            : IconButton(
                                icon: const Icon(Icons.delete_outline),
                                onPressed: () => context
                                    .read<TaskBoardCubit>()
                                    .deleteTask(task.id),
                              ),
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
```
