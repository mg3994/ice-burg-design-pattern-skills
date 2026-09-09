# Supabase Realtime Postgres Stream Submersion

Submerging Supabase Realtime Postgres Changes (`postgres_changes`) beneath the Iceberg repository waterline isolates Flutter UI widgets from channel lifecycle management and WebSocket reconnections.

```
┌─────────────────────────────────────────────────────────────┐
│                 SUPABASE REALTIME SUBMERSION                │
│                                                             │
│   Supabase SDK: Supabase.instance.client.from('tasks')       │
│                         │                                   │
│            .stream(primaryKey: ['id'])                      │
│                         │                                   │
│                         ▼                                   │
│                   ┌───────────────────┐                     │
│                   │ streamSignal()    │                     │
│                   │ TaskRepository    │                     │
│                   └─────────┬─────────┘                     │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ ReadonlySignal<T> │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Submersion Code Pattern

```dart
class SupabaseTaskRepository {
  SupabaseTaskRepository(SupabaseClient client) : _client = client {
    _streamSignal = streamSignal(
      () => _client
          .from('tasks')
          .stream(primaryKey: ['id'])
          .map((list) => list.map(_mapRowToTask).toList()),
      options: AsyncSignalOptions(initialValue: []),
    );
  }

  final SupabaseClient _client;
  late final StreamSignal<List<Task>> _streamSignal;

  ReadonlySignal<List<Task>> get tasks => _streamSignal;

  Task _mapRowToTask(Map<String, dynamic> row) {
    return (
      id: row['id'] as String,
      title: row['title'] as String,
      isCompleted: row['is_completed'] as bool? ?? false,
      tags: List<String>.from(row['tags'] ?? []),
    );
  }
}
```
