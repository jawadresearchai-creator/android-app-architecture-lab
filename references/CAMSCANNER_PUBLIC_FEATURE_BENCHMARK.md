# CamScanner public-feature benchmark

This document is intentionally based only on CamScanner's public product and developer documentation. It is **not** derived from decompiled CamScanner code.

## Why CamScanner itself is not decompiled here

CamScanner's current Terms of Service restrict reverse engineering/decompilation and also restrict using the service to develop a competing product, except where applicable law mandatorily overrides those restrictions. For this lab, CamScanner is therefore treated as a **black-box product benchmark**, not a source-code reference.

## Publicly documented scanner capabilities

### Capture and document detection
- Mobile document capture.
- Smart document-edge detection.
- Automatic crop/background removal.
- Page flattening / geometry correction.
- Manual detail/crop adjustment.

### Image enhancement
- Multiple image-enhancement modes / filters.
- High-quality text/graphics enhancement.
- Background cleanup.

### OCR and document intelligence
- OCR / image-to-text.
- Public product documentation advertises multilingual OCR.
- Conversion/export to document-oriented formats.

### Document pipeline
A neutral architecture derived from the publicly described behavior is:

```text
Camera / Gallery
      |
      v
Frame quality checks
      |
      v
Document boundary detection
      |
      +--> confidence / stability logic
      |
      v
Four-corner geometry
      |
      +--> manual corner adjustment
      |
      v
Perspective / page-flatten transform
      |
      v
Background cleanup
      |
      v
Image enhancement / filters
      |
      +--> original
      +--> enhanced / magic-like
      +--> grayscale
      +--> black & white
      +--> other presets
      |
      v
OCR
      |
      v
Page model
      |
      v
Multi-page document model
      |
      +--> reorder / delete / retake
      |
      v
PDF/JPG/text export + sharing + sync
```

## Engineering benchmark for our own app

We should evaluate our scanner against these black-box outcomes rather than copying implementation details:

1. edge detection reliability across cluttered backgrounds;
2. low-light and blur handling;
3. corner stability before auto-capture;
4. manual crop precision and magnified corner loupe;
5. perspective correction quality;
6. curved-page / page-flatten behavior;
7. background removal quality;
8. filter quality on receipts, IDs, books, forms, and ordinary A4 pages;
9. OCR accuracy and confidence handling;
10. multi-page workflow speed;
11. export quality versus file size;
12. offline/private processing where feasible;
13. graceful failure when no quadrilateral is detected.

## Clean-room rule

CamScanner is used only to define **observable capabilities and UX targets**. Implementation architecture should come from our own engineering work and permissively licensed/open-source references.
