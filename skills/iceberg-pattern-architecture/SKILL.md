---
name: iceberg-pattern-architecture
description: Design real-time Flutter apps with the Iceberg Pattern, pairing submerged repository engines with screen-scoped facades, dual-track mutations, and pure Dart 3 records for 0ms optimistic UI. Use when architecting real-time Flutter/Dart applications or refactoring stream-heavy Clean Architecture codebases.
license: MIT
metadata:
  author: RandalSchwartz
  category: architecture
---

# Iceberg Pattern Architecture

The Iceberg Pattern is an architectural framework for real-time Flutter and Dart applications designed to solve the limitations of Uncle Bob's Clean Architecture when handling asynchronous streams, optimistic UI, and cloud synchronization.

```
                    ┌────────────────────────┐
                    │      FLUTTER UI        │
                    │  Synchronous Widgets   │
                    └───────────┬────────────┘
════════════════════════════════╪═════════════════════════════════ WATERLINE
                    ┌───────────▼────────────┐
                    │    SCREEN FACADE       │  (Visible Boundary)
                    │   TaskBoardCubit       │  CubitSignal + computed
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   REPOSITORY ENGINE    │  (Submerged Engine)
                    │    TaskRepository      │  streamSignal + signals
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┘
                    │   REAL-TIME CLOUD      │  Firestore / WebSocket / SSE
                    └────────────────────────┘
```

## Core Architectural Axioms

1. **Collapse Asynchrony at the Waterline**: Asynchronous streams (Firestore snapshots, WebSockets, gRPC streams) are submerged inside the Repository Engine. Above the waterline (Cubits and UI), all data flow is 100% synchronous projection (`UI = f(State)`).
2. **Dual-Track Mutations**:
   - **Optimistic Track (0ms latency)**: Used for high-frequency, non-destructive user actions (e.g. toggling checkboxes). State updates instantly across all screens in 0ms; syncs in background; silently rolls back on failure.
   - **Pessimistic Track**: Used for destructive or irreversible actions (e.g. resource deletion). Awaits cloud confirmation while providing row-level/action-level loading indicators.
3. **Screen-Scoped Facades**: Use `CubitSignal` as a lightweight screen facade to transform domain signals into view-specific models, handle ephemeral UI filters, and translate repository exceptions into standard BLoC error streams (`onError`).
4. **Stale-While-Revalidate UX**: On network disconnects or cloud write rejections, keep cached state visible with a non-intrusive warning banner instead of tearing down the UI or replacing screens with error widgets.
5. **Pure Dart 3 Data Layer**: Domain entities are represented using pure Dart 3 records (`typedef Task = ({String id, String title, bool isCompleted, List<String> tags});`), removing boilerplate like `copyWith`, `props`, or code generation.

---

## Workflow Checklist for Implementation

Progress:
- [ ] Step 1: Define Domain Model using Pure Dart 3 records (see `references/domain-and-engine.md`).
- [ ] Step 2: Build Submerged Repository Engine with `streamSignal`, local `signal` patches, and `computed` outputs.
- [ ] Step 3: Implement Dual-Track Mutations (`toggleTask` with optimistic `batch()` rollback, `deleteTask` with pessimistic await).
- [ ] Step 4: Create Screen Facade (`CubitSignal`) connecting Repository signals to UI-filtered state.
- [ ] Step 5: Connect Flutter UI using `BlocBuilder` (zero `StreamBuilder` or `FutureBuilder` widgets in UI).

---

## Gotchas & Critical Rules

- **Never leak streams into UI**: Avoid `StreamBuilder`, `FutureBuilder`, or stream subscriptions inside Flutter widgets. All reactive data must be exposed via `ReadonlySignal` or `CubitSignal`.
- **Atomic Rollbacks with `batch()`**: Always wrap optimistic patch updates and error status changes inside `batch()` blocks to prevent intermediate torn frames.
- **In-Flight Mutation Guards**: Maintain a `Set<String>` of in-flight operation IDs inside the repository engine to prevent rapid re-entrant user taps from triggering race conditions.
- **Pure Dart Portability**: Ensure Domain and Data layers have zero imports from `package:flutter/widgets.dart` or `package:flutter/material.dart`. Keep core logic pure Dart for native execution speed and CLI testability.

For detailed architecture diagrams and engine implementation code templates, see:
- [Domain & Submerged Engine Reference](references/domain-and-engine.md)
- [Facade & Flutter UI Reference](references/facade-and-ui.md)
