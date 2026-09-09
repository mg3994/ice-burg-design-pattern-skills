# FIC & BlocSignal: The Four Horsemen & Structural Sharing

Pairing `BlocSignal` with `fast_immutable_collections` (`IList`, `ISet`, `IMap`) eliminates in-place collection state bugs in Flutter applications.

## The Four Horsemen of Collection State Bugs

```
┌────────────────────────────────────────────────────────────────────────┐
│               THE FOUR HORSEMEN OF COLLECTION STATE BUGS               │
├──────────────────────────┬─────────────────────────────────────────────┤
│ 1. The Ghost Rebuild     │ In-place mutation (state.items.add(x)) has  │
│    (Skipped Rebuild)     │ identical identity: emit() drops the change │
│                          │ and Flutter's UI stays frozen!              │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 2. Corrupted Undo Stack  │ Time-travel history buffers hold pointers   │
│    (Historical Amnesia)  │ to the same mutable list: mutating present  │
│                          │ silently corrupts past snapshots!           │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 3. Defensive Copy Tax    │ Writing [...state.items, x] copies N items  │
│    (Garbage Collector)   │ on every keystroke: memory spikes and 120Hz │
│                          │ frame drops.                                │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 4. Concurrent Mutation   │ ListView.builder iterates while an async    │
│    Crash                 │ handler modifies the list in-place: throws  │
│                          │ ConcurrentModificationError at runtime.     │
└──────────────────────────┴─────────────────────────────────────────────┘
```

## FIC State Construction Code Pattern

```dart
import 'package:fast_immutable_collections/fast_immutable_collections.dart';
import 'package:bloc_signals/bloc_signals.dart';

/// Unbreakable Shopping Cart State defined with Dart 3 record syntax
typedef CartState = ({
  IList<CartItem> items,
  IMap<String, int> itemQuantities,
  bool isCheckingOut,
});

class CartCubit extends CubitSignal<CartState> {
  CartCubit()
      : super(
          initialState: (
            items: IList<CartItem>(),
            itemQuantities: IMap<String, int>(),
            isCheckingOut: false,
          ),
        );

  void addItem(CartItem item) {
    // ✅ O(1) / O(log N) Persistent Structural Sharing
    final newItems = stateValue.items.add(item);
    final newQuantities = stateValue.itemQuantities.add(item.id, 1);

    emit((
      items: newItems,
      itemQuantities: newQuantities,
      isCheckingOut: false,
    ));
  }
}
```
