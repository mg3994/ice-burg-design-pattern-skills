---
name: riverpod-to-bloc-signal-migration
description: Migrate legacy Riverpod StateNotifierProvider, AsyncValue, and ConsumerWidget codebases to BlocSignal CubitSignal facades and fine-grained signals_core primitives. Use when refactoring Riverpod applications to BlocSignal.
license: MIT
metadata:
  category: state-migration
---

# Riverpod to BlocSignal Migration Guide

Migrating applications from Riverpod (`StateNotifierProvider`, `AsyncValue`) to `BlocSignal` (`CubitSignal`, `streamSignal`) reduces provider scope complexity and eliminates `WidgetRef` lifecycle memory leaks.

```
┌─────────────────────────────────────────────────────────────┐
│                      RIVERPOD MIGRATION                     │
│                                                             │
│   Legacy Riverpod Architecture     ──>    BlocSignal        │
│   ────────────────────────────            ──────────        │
│   StateNotifierProvider            ──>    CubitSignal       │
│   StreamProvider                   ──>    streamSignal      │
│   ConsumerWidget / WidgetRef       ──>    BlocBuilder       │
│   AsyncValue<T>                    ──>    Computed Signals  │
└─────────────────────────────────────────────────────────────┘
```

## Migration Checklist

- [ ] Replace `StateNotifierProvider` classes with `CubitSignal<State>`.
- [ ] Replace `StreamProvider` with repository-level `streamSignal()`.
- [ ] Convert `ConsumerWidget` classes to standard `StatelessWidget` with `BlocBuilder`.
- [ ] Run `python3 scripts/detect_riverpod_ref_leaks.py lib/` to scan for legacy Riverpod usage.

For mapping tables and migration examples, see:
- [Riverpod to BlocSignal Migration Reference](references/riverpod-migration-guide.md)
