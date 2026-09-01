# Updated DocVault ZIP — Intake Checklist

When the actual updated source ZIP is supplied, execute this checklist without another approval round.

1. Record ZIP name, size and SHA-256.
2. Run `scripts/reconcile_docvault_source.py <zip> --out <report-dir>`.
3. Reject the known stale source hash `ab5610a7a1fbe177c17709e2bf79c299a52bb81fb2f43609cf86e365dc1eb8de` as a modification baseline.
4. Confirm `DocumentDetector.kt` exists and preserve its APK-era/newer implementation.
5. Inspect `DocumentImageProcessor.kt`, `DocumentGeometry.kt`, `DocumentCropView.kt`, `ScannerScreen.kt`, `VaultViewModel.kt`, OCR, security, Room and backup sources.
6. Generate an authored-source SHA-256 manifest before editing.
7. Build/test the unmodified source. Record Gradle/JDK/AGP/Kotlin versions and all failures.
8. Reconcile source behavior with current target APK SHA-256 `87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`.
9. Freeze the reconciled source as the new canonical baseline.
10. Apply P1 changes incrementally, preserving a changed-file manifest and diff.
11. Run pure unit tests first, then Android build/tests.
12. Package a new canonical source ZIP only after build/static checks pass.
13. Update GitHub issue #1 and the current-build reports with exact evidence.
14. Produce an Antigravity physical-test prompt only after code/build evidence is ready.

No P2/P3/P4 changes should be mixed into the first P1 patch unless required to keep the project compiling.
