# DocVault Source Authority Status — 2026-09-02

## Authoritative source

The user supplied `Document Vault.rar` on 2026-09-02. This archive is now the authoritative editable DocVault source baseline.

Observed attachment metadata:
- Filename: `Document Vault.rar`
- Size: 342,302,898 bytes
- Source: direct user upload in the current conversation

## Authority order

1. `Document Vault.rar` — authoritative source to inspect, build and modify.
2. Current `Docvault.apk` / `Docvault(1).apk` — authoritative compiled-build evidence for behavior/version comparison.
3. `docvault-reconstructed-p1` branch — comparison/reference only until reconciled against `Document Vault.rar`.
4. Historical `document-vault.zip` — stale comparison reference only; do not use as modification baseline.

## Required next gate

Before any additional P1 source changes are accepted:
1. extract `Document Vault.rar`;
2. identify Android project root(s), Gradle wrapper, app module and current package/application id;
3. fingerprint source tree and dependency files;
4. compare scanner-critical files against the current APK decompilation and `docvault-reconstructed-p1`;
5. keep real-source implementations where newer/equivalent;
6. port only missing P1 behavior from the reconstructed reference;
7. run `testDebugUnitTest` and `assembleDebug` on the real source;
8. preserve exact changed-file evidence and build artifacts.

## Scanner-critical comparison set

- `ScannerScreen*`
- `DocumentDetector*`
- `DocumentImageProcessor*`
- `DocumentQuad*`
- crop/corner/loupe components
- `VaultViewModel*`
- scan draft/session models
- OCR engine + verification flow
- AndroidManifest camera permissions
- CameraX/ML Kit dependencies
- scanner/unit tests

## Safety / clean-room boundary

CamScanner-derived reports remain behavioral/architectural evidence only. Do not copy proprietary source bodies, native libraries, models, assets, keys or private endpoints into DocVault.

## Current runtime note

The uploaded archive has been materialized successfully, but the current execution runtime is failing before archive-extraction commands start. No source edits from the reconstructed branch should be merged into the authoritative source until extraction and reconciliation have actually run.
