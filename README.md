# Android App Architecture Lab

Private workspace for repeatable static analysis of Android application packages using JADX and supporting scripts.

## Purpose

This repository turns an APK/APKM/XAPK analysis run into structured engineering outputs that are easier to inspect from ChatGPT than raw decompiled source alone.

## Workflow

1. Place an Android package in `input/` (or run the workflow manually after adding one).
2. GitHub Actions downloads the pinned JADX release.
3. JADX decompiles the package into a temporary workspace.
4. `scripts/analyze_architecture.py` inventories packages, Android components, frameworks, data/network layers, permissions, native libraries, and likely architectural patterns.
5. The workflow uploads both the structured reports and the complete JADX output as GitHub Actions artifacts.

## Outputs

The `reports/` artifact contains:

- `APP_SUMMARY.md`
- `ARCHITECTURE_MAP.md`
- `ANDROID_COMPONENTS.md`
- `LIBRARY_INVENTORY.md`
- `NETWORK_AND_DATA_LAYER.md`
- `SEARCH_INDEX.txt`
- `analysis.json`

The full JADX tree is retained as a separate workflow artifact so it does not have to be committed to Git history.

## Security and clean-room use

This repository is intended for lawful analysis of apps you are authorized to inspect. Treat third-party decompiled code as reference material: derive architecture, interfaces, feature behavior, and requirements, then implement your own code rather than copying proprietary source, secrets, assets, or protected backend logic.

## Pinned tooling

- JADX: `1.5.6`
- Runner: GitHub-hosted Ubuntu
- Java: Temurin 21
- Python: 3.x

