# Clean Architecture to Iceberg Pattern Refactoring Guide

Legacy Clean Architecture codebases often suffer from anemic 3-line use cases, heavy `@freezed` code-generation overhead, and stream leaks in Flutter presentation layers.

## Step 1: Remove Anemic Use Cases & Interactors

In Clean Architecture, developers write pass-through interactors like:

```dart
// ❌ Legacy Clean Architecture Anemic Use Case
class GetTasksUseCase {
  GetTasksUseCase(this.repository);
  final TaskRepository repository;
  Stream<List<Task>> call() => repository.getTasksStream();
}
```

**Iceberg Migration Strategy**: Delete `GetTasksUseCase`. Expose reactive `ReadonlySignal<List<Task>>` directly from `TaskRepository` to the `CubitSignal` facade.

---

## Step 2: Convert OOP Classes / Freezed to Dart 3 Records

```dart
// ❌ Legacy OOP Class with copyWith & Equatable
class Task extends Equatable {
  final String id;
  final String title;
  final bool isCompleted;
  // ... 40 lines of copyWith, props, and constructor ...
}

// ✅ Migrated Iceberg Pure Dart 3 Record
typedef Task = ({
  String id,
  String title,
  bool isCompleted,
  List<String> tags,
});
```

---

## Step 3: Replace `StreamBuilder` with `BlocSignalBuilder`

```dart
// ❌ Legacy StreamBuilder in Widget Tree
StreamBuilder<List<Task>>(
  stream: getTasksUseCase(),
  builder: (context, snapshot) {
    if (snapshot.hasError) return ErrorWidget(...);
    if (!snapshot.hasData) return CircularProgressIndicator();
    return ListView(...);
  },
);

// ✅ Migrated Synchronous Iceberg Projection
BlocBuilder<TaskBoardCubit, TaskBoardState>(
  builder: (context, state) => ListView.builder(
    itemCount: state.tasks.length,
    itemBuilder: (context, index) => TaskTile(task: state.tasks[index]),
  ),
);
```
