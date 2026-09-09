# gRPC Server-Streaming vs. GraphQL Subscriptions

| Dimension | gRPC Server-Streaming (`ResponseStream<T>`) | GraphQL Subscriptions (`WebSocket`) |
| :--- | :--- | :--- |
| **Protocol** | HTTP/2 Multiplexed Binary Streams (Protobuf) | WebSocket / HTTP GET EventStream (JSON) |
| **Parsing Cost** | Low (Fast Protobuf Binary Deserialization) | Higher (JSON parsing + string key lookups) |
| **Reconnection** | Native HTTP/2 channel re-establishment | Requires WebSocket keep-alive & reconnect handshakes |
| **Iceberg Submersion** | `streamSignal(() => client.listenToUpdates())` | `streamSignal(() => client.subscribe(query))` |

## gRPC Iceberg Submersion Engine Pattern

```dart
class TaskGrpcRepository {
  TaskGrpcRepository(TaskServiceClient client) : _client = client {
    _streamSignal = streamSignal(
      () => _client.subscribeTasks(Empty()),
      options: AsyncSignalOptions(initialValue: []),
    );
  }

  final TaskServiceClient _client;
  late final StreamSignal<List<Task>> _streamSignal;

  ReadonlySignal<List<Task>> get tasks => _streamSignal;
}
```
