# Uploaded APK Decompilation Completion Report

## Exact inputs

- Reference: CamScanner `7.23.5.2608050000`, package `com.intsig.camscanner`.
- Uploaded APKM SHA-256: `2f62abc367c8e34c6234bde6108c5b317aec027e132237a8673cf43c11cb0a52`.
- CamScanner `base.apk` SHA-256: `801514f2226f4cf35ee1992260b456c221847d8f8a212c4d0e06d17b1b31f973`.
- Target: uploaded `Docvault.apk`, SHA-256 `87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`.

## Toolchain

- Java 21.
- JADX CLI 1.5.6.
- JADX distribution was downloaded and checksum-verified by the private GitHub Actions lab, exported as an Actions artifact, then used against the exact uploaded APKM in the chat execution environment.

## CamScanner recovery

A whole-APKM normal-mode pass decoded resources and produced a large call graph but became computationally expensive in heavily obfuscated first-party code. A whole-app simple-mode pass later exhausted the Java heap at approximately 49%.

To finish the first-party surface reliably, the app-heavy DEX files were isolated and decompiled independently with a 4 GB Java heap and one JADX worker:

| DEX | Recovered Java files | JADX result |
|---|---:|---|
| `classes10.dex` | 2,184 | completed; 10 imperfect classes reported |
| `classes11.dex` | 1,021 | completed; 3 imperfect classes reported |
| `classes12.dex` | 3,787 | completed; 17 imperfect classes reported |
| `classes13.dex` | 2,784 | completed; 3 imperfect classes reported |
| `classes14.dex` | 2,547 | completed cleanly |
| **Total** | **12,323** | **all five passes completed** |

Of these, **10,389 Java files are under `com.intsig.camscanner`**. These split results complement the earlier static DEX inventory, which indexed the broader application surface and feature evidence.

## High-value recovered scanner functions

`ScannerUtils` exposes readable functional boundaries including `detectFrameBorder`, `detectSingleFrameBorder`, `findCandidateLines`, `getScanBound`, `checkCropBounds`, `adjustRect`, `trimImageF`, `trimImageS`, `surfaceCorrectWithoutBorder`, `dewarpImagePlane`, `detectCurveBorder`, `detectBookTurnPage`, `detectFinger`, `detectInvoice`, `deBlurImageBitmap`, `deBlurImageFile`, `enhanceImage`, `enhanceImageBySuperFilter`, `getPageScene`, `getPageSceneWithOcr`, `getTaxonomyPageScene`, `radarClassifyImageFile`, `loadTAGModel`, `scaleAndRotateImagePath`, `encodeImageS`, and `decodeImageS`.

These names provide strong evidence for scanner responsibilities, but DocVault should reproduce the behavior with independently written modules rather than porting proprietary implementations.

## DocVault recovery

The DocVault fast JADX pass recovered approximately **27,057 Java files in total** including dependencies, with **152 first-party Java files under `com.example`**. Key first-party components include:

- `DocumentDetector`
- `DocumentImageProcessor`
- `DefaultOcrEngine` / `IOcrEngine`
- `DocumentClassifier`
- `FieldExtractor`
- `DocumentExporter`
- `VaultCrypto`
- `BiometricAuthHelper`
- `VaultBackupManager`
- `VaultRepository`
- `VaultViewModel`
- Compose screens for scanner, crop, OCR verification, redaction/share, search, people, collections, expiry, security and backup.

## Architecture conclusion

Do **not** replace DocVault with CamScanner's internal architecture. DocVault already has a cleaner bounded architecture. The implementation strategy is to preserve its Compose/ViewModel/Repository/Room/security foundation and add independent domain engines for scanner acquisition, temporal quad tracking, geometry, enhancement, OCR regions, PDF editing, annotations, advanced capture modes and other parity capabilities.

See `SCANNER_PIPELINE_METHOD_MAP.md` and `DOCVAULT_PARITY_IMPLEMENTATION_SPEC.md` in this directory for the implementation mapping.
