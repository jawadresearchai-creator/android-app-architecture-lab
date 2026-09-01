# DocVault Source ZIP vs Current APK — Reconciliation Audit

## Decision

Do **not** apply the P1 scanner patch to the Library `document-vault.zip` baseline. That ZIP is older than the executable APK currently under audit.

The current APK SHA-256 is:

`87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`

The old Library source ZIP SHA-256 is:

`ab5610a7a1fbe177c17709e2bf79c299a52bb81fb2f43609cf86e365dc1eb8de`

## Concrete drift evidence

### `DocumentDetector.kt`

The current APK contains a manually authored `com.example.domain.image.DocumentDetector` compiled from `DocumentDetector.kt`. The old source ZIP does not contain that Kotlin file.

Current APK responsibilities recovered by JADX include:

- `detect()`
- `simplifyPolygon()`
- `pointToLineDistance()`
- `computeConvexHull()`
- `evaluateCandidate()`
- `findOptimalQuad()`
- `findDiagonalExtremaQuad()`
- `orderCorners()`
- confidence, candidate-area, minimum/mean edge-support and border-penalty metrics

This file is part of the scanner foundation and must be preserved from the forthcoming updated source ZIP.

### `DocumentImageProcessor.kt`

The old ZIP contains a simpler `detectDocumentQuad()` implementation based on directional edge scans and insets. In the current APK, `detectDocumentQuad(bitmap)` delegates to `DocumentDetector.detect(bitmap)` and returns its detected quad.

The current APK also has a materially newer perspective implementation. It calculates a projective transform and samples the source image into the destination rectangle with interpolation. The old ZIP uses `Matrix.setPolyToPoly()` and falls back to a bounding-box crop when that operation fails.

Therefore replacing the APK-era source with the old ZIP would regress document detection/perspective work.

### `DocumentGeometry.kt`

The current APK `DocumentQuad` contains additional geometry helpers not present in the old ZIP, including:

- `area()`
- `withOffset(dx, dy)`
- `containsPoint()`

These are evidence that geometry code continued evolving after the old ZIP was created.

### `DocumentCropView.kt`

The old ZIP keeps crop interaction as local composable state. The current APK contains a dedicated `CropInteractionState` class with normalized↔screen coordinate conversion and corner drag lifecycle methods.

The current APK crop UI also integrates `DocumentDetector.DetectionResult` confidence state and contains the existing precision loupe/magnifier implementation.

The updated source ZIP must preserve these later changes.

### `ScannerScreen.kt`

The current APK still uses a one-shot managed camera launcher + temporary `Uri`, so the central P1 live-scanner gap remains. This is one area where the forthcoming patch should intentionally change behavior.

### Generated files

Room-generated `_Impl` classes recovered from the APK but absent from the source ZIP are expected build outputs and are **not** source drift. Compose `LazyDsl.kt` references are generated/inlined compiler artifacts and are also not treated as missing authored source.

## Updated ZIP acceptance gate

Before any source modification, the new ZIP supplied by the user must pass the following reconciliation checks:

1. It must contain `app/src/main/java/com/example/domain/image/DocumentDetector.kt`.
2. Its `DocumentImageProcessor.detectDocumentQuad()` should use the newer detector or an equal/newer implementation.
3. Its geometry layer should contain the newer `DocumentQuad` helpers or demonstrably supersede them.
4. Its crop implementation should contain the later crop interaction/loupe/confidence work rather than the older inline-only version.
5. Its `ScannerScreen` should be classified as either the same launcher baseline or a newer internal-camera implementation.
6. Existing encryption, OCR, Room schema, backup/restore and metadata code must be diffed before patching so no later features are overwritten.

Only after these checks should the P1 CameraX/quad-tracking/auto-capture patch be applied.
