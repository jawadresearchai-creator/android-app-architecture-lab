#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path

CURRENT_APK_SHA256 = "87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286"
STALE_LIBRARY_ZIP_SHA256 = "ab5610a7a1fbe177c17709e2bf79c299a52bb81fb2f43609cf86e365dc1eb8de"

REQUIRED = {
    "detector": "app/src/main/java/com/example/domain/image/DocumentDetector.kt",
    "image_processor": "app/src/main/java/com/example/domain/image/DocumentImageProcessor.kt",
    "geometry": "app/src/main/java/com/example/domain/image/DocumentGeometry.kt",
    "crop": "app/src/main/java/com/example/ui/components/DocumentCropView.kt",
    "scanner": "app/src/main/java/com/example/ui/screens/ScannerScreen.kt",
    "viewmodel": "app/src/main/java/com/example/ui/viewmodel/VaultViewModel.kt",
    "ocr": "app/src/main/java/com/example/domain/ocr/OcrEngine.kt",
    "crypto": "app/src/main/java/com/example/domain/security/VaultCrypto.kt",
    "database": "app/src/main/java/com/example/data/local/AppDatabase.kt",
}

@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_sha256(path: Path) -> str:
    return sha256(path)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.I | re.M) for p in patterns)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_zip", type=Path)
    ap.add_argument("--out", type=Path, default=Path("reconciliation"))
    args = ap.parse_args()

    source_zip = args.source_zip.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    zip_hash = sha256(source_zip)

    with tempfile.TemporaryDirectory(prefix="docvault-reconcile-") as td:
        root = Path(td)
        with zipfile.ZipFile(source_zip) as zf:
            zf.extractall(root)

        # Support a ZIP containing one top-level project folder.
        candidates = [root]
        candidates += [p for p in root.iterdir() if p.is_dir()]
        project = next((p for p in candidates if (p / "app/src/main/java/com/example").exists()), root)

        checks: list[Check] = []
        files = {k: project / v for k, v in REQUIRED.items()}

        for key, path in files.items():
            checks.append(Check(f"required:{key}", path.exists(), str(path.relative_to(project)) if path.exists() else f"missing {REQUIRED[key]}"))

        detector = read(files["detector"])
        processor = read(files["image_processor"])
        geometry = read(files["geometry"])
        crop = read(files["crop"])
        scanner = read(files["scanner"])

        checks.append(Check(
            "detector:confidence-metrics",
            contains_any(detector, [r"candidateArea", r"minEdgeSupport", r"meanEdgeSupport", r"borderPenalty", r"findOptimalQuad"]),
            "APK-era detector confidence/candidate signals detected" if detector else "DocumentDetector.kt unavailable",
        ))
        checks.append(Check(
            "processor:uses-document-detector",
            "DocumentDetector" in processor,
            "DocumentImageProcessor references DocumentDetector",
        ))
        checks.append(Check(
            "geometry:newer-quad-helpers",
            contains_any(geometry, [r"fun\s+area\s*\(", r"fun\s+containsPoint\s*\(", r"fun\s+withOffset\s*\("]),
            "newer DocumentQuad helpers found",
        ))
        checks.append(Check(
            "crop:precision-loupe",
            contains_any(crop, [r"loupe", r"magnifier", r"zoomFactor", r"Crosshair", r"Reticle"]),
            "precision crop loupe/magnifier evidence found",
        ))
        checks.append(Check(
            "crop:detector-confidence",
            contains_any(crop, [r"DetectionResult", r"edge confidence", r"confidence"]),
            "crop UI consumes detector confidence/evidence",
        ))

        internal_camera = contains_any(scanner, [
            r"LifecycleCameraController", r"PreviewView", r"ImageAnalysis", r"ImageCapture", r"ProcessCameraProvider"
        ])
        external_camera = contains_any(scanner, [r"ActivityResultContracts\.TakePicture", r"cameraLauncher", r"tempCameraUri"])
        checks.append(Check(
            "scanner:classified-camera-path",
            internal_camera or external_camera,
            "internal CameraX scanner detected" if internal_camera else ("external/one-shot camera launcher detected" if external_camera else "camera path not recognized"),
        ))

        # Source manifest.
        manifest = []
        for p in sorted(project.rglob("*")):
            if p.is_file() and ".git" not in p.parts:
                try:
                    rel = str(p.relative_to(project))
                    manifest.append({"path": rel, "size": p.stat().st_size, "sha256": file_sha256(p)})
                except OSError:
                    pass

        authored_kt = [x for x in manifest if x["path"].endswith(".kt") and "/build/" not in x["path"]]
        failed = [c for c in checks if not c.passed]

        result = {
            "source_zip": source_zip.name,
            "source_zip_sha256": zip_hash,
            "known_stale_library_zip": zip_hash == STALE_LIBRARY_ZIP_SHA256,
            "current_target_apk_sha256": CURRENT_APK_SHA256,
            "project_root": str(project),
            "authored_kotlin_files": len(authored_kt),
            "checks": [asdict(c) for c in checks],
            "failed_checks": len(failed),
            "camera_path": "internal_camerax" if internal_camera else ("external_launcher" if external_camera else "unknown"),
        }

        (out / "SOURCE_RECONCILIATION.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        (out / "SOURCE_FILE_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        md = [
            "# DocVault Source Reconciliation",
            "",
            f"- ZIP: `{source_zip.name}`",
            f"- SHA-256: `{zip_hash}`",
            f"- Known stale Library baseline: **{'YES' if zip_hash == STALE_LIBRARY_ZIP_SHA256 else 'NO'}**",
            f"- Current target APK SHA-256: `{CURRENT_APK_SHA256}`",
            f"- Authored Kotlin files: **{len(authored_kt)}**",
            f"- Camera path: **{result['camera_path']}**",
            f"- Failed reconciliation checks: **{len(failed)}**",
            "",
            "## Checks",
            "",
        ]
        for c in checks:
            md.append(f"- {'PASS' if c.passed else 'FAIL'} — **{c.name}**: {c.detail}")
        md += [
            "",
            "## Gate",
            "",
            "The source may enter P1 modification only after authored-source failures are explained and any newer APK-era work is preserved. Generated Room/Compose artifacts are not required in source.",
            "",
        ]
        (out / "SOURCE_RECONCILIATION.md").write_text("\n".join(md), encoding="utf-8")

        print(json.dumps(result, indent=2))
        if zip_hash == STALE_LIBRARY_ZIP_SHA256:
            raise SystemExit(3)
        if failed:
            raise SystemExit(2)

if __name__ == "__main__":
    main()
