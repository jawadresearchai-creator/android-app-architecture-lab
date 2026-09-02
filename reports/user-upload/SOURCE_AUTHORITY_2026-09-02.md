# DocVault Source Authority — 2026-09-02

Authoritative editable source supplied by the user:

- file: `Document Vault.rar`
- conversation file id: `file_00000000239c820894799cedf4a40781`
- size: 342,302,898 bytes
- uploaded UTC: 2026-09-02T07:39:07.247Z

## Authority rule

This RAR supersedes the historical `document-vault.zip` and the reconstructed `docvault-reconstructed-p1` branch as the source of truth.

The reconstructed branch is retained only as a comparison/reference for P1 ideas. Do not merge it into the authoritative source wholesale.

## Required continuation

1. Extract the RAR.
2. Identify the Gradle root and app module.
3. Compare real source scanner components (`ScannerScreen`, `DocumentDetector`, `DocumentImageProcessor`, `DocumentQuad`, crop/loupe code, `VaultViewModel`, OCR and tests) against the current APK and the parity specification.
4. Preserve every source implementation that is newer or stronger than the reconstruction.
5. Port only missing P1 features.
6. Run `testDebugUnitTest` and `assembleDebug` (or the equivalent tasks exposed by the project).
7. Fix failures until CI is green before physical-device validation.

## Temporary environment note

At the time this authority record was written, the chat execution/container runtime was failing before command startup, so archive extraction had not yet been performed. This is an execution-environment limitation, not a source-file problem. No source modifications should be claimed until extraction and build validation actually occur.
