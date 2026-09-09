# Signal Graph Telemetry & Debugging Guide

Debugging reactive signal graphs (`signals_core`) requires tracking signal evaluation cycles and catching cyclic update loops.

```
┌─────────────────────────────────────────────────────────────┐
│                 SIGNAL TELEMETRY ENGINE                     │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ signal.value = x     │ ──>   │ DevTools / Console   │   │
│   └──────────┬───────────┘       │ Telemetry Logger     │   │
│              │                   └──────────────────────┘   │
│              ▼                                              │
│   ┌──────────────────────┐                                  │
│   │ computed()           │                                  │
│   │ Re-evaluation Pass   │                                  │
│   └──────────────────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

## 1. DevTools Telemetry Logging Pattern

```dart
void setupSignalTelemetry() {
  SignalsObserver.instance = CustomSignalObserver();
}

class CustomSignalObserver extends SignalsObserver {
  @override
  void onSignalCreated(Signal instance) {
    print('💡 Signal Created: ${instance.name ?? instance.hashCode}');
  }

  @override
  void onSignalUpdated(Signal instance, dynamic value) {
    print('🔄 Signal Updated: ${instance.name ?? instance.hashCode} -> $value');
  }
}
```

## 2. Preventing Infinite Evaluation Loops

An infinite loop occurs when a `computed()` or effect reads a signal and modifies that same signal inside the evaluation pass:

```dart
// ❌ Dangerous Cyclic Update
final counter = signal(0);
effect(() {
  print(counter.value);
  counter.value++; // Triggers infinite loop!
});

// ✅ Correct Non-Cyclic Mutation
final counter = signal(0);
void incrementCounter() => counter.value++;
```
