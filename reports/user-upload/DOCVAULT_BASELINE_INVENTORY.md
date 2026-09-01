# DocVault Baseline Architecture Inventory

This inventory is derived directly from the user-supplied `Docvault.apk` and defines the target baseline before feature-parity work.

## Application scale

- APK size: 67,152,965 bytes
- 14 DEX files
- 42,073 total class definitions including dependencies
- First-party namespace: `com.example`
- Single first-party Activity detected: `com.example.MainActivity`
- Primary state holder: `com.example.ui.viewmodel.VaultViewModel`
- Primary repository: `com.example.data.repository.VaultRepository`
- Room database: `com.example.data.local.AppDatabase`

## UI/navigation architecture

DocVault is a modern single-activity Jetpack Compose application. First-party UI is concentrated under `com.example.ui.screens` and `com.example.ui.components`.

Important screens observed include:

- `HomeScreen`
- `ScannerScreen`
- `DocumentsScreen`
- `DocumentDetailScreen`
- `CollectionsScreen`
- `PeopleScreen`
- `ExpiryCenterScreen`
- `UniversalSearchScreen`
- `OcrVerificationScreen`
- `RedactionShareScreen`
- `SecurityPrivacyScreen`
- `BackupRestoreScreen`
- `VaultAiScreen`
- `VaultLockScreen`

## Data layer

Room/data classes expose a document-vault model rather than only a scanner model. DAOs observed:

- `AuditDao`
- `CollectionDao`
- `DocumentDao`
- `PersonProfileDao`
- `ReminderDao`

The repository already supports document persistence, collections/profiles, reminders, favorites/pinning, soft/hard delete and restore, expiry state, search, backup/restore, custom extracted fields, sharing audits and security diagnostics.

## Existing scanner/image pipeline

`com.example.domain.image.DocumentDetector` already implements a nontrivial quadrilateral detector with methods/signals for:

- document detection
- candidate evaluation
- diagonal-extrema quadrilateral generation
- optimal quadrilateral selection
- convex hull computation
- polygon simplification
- corner ordering
- point-to-line distance
- edge-support scoring
- confidence scoring
- border-penalty logic

`com.example.domain.image.DocumentImageProcessor` already exposes:

- `detectDocumentQuad`
- `cropBitmap`
- `rectifyPerspective`
- `cleanDocumentBackground`
- `applyFilter`
- `enhanceContrast`
- `toGrayscale`
- `toHighContrastBlackAndWhite`
- `rotateBitmap`
- image load/save/thumbnail/temp-scan handling

This means DocVault does not need a scanner feature written from zero. The main work is replacing/strengthening the capture and processing pipeline to achieve robust real-world behavior.

## OCR and document intelligence

`DefaultOcrEngine` provides OCR through bundled ML Kit OCR components.

`DocumentClassifier` exposes document classification and document-detail inference.

`FieldExtractor` already contains structured extraction flows for:

- owner/person name
- document number
- issue date
- expiry date
- authority/issuer
- semantic role inference
- document-number/date/name validation
- suggested-title generation
- structured-field candidate discovery

## Security

DocVault already has a strong security foundation under `com.example.domain.security`, including `VaultCrypto`, biometric support and security preferences.

Observed cryptographic workflows include:

- encrypt/decrypt data
- encrypted VLT envelope handling
- master key management
- biometric key-encryption-key management
- backup-key derivation
- device-bound PIN hashing/verification
- atomic encrypted file writes
- SHA-256 integrity support

## Export and sharing

`DocumentExporter` already provides:

- PDF generation
- redacted image generation
- applying redactions to bitmaps
- Android share-intent creation

## Backup and reminders

`VaultBackupManager` supports encrypted backup creation and restore.

`ReminderReceiver` supplies reminder/expiry notification infrastructure.

## Current architectural advantage

Compared with the reference app, DocVault is far smaller and structurally cleaner: single-activity Compose UI, centralized ViewModel/repository, Room persistence, domain modules for image/OCR/security/export/backup. The recommended path is to preserve this architecture and add scanner/processing capabilities behind explicit interfaces instead of importing the reference application's legacy Activity/Fragment/service structure.
