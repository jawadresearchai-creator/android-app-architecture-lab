# Static Architecture Findings — CamScanner vs DocVault

## CamScanner reference evidence

The uploaded CamScanner 7.23.5 base APK exposes a large app-specific architecture under `com.intsig.*`, including dedicated subsystems for capture, document geometry, enhancement, OCR, PDF tooling, signatures, batch processing, long-image stitching, invoice/receipt recognition, search, cloud sync, conversion, translation and Markdown.

Representative classes recovered from the DEX symbol inventory include:

- Camera/capture: `com.intsig.android.camerax.CameraX`, `CameraXPreview`, `CameraXCameraFactory`.
- Edge/corner handling: `com.intsig.camscanner.EdgeClient`, corner-selection bindings and page-selection components.
- Crop/dewarp: `com.intsig.camscanner.scanner.cropdewrap.CropDewrapUtils`, `LargeScanCropFragment`, `CropWindowHandler`, `CropWindowMoveHandler`.
- Enhancement: `GPSuperFilterChecker`, `GPSuperFilterStrategyControl`, `CSDetectTaskPool`; native engines include `libmagicenhancer.so`, `libenhance4draft.so`, `libimageprocessor.so`, `libopencv.so` and `libpagescanner.so`.
- OCR: `ToOcrServiceImpl`, batch OCR items, native `libOCREngine.so`, `libTAGEngine.so`, `libTAGEngineV2.so`, classifier libraries.
- PDF: PDF routing/services plus native `libpdfengine.so`, `libpdfium.so`, `libpdfium_jni.so`.
- E-sign/watermark: `RouterToEsignService`, PDF watermark managers, long-image watermark components.
- Batch/multipage: `BatchModeActivity`, `BatchImageTask`, multi-page import/delete flows.
- Long image: `LongImageStitchClient`, `LongImageStitchItem`, `LongRegionImageStitchItem`; native `liblongImageStitch.so`.
- Invoice/receipt: `RouterToInvoiceReceiptRecognize`, `RouterToInvoiceRecognize`, invoice capture classes and invoice API components.
- Search: `com.intsig.camscanner.search.*`, `AiBuildUiStrategy`, search repositories/loaders.
- Cloud/sync: scan-done cloud sync dialogs, document sync managers and cloud repositories.
- Conversion: PDF-to-image and document merge routing/services.
- Translation: `RouterTranslateService`, `TranslateClient`, translation data models.
- Markdown: `MarkdownBinaryDetector`, Markdown import handlers and Markdown print flows.

## DocVault target evidence

The uploaded DocVault APK already has a meaningful clean architecture under `com.example.*`:

- UI: Jetpack Compose screens/components including `ScannerScreenKt`, `DocumentCropViewKt`, `UniversalSearchScreenKt`, `BackupRestoreScreenKt`.
- Geometry: `com.example.domain.image.DocumentDetector`, `CornerPosition`.
- OCR: `DefaultOcrEngine`, `IOcrEngine`, `DocumentClassifier`, `FieldExtractor`, `DocumentAnalysisResult`.
- Data: `VaultRepository`, local entities/converters and domain models.
- Export: `DocumentExporter.generatePdf`.
- Search: repository search plus `UniversalSearchScreen`.
- Backup/restore: repository and ViewModel backup/restore flows.
- Security foundations: AndroidX biometric and crypto/security components are present.
- Native layer is currently mostly ML Kit/AndroidX support; it lacks CamScanner-like dedicated page scanning, enhancement, PDF, long-image and custom OCR native engines.

## Clean-room migration targets

1. Strengthen `DocumentDetector` into a production geometry pipeline: live quadrilateral detection, confidence, stability, edge snapping, four-corner editor, loupe and perspective rectification.
2. Add a dedicated non-destructive image-processing domain layer with Magic, B&W, Gray, Contrast, shadow cleanup, denoise and original preservation.
3. Extend OCR from basic ML Kit recognition into batch OCR, searchable page text, document classification, receipt/invoice parsing and stronger structured field extraction.
4. Replace the thin PDF-export-only layer with a PDF subsystem supporting multipage generation, reorder, rotate, crop, merge/split, compression, annotation, signature and watermark.
5. Add true batch/continuous scanning and page-session management.
6. Add long-image stitching and region stitching.
7. Add QR/barcode workflows, print, translation and Markdown import/view/export where appropriate.
8. Keep DocVault's existing reminder/expiry, backup/restore and security strengths; CamScanner is not automatically superior in those areas.

The implementation goal is feature and quality parity using independently written code and permissively licensed components, not copying CamScanner proprietary source, assets, identifiers, credentials or backend behavior.
