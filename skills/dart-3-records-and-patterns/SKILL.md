---
name: dart-3-records-and-patterns
description: Leverage pure Dart 3 Records, exhaustive Pattern Matching, Guard clauses, Sealed Class hierarchies, and Class Modifiers for boilerplate-free domain models. Use when designing Dart 3 domain models or refactoring legacy Equatable/Freezed classes.
license: MIT
metadata:
  category: dart3
---

# Dart 3 Records, Patterns & Class Modifiers

Dart 3 introduces Records, Pattern Matching, and Class Modifiers (`sealed`, `final`, `interface`, `base`) to express complex domain modeling with zero code generation or runtime reflection overhead.

```
┌─────────────────────────────────────────────────────────────┐
│                    DART 3 DOMAIN PRIMITIVES                 │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Typedef Records      │       │ Pattern Destructuring│   │
│   │ typedef Task = ({..})│       │ switch (task) {..}   │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Structural        │                     │
│                   │ Value Equality    │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Core Constructs

### 1. Named Record Typedefs
```dart
typedef Task = ({
  String id,
  String title,
  bool isCompleted,
  List<String> tags,
});
```

### 2. Pattern Matching & Switch Expressions
```dart
String describeState(TaskState state) => switch (state) {
  (:final tasks, hasSyncError: true) => 'Offline (${tasks.length} cached)',
  (:final tasks, activeFilterTag: final filter?) => 'Filtered ($filter): ${tasks.length}',
  (:final tasks, activeFilterTag: null) => 'All tasks: ${tasks.length}',
};
```

---

## Workflow Checklist

- [ ] Replace `@freezed` / `Equatable` data classes with Dart 3 Records.
- [ ] Run `python3 scripts/audit_dart3_features.py lib/` to scan for legacy class boilerplate.

For record comparisons and pattern matching idioms, see:
- [Records vs. Classes Comparison](references/records-vs-classes.md)
