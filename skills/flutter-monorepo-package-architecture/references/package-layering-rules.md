# Monorepo Package Layering Rules

In production Flutter monorepos (managed via Dart Workspaces or Melos), enforce strict boundaries between Pure Dart packages and Flutter Presentation packages.

```
┌─────────────────────────────────────────────────────────────┐
│                 MONOREPO PACKAGE DEPENDENCIES               │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ app_presentation (Flutter Package - UI & Screens)   │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ app_domain (Pure Dart Package - Records & Signals)  │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ app_data (Pure Dart Package - Repository Engines)   │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Layering Rules Table

| Package Layer | Allowed Dependencies | Forbidden Dependencies |
| :--- | :--- | :--- |
| `app_domain` | Pure Dart packages (`signals_core`, `equatable`) | `flutter`, `flutter_test`, `app_presentation` |
| `app_data` | `app_domain`, network/database clients (`http`, `hive`, `grpc`) | `flutter`, `app_presentation` |
| `app_presentation` | `app_domain`, `app_data`, `flutter`, `flutter_bloc` | Direct internal imports of private data models |
