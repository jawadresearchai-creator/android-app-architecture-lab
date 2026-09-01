# Clean-Room CamScanner-Class Capability Roadmap for DocVault

## Goal

Bring the useful document-scanning, processing, OCR, PDF, organization and editing capabilities observed in the reference application into DocVault while preserving DocVault's cleaner Compose/MVVM/Room/security architecture and independently implementing the functionality.

## Architectural rule

Do not transplant the reference application's Activity/Fragment hierarchy or proprietary native engines. Treat each observed capability as a product requirement and implement it behind DocVault-owned interfaces.

Recommended module boundaries:

```text
ui/scanner
  ScannerScreen
  ScannerViewModel / ScanSession state

capture/
  CameraController
  FrameAnalyzer
  AutoCaptureController
  MotionFocusGate

detection/
  DocumentDetector
  QuadTracker
  QuadScorer
  EdgeSnapper

crop/
  CropEditor
  CornerHandleModel
  MagnifierController
  PerspectiveTransformer

enhancement/
  EnhancementEngine
  IlluminationNormalizer
  ShadowSuppressor
  AdaptiveContrast
  Binarizer
  FilterPipeline

ocr/
  OcrEngine
  OcrQueue
  DocumentClassifier
  FieldExtractor
  SearchIndexer

pdf/
  PdfRenderer
  PdfComposer
  PdfCompressor
  PdfOperations
  PdfSecurity

editing/
  AnnotationEngine
  SignatureEngine
  WatermarkEngine
  RedactionEngine
  SmartEraseEngine

specialized/
  IdCardScanner
  ReceiptInvoiceScanner
  BookScanner
  LargePageScanner
  QrBarcodeScanner
  LongImageStitcher

storage/
  VaultRepository
  Room DAOs
  EncryptedFileStore
  BackupManager

export/
  DocumentExporter
  OfficeExporter
  PrintAdapter
```

## Phase 1 — scanner foundation (highest priority)

### 1. Camera pipeline

Use CameraX with a high-resolution `ImageCapture` use case and a separate lower-resolution `ImageAnalysis` stream. Detection runs on analysis frames; final processing always uses the full captured image.

Requirements:

- orientation-safe coordinate mapping between analyzer frame, preview and final image
- backpressure strategy that never queues stale frames
- focus/exposure metering at document center
- torch control
- camera lens selection where appropriate
- lifecycle-safe camera rebinding
- explicit memory ceilings for large bitmaps

### 2. Stable live document detection

Keep the existing `DocumentDetector` interface but replace/augment internals with a staged detector:

1. downscale analysis frame
2. grayscale + local contrast normalization
3. blur/noise suppression
4. adaptive/Canny-style edge extraction
5. contour/line candidates
6. convex quadrilateral generation
7. geometric scoring (area, angles, convexity, edge support)
8. border/background penalties
9. temporal tracking across frames
10. confidence output

Add `QuadTracker` using exponential smoothing/Kalman-style state so corners do not jump frame to frame.

### 3. Auto-capture

Auto-capture should trigger only when all conditions remain true for a stable window:

- detector confidence above threshold
- all four corners inside safe margins
- quad movement below threshold
- device/frame motion below threshold
- autofocus/exposure settled when available
- document area above minimum
- no recent capture cooldown

Provide visible stability feedback and a cancellable countdown.

### 4. Manual crop editor

Required interaction quality:

- four individually draggable corner handles
- handle stays directly under finger
- enlarged magnifier/loupe showing source-resolution pixels
- edge snapping to nearby strong line/edge
- prevention of self-crossing quadrilaterals
- optional reset to detected quad/full image
- rotate before/after crop with coordinate remapping
- undo/redo

### 5. Perspective transform

Implement robust projective transform with:

- ordered TL/TR/BR/BL corners
- destination dimensions estimated from opposing edge lengths
- high-quality interpolation
- no clipping of valid page pixels
- optional 1–2% inward safety correction only when justified
- deterministic unit tests using synthetic quadrilaterals

## Phase 2 — CamScanner-class image quality

Build a non-destructive enhancement graph. Store the original capture and edit parameters rather than repeatedly rewriting the image.

Presets should be parameter sets over the same engine:

- Original
- Auto/Magic
- Document
- B&W
- Gray
- Color Enhance
- Lighten
- Photo

`Auto/Magic` should combine illumination normalization, paper/background estimation, local contrast, color cast correction, shadow suppression, mild sharpening and text-preserving tone mapping. It must not simply raise global contrast.

Add border cleanup and optional smart erase as separate reversible operations.

## Phase 3 — OCR and metadata intelligence

Retain ML Kit as the baseline OCR provider but redesign orchestration:

- queue OCR after final high-resolution rectification
- page-level progress and cancellation
- cache OCR results keyed by image hash + OCR config
- language/script hints where available
- searchable normalized text index
- confidence-aware field extraction
- document-type schemas
- explicit user verification before authoritative metadata is stored

Add specialized extraction profiles for identity cards, passports/certificates, receipts and invoices.

## Phase 4 — document/PDF workbench

Implement:

- multi-page reorder/delete/duplicate/rotate
- bulk filters
- merge documents
- split PDFs
- import PDF pages
- render PDF pages for editing
- configurable page sizes/margins
- compression quality profiles
- searchable PDF output using OCR text layer where technically reliable
- PDF password protection for exported copies
- metadata editing

## Phase 5 — markup and signatures

Add reversible document layers:

- freehand pen/highlighter
- text boxes
- rectangles/arrows
- signature capture/import
- signature resize/rotate/place
- watermark text/image
- permanent redaction export with verification that underlying pixels/text are removed

## Phase 6 — specialized scanner modes

Implement as thin mode configurations over the same capture/detection/processing core, not separate scanner engines:

- ID card/front-back
- passport/certificate
- receipt/invoice
- QR/barcode
- book/two-page spread
- long/large page
- long-image stitch

Each mode supplies framing constraints, classifier schema, post-processing and output behavior.

## Phase 7 — search, organization and AI

DocVault already has the correct foundation. Extend it with:

- full-text OCR index
- tags
- saved/smart searches
- document-type/person/expiry filters
- duplicate detection using image/document fingerprints
- grounded AI retrieval only from documents selected by the user
- AI answers carrying page/document references rather than unsupported free-form claims

## Phase 8 — export, backup and interoperability

Add/strengthen:

- secure temporary export lifecycle
- PDF/JPEG/PNG/TXT export
- optional DOCX/CSV/XLSX export from OCR/structured tables
- Android Print Framework
- encrypted versioned backups with integrity manifest
- backup migration testing
- optional cloud sync as a separate opt-in subsystem

## Quality gates

Each scanner release must pass a fixed real-device corpus, including:

- white paper on dark table
- white paper on light table
- colored/low-contrast paper
- shadows across page
- glossy ID card
- skewed document
- partial occlusion/finger
- cluttered background
- document near frame edge
- portrait and landscape
- low and strong illumination
- text-heavy and photo-heavy pages
- multi-page batch run

Measure boundary corner error, crop success rate, false auto-capture rate, rectification clipping, processing latency, OCR character/word quality, memory peak, crash rate and output file size.

## Recommended implementation order

1. Coordinate mapping and live detector stabilization
2. Crop editor/loupe/edge snapping
3. Perspective transform correctness
4. Adaptive enhancement engine
5. Auto-capture
6. Batch/multi-page reliability
7. OCR queue/search indexing
8. specialized document profiles
9. PDF operations/compression/security
10. annotations/signatures/watermarks
11. book/large/stitch modes
12. office exports/printing/cloud extras

Do not begin with fax, social integrations, advertisements or subscription infrastructure; these do not improve DocVault's core document-vault value.
