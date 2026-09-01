# CamScanner Pre-JADX Architecture Inventory

This inventory is derived directly from the user-supplied CamScanner APKM before full JADX source recovery. It records package/class/native-engine structure without reproducing proprietary source code.

## Application scale

- 15 DEX files in the base APK
- 92,274 total class definitions
- Large first-party feature domains under `com.intsig.camscanner`
- 250 first-party Activity classes detected
- 218 first-party Fragment classes detected
- 165 first-party ViewModel classes detected
- 8 first-party Repository classes detected
- 35 first-party Service classes detected
- 16 first-party Receiver classes detected

## Largest first-party feature domains

| Package | Approx. classes | Architectural signal |
|---|---:|---|
| `capture` | 2,277 | Camera/capture modes and scan orchestration |
| `mainmenu` | 2,158 | Home/document navigation and document management |
| `office_doc` | 1,897 | Office-document preview/conversion workflows |
| `pagelist` | 1,395 | Multi-page document management |
| `multiimageedit` | 1,191 | Batch/multi-image editing |
| `share` | 904 | Export/share/compression workflows |
| `imageconsole` | 891 | Image editing console |
| `newsign` | 891 | E-signature workflows |
| `csai` | 612 | AI document functionality |
| `mode_ocr` | 474 | OCR UI/state/data workflows |
| `search` | 451 | Document/function search |
| `jsondoc` | 404 | Structured document/office export |
| `gallery` | 367 | Gallery/import workflows |
| `pdf` | 355 | PDF workflows |
| `pic2word` | 332 | Image-to-Word/document conversion |
| `autocomposite` | 148 | Automatic composition/certificate workflows |
| `printer` | 135 | Printing integration |
| `layout_restoration` | 122 | Document layout restoration |
| `smarterase` | 114 | Smart erase/image cleanup |
| `formula` | 113 | Formula recognition/handling |
| `docimport` | 99 | Document import |
| `imagescanner` | 96 | Scanner processing services |
| `aidetect` | 93 | AI detection workflow |
| `imageaiprocess` | 88 | AI image processing |
| `scanner` | 86 | Scanner support/orchestration |
| `booksplitter` | 72 | Book/page split workflows |
| `pdfengine` | 71 | PDF rendering/processing |
| `bankcardjournal` | 68 | Card/document specialized workflow |
| `filter` | 67 | Image filters |
| `ai` | 65 | AI document services |
| `lock` | 62 | App/document locking |
| `translate_new` | 61 | Translation |
| `imagestitchv3` | 60 | Long-image stitching |
| `signature` | 59 | Signature tooling |
| `merge` | 59 | Document/page merging |
| `borderenhance` | 51 | Border enhancement |
| `backup` | 44 | Backup |
| `securitymark` | 43 | Security/watermark features |

## Capture modes and specialized workflows observed

Class/package names expose dedicated workflows for normal capture, batch capture, certificates/certificate photos, invoice and receipt capture, QR code capture, large scans, topic/problem scans, mark-camera/watermark capture, count/region capture, book scanning/splitting, gallery import and document import.

Representative classes include `CaptureActivity`, `CaptureFlowController`, `CaptureDocController`, `LargeScanCropViewModel`, `InvoiceViewModel`, `ReceiptViewModel`, `CertificatePhotoPreviewActivity`, `ImageScannerActivity`, `BatchModeActivity`, `EngineService`, `ImageProcessService`, and `LocalOcrService`.

## Image-processing and native engine layer

The ABI split contains dedicated native components that strongly indicate a multi-stage native processing pipeline. Important libraries include:

- `libpagescanner.so` — page/document scanning engine
- `libscannercs.so` — scanner engine
- `libopencv.so` — computer vision primitives
- `libimageprocessor.so` — image processing
- `libmagicenhancer.so` — enhancement pipeline
- `libenhance4draft.so` — document enhancement
- `libOCREngine.so` — OCR engine
- `libQREngine.so` — QR engine
- `libTAGEngine.so`, `libTAGEngineV2.so` — recognition/tagging components
- `liblongImageStitch.so` — long-image stitching
- `libpdfengine.so`, `libpdfium.so`, `libpdfium_jni.so` — PDF rendering/processing
- `libMNN.so`, `libncnn.so`, `libCVNN.so` — neural-network inference runtimes
- `liboctopus_classifier.so` — classification engine
- `libdigital_ink.so` — digital ink/handwriting-related processing
- `libwcdb.so` — native database layer
- `libencryptfile.so`, `libEncryptorP.so` — encryption-related native functions
- `libyuv-decoder.so` — camera/image format processing

These engines should not be copied. For DocVault they translate into independently implemented modules with CameraX/OpenCV/ML Kit or other permissively licensed equivalents.

## Architectural style signals

CamScanner is not a single clean architecture. It appears to be a mature modular application containing a mixture of Activities/Fragments, ViewModels, repositories, presenters, controllers, services, native engines, Flutter-hosted modules, and feature-specific managers. The key lesson for DocVault is therefore not to reproduce CamScanner's historical structure, but to separate the capabilities into clean independently testable modules.

## High-value capability clusters for DocVault

1. Capture and camera orchestration
2. Robust document boundary detection and auto-capture
3. Manual four-corner correction with preview/loupe/edge snapping
4. Perspective correction and page rectification
5. Document/background cleanup and shadow handling
6. Multiple enhancement/filter pipelines
7. Batch and multi-page scan workflows
8. Specialized capture modes (ID/certificate/receipt/invoice/book/QR/large scan)
9. OCR and structured-field extraction
10. Image-to-document/office conversion workflows
11. PDF render, merge, split, compress, reorder and protect
12. Annotation, signature, watermark and smart erase
13. Long-image stitching
14. Search, tags, OCR search and AI-assisted retrieval
15. Backup/sync/security/export/printing workflows
