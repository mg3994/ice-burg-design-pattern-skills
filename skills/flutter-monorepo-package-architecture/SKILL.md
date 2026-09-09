---
name: flutter-monorepo-package-architecture
description: Architect multi-package Dart Workspaces and Melos monorepos for Flutter applications. Separates pure Dart domain/data packages from Flutter presentation packages for native CLI test execution speed. Use when structuring or refactoring Flutter monorepos.
license: MIT
metadata:
  category: monorepo-architecture
---

# Flutter Monorepo Package Architecture

Multi-package monorepos (using Dart Workspaces or Melos) enforce architectural boundaries by physically isolating Domain and Data layers into pure Dart packages separate from Flutter presentation packages.

```
┌─────────────────────────────────────────────────────────────┐
│                   DART WORKSPACE STRUCTURE                  │
│                                                             │
│   packages/                                                 │
│   ├── app_domain/       (Pure Dart: Records & Signals)      │
│   ├── app_data/         (Pure Dart: Submerged Repositories) │
│   └── app_presentation/ (Flutter UI & Widgets)              │
└─────────────────────────────────────────────────────────────┘
```

## Monorepo Architecture Checklist

- [ ] Ensure `app_domain` and `app_data` packages have no `sdk: flutter` dependency in `pubspec.yaml`.
- [ ] Run domain/data unit tests using `dart test` natively without `flutter test`.
- [ ] Run `python3 scripts/audit_monorepo_dependencies.py .` to audit monorepo layer purity.

For package dependency rules and layering tables, see:
- [Monorepo Package Layering Reference](references/package-layering-rules.md)
