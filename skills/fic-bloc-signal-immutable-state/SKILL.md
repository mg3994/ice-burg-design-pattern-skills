---
name: fic-bloc-signal-immutable-state
description: Pair BlocSignal / CubitSignal with fast_immutable_collections (IList, ISet, IMap) for bulletproof immutable state management in Flutter. Eliminates ghost rebuilds, corrupted undo stacks, defensive copying GC tax, and concurrent modification crashes. Use when designing collection-heavy Flutter state models.
license: MIT
metadata:
  category: immutable-collections
---

# Fast Immutable Collections (FIC) & BlocSignal

Pairing `BlocSignal` state containers with Marcelo Glasberg's `fast_immutable_collections` (`IList`, `ISet`, `IMap`) eliminates in-place collection mutation bugs and guarantees compile-time immutability with O(1)/O(log N) persistent structural sharing.

```
┌─────────────────────────────────────────────────────────────┐
│                 UNBREAKABLE IMMUTABLE STATE                 │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ IList<CartItem>      │       │ CubitSignal          │   │
│   │ O(1) Copy-on-Write   │ ──>   │ Synchronous Frame 0  │   │
│   │ Structural Sharing   │       │ De-duplication       │   │
│   └──────────────────────┘       └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Immutable Collection Checklist

- [ ] Use `IList<T>`, `ISet<T>`, and `IMap<K, V>` inside state record typedefs.
- [ ] Perform collection updates using `.add()`, `.remove()`, or `.update()` methods returning new immutable instances.
- [ ] Run `python3 scripts/audit_mutable_collections.py lib/` to scan state classes for mutable standard collections.

For the Four Horsemen bug taxonomy and code patterns, see:
- [FIC Patterns & The Four Horsemen Reference](references/fic-patterns-and-horsemen.md)
