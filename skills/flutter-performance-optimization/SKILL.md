---
name: flutter-performance-optimization
description: Optimize Flutter app performance, target 60/120 FPS frame budgets, eliminate redundant widget rebuilds with fine-grained signals, audit memory leaks, and isolate paint layers. Use when profiling or optimizing performance in Flutter applications.
license: MIT
metadata:
  author: RandalSchwartz
  category: performance
---

# Flutter Performance Optimization & Rebuild Elimination

Achieving smooth 60 FPS (16.6ms per frame) or 120 FPS (8.3ms per frame) animations in Flutter requires minimizing widget rebuilds, reducing element tree diffing cost, and preventing memory leaks.

```
┌─────────────────────────────────────────────────────────────┐
│                 FLUTTER FRAME PIPELINE                      │
│                                                             │
│   Build Phase   ──>   Layout Phase   ──>   Paint Layer      │
│   (Widget Tree)       (RenderObject)       (Rasterizer)     │
│        │                   │                    │           │
│        ▼                   ▼                    ▼           │
│   Minimize via        Bypass with          Isolate via      │
│   Signals & `const`   Fixed Constraints    RepaintBoundary  │
└─────────────────────────────────────────────────────────────┘
```

## Performance Principles

1. **Fine-Grained Signal Rebuilds**: Target widget rebuilds exclusively to components whose dependent state has mutated.
2. **Static Construction (`const`)**: Mark all static subtrees `const` to skip widget creation and element reconciliation phases.
3. **Layer Isolation**: Use `RepaintBoundary` around complex subtrees to create separate Compositing Layers.
4. **Key Preservation**: Pass unique keys (`Key(item.id)`) to dynamically reordered lists to prevent element destruction.

---

## Performance Audit Checklist

- [ ] Audit presentation code using `scripts/audit_flutter_performance.py lib/`.
- [ ] Wrap `ListView.builder` items with explicit item keys.
- [ ] Isolate heavy custom painting or canvas widgets using `RepaintBoundary`.
- [ ] Pass custom `equals` functions to `CubitSignal` to eliminate redundant frame triggers.

For rebuild optimization comparisons and code patterns, see:
- [Rebuild Optimization Guide](references/rebuild-optimization.md)
