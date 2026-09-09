# WebSocket & Gateway Reconnection Protocol

When connecting real-time client applications to microservice gateways via WebSockets or Server-Sent Events (SSE), connection resiliency requires heartbeat ping-pong framing and exponential backoff retry algorithms.

```
┌─────────────────────────────────────────────────────────────┐
│                 WEBSOCKET GATEWAY RECONNECT                 │
│                                                             │
│   Client App               Gateway               Microservice
│       │                       │                       │
│       │─── WebSocket Connect ─>│                       │
│       │<── Connection ACK ────│                       │
│       │                       │<── Event Stream ──────│
│       │<── Push JSON Event ───│                       │
│       │                       │                       │
│       ├─ [ Connection Drop ] ─┤                       │
│       │                       │                       │
│       ├── Exponential Backoff ┤                       │
│       ├── Retry (1s, 2s, 4s) ─>│                       │
│       │<── Reconnected ───────│                       │
└─────────────────────────────────────────────────────────────┘
```

## Reconnection Backoff Spec

1. **Initial Retry**: 1,000ms delay.
2. **Backoff Multiplier**: 2.0x (1s -> 2s -> 4s -> 8s -> 16s).
3. **Jitter**: ±20% random variation to avoid thundering herd problem.
4. **Max Backoff Cap**: 30,000ms.
