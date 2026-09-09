---
name: signal-graph-debugging-telemetry
description: Debug and trace fine-grained reactive signal graphs using DevTools telemetry, SignalsObserver, and static cycle detection. Prevents infinite evaluation loops and identifies unneeded computations. Use when debugging signals_core or BlocSignal.
license: MIT
metadata:
  category: debugging-telemetry
---

# Signal Graph Debugging & Telemetry

Debugging complex reactive signal graphs requires observing signal value propagation, tracking computed recalculations, and preventing infinite evaluation loops.

```
┌─────────────────────────────────────────────────────────────┐
│                 SIGNAL GRAPH TELEMETRY                      │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ signal.value = x     │ ──>   │ SignalsObserver      │   │
│   └──────────┬───────────┘       │ Telemetry Logger     │   │
│              │                   └──────────────────────┘   │
│              ▼                                              │
│   ┌──────────────────────┐                                  │
│   │ computed()           │                                  │
│   │ Re-evaluation Pass   │                                  │
│   └──────────────────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

## Debugging Checklist

- [ ] Attach `SignalsObserver` in debug builds to log signal creation and mutation events.
- [ ] Ensure `computed()` functions are pure getters with zero side effects or signal assignments.
- [ ] Run `python3 scripts/detect_cyclic_signals.py lib/` to scan for cyclic update bugs.

For observer code patterns and debugging techniques, see:
- [Telemetry & Debugging Guide](references/telemetry-debugging-guide.md)
