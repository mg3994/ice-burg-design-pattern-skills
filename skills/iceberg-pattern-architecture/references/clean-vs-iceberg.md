# Clean Architecture vs. The Iceberg Pattern

| Architectural Dimension | Uncle Bob's Clean Architecture | The Iceberg Pattern |
| :--- | :--- | :--- |
| **Primary Paradigm** | Imperative Request-Response (`Future<Either<Failure, Success>>`) | Synchronous Reactive State Projection (`UI = f(State)`) |
| **Stream Management** | Leaked to UI via `StreamBuilder` or custom stream listeners | Submerged inside Repository Engine via `streamSignal` |
| **User Interaction Latency** | Network RTT wait (100ms - 2000ms async delay) | 0ms instant optimistic state transition |
| **Entity Representation** | Heavy class OOP models with `@freezed` or `copyWith` boilerplate | Lightweight, native Pure Dart 3 records (`typedef Task = ({...})`) |
| **Use Cases / Interactors** | Anemic 3-line passthrough classes forwarding repository calls | Screen-scoped facades (`CubitSignal`) computing derived UI views |
| **Error Handling** | Full-screen error widgets or destructive state replace | Stale-while-revalidate cached state with non-intrusive warning banners |
| **Testing Overhead** | Complex async mocks, `pumpAndSettle`, widget testers | Pure Dart declarative tests with `blocSignalTest` running in milliseconds |

## Microtask Queue & Latency Breakdown

```
CLEAN ARCHITECTURE LATENCY PIPELINE:
User Tap ──> Cubit/UseCase ──> Async Future ──> Network RTT (200ms) ──> Stream Event ──> UI Rebuild
Total User Perceived Latency: ~200ms - 1500ms 🐢

ICEBERG PATTERN LATENCY PIPELINE:
User Tap ──> Optimistic Patch Signal ──> Synchronous Computed Re-render (Frame 0)
Total User Perceived Latency: 0ms ⚡ (Background sync happens asynchronously)
```

## Architectural Trade-offs

Use Clean Architecture when:
- The app is predominantly offline-first or CRUD-heavy without real-time cloud streams.
- Interaction flows require sequential step-by-step wizard forms where intermediate validation must block navigation.

Use the Iceberg Pattern when:
- App relies on real-time web sockets, Firestore streams, gRPC channels, or Server-Sent Events (SSE).
- Users demand desktop-grade, zero-latency responsive feedback (e.g. check boxes, toggle buttons, live counters).
- You want to reduce architectural boilerplate and speed up unit execution times by 10x.
