# DocVault Parity — Implementation Technology Decisions

Date: 2026-09-02

Purpose: lock the implementation stack before the updated source ZIP arrives, while keeping dependency changes separate from P0 source reconciliation.

## Decision 1 — Camera: CameraX remains the primary acquisition layer

**Target after P0:** AndroidX CameraX `1.6.2` (current stable as of 2026-08-26).

Use:
- `camera-core`
- `camera-camera2`
- `camera-lifecycle`
- `camera-view`

Architecture:
- Preview is never blocked by detection.
- `ImageAnalysis` uses `STRATEGY_KEEP_ONLY_LATEST`.
- Analyze a reduced-resolution frame stream.
- Capture accepted pages through full-resolution `ImageCapture`.
- Camera lifecycle remains isolated behind `CameraEngine`/`LiveDocumentCamera` rather than `ScannerScreen` owning all camera state.

Migration rule: build the updated ZIP unchanged first. Only after the P0 baseline passes should CameraX be upgraded from any older pinned version to 1.6.2, so source drift and dependency regressions remain distinguishable.

## Decision 2 — Do not use Google ML Kit Document Scanner as the primary DocVault scanner

Google's document-scanner API is useful and GA, but its viewfinder/preview UI and scanning logic are provided by dynamically downloaded Google Play services. It is therefore a poor primary fit for DocVault because we require:
- our own live boundary overlay;
- our own temporal quad tracker;
- our own quality gate / auto-capture policy;
- our own crop/loupe/edge-snapping UX;
- deterministic integration with encrypted scan-session state;
- offline/private control independent of a downloaded Google UI flow.

Potential use: optional fallback scanner on supported Play-services devices, never the canonical acquisition path.

## Decision 3 — Preserve the existing DocVault detector first; OpenCV is an enhancement layer, not a replacement

The current APK already contains a substantial manually authored `DocumentDetector`. P1 should initially connect that detector to CameraX and measure it under real video-frame conditions.

Only add OpenCV where measured gaps justify it, behind bounded interfaces:
- contour extraction / line finding;
- morphology;
- perspective transforms where useful;
- illumination normalization;
- CLAHE/local contrast;
- adaptive thresholding;
- optional blur/sharpness metrics.

Current OpenCV releases as of this decision are 5.0.0 (2026-08-19) and 4.14.0 (2026-07-19). For DocVault, start evaluation with the mature 4.14 line unless 5.0 provides a demonstrated Android benefit and passes APK-size/native-ABI/device tests. Do not introduce OpenCV merely to imitate the reference's native library inventory.

## Decision 4 — OCR: keep ML Kit behind `IOcrEngine`

Current bundled ML Kit text-recognition artifact: `com.google.mlkit:text-recognition:16.0.1`.

Rules:
- retain the `IOcrEngine` abstraction;
- run OCR on the confirmed rectified/enhanced page, not continuously on every preview frame;
- use lower-resolution OCR only for optional scene assistance;
- retain raw OCR, normalized OCR and user-corrected OCR separately;
- support region OCR;
- keep provider/language routing replaceable.

For any real-time vision work, CameraX analysis must use latest-frame backpressure and close each `ImageProxy` promptly.

## Decision 5 — QR/barcode: ML Kit Barcode Scanning for custom UI

Target bundled API: `com.google.mlkit:barcode-scanning:17.3.0`.

Reason: DocVault needs its own camera UI and scan-session architecture. Google Code Scanner is simpler and permission-light, but Google explicitly recommends the direct ML Kit Barcode Scanning API for complex/custom UI cases.

`CodeRecognitionEngine` must be separate from document-boundary detection even though it may share CameraX acquisition.

## Decision 6 — PDF: split generation/editing from viewing

AndroidX PDF reached `1.0.0-beta01` on 2026-08-26 and now exposes PDF viewer/editable-viewer, annotations and OCR-provider APIs. It is worth evaluating for modern Android PDF viewing/editing, but it should not become a hidden hard dependency for all DocVault PDF operations until min-SDK/device compatibility and beta stability are proven.

Architecture:
- `PdfEngine`: DocVault-owned generation/export abstraction.
- `PdfPageEngine`: page order/rotation/insert/delete/merge/split abstraction.
- `PdfCompressionEngine`: output optimization abstraction.
- optional AndroidX PDF adapter for compatible devices/viewing/editing.

Keep API 24-era support paths separate if the updated source still targets minSdk 24.

## Decision 7 — Scanner state is an immutable recipe, not a chain of destructive bitmaps

Each scan page should converge toward a durable model containing:
- original URI/file identity;
- detected quad;
- confirmed quad;
- rotation;
- enhancement recipe and parameters;
- raw OCR;
- normalized OCR;
- corrected OCR;
- thumbnail/cache identity;
- page order;
- timestamps/version identifiers.

Preview and export bitmaps are derivatives. This is the architectural prerequisite for re-crop, re-filter, re-OCR, undo, PDF page editing and long-term auditability.

## Decision 8 — Performance budgets must be designed in from P1

Target behavior on the physical TECNO KM7-class device:
- Preview remains responsive while analysis runs.
- At most one detector frame is being processed at a time.
- Static detector receives downscaled images appropriate for geometry, not full capture resolution.
- Capture is blocked only by the explicit quality/dwell gate, not by detector backlog.
- Full-resolution image processing is moved off the main thread.
- Bitmaps are not retained redundantly across page drafts.
- Batch sessions are tested for memory pressure and process recreation.

## Decision 9 — Clean-room implementation boundary

Reference decompilation may establish capabilities, state boundaries and behavioral requirements. It is not an implementation source.

Never transplant:
- CamScanner implementation bodies;
- native libraries;
- models;
- assets/branding/strings;
- server URLs/private APIs;
- keys/identifiers;
- commercial gating/analytics protocols.

Implement equivalent DocVault behavior using platform APIs, independently written code and dependencies whose licenses are explicitly acceptable.

## Execution order when updated ZIP arrives

1. Run `scripts/reconcile_docvault_source.py`.
2. Produce source hash manifest and APK/source reconciliation report.
3. Build/test the source unchanged.
4. Freeze baseline commit/archive.
5. Implement P1 camera shell with existing detector.
6. Add temporal tracking + quality/autocapture state engines with unit tests.
7. Integrate detected quad into existing crop/loupe flow and add edge snapping/constraints.
8. Harden edit recipe, batch session and OCR ordering.
9. Physical-device evidence gate.
10. Only then introduce optional OpenCV enhancements based on measured failures.
