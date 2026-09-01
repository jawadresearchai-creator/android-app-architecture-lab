# Scanner Pipeline Method Map — CamScanner evidence to independent DocVault equivalents

This is a clean-room behavioral map. CamScanner method names are used as evidence of capabilities and orchestration boundaries; DocVault implementations must be independently written.

## 1. Frame acquisition and scan state

**CamScanner evidence**
- `CaptureActivity`
- `ScannerUtils.init()` / `initThreadContext()` / `destroyThreadContext()`
- `ScannerPreferenceHelper`
- `ScannerEntities.TrimParam`

**DocVault current**
- `ScannerScreen`
- `VaultViewModel.startNewScanSession()`
- `VaultViewModel.addScannedPage()` / `updateScannedPage()` / `removeScannedPage()`

**Required DocVault parity**
- Add `CameraEngine` using CameraX `Preview`, `ImageAnalysis`, `ImageCapture`.
- Add `ScanSessionManager` with explicit page state and lifecycle-safe persistence.
- Add frame backpressure and analyzer throttling so detection cannot block preview.

## 2. Live page boundary detection

**CamScanner evidence**
- `ScannerUtils.detectFrameBorder()`
- `ScannerUtils.detectSingleFrameBorder()`
- `ScannerUtils.findCandidateLines()`
- `ScannerUtils.getScanBound()` / `getScanBoundF()`
- `ScannerUtils.findDefaultRect()`
- `CandidateLinesManager`
- `MultiDirectionDetectCollectManager`

**DocVault current**
- `DocumentDetector.detect()`
- `DocumentDetector.evaluateCandidate()`
- `DocumentDetector.findOptimalQuad()`
- `DocumentDetector.findDiagonalExtremaQuad()`
- `DocumentDetector.computeConvexHull()`
- `DocumentDetector.orderCorners()`

**Required DocVault parity**
- Preserve `DocumentDetector` as a static frame detector.
- Add `QuadTracker` to smooth corner coordinates over consecutive frames.
- Add `FrameQualityAnalyzer` for blur, glare, exposure, motion and document area.
- Add `AutoCaptureController` that requires stable quad + quality threshold + dwell time.
- Add confidence hysteresis so the blue boundary does not jump/disappear frame-to-frame.

## 3. Corner editing, crop bounds and edge snapping

**CamScanner evidence**
- `ScannerUtils.adjustRect()`
- `ScannerUtils.checkCropBounds()`
- `ScannerUtils.isLegalBound()`
- `ScannerUtils.isUnavailableBorder()`
- `ScannerUtils.overBoundary()`
- `ScannerUtils.rectToBorder()`
- `ScannerUtils.getFullBorder()` / `getFullBorderF()`

**DocVault current**
- `DocumentCropView`
- `DocumentQuad`
- `CornerPosition`
- `CropInteractionState`

**Required DocVault parity**
- Independent dragging of all four corners.
- Larger invisible touch targets than the visible handles.
- Screen↔bitmap coordinate mapping that remains correct after rotation/orientation changes.
- Edge snapping based on local gradient/line evidence.
- Loupe/magnifier centered near the active corner, offset so the finger does not hide the edge.
- Hard convexity, minimum-area, non-crossing and image-bound constraints.

## 4. Perspective correction and dewarping

**CamScanner evidence**
- `ScannerUtils.trimImageF()` / `trimImageS()` and multiprocess variants
- `ScannerUtils.surfaceCorrectWithoutBorder()` and bitmap/multiprocess variants
- `ScannerUtils.dewarpImagePlane()` / `dewarpImagePlaneMultiProcess()`
- `ScannerUtils.detectCurveBorder()`
- `ScannerUtils.detectBookTurnPage()`

**DocVault current**
- `DocumentImageProcessor.cropBitmap()`
- `DocumentImageProcessor.rectifyPerspective()`

**Required DocVault parity**
- Move homography/perspective work to `GeometryEngine`.
- Make the confirmed `DocumentQuad` mandatory input; never silently revert to full-frame crop.
- Preserve original image and save geometry as an edit recipe.
- Add curved-page/dewarp path later for book scans.
- Add book-spread detection and page split as a separate `BookSplitEngine`.

## 5. Blur recovery and quality enhancement

**CamScanner evidence**
- `ScannerUtils.deBlurImageBitmap()` / `deBlurImageFile()` / `deBlurImagePtr()` / `deBlurImageStruct()`
- `ScannerUtils.prepareAndExecuteDeBlur()`
- `ScannerUtils.enhanceImage()` / `enhanceImageFile()` / `enhanceImageS()`
- `ScannerUtils.enhanceImageBySuperFilter()`
- `ScannerUtils.getEnhanceMode()` / `getCurrentEnhanceMode()`
- `ScannerUtils.isSuperFilterMode()`
- native engines observed: `libmagicenhancer.so`, `libenhance4draft.so`, `libimageprocessor.so`, `libopencv.so`

**DocVault current**
- `DocumentImageProcessor.applyFilter()`
- `enhanceContrast()`
- `toGrayscale()`
- `toHighContrastBlackAndWhite()`
- `cleanDocumentBackground()`

**Required DocVault parity**
- Refactor into `EnhancementEngine` processors operating on immutable recipes.
- Add illumination normalization, local contrast/CLAHE, shadow suppression, white-background normalization, color preservation and adaptive B&W.
- Add blur scoring and mild deconvolution/unsharp recovery only when needed.
- Add preview-quality processing plus full-resolution export-quality processing.
- Filters remain non-destructive and reversible.

## 6. Scene classification and smart filter recommendation

**CamScanner evidence**
- `ScannerUtils.getPageScene()` / `getPageSceneWithOcr()`
- `ScannerUtils.getTaxonomyPageScene()` / `getTaxonomyPageSceneWithOcr()`
- `ScannerUtils.getTAGNewPageScene()`
- `ScannerUtils.radarClassifyImageFile()` / `radarClassifyImageStruct()`
- `ScannerUtils.loadTAGModel()` / `loadTAGV2Model()`
- `listToJsonStringWithFeatSmartRecommendV3()`

**DocVault current**
- `DocumentClassifier.classifyDocument()`
- `DocumentClassifier.inferDocumentDetails()`

**Required DocVault parity**
- Keep semantic document classification separate from visual page-scene classification.
- Add `PageSceneClassifier` returning photo/document/receipt/ID/book/whiteboard/etc. visual type.
- Feed page-scene output into filter recommendation; user remains able to override it.

## 7. OCR and region OCR

**CamScanner evidence**
- `mode_ocr` and `ocrapi` packages
- `OcrRegionActivity`
- native `libOCREngine.so`
- page-scene methods that optionally consume OCR

**DocVault current**
- `IOcrEngine`
- `DefaultOcrEngine.recognizeText()`
- `OcrVerificationScreen`
- `FieldExtractor`

**Required DocVault parity**
- Keep ML Kit behind `IOcrEngine`.
- Add region OCR/crop-to-text.
- Persist raw OCR, normalized OCR and user-corrected OCR separately.
- Run OCR after geometry correction and selected enhancement, not on the raw camera frame only.
- Add language/model routing without hard-coding UI to one OCR provider.

## 8. Batch scanning and page editor

**CamScanner evidence**
- `BatchModeActivity`
- `batch` package
- `multiimageedit` package
- `MovePageActivity`
- `pagelist` / `pagedetail` packages

**DocVault current**
- `ScannedPageDraft`
- `VaultViewModel` page add/update/remove/rotate/filter methods

**Required DocVault parity**
- Treat batch mode as a first-class scan session, not repeated isolated scans.
- Add page reorder, duplicate, delete, re-crop, re-filter and re-OCR.
- Preserve per-page original + edit recipe + OCR + thumbnail.

## 9. Advanced capture modes

**CamScanner evidence**
- `capture.largescan`
- `infinityscan`
- `booksplitter`
- `imagestitch`, `imagestitchnew`, `imagestitchv3`
- `capture.invoice`
- `capture.certificates`
- `card_photo`
- `capture.qrcode`

**Required independent DocVault engines**
- `LargeScanEngine`
- `BookSplitEngine`
- `StitchEngine`
- `InvoiceMode`
- `IdentityDocumentMode`
- `CodeRecognitionEngine`

These should share the same CameraX acquisition layer but have separate detectors/postprocessors rather than one large conditional scanner class.

## Scanner P1 completion definition

P1 is complete only when all of the following are demonstrated on a physical Android device:
1. stable live document outline;
2. reliable auto-capture quality gate;
3. draggable corners with loupe + edge snapping;
4. correct perspective crop with no background leakage;
5. non-destructive Magic/Color/Gray/B&W/Contrast processing;
6. batch capture and page re-edit;
7. post-rectification OCR and editable OCR;
8. state restoration after rotation/backgrounding;
9. no regression in encryption, storage or biometric lock;
10. screenshot/video evidence for each acceptance criterion.
