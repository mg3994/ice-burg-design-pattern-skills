# CQRS & Read-Model Signal Projections

Command-Query Responsibility Segregation (CQRS) separates read operations (Queries) from write operations (Commands).

```
                            ┌────────────────────────┐
                            │      FLUTTER UI        │
                            └───────────┬────────────┘
                                        │
                      ┌─────────────────┴─────────────────┐
                      ▼                                   ▼
          [ COMMAND DISPATCH ]                    [ QUERY PROJECTION ]
          TaskRepository.toggleTask()             ReadonlySignal<List<Task>>
                      │                                   │
                      ▼                                   ▼
            ┌───────────────────┐               ┌───────────────────┐
            │ Write Side        │               │ Read Model        │
            │ (Event Store /    │ ────────────> │ (Computed Signal  │
            │ Cloud Mutations)  │  Event Stream │  Projections)     │
            └───────────────────┘               └───────────────────┘
```

## 1. Command Side (Write Model)

Commands represent user intent. Commands are dispatched asynchronously and do not return data:

```dart
abstract class TaskCommand {}

class ToggleTaskCommand extends TaskCommand {
  ToggleTaskCommand(this.id, this.isCompleted);
  final String id;
  final bool isCompleted;
}
```

## 2. Query Side (Read Model Signals)

Queries are synchronous reactive signals derived from incoming event streams and local optimistic overrides:

```dart
class TaskReadModel {
  TaskReadModel(Stream<List<Task>> cloudStream) {
    _streamSignal = streamSignal(() => cloudStream);
    _readModel = computed(() => _streamSignal.value.value ?? []);
  }

  late final StreamSignal<List<Task>> _streamSignal;
  late final Computed<List<Task>> _readModel;

  ReadonlySignal<List<Task>> get tasks => _readModel;
}
```
