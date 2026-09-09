---
name: flutter-testing-harness-automation
description: Automate Flutter widget testing harnesses, mock real-time stream snapshots, and perform deterministic frame assertions for BlocSignal applications. Use when writing widget or integration tests in Flutter.
license: MIT
metadata:
  category: widget-testing
---

# Flutter Testing Harness Automation

Automating Flutter widget tests for real-time reactive applications requires mocking background stream controllers and verifying widget tree rendering synchronously.

```
┌─────────────────────────────────────────────────────────────┐
│                 WIDGET HARNESS ARCHITECTURE                 │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Fake StreamController│       │ Pure Dart Repository │   │
│   │ (cloudController)    │ ──>   │ (TaskRepository)     │   │
│   └──────────────────────┘       └──────────┬───────────┘   │
│                                             │               │
│                                             ▼               │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ tester.pumpWidget()  │ <──   │ TaskBoardCubit       │   │
│   │ Widget Tree          │       │ (CubitSignal)        │   │
│   └──────────────────────┘       └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Testing Harness Checklist

- [ ] Wrap widget test subjects in `MaterialApp` and `BlocProvider`.
- [ ] Inject fake `StreamController.broadcast()` instances into repositories.
- [ ] Run `python3 scripts/audit_test_coverage.py test/` to verify test suite structure.

For complete widget harness code snippets, see:
- [Widget Test Harness Reference](references/widget-test-harness.md)
