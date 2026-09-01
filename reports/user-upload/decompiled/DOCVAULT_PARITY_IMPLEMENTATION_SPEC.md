# DocVault CamScanner-Parity Implementation Specification

Goal: reproduce the **user-facing capabilities and quality characteristics** observed in the reference while keeping DocVault-owned architecture and independently implemented code. Do not transplant CamScanner source, assets, keys, models, branding, or private service endpoints.

## Architecture decision

Keep the current DocVault layering and add bounded domain engines behind interfaces. The scanner should become a pipeline rather than a single screen-level utility:

`CameraX acquisition → live quality gate → page detector → stable quad tracker → corner editor/loupe → perspective rectifier → cleanup/enhancement → OCR/classification → page editor → encrypted persistence/export`

## Capability backlog

| Capability | State | Proposed DocVault owner | Delivery phase |
|---|---|---|---|
| Capture & camera | STRENGTHEN | `domain.scan.CameraEngine` | P1 scanner parity |
| Auto boundary / page detection | STRENGTHEN | `domain.scan.PageDetectionEngine` | P1 scanner parity |
| Crop, corners & perspective | STRENGTHEN | `domain.scan.GeometryEngine` | P1 scanner parity |
| Deblur / quality recovery | STRENGTHEN | `domain.image.QualityRecoveryEngine` | P1 scanner parity |
| Enhancement & filters | STRENGTHEN | `domain.image.EnhancementEngine` | P1 scanner parity |
| Background / shadow cleanup | STRENGTHEN | `domain.image.DocumentCleanupEngine` | P1 scanner parity |
| Batch / multi-page scanning | STRENGTHEN (page drafts exist; live batch capture missing) | `domain.scan.ScanSessionManager` | P1 scanner parity |
| Large / infinity scan | ADD | `domain.scan.LargeScanEngine` | P3 advanced capture/tools |
| Book/page split | ADD | `domain.scan.BookSplitEngine` | P3 advanced capture/tools |
| Long image stitching | ADD | `domain.image.StitchEngine` | P3 advanced capture/tools |
| OCR core | STRENGTHEN | `domain.ocr.OcrEngine` | P1 scanner parity |
| OCR region / verification | STRENGTHEN | `domain.ocr.OcrRegionEngine` | P1 scanner parity |
| Document classification / page scene | STRENGTHEN | `domain.ai.DocumentClassifier` | P3 advanced capture/tools |
| Structured field extraction | STRENGTHEN | `domain.ocr.StructuredExtractionEngine` | P3 advanced capture/tools |
| QR / barcode | ADD | `domain.vision.CodeRecognitionEngine` | P3 advanced capture/tools |
| PDF creation / rendering | STRENGTHEN | `domain.pdf.PdfEngine` | P2 document editor/export |
| PDF merge / split / reorder | ADD | `domain.pdf.PdfPageEngine` | P2 document editor/export |
| PDF compression | ADD | `domain.pdf.PdfCompressionEngine` | P2 document editor/export |
| PDF annotation / doodle | ADD (redaction exists; general annotation does not) | `domain.annotation.AnnotationEngine` | P2 document editor/export |
| Signature | ADD | `domain.annotation.SignatureEngine` | P2 document editor/export |
| Watermark | ADD | `domain.annotation.WatermarkEngine` | P2 document editor/export |
| Redaction / smart erase | PRESENT / VERIFY | `domain.image.RedactionEngine` | P2 document editor/export |
| Image restore / cleanup | ADD beyond current basic cleanup | `domain.image.RestorationEngine` | P3 advanced capture/tools |
| Image to Word / office conversion | ADD | `domain.export.OfficeExportEngine` | P4 intelligent/cloud extensions |
| Formula recognition | ADD | `domain.ocr.FormulaEngine` | P4 intelligent/cloud extensions |
| Markdown conversion | ADD | `domain.export.MarkdownEngine` | P4 intelligent/cloud extensions |
| Translation | ADD | `domain.translate.TranslationEngine` | P4 intelligent/cloud extensions |
| Search / indexing | STRENGTHEN | `data.search.VaultSearchIndex` | P2 document editor/export |
| Tags / folders / organization | STRENGTHEN | `data.organization.CollectionRepository` | P2 document editor/export |
| Favorites / pinning | PRESENT / VERIFY | `data.repository.VaultRepository` | Preserve existing / optional |
| Cloud / sync | ADD (local encrypted backup exists; sync does not) | `domain.sync.SyncEngine` | P4 intelligent/cloud extensions |
| Backup / restore | PRESENT / VERIFY | `domain.backup.VaultBackupManager` | Preserve existing / optional |
| Encryption / vault locking | STRENGTHEN | `domain.security.VaultCrypto` | Preserve existing / optional |
| Sharing / export | STRENGTHEN | `domain.export.ShareEngine` | P2 document editor/export |
| Print / fax | ADD / fax optional | `domain.export.PrintEngine` | P3 advanced capture/tools |
| Document import / archives | STRENGTHEN | `domain.importer.DocumentImportEngine` | P3 advanced capture/tools |
| AI document features | STRENGTHEN | `domain.ai.VaultAiEngine` | P4 intelligent/cloud extensions |
| People / identity association | STRENGTHEN | `data.people.PersonRepository` | Preserve existing / optional |
| Expiry / reminders | PRESENT / VERIFY | `domain.notification.ExpiryEngine` | Preserve existing / optional |
| Audit / history | STRENGTHEN | `data.audit.AuditRepository` | Preserve existing / optional |
| Cache / cleanup / migration | STRENGTHEN | `data.maintenance.MaintenanceEngine` | Preserve existing / optional |
| Enterprise / collaboration | OPTIONAL ADD | `domain.collaboration.CollaborationEngine` | P4 intelligent/cloud extensions |
| Purchase / subscriptions / ads | Do not port by default (commercial/engagement surface) | `optional.commercial` | Preserve existing / optional |
| Messages / engagement | Do not port by default (commercial/engagement surface) | `optional.engagement` | Preserve existing / optional |

## P1 acceptance criteria — scanner quality gate

- Live document boundary should be visible before capture and remain stable rather than jumping frame-to-frame.
- Auto-capture should fire only after quad stability, sufficient sharpness, acceptable glare/exposure, and minimal motion are satisfied for a short dwell period.
- Four corners must remain independently draggable after capture; dragging must show a loupe/magnifier and edge snapping.
- Perspective correction must use the user-confirmed quadrilateral, never a hidden full-frame crop fallback.
- Background outside the quad must not remain in the rectified image.
- Original pixels must remain recoverable; filters are non-destructive.
- Filters should include Original, Auto/Magic, Gray, B&W, Contrast/Color, plus adaptive shadow/background cleanup.
- Batch capture must preserve per-page original, quad, rotation, filter, OCR, and edit history.
- OCR should run after rectification/enhancement and allow region OCR plus verification/correction.

## P1 concrete code changes against current DocVault

1. Split `DocumentDetector` into detection + temporal quad tracking + confidence/quality scoring. Preserve its current geometric candidate logic as the static detector.
2. Replace one-shot camera/photo-pick behavior in `ScannerScreen` with a CameraX preview/analyzer loop and `ScanSessionManager`.
3. Extend the crop UI with edge snapping, corner hit-target normalization, loupe overlay, rotation-safe coordinate mapping, and a visible auto-detected confidence state.
4. Move `rectifyPerspective()` into `GeometryEngine` and require an explicit `DocumentQuad` as input.
5. Break `DocumentImageProcessor.applyFilter()` into composable processors and add illumination normalization, local contrast, shadow suppression, deblur/sharpen, and adaptive B&W.
6. Add a per-page immutable edit recipe (`originalUri`, quad, rotation, filter parameters, OCR version) and render derivatives on demand.
7. Add OCR region selection/verification and keep raw OCR + edited OCR separately for auditability.
8. Persist scan-session state across configuration/process death before committing the final document.

## What should not be copied from CamScanner

- Proprietary native libraries (`libpagescanner`, `libscannercs`, `libmagicenhancer`, `libOCREngine`, etc.). Implement equivalents with permissive libraries / own code.
- Obfuscated Java/Kotlin implementation bodies.
- Branding, icons, layouts, strings, premium gating, analytics identifiers, keys, server URLs, or private cloud protocols.
- Purchase/ad/engagement modules unless DocVault independently needs a commercial product layer.

## Suggested permissive implementation stack

- CameraX for camera lifecycle, preview, analysis, focus/exposure and image capture.
- OpenCV for contours, perspective transforms, morphology, illumination normalization and image enhancement.
- ML Kit Text Recognition for the existing OCR path; keep `IOcrEngine` so a second offline OCR engine can be added later.
- Android PdfRenderer / PDFBox-compatible Android tooling as appropriate for local PDF manipulation, after license/size evaluation.
- Room/DataStore/Android Keystore already fit the current DocVault architecture.
