# Stale-While-Revalidate Caching & Warning Banner UX

The Iceberg Pattern maintains cached state visibility when network connection drops or optimistic mutations fail.

```
┌─────────────────────────────────────────────────────────────┐
│               STALE-WHILE-REVALIDATE UX BANNER              │
│                                                             │
│   Scaffold(                                                 │
│     appBar: AppBar(                                         │
│       title: Text('Task Board'),                            │
│       bottom: state.hasSyncError                            │
│           ? PreferredSize(                                  │
│               child: ColoredBox(                            │
│                 color: Colors.amber,                        │
│                 child: Text('Offline — Showing Cached'),    │
│               ),                                            │
│             )                                               │
│           : null,                                           │
│     ),                                                      │
│     body: TaskListView(tasks: state.tasks),                 │
│   )                                                         │
└─────────────────────────────────────────────────────────────┘
```

## UX Principles

1. **Keep Cached Data Visible**: Never dismantle the list view or show full-screen error widgets when a background write fails.
2. **Top Warning Banner**: Display a non-intrusive amber banner in `AppBar.bottom` when `hasSyncError == true`.
3. **SnackBar Error Toasts**: Trigger one-off error notifications via `BlocListener` when background exceptions hit `onError`.
