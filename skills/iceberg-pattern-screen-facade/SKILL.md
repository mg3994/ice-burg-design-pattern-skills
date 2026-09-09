---
name: iceberg-pattern-screen-facade
description: Implement the Visible Screen Facade tier of the Iceberg Pattern using CubitSignal. Filters domain data, tracks ephemeral screen state, manages row-level spinners, and forwards repository errors to BLoC onError. Use when building screen controllers.
license: MIT
metadata:
  category: iceberg-facade
---

# Screen Facade Tier Architecture

The Visible Screen Facade is Tier 3 of the Iceberg Pattern. It sits directly above the Waterline and transforms domain signals into screen-scoped presentation state.

```
┌─────────────────────────────────────────────────────────────┐
│                    VISIBLE SCREEN FACADE                    │
│                                                             │
│   Submerged Repository Signal  ──>   CubitSignal Facade     │
│   ReadonlySignal<List<Task>>         TaskBoardCubit         │
│                                            │                │
│                                  [ Screen Filters ]         │
│                                  [ Row-level Spinners ]     │
│                                  [ Exception Routing ]      │
│                                            │                │
│                                            ▼                │
│                                  Synchronous Presentation   │
└─────────────────────────────────────────────────────────────┘
```

## Facade Checklist

- [ ] Extend `CubitSignal<State>` in screen facade classes.
- [ ] Compute view models from repository signals via `computed()`.
- [ ] Pass custom structural record equality comparator (`equals`) to constructor.
- [ ] Route background mutation exceptions to `onError(error, st)`.
- [ ] Run `python3 scripts/verify_screen_facade.py lib/` to audit screen facades.

For facade code templates and patterns, see:
- [Screen Facade Patterns Reference](references/facade-patterns.md)
