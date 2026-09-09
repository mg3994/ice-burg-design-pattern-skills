# The 4-Tier Iceberg Architecture Taxonomy

The Iceberg Pattern splits a real-time application into four distinct architectural tiers divided by the **Waterline**.

```
═════════════════════════════════════════════════════════════════════════════ ABOVE WATERLINE (SYNCHRONOUS)
TIER 4: SYNCHRONOUS FLUTTER PRESENTATION LAYER
- Flutter Screen Widgets (`TaskBoardScreen`)
- Pure synchronous UI projections (`UI = f(State)`) via `BlocBuilder` / `SignalBuilder`
- Zero async builders (`StreamBuilder` / `FutureBuilder`) in widget tree

TIER 3: VISIBLE SCREEN FACADE LAYER
- Screen-scoped controllers (`TaskBoardCubit` extending `CubitSignal<State>`)
- Computes screen-specific view models (e.g. category filters, pagination)
- Handles row-level action loading indicators
- Translates repository background exceptions directly to `onError(error, st)`
═════════════════════════════════════════════════════════════════════════════ WATERLINE (ASYNC BOUNDARY)
TIER 2: SUBMERGED REPOSITORY ENGINE LAYER
- Submerged data engines (`TaskRepository`)
- Quarantines real-time SDK streams using `streamSignal()`
- Tracks un-ACKed optimistic client overrides in `signal<Map<String, Patch>>`
- Merges streams & patches into unified memoized `computed()` signals
- Protects against rapid user double-taps via in-flight `Set<String>` guards

TIER 1: EXTERNAL REAL-TIME CLOUD DATASTORE LAYER
- Cloud infrastructure (Firebase Firestore, Supabase, WebSockets, gRPC, SSE)
- Asynchronous stream producers & remote mutation endpoints
═════════════════════════════════════════════════════════════════════════════ BELOW WATERLINE (ASYNCHRONOUS)
```

## Layer-by-Layer Responsibilities

### Tier 4: Synchronous Presentation Layer
- Renders widgets from synchronous state snapshots in **Frame 0**.
- Listens for one-off side effects (e.g., displaying `SnackBar` messages) via `BlocListener`.
- Dispatches user intent directly to Tier 3 Cubits.

### Tier 3: Visible Screen Facade Layer
- Subscribes to Tier 2 repository signals via `computed()` signals.
- Implements custom structural equality comparators (`equals`) to drop redundant re-renders.
- Manages transient screen UI states (such as active tag filter or deleting spinner ID).

### Tier 2: Submerged Repository Engine Layer
- Submerges Tier 1 streams using `streamSignal()` in pure Dart.
- Manages optimistic patch maps and sync error boolean signals (`hasSyncError`).
- Guarantees atomic state updates using `batch()` during write confirmation or rollback.

### Tier 1: External Cloud Datastore Layer
- Produces real-time event streams and handles network requests over the wire.
