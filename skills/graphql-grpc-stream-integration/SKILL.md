---
name: graphql-grpc-stream-integration
description: Submerge gRPC server-streaming (ResponseStream) and GraphQL WebSocket subscriptions beneath the Iceberg repository waterline using streamSignal and signals_core. Use when integrating gRPC or GraphQL real-time streams into Flutter applications.
license: MIT
metadata:
  category: network-streams
---

# gRPC & GraphQL Stream Integration

Integrating real-time gRPC HTTP/2 streams or GraphQL WebSocket subscriptions requires quarantining transport-layer subscriptions inside Submerged Repositories to keep UI layers 100% synchronous.

```
┌─────────────────────────────────────────────────────────────┐
│                 NETWORK STREAM SUBMERSION                   │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ gRPC ResponseStream  │       │ GraphQL WebSocket    │   │
│   │ (HTTP/2 Binary)      │       │ Subscription         │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ streamSignal()    │                     │
│                   │ Submerged Engine  │                     │
│                   └─────────┬─────────┘                     │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ ReadonlySignal<T> │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Protocol Submersion Checklist

- [ ] Wrap gRPC `ResponseStream` or GraphQL `subscribe()` inside `streamSignal`.
- [ ] Provide safe fallback initial values in `AsyncSignalOptions`.
- [ ] Run `python3 scripts/audit_stream_subscriptions.py lib/` to scan for presentation-layer leaks.

For protocol comparisons and code templates, see:
- [gRPC vs GraphQL Stream Comparison](references/grpc-vs-graphql-streams.md)
