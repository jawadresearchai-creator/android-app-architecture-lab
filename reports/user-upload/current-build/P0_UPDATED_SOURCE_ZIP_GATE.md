# P0 — Updated Source ZIP Gate

Before modifying DocVault source, verify the forthcoming ZIP against the current APK (`87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`).

Required authored-source checks:

- `domain/image/DocumentDetector.kt` exists and contains the APK-era candidate/edge/confidence detector or a newer replacement.
- `DocumentImageProcessor.detectDocumentQuad()` uses that detector or a superseding implementation.
- `DocumentImageProcessor.rectifyPerspective()` is not the stale Matrix+bounding-box-fallback version from the old Library ZIP.
- `DocumentGeometry.kt` contains the newer quad helpers or superseding geometry logic.
- `DocumentCropView.kt` contains current crop confidence/loupe/interaction improvements.
- `ScannerScreen.kt` is classified as external one-shot capture or a newer internal CameraX implementation.
- `VaultViewModel.kt`, Room entities/DAOs, OCR, security, backup and AI files are diffed against current APK evidence before any patch.

Output artifacts after reconciliation:

1. source file manifest + SHA-256 list;
2. old-vs-new changed-file inventory;
3. current APK-vs-source capability reconciliation;
4. build/test baseline;
5. only then P1 scanner changes.
