# DocVault Current APK — P1 Scanner Audit

## Build identity

The newly supplied `Docvault(1).apk` is **byte-for-byte identical** to the previously supplied `Docvault.apk`.

- SHA-256: `87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`
- Size: approximately 65 MiB
- Android package contains multiple DEX files and bundled ML Kit OCR native/models.

Therefore the `(1)` filename does **not** represent a new executable build. All existing DocVault decompilation evidence remains authoritative for this APK.

## P1 evidence from JADX 1.5.6 decompilation

### 1. Internal live CameraX scanner — ABSENT in first-party code

No first-party `com.example` source references were recovered for:

- `LifecycleCameraController`
- `PreviewView`
- `ImageAnalysis`
- `ImageCapture`
- `ProcessCameraProvider`
- `CameraController`

`ScannerScreenKt` instead contains a managed camera launcher, temporary camera `Uri`, permission launcher and callback flow. The recovered control methods include `ScannerScreen$launchCamera`, `cameraLauncher`, `tempCameraUri` and a callback that loads the resulting captured image. This is consistent with an external/one-shot capture flow rather than a persistent CameraX preview/analyzer pipeline.

**P1 consequence:** the principal scanner defect remains: there is no live frame analysis loop, no continuously updated document polygon and no automatic capture gate.

### 2. Static document detection — PRESENT

`com.example.domain.image.DocumentDetector` is already substantial. Recovered responsibilities include:

- `detect()`
- polygon simplification
- convex-hull construction
- candidate evaluation
- optimal-quad selection
- diagonal-extrema fallback
- corner ordering
- confidence / candidate area / edge-support scoring

**P1 action:** preserve this detector and call it from a throttled CameraX `ImageAnalysis` pipeline. Do not replace it wholesale.

### 3. Four-corner crop editor — PRESENT

`DocumentCropView` + `CropInteractionState` already support normalized screen/image coordinate mapping and independent active-corner dragging.

### 4. Loupe / magnifier — PRESENT

The current APK contains an actual loupe implementation in `DocumentCropViewKt`, including active-corner positioning, translated/scaled bitmap rendering and crosshair overlays.

**P1 action:** preserve and tune the existing loupe rather than rebuilding it.

### 5. Edge snapping — NOT EVIDENCED

The crop editor displays edge-confidence messaging, but no first-party crop-state implementation of local gradient/line edge snapping was recovered.

**P1 action:** add snapping as a bounded helper that proposes the strongest nearby edge/corner while maintaining convexity and minimum-area constraints.

### 6. Perspective correction — PRESENT, must be hardened

`DocumentImageProcessor` contains both `cropBitmap()` and `rectifyPerspective(source, quad)`.

**P1 action:** make the confirmed `DocumentQuad` mandatory for scanner acceptance; invalid geometry should remain in edit mode instead of silently using a rectangular/full-frame substitute.

### 7. Non-destructive page drafts and filters — PARTIALLY PRESENT

`ScannedPageDraft` stores:

- base bitmap
- selected `PageFilterType`
- rotation angle
- cached filtered bitmap

`VaultViewModel` supports:

- `addScannedPage()`
- `updateScannedPage()`
- `removeScannedPage()`
- `rotateScannedPage()`
- `applyFilterToScannedPage()`

This is a useful base for batch scanning, but it does not yet represent a complete persistent edit recipe including source URI, detected/confirmed quad, OCR revisions and process-death recovery.

### 8. Live batch capture — INCOMPLETE

Multiple in-memory page drafts exist, but because acquisition is still a one-shot launcher flow, the app lacks a true continuous scanner session comparable to a production document scanner.

### 9. OCR — PRESENT

ML Kit OCR is bundled and `DefaultOcrEngine` / `IOcrEngine` are present. Structured extraction and an OCR verification flow also exist.

**P1 action:** run OCR from the finalized rectified/enhanced page, preserve raw and corrected OCR separately, and add region OCR later.

## P1 implementation order for the updated source ZIP

1. Add an internal `LiveDocumentCamera` / `CameraEngine` based on CameraX Preview + ImageAnalysis + ImageCapture.
2. Feed throttled analysis frames through the existing `DocumentDetector`.
3. Add `QuadTracker` for temporal smoothing and confidence hysteresis.
4. Add `FrameQualityAnalyzer` for blur, glare, exposure, motion and document-area gates.
5. Add `AutoCaptureController` with stable-quad dwell time and capture cooldown.
6. Carry the detected quadrilateral into the existing crop editor instead of redetecting from scratch.
7. Preserve the existing four-corner loupe UI and add edge snapping + geometry validity constraints.
8. Harden perspective rectification and remove any silent rectangular fallback from the scanner acceptance path.
9. Extend `ScannedPageDraft` into a durable per-page edit recipe and recover scan sessions across configuration/process recreation.
10. Move OCR to the post-rectification/enhancement stage and retain raw/edited OCR revisions.

## Acceptance gate

P1 is not complete until physical-device evidence demonstrates stable live outline, auto-capture, four-corner editing + loupe + snapping, clean perspective rectification without background leakage, reversible filters, true batch scanning, post-rectification OCR and no security/storage regressions.
