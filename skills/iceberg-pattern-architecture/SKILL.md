---
name: iceberg-pattern-architecture
description: Design real-time Flutter apps with the Iceberg Pattern, pairing submerged repository engines with screen-scoped facades, dual-track mutations, and pure Dart 3 records for 0ms optimistic UI. Use when architecting real-time Flutter/Dart applications, refactoring stream-heavy Clean Architecture codebases, or eliminating StreamBuilder anti-patterns.
license: MIT
metadata:
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
                    ┌───────────▼────────────┐
                    │   REAL-TIME CLOUD      │  Firestore / WebSocket / SSE
                    └────────────────────────┘
```

## Core Architectural Axioms

1. **Collapse Asynchrony at the Waterline**: Asynchronous streams (Firestore snapshots, WebSockets, gRPC streams) are submerged inside the Repository Engine. Above the waterline (Cubits and UI), all data flow is 100% synchronous projection (`UI = f(State)`).
2. **Dual-Track Mutations**:
   - **Optimistic Track (0ms latency)**: Used for high-frequency, non-destructive user actions (e.g. toggling checkboxes). State updates instantly across all screens in 0ms; syncs in background; silently rolls back on failure using atomic `batch()`.
   - **Pessimistic Track**: Used for destructive or irreversible actions (e.g. resource deletion). Awaits cloud confirmation while providing row-level/action-level loading indicators in the screen state.
3. **Screen-Scoped Facades**: Use `CubitSignal` as a lightweight screen facade to transform domain signals into view-specific models, handle ephemeral UI filters, and translate repository exceptions into standard BLoC error streams (`onError`).
4. **Stale-While-Revalidate UX**: On network disconnects or cloud write rejections, keep cached state visible with a non-intrusive warning banner instead of tearing down the UI or replacing screens with error widgets.
5. **Pure Dart 3 Data Layer**: Domain entities are represented using pure Dart 3 records (`typedef Task = ({String id, String title, bool isCompleted, List<String> tags});`), removing boilerplate like `copyWith`, `props`, or code generation.

---

## Technical Deep-Dive & Layer Responsibilities

### Tier 1: External Datastore Layer
- Cloud infrastructure (Firebase, Supabase, WebSockets, gRPC, SSE).
- Produces real-time event streams and remote mutation endpoints.

### Tier 2: Submerged Repository Engine (`TaskRepository`)
- Submerges cloud streams into pure Dart using `streamSignal()`.
- Stores optimistic overrides in a private `signal<Map<String, bool>>`.
- Exposes derived state via a memoized `computed()` signal.
- Enforces in-flight mutation guards (`Set<String>`) to prevent re-entrant double-tap race conditions.

### Tier 3: Screen Facade (`TaskBoardCubit`)
- Listens synchronously to repository signals.
- Computes screen-scoped view models (e.g., active category filters).
- Routes async background exceptions directly to `onError(error, st)`.

### Tier 4: Synchronous Presentation Layer (`TaskBoardScreen`)
- Renders UI purely using `BlocBuilder` or `SignalBuilder`.
- Eliminates `StreamBuilder` and `FutureBuilder` anti-patterns.
- Projects UI state synchronously in Frame 0.

---

## Workflow Checklist for Implementation

Progress:
- [ ] Step 1: Define Domain Model using Pure Dart 3 records (see `references/domain-and-engine.md`).
- [ ] Step 2: Build Submerged Repository Engine with `streamSignal`, local `signal` patches, and `computed` outputs.
- [ ] Step 3: Implement Dual-Track Mutations (`toggleTask` with optimistic `batch()` rollback, `deleteTask` with pessimistic await).
- [ ] Step 4: Create Screen Facade (`CubitSignal`) connecting Repository signals to UI-filtered state.
- [ ] Step 5: Connect Flutter UI using `BlocBuilder` (zero `StreamBuilder` or `FutureBuilder` widgets in UI).
- [ ] Step 6: Validate architecture by executing `scripts/validate_iceberg_architecture.py lib/`.

---

## Automated Architectural Validator

This skill bundles an executable analysis script to verify codebase adherence:

```bash
python3 scripts/validate_iceberg_architecture.py <path-to-lib>
```

For detailed architecture diagrams, comparisons, and engine implementation code templates, see:
- [4-Tier Architecture Taxonomy Reference](references/architecture-layers.md)
- [Dual-Track Mutation Protocol Reference](references/dual-track-mutations.md)
- [In-Flight Mutation Guards Reference](references/in-flight-mutation-guards.md)
- [Clean Architecture vs. Iceberg Pattern Comparison](references/clean-vs-iceberg.md)
- [Stale-While-Revalidate Caching Reference](references/stale-while-revalidate.md)
- [Domain & Submerged Engine Reference](references/domain-and-engine.md)
- [Facade & Flutter UI Reference](references/facade-and-ui.md)
