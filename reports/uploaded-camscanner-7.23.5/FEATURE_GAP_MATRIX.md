# CamScanner → DocVault Feature Gap Matrix

This matrix is a clean-room feature/architecture comparison derived from package/class/method/native-library evidence. It is not a source-code transplant plan.

| Capability | CamScanner evidence | DocVault evidence | Initial gap |
|---|---:|---:|---|
| Scanning/capture | 2979 cls / 22464 meth | 78 cls / 278 meth | Present in DocVault but much thinner than CamScanner |
| Auto edge/boundary detection | 41 cls / 357 meth | 2 cls / 20 meth | Present in DocVault but much thinner than CamScanner |
| Crop & perspective correction | 137 cls / 981 meth | 25 cls / 100 meth | Present in DocVault but much thinner than CamScanner |
| Image enhancement & filters | 675 cls / 4878 meth | 1 cls / 29 meth | Present in DocVault but much thinner than CamScanner |
| OCR/text recognition | 980 cls / 6399 meth | 126 cls / 554 meth | Present in DocVault but much thinner than CamScanner |
| PDF engine & editing | 2200 cls / 13736 meth | 1 cls / 6 meth | Present in DocVault but much thinner than CamScanner |
| Annotation/drawing | 871 cls / 6125 meth | 1 cls / 5 meth | Present in DocVault but much thinner than CamScanner |
| Watermark/signature | 1696 cls / 10645 meth | 0 cls / 0 meth | Missing/needs implementation in DocVault |
| Batch/multi-page | 329 cls / 2707 meth | 0 cls / 0 meth | Missing/needs implementation in DocVault |
| Long image/stitching | 212 cls / 1361 meth | 0 cls / 0 meth | Missing/needs implementation in DocVault |
| QR/barcode | 422 cls / 3813 meth | 0 cls / 45 meth | Present in DocVault but much thinner than CamScanner |
| ID/passport/card | 18 cls / 110 meth | 0 cls / 3 meth | Present in DocVault but much thinner than CamScanner |
| Receipt/invoice | 370 cls / 2202 meth | 0 cls / 0 meth | Missing/needs implementation in DocVault |
| Search/indexing | 627 cls / 3452 meth | 21 cls / 70 meth | Present in DocVault but much thinner than CamScanner |
| Folders/tags/document organization | 558 cls / 3414 meth | 4 cls / 35 meth | Present in DocVault but much thinner than CamScanner |
| Cloud/sync/backup | 976 cls / 5901 meth | 38 cls / 171 meth | Present in DocVault but much thinner than CamScanner |
| Share/export/print | 3310 cls / 20180 meth | 53 cls / 231 meth | Present in DocVault but much thinner than CamScanner |
| Compression/conversion | 965 cls / 5117 meth | 1 cls / 17 meth | Present in DocVault but much thinner than CamScanner |
| Encryption/security | 325 cls / 2079 meth | 265 cls / 1269 meth | Present; needs behavioral/quality comparison |
| Biometric/auth | 87 cls / 567 meth | 3 cls / 29 meth | Present in DocVault but much thinner than CamScanner |
| Reminders/expiry | 11 cls / 93 meth | 83 cls / 332 meth | Present; needs behavioral/quality comparison |
| Translation | 180 cls / 1237 meth | 0 cls / 0 meth | Missing/needs implementation in DocVault |
| Markdown | 64 cls / 406 meth | 0 cls / 0 meth | Missing/needs implementation in DocVault |
| AI/smart features | 374 cls / 2399 meth | 3 cls / 31 meth | Present in DocVault but much thinner than CamScanner |

## High-value CamScanner native engines absent from DocVault

- `libCVNN.so`
- `libEncryptorP.so`
- `libMNN.so`
- `libOCREngine.so`
- `libQREngine.so`
- `libTAGEngine.so`
- `libTAGEngineV2.so`
- `libencryptfile.so`
- `libenhance4draft.so`
- `libimageprocessor.so`
- `liblongImageStitch.so`
- `libmagicenhancer.so`
- `libnative-encrypt.so`
- `liboctopus_classifier.so`
- `libopencv.so`
- `libpagescanner.so`
- `libpdfengine.so`
- `libpdfium.so`
- `libpdfium_jni.so`
- `libscannercs.so`

## Recommended DocVault implementation order

1. Scanner acquisition: stable CameraX capture, orientation, focus/exposure, batch capture.
2. Document geometry: page detection, four-corner editor, loupe, edge snapping, perspective correction.
3. Image pipeline: background cleanup, shadow removal, Magic/B&W/Gray/Contrast filters, non-destructive originals.
4. OCR + extraction: offline OCR, searchable text, structured field extraction, receipt/ID/document classifiers.
5. PDF stack: multipage PDF, page reorder/rotate/crop, annotation, signature, watermark, compression, merge/split.
6. Organization/search: folders, tags, favorites, full-text indexing, smart search.
7. Security: encryption-at-rest, biometric gate, secure export/sharing, backup/restore.
8. Advanced parity: long-image stitching, QR/barcode, print, translation, smart/AI utilities.

Implementation should reproduce user-visible capabilities with independently written code and permissively licensed libraries; do not copy proprietary CamScanner source/assets/keys.
