---
name: iceberg-pattern-stale-while-revalidate
description: Implement stale-while-revalidate caching and non-blocking amber error banners in Flutter applications. Retains cached state during network loss and displays top warning banners instead of full-screen error widgets. Use when implementing offline UX.
license: MIT
metadata:
  category: iceberg-ux
---

# Stale-While-Revalidate UX Architecture

Stale-While-Revalidate UX ensures that users retain access to cached data during background network failures or stream drops, presenting non-intrusive warning banners instead of tearing down the UI.

```
┌─────────────────────────────────────────────────────────────┐
│                 STALE-WHILE-REVALIDATE UX                   │
│                                                             │
│   ┌──────────────────────┐       ┌──────────────────────┐   │
│   │ Cached Server State  │       │ hasSyncError Flag    │   │
│   │ (Visible List View)  │       │ (amber top banner)   │   │
│   └──────────┬───────────┘       └──────────┬───────────┘   │
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             ▼                               │
│                   ┌───────────────────┐                     │
│                   │ Non-blocking UI   │                     │
│                   │ Screen Projection │                     │
│                   └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Stale-While-Revalidate Checklist

- [ ] Track `hasSyncError` boolean signal in Submerged Repository Engine.
- [ ] Display an amber top warning banner in `AppBar.bottom` when `hasSyncError == true`.
- [ ] Avoid replacing data lists with full-page error widgets during transient failures.
- [ ] Run `python3 scripts/verify_stale_revalidate.py lib/` to audit UX warning banners.

For banner code snippets and UX principles, see:
- [Caching & Banners Reference](references/caching-and-banners.md)
