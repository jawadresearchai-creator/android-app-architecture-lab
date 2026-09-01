# P1 Scanner — Test Contracts

These tests define acceptance before UI polish or later CamScanner-parity phases.

## Pure unit tests

### QuadTracker
- stationary quad with detector noise converges instead of jittering;
- one-frame outlier does not move the displayed quad materially;
- persistent movement follows the new location within a bounded number of frames;
- confidence decays when detections disappear;
- tracker resets after configured loss interval;
- coordinate ordering remains TL/TR/BR/BL;
- tracked quad never becomes self-intersecting.

### FrameQualityAnalyzer
- synthetic sharp edge scores higher than intentionally blurred equivalent;
- overexposed frame is rejected;
- severely underexposed frame is rejected;
- large saturated/glare region is penalized;
- document-area gate rejects tiny distant pages;
- metrics remain normalized across analysis resolutions.

### AutoCaptureController
- cannot capture without a valid quad;
- cannot capture below confidence threshold;
- cannot capture during unstable movement;
- dwell timer resets when stability/quality falls below threshold;
- capture fires once after sustained valid state;
- cooldown prevents duplicate captures;
- manual capture bypasses auto-dwell but still yields explicit page state.

### Geometry / crop validity
- every accepted quad is convex and non-crossing;
- minimum document area is enforced;
- corner drag cannot cross adjacent edges;
- edge snap proposal remains inside bitmap bounds;
- normalized coordinates round-trip through screen mapping within tolerance;
- rotation 0/90/180/270 preserves corresponding corner identity;
- perspective transform maps confirmed corners to destination corners;
- invalid geometry never silently becomes a full-frame/rectangular crop.

### Edit recipe
- applying/removing filter leaves original identity unchanged;
- recrop changes only geometry recipe and derived cache;
- rotation does not mutate original bitmap/file;
- OCR raw text is immutable after capture;
- user correction creates/updates corrected OCR without replacing raw OCR;
- page reordering changes order only;
- serialization/deserialization preserves the recipe exactly.

## Android/instrumentation tests

### Camera lifecycle
- scanner starts preview after permission grant;
- denial returns a clear UI state without crash;
- background/foreground rebinds camera once;
- rotation/config recreation does not duplicate analyzer/capture callbacks;
- torch/focus controls fail gracefully when hardware support is absent.

### Analyzer backpressure
- detector cannot queue unlimited frames;
- preview remains responsive while detector intentionally sleeps;
- every received `ImageProxy` is closed on success, rejection and exception paths.

### Capture-to-crop handoff
- accepted live quad is transferred to captured-image coordinate space;
- crop editor opens with that quad, not a fresh unrelated default;
- user can drag all corners independently;
- loupe remains aligned with active corner;
- snapping can be overridden manually.

### Batch session
- capture page 1 → page 2 → page 3 without leaving scanner;
- reorder/delete/rotate/recrop/refilter/re-OCR any page;
- process recreation restores page list and edit recipes;
- completing session persists the expected final document/pages;
- cancelling session removes temporary data but never deletes prior vault documents.

### OCR ordering
- OCR is invoked on finalized rectified/enhanced image;
- correction screen retains both raw and corrected text;
- OCR failure does not block saving an image-only document;
- region OCR results attach to correct page/region.

## Physical-device evidence matrix

Each item requires video/screenshot evidence plus build/test output:

| Gate | Required evidence |
|---|---|
| Live outline | document border follows page smoothly while camera moves |
| Auto capture | capture only after stable, sharp, well-framed page |
| Motion rejection | moving phone/page does not auto-fire |
| Glare/blur rejection | bad-quality frame visibly remains unaccepted |
| Manual crop | four corners drag independently |
| Loupe | magnified corner/edge visible without finger occlusion |
| Edge snap | corner proposes nearby document edge but remains manually overridable |
| Perspective | output rectangle contains page, not surrounding table/background |
| Filters | Original restores original; all filters are reversible |
| Batch | multiple pages captured continuously and individually re-editable |
| OCR | text is extracted after page correction and can be edited |
| Lifecycle | scanner survives rotate/background/reopen |
| Security | biometric/encryption behavior unchanged |
| Memory | multi-page session does not crash/ANR on target device |

## Regression rule

A P1 scanner improvement is not accepted if it regresses encryption, biometric lock, Room migrations, backup/restore, document metadata, existing OCR verification, sharing or previously stored vault data.
