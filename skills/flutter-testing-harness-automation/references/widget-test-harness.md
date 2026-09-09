# Automated Flutter Widget & Stream Test Harness

Testing real-time Flutter widgets requires mocking stream controllers and injecting fake repository signals.

```dart
void main() {
  group('TaskBoardScreen Widget Harness', () {
    late StreamController<List<Task>> cloudController;
    late TaskRepository repository;

    setUp(() {
      cloudController = StreamController<List<Task>>.broadcast();
      repository = TaskRepository(
        cloudSnapshotStream: cloudController.stream,
        updateCloudTask: (_, __) async {},
        deleteCloudTask: (_) async {},
        initialTasks: [
          (id: '1', title: 'Test Task', isCompleted: false, tags: const []),
        ],
      );
    });

    tearDown(() {
      repository.dispose();
      cloudController.close();
    });

    testWidgets('renders initial tasks synchronously', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider(
            create: (_) => TaskBoardCubit(repository: repository),
            child: const TaskBoardScreen(),
          ),
        ),
      );

      expect(find.text('Test Task'), findsOneWidget);
    });
  });
}
```
