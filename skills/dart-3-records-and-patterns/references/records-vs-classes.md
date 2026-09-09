# Dart 3 Records vs. OOP Classes Comparison

| Attribute | Pure Dart 3 Records (`typedef Task = ({...})`) | Traditional OOP Classes / `@freezed` |
| :--- | :--- | :--- |
| **Boilerplate** | Zero (Single line `typedef`) | Heavy (`copyWith`, `props`, generated `.freezed.dart` files) |
| **Structural Equality** | Built-in by default (`(a: 1) == (a: 1)`) | Manual override of `operator ==` and `hashCode` or build_runner |
| **Destructuring** | Native pattern matching (`final (:title, :isCompleted) = task;`) | Verbose property access (`task.title`, `task.isCompleted`) |
| **Compilation Speed** | Native SDK execution, zero code-gen overhead | Slow `build_runner watch` or `build_runner build` steps |
| **Immutability** | Implicitly immutable values | Requires `final` fields or custom const constructors |

## Record Typedef Idiom

```dart
/// Pure Dart 3 Record representation of a Task domain entity
typedef Task = ({
  String id,
  String title,
  bool isCompleted,
  List<String> tags,
});
```

## Pattern Matching with Records

```dart
String formatTaskStatus(Task task) {
  return switch (task) {
    (:final title, isCompleted: true) => '✅ Completed: $title',
    (:final title, isCompleted: false) => '⏳ Pending: $title',
  };
}
```
