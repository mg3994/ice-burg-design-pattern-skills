# Firebase Firestore Real-Time Snapshot Submersion

Submerging Cloud Firestore `snapshots()` streams beneath the repository waterline isolates Flutter UI widgets from SDK listener lifecycle management.

```
┌─────────────────────────────────────────────────────────────┐
│                 FIRESTORE SNAPSHOT SUBMERSION               │
│                                                             │
│   Firestore SDK: FirebaseFirestore.instance.collection()     │
│                         │                                   │
│                 .snapshots() Stream                         │
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

## Submersion Pattern Code

```dart
class FirestoreTaskRepository {
  FirestoreTaskRepository(FirebaseFirestore firestore) : _firestore = firestore {
    _streamSignal = streamSignal(
      () => _firestore
          .collection('tasks')
          .snapshots()
          .map((snapshot) => snapshot.docs.map(_docToTask).toList()),
      options: AsyncSignalOptions(initialValue: []),
    );
  }

  final FirebaseFirestore _firestore;
  late final StreamSignal<List<Task>> _streamSignal;

  ReadonlySignal<List<Task>> get tasks => _streamSignal;

  Task _docToTask(QueryDocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return (
      id: doc.id,
      title: data['title'] as String? ?? '',
      isCompleted: data['isCompleted'] as bool? ?? false,
      tags: List<String>.from(data['tags'] ?? []),
    );
  }
}
```
