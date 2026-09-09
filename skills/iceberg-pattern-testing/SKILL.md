---
name: iceberg-pattern-testing
description: Write fast, declarative unit and integration tests for Iceberg Pattern Flutter applications using bloc_signals_test. Features pure Dart testing, 0ms optimistic verification, and silent rollback assertion without Flutter widget spinners or mock platform channels.
license: MIT
metadata:
  category: testing
---

# Iceberg Pattern Unit & Declarative Testing

Because the Domain Model, Repository Engine, and Cubit Facade in the Iceberg Pattern are pure Dart, architecture tests run instantly in pure Dart without spinning up Flutter engines or mocking platform channels.

```
┌─────────────────────────────────────────────────────────────┐
│                 blocSignalTest execution                    │
│                                                             │
│   1. build()    -> Instantiate pure Dart repository & cubit │
│   2. act()      -> Trigger cubit method (e.g. toggleTask)   │
│   3. expect()   -> Assert synchronous 0ms optimistic state   │
│   4. wait/error -> Assert background stream sync or rollback│
└─────────────────────────────────────────────────────────────┘
```

## Key Testing Capabilities

1. **0ms Optimistic Latency Testing**: Verify that an optimistic action emits state changes instantly (Frame 1) *before* the async cloud future completes.
2. **Rollback & Exception Assertions**: Verify that a cloud rejection silently reverts the optimistic state change and triggers the `onError` error stream.
3. **Synchronous Stream Integration**: Test stream snapshot updates from fake cloud controllers (`StreamController.broadcast()`) synchronously with zero microtask lag.

---

## Testing Workflow Checklist

- [ ] Use `blocSignalTest<Cubit, State>` from `package:bloc_signals_test/bloc_signals_test.dart`.
- [ ] Create a `StreamController<List<Task>>.broadcast()` to simulate real-time cloud snapshot updates.
- [ ] Test 1: **Cloud Stream Sync** — Push stream event to `cloudController.add(...)` and expect updated state array.
- [ ] Test 2: **0ms Optimistic Update** — Pass a hanging `Completer` to cloud update function, call `toggleTask`, and assert optimistic state emission in Frame 1.
- [ ] Test 3: **Rollback & Sync Error** — Pass throwing function to cloud update, call `toggleTask`, and expect Frame 1 (optimistic) -> Frame 2 (rollback + error flag) -> `errors` matcher.
- [ ] Copy reusable test harness template from `assets/test_suite_template.dart`.

For complete test recipes and executable code examples, see:
- [Testing Recipes Guide](references/testing-recipes.md)
- [Declarative Testing Reference Guide](references/testing-guide.md)
- [Test Suite Asset Template](assets/test_suite_template.dart)
