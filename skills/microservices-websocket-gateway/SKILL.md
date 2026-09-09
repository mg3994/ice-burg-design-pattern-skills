---
name: microservices-websocket-gateway
description: Connect real-time client applications to microservice WebSocket and Server-Sent Events (SSE) gateways. Handles heartbeat framing, exponential backoff, and submerging raw socket streams into streamSignals. Use when integrating real-time gateways in Flutter.
license: MIT
metadata:
  category: network-gateways
---

# Microservices WebSocket Gateway Integration

Connecting client applications to backend microservice gateways via WebSockets or Server-Sent Events (SSE) requires robust connection management, heartbeat ping-pong framing, and stream submersion.

```
┌─────────────────────────────────────────────────────────────┐
│                 WEBSOCKET GATEWAY SUBMERSION                │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Microservice Gateway │       │ Heartbeat &          │   │
│   │ (wss://gateway/v1)   │       │ Reconnection Manager │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ streamSignal()    │                     │
│                   │ Submerged Engine  │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Checklist

- [ ] Wrap WebSocket / SSE channel streams in `streamSignal`.
- [ ] Implement heartbeat ping-pong framing to detect silent socket drops.
- [ ] Use exponential backoff with random jitter on connection loss.
- [ ] Test connection backoff using `scripts/simulate_websocket_connection.py`.

For reconnection specifications and protocol details, see:
- [WebSocket Reconnection Protocol Reference](references/websocket-reconnection-protocol.md)
