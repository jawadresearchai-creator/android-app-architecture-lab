# CamScanner → DocVault Feature Gap Matrix

This matrix converts observed reference capabilities into independent DocVault requirements. `Existing` means the target APK already exposes meaningful implementation; `Strengthen` means the capability exists but needs major quality/reliability work; `Add` means a distinct module/workflow is missing or not evident from the APK inventory.

| Capability | CamScanner evidence | DocVault state | Required action |
|---|---|---|---|
| Camera capture | Large `capture` domain, CameraX/camera packages, capture controllers | Scanner screen exists | **Strengthen** live camera orchestration |
| Live document-edge detection | page/scanner engines; capture controllers | `DocumentDetector` exists | **Strengthen** with frame-by-frame stability, confidence and latency targets |
| Auto-capture | mature capture flow signals | not established as reliable | **Add/Strengthen** stability gate + countdown + motion/focus checks |
| Four-corner crop editing | scanner/page workflows | quad model and perspective functions exist | **Strengthen** draggable corners, magnifier/loupe, edge snapping, constraints |
| Perspective correction | scanner/native image engines | `rectifyPerspective` exists | **Strengthen** geometry, interpolation and output bounds |
| Background cleanup | image-processing engines | `cleanDocumentBackground` exists | **Strengthen** illumination/shadow/background separation |
| Magic enhancement | `libmagicenhancer`, image console/filter domains | basic filters exist | **Add** independent adaptive document enhancement pipeline |
| B&W/gray/contrast | filter/image console | present | **Strengthen** document-adaptive thresholds and preview parity |
| Border enhancement | dedicated `borderenhance` domain | not explicit | **Add** page-border cleanup/enhancement |
| Smart erase | dedicated `smarterase` domain | redaction exists, not smart object erase | **Add** optional cleanup tool |
| Batch scanning | `BatchModeActivity`, batch/background scan domains | multi-page session exists | **Strengthen** rapid capture, reorder, bulk processing, session recovery |
| Multi-image editing | `multiimageedit` domain | limited | **Add** bulk crop/filter/rotate/delete/reorder |
| ID/certificate capture | certificate/certificate-photo/card domains | generic document classification | **Add** specialized framing and card/certificate templates |
| Receipt/invoice capture | invoice/receipt ViewModels and export flows | generic fields | **Add** receipt/invoice profile and table/amount/date extraction |
| QR/barcode scan | QR engine and capture package | not evident | **Add** ML Kit barcode/QR mode |
| Book scan/page split | `booksplitter` | not evident | **Add** gutter detection, dual-page split, curvature correction later |
| Large scan | `largescan` | not evident | **Add** large-page capture workflow |
| Long-image stitch | `liblongImageStitch`, stitch modules | not evident | **Add** stitch pipeline |
| OCR | `mode_ocr`, `LocalOcrService`, OCR native engine | ML Kit OCR exists | **Strengthen** multi-page queues, language/model strategy, error UI |
| OCR search | search + OCR domains | universal search exists | **Strengthen** index OCR text and ranked full-text search |
| Structured field extraction | invoice/certification/OCR modules | `FieldExtractor` exists | **Strengthen** type-specific schemas, confidence and verification |
| Document classification | AI/classifier/native inference | `DocumentClassifier` exists | **Strengthen** classifier confidence, fallback, user correction |
| Image-to-Word | `pic2word` | absent | **Add** DOCX/RTF-style export through independent implementation |
| Excel/table export | invoice/export/jsondoc Excel signals | absent | **Add** table detection + CSV/XLSX export where justified |
| Translation | `translate_new` | absent | **Add** optional OCR-text translation layer |
| PDF generation | PDF/native engines | present | **Strengthen** page size, compression, metadata and quality controls |
| PDF rendering | pdfium/pdfengine | basic export focus | **Add/Strengthen** reliable viewer/rasterizer |
| PDF merge/split/reorder | merge/pdf/page-list domains | page operations partial | **Strengthen** full document operations |
| PDF compression | `share.pdf_compress` | not evident | **Add** configurable image/PDF compression |
| Password-protected PDF | security/PDF signals | vault encryption exists | **Add** standard PDF password/export protection |
| Annotation/doodle | doodle/annotation domains | redaction only | **Add** pen/highlight/text/shape annotations |
| E-signature | `newsign`, signature modules | absent | **Add** signature capture/place/resize/rotate/save |
| Watermark/security mark | WaterMarkActivity/securitymark | absent/limited | **Add** text/image watermark engine |
| Redaction | reference has removal/security tooling | present | **Strengthen** permanent raster/PDF redaction verification |
| Search/tags/folders | search/mainmenu/tags | collections/search/favorites present | **Strengthen** indexing, tags and smart views |
| AI search/document assistant | `csai` / AI services | `VaultAiEngine` exists | **Strengthen** local-first metadata/OCR retrieval and source-grounding |
| Backup | dedicated backup | encrypted backup present | **Strengthen** versioning, integrity verification, incremental strategy |
| Cloud sync | sync/onecloud | not core | **Optional Add** only with explicit privacy model |
| App/document lock | lock/security modules | strong biometric/crypto foundation | **Existing/Strengthen** UX, recovery and tamper diagnostics |
| Printing | printer modules | not evident | **Add** Android Print Framework |
| Remote fax | reference feature | absent | **Do not prioritize**; requires external paid service |
| Share/export | large share domain | present | **Strengthen** export profiles, audit and temporary-file security |

## Priority interpretation

The highest-value gap is not the number of menu features. It is the **quality of the capture → boundary → crop → rectify → enhance → OCR pipeline**. DocVault already contains most architectural primitives for a vault application; scanner parity should therefore be achieved by replacing the weak processing internals while keeping its cleaner domain/repository/security architecture.

## Definition of scanner-parity quality

A release should not be called parity-ready until it demonstrates on a device corpus:

- stable live quadrilateral tracking without corner jumping
- correct capture of rotated/skewed pages
- strong rejection of background/table edges
- manual handles that remain under the finger and expose a usable magnifier
- perspective output that preserves the full page without background wedges
- adaptive enhancement that improves paper/background separation without destroying text/photos
- repeatable batch scanning without leaks, freezes or lost pages
- OCR performed on the final rectified high-resolution page rather than low-quality previews
- non-destructive edit history so Original always restores the source capture
