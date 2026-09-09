# Flutter Rebuild & Fine-Grained Performance Optimization

Maintaining 60 FPS (16.6ms frame budget) or 120 FPS (8.3ms frame budget) requires eliminating unnecessary widget rebuilds and layout recalculations.

## 1. Fine-Grained Signals vs. Coarse-Grained BLoCs

In traditional BLoC, updating a single property in a state object triggers a rebuild of all `BlocBuilder` widgets listening to that state unless `buildWhen` is explicitly written for every widget.

With Fine-Grained Signals (`BlocSignal`), only widgets that consume modified signal fields re-render:

```dart
// ❌ Coarse Rebuild: Rebuilds whole screen list on counter change
BlocBuilder<TaskCubit, TaskState>(
  builder: (context, state) => ...
);

// ✅ Fine-Grained Rebuild: Rebuilds ONLY the specific task row
Widget build(BuildContext context) {
  final task = context.select((TaskBoardCubit c) => c.taskById(id));
  return ListTile(title: Text(task.title));
}
```

## 2. Rebuild Elimination Techniques

1. **`const` Widget Constructors**: Always mark static subtrees `const` to bypass element tree rebuild passes.
2. **Repaint Boundaries**: Wrap complex paint operations (e.g., custom canvases or heavy list items) in `RepaintBoundary` to isolate rasterization layers.
3. **ListView Item Keys**: Pass explicit `Key(task.id)` to `ListView.builder` items to preserve element state during dynamic list re-ordering.
4. **Custom Record Comparators**: Use custom structural record equality on `CubitSignal` constructors to drop redundant state emissions.
