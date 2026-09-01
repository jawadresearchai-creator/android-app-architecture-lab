# DocVault Master Parity Roadmap

## Objective

Reproduce the useful user-facing capability envelope evidenced in the CamScanner 7.23.5.2608050000 reference while retaining a DocVault-owned, privacy-first architecture. Implementation must be independent; proprietary CamScanner source bodies, native libraries, models, assets, keys, branding and private service protocols are not transplant targets.

This roadmap is derived from JADX 1.5.6 analysis of the uploaded CamScanner APKM plus the current DocVault APK.

## Delivery dependency chain

`P0 source reconciliation → P1 scanner acquisition/geometry/quality → P2 document/PDF editor → P3 advanced capture + structured vision → P4 intelligent/conversion/sync → P5 hardening/performance/release`

The phases are intentionally dependency ordered. For example, book splitting and large scans should not be implemented before the basic live scanner, page model and geometry pipeline are trustworthy.

---

## P0 — Reconcile the updated source ZIP with the executable APK

**Purpose:** establish a no-regression source baseline before any code is changed.

Required checks:

- preserve the APK-era `DocumentDetector.kt` implementation;
- preserve newer `DocumentImageProcessor` geometry/detector integration;
- preserve current `DocumentQuad` helpers;
- preserve current crop confidence/loupe interaction improvements;
- preserve OCR, security, Room schema, backup/restore, AI and metadata changes;
- establish a source-tree hash manifest before patching;
- build the unmodified ZIP and compare package/version/test behavior with the current APK.

P0 ends with a canonical source snapshot and a reproducible debug build.

---

## P1 — Production scanner parity

### A. Internal camera acquisition

CamScanner evidence surface: **1,128 recovered matching files**.

DocVault target modules:

- `domain.scan.CameraEngine`
- `ui.components.LiveDocumentCamera`

Required behavior:

- CameraX Preview + ImageAnalysis + ImageCapture;
- back camera selection and lifecycle binding;
- tap-to-focus / exposure where supported;
- torch control;
- analysis backpressure (`KEEP_ONLY_LATEST`);
- analyzer throttling independent from preview FPS;
- full-resolution capture while analysis runs at reduced resolution.

### B. Live document detection and auto-capture

CamScanner evidence surface: **90 page-boundary files** with scanner methods such as `detectFrameBorder`, `detectSingleFrameBorder`, `findCandidateLines` and `getScanBound`.

DocVault target modules:

- preserve `DocumentDetector` as the static detector;
- add `PageDetectionEngine` adapter;
- add `QuadTracker`;
- add `FrameQualityAnalyzer`;
- add `AutoCaptureController`.

Quality gate must consider:

- detector confidence;
- document area;
- temporal corner movement;
- blur/sharpness;
- motion;
- exposure;
- glare/highlight clipping;
- dwell time;
- cooldown after capture.

### C. Crop, geometry and dewarp

CamScanner evidence surface: **230 crop/perspective files**.

Preserve current DocVault strengths:

- four independently draggable corners;
- large touch targets;
- existing precision loupe;
- current projective rectification.

Add/harden:

- local edge snapping;
- convexity/non-crossing/minimum-area constraints;
- rotation-safe normalized coordinates;
- explicit detected-quad handoff from live camera to crop editor;
- no silent rectangular/full-frame fallback on the scanner acceptance path;
- immutable geometry edit recipe.

### D. Image quality and filters

CamScanner evidence surfaces:

- enhancement/filter: **629 files**;
- background/shadow cleanup: **411 files**;
- deblur/quality recovery: **108 files**.

DocVault target modules:

- `EnhancementEngine`
- `DocumentCleanupEngine`
- `QualityRecoveryEngine`

Processing should be composable and non-destructive:

- Original;
- Auto/Magic;
- Color;
- Gray;
- B&W;
- Contrast;
- white-background normalization;
- illumination/shadow correction;
- local contrast;
- mild sharpening/deblur only when quality metrics justify it.

Use separate preview-resolution and export-resolution processing paths.

### E. True scan session / batch mode

CamScanner evidence surface: **412 files**.

DocVault target: `ScanSessionManager` plus durable per-page edit recipe.

Each page should retain:

- original capture/import URI;
- confirmed quad;
- rotation;
- enhancement recipe;
- OCR raw text;
- OCR corrected text;
- thumbnail;
- page order;
- edit/version metadata.

Required operations: capture next, reorder, duplicate, delete, recrop, refilter, rotate and re-OCR without destroying originals.

### F. OCR integration

CamScanner OCR evidence: **347 core + 144 region/verification files**.

Preserve ML Kit behind `IOcrEngine` and add:

- OCR after rectification/enhancement;
- region OCR;
- raw/normalized/user-corrected OCR separation;
- language/provider routing;
- editable verification.

### P1 acceptance gate

Physical-device evidence must show stable live outline, reliable auto-capture, four-corner loupe + snapping, clean perspective result, reversible filters, continuous batch capture, post-rectification OCR, state restoration and no encryption/biometric/storage regressions.

---

## P2 — Document editor, PDF and export parity

### PDF engine

CamScanner evidence:

- PDF creation/rendering: **867 files**;
- merge/split/reorder: **105 files**;
- compression: **146 files**.

DocVault modules:

- `PdfEngine`
- `PdfPageEngine`
- `PdfCompressionEngine`

Required operations:

- create multipage PDF from scan-session pages;
- render existing PDFs to editable page objects;
- insert/delete/reorder/rotate pages;
- merge documents;
- split ranges/pages;
- configurable compression profiles;
- preserve originals and edit history.

### Annotation/signature/watermark/redaction

CamScanner evidence:

- annotation/doodle: **59 files**;
- signature: **470 files**;
- watermark: **241 files**;
- redaction/smart erase: **173 files**.

DocVault modules:

- `AnnotationEngine`
- `SignatureEngine`
- `WatermarkEngine`
- strengthen existing `RedactionEngine`.

Add freehand/text/highlight/shapes, reusable secure signatures, text/image watermarks and explicit destructive-vs-editable export semantics.

### Search and organization

CamScanner evidence:

- search/indexing: **227 files**;
- tags/folders/organization: **380 files**;
- favorites/pinning: **26 files**.

Strengthen DocVault indexing across OCR, structured fields, document metadata, people, collections and tags. Keep favorites/pinning integrated with the same index rather than separate search paths.

### Sharing/export/import

CamScanner evidence:

- sharing/export: **1,078 files**;
- document import/archive: **345 files**;
- print/fax: **99 files**.

DocVault modules:

- `ShareEngine`
- `DocumentImportEngine`
- `PrintEngine`

Support image/PDF sharing through secure temporary files, metadata-aware export, import of images/PDFs, page extraction and Android print. Fax is optional unless product requirements independently justify it.

---

## P3 — Advanced capture and structured vision

### Large / infinity scanning

CamScanner evidence: **40 files**.

Implement `LargeScanEngine` using sequential overlapping captures + alignment/stitch state. It should share camera acquisition but maintain its own capture/session logic.

### Book/page split and curved-page handling

CamScanner evidence: **55 files**, including methods associated with curve-border/book-turn detection.

Implement `BookSplitEngine`:

- detect two-page spreads;
- infer spine/divider;
- produce left/right pages;
- optional curved-page mesh correction after basic geometry is stable.

### Long-image stitching

CamScanner evidence: **82 files**.

Implement `StitchEngine` for vertically/horizontally overlapping document images, alignment confidence, seam blending and crop normalization.

### QR/barcode

CamScanner evidence: **77 files**.

Implement `CodeRecognitionEngine` with camera/gallery decode, supported-code result types, safe URL handling and scan history if desired.

### Identity, certificate, invoice and receipt modes

CamScanner evidence includes certificate/card/invoice/capture packages and **407 structured-field-extraction matching files**.

Implement separate bounded modes rather than one giant conditional scanner:

- `IdentityDocumentMode`
- `InvoiceMode`
- receipt mode
- certificate/card framing
- shared structured extraction interfaces.

### Page-scene classification

CamScanner evidence: **165 files**.

Keep visual page-scene classification separate from semantic document classification. A `PageSceneClassifier` can classify photo/document/receipt/ID/book/whiteboard/etc. and recommend enhancement recipes without forcing them.

### Restoration

CamScanner evidence: **9 directly matched restoration/cleanup files** plus native enhancement engines.

Implement only independently feasible restoration: de-noise, illumination repair, contrast recovery, mild sharpen/deblur and degraded-photo cleanup. Do not port proprietary ML models.

---

## P4 — Intelligent, conversion and sync extensions

### Office/document conversion

CamScanner evidence:

- image-to-Word/office conversion: **820 files**;
- formula recognition: **71 files**;
- Markdown conversion: **37 files**;
- translation: **75 files**.

DocVault modules:

- `OfficeExportEngine`
- `FormulaEngine`
- `MarkdownEngine`
- `TranslationEngine`

These should consume DocVault OCR/layout structures rather than introduce a second document model.

### AI document features

CamScanner broad AI-related evidence: **1,989 matched files**.

Strengthen `VaultAiEngine` around DocVault-owned data and explicit user actions:

- grounded Q&A over selected/local documents;
- summaries;
- metadata extraction suggestions;
- expiry/action suggestions;
- compare documents;
- structured search assistance.

Core vault data must not be sent to remote providers by default. Network AI must be opt-in and provider-isolated.

### Sync and backup

CamScanner sync evidence: **416 files**; backup/restore evidence: **28 files**.

DocVault already has encrypted backup/restore. Build `SyncEngine` separately with:

- opt-in providers;
- encrypted remote payloads;
- conflict/version handling;
- offline-first local authority;
- audit trail.

### People / identity association and expiry workflows

CamScanner evidence:

- people/identity association: **212 files**;
- expiry/reminders: **49 files**.

DocVault already has native strengths here. Preserve them and integrate scanned structured fields into person/document relationships and reminder generation.

### Audit/history and maintenance

CamScanner matching evidence:

- audit/history: **1,238 files**;
- cache/cleanup/migration: **127 files**.

DocVault should strengthen version-aware audit history, edit provenance, failed-operation reporting, cache limits, cleanup, schema migrations and recovery tests.

### Enterprise/collaboration

CamScanner evidence: **1,197 matched files**.

Treat collaboration as an optional later product layer. If implemented, keep sharing permissions, collaboration identities and remote data outside the scanner/security core.

---

## Commercial and engagement surfaces

Reference evidence also includes:

- purchase/subscriptions/ads: **525 matched files**;
- messages/engagement: **758 matched files**.

These are catalogued so the reference feature map is complete, but they are not prerequisites for document-scanner parity. DocVault should only add subscription, licensing, analytics, messaging or promotional layers if independently required by the product. Do not reproduce reference ad networks, purchase gating, identifiers or engagement protocols.

---

## P5 — Hardening, performance and release gates

Every prior phase must finish with:

- unit tests for pure geometry/state engines;
- instrumentation/device tests for camera and storage;
- screenshot/video evidence for UX-critical flows;
- low-memory testing with multipage scans;
- process-death/configuration restoration;
- encryption/biometric regression suite;
- migration tests from existing DocVault databases/backups;
- export fidelity checks;
- privacy/network audit;
- APK size and startup/performance budget;
- hostile error-path tests: camera denied, storage pressure, corrupt import, OCR failure, invalid quad, interrupted backup/sync.

## Architecture rule

Do not make `ScannerScreen`, `VaultViewModel` or `VaultRepository` the implementation home for every feature. New capability should enter through bounded interfaces/engines with state owned at the appropriate layer. The existing DocVault architecture is cleaner than the reference and should stay that way while its capability envelope expands.
