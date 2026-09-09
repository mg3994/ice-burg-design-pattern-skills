# In-Flight Mutation Guards & Re-Entrancy Prevention

When users rapidly double-tap interactive elements (such as checkboxes or delete icons), asynchronous background requests can trigger race conditions if not guarded at the repository level.

## In-Flight Guard Pattern

The Submerged Engine tracks active operation IDs using a private `Set<String>`:

```dart
class TaskRepository {
  // In-flight guard set
  final _inFlightToggles = <String>{};

  Future<void> toggleTask(String id, bool currentStatus) async {
    // 1. Guard against re-entrant calls
    if (_inFlightToggles.contains(id)) return;
    _inFlightToggles.add(id);

    try {
      // 2. Perform optimistic state update
      _optimisticPatches.value = {..._optimisticPatches.value, id: !currentStatus};

      // 3. Sync with cloud backend
      await _updateCloudTask(id, !currentStatus);

      // 4. Reconcile on success
      batch(() {
        _hasSyncError.value = false;
        final updated = Map<String, bool>.from(_optimisticPatches.value)..remove(id);
        _optimisticPatches.value = updated;
      });
    } catch (e, st) {
      // 5. Revert on failure
      batch(() {
        final updated = Map<String, bool>.from(_optimisticPatches.value)..remove(id);
        _optimisticPatches.value = updated;
        _hasSyncError.value = true;
      });
      rethrow;
    } finally {
      // 6. Always clean up in-flight set
      _inFlightToggles.remove(id);
    }
  }
}
```
