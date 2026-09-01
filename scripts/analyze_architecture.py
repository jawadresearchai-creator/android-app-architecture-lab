#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

LIBRARIES = {
    "AndroidX": ["androidx/", "import androidx."],
    "Jetpack Compose": ["@Composable", "androidx.compose"],
    "Navigation Component": ["androidx.navigation", "NavHost", "NavController"],
    "Room": ["androidx.room", "@Database", "@Dao", "@Entity"],
    "DataStore": ["androidx.datastore", "DataStore<", "preferencesDataStore"],
    "WorkManager": ["androidx.work", "WorkManager", "Worker("],
    "CameraX": ["androidx.camera", "CameraProvider", "ImageAnalysis"],
    "Lifecycle/ViewModel": ["androidx.lifecycle", "ViewModel"],
    "Retrofit": ["retrofit2", "@GET(", "@POST(", "@PUT(", "@DELETE("],
    "OkHttp": ["okhttp3", "OkHttpClient"],
    "Moshi": ["com.squareup.moshi", "Moshi"],
    "Gson": ["com.google.gson", "Gson"],
    "Dagger/Hilt": ["dagger.hilt", "@HiltAndroidApp", "@AndroidEntryPoint", "@Inject"],
    "Koin": ["org.koin", "by inject()", "by viewModel()"],
    "Firebase": ["com.google.firebase", "Firebase"],
    "ML Kit": ["com.google.mlkit", "TextRecognition", "BarcodeScanning"],
    "OpenCV": ["org.opencv", "OpenCVLoader", "Mat("],
    "Glide": ["com.bumptech.glide", "Glide.with"],
    "Coil": ["coil.", "AsyncImage"],
    "Picasso": ["com.squareup.picasso", "Picasso.get"],
    "Flutter": ["io.flutter", "FlutterActivity"],
    "React Native": ["com.facebook.react", "ReactActivity"],
    "WebView": ["android.webkit.WebView", "WebView("],
}

NETWORK_MARKERS = [
    "retrofit2", "okhttp3", "HttpURLConnection", "URLConnection", "Socket(",
    "WebSocket", "@GET(", "@POST(", "@PUT(", "@PATCH(", "@DELETE(", "@Headers("
]
DATA_MARKERS = [
    "androidx.room", "SQLiteDatabase", "SQLiteOpenHelper", "SharedPreferences",
    "androidx.datastore", "Realm", "ObjectBox", "FirebaseFirestore", "FirebaseDatabase"
]

SECRET_PATTERNS = {
    "generic api-key assignment": re.compile(r"(?i)(api[_-]?key|client[_-]?secret|secret[_-]?key)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
    "bearer token literal": re.compile(r"(?i)Bearer\s+[A-Za-z0-9._~+/-]{16,}"),
}

URL_RE = re.compile(r"https?://[^\s\"'<>]+")
ENDPOINT_RE = re.compile(r"@(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s*\(\s*[\"']([^\"']*)[\"']")
PACKAGE_RE = re.compile(r"^\s*package\s+([A-Za-z0-9_.]+)\s*;?", re.MULTILINE)
CLASS_RE = re.compile(r"\b(class|interface|enum|record)\s+([A-Za-z_$][A-Za-z0-9_$]*)")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def iter_source_files(root: Path) -> Iterable[Path]:
    for ext in ("*.java", "*.kt"):
        yield from root.rglob(ext)


def iter_text_files(root: Path) -> Iterable[Path]:
    allowed = {".java", ".kt", ".xml", ".json", ".properties", ".gradle", ".smali", ".txt"}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in allowed:
            yield p


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def parse_manifest(manifest: Path) -> dict:
    out = {
        "package": None,
        "version_name": None,
        "version_code": None,
        "min_sdk": None,
        "target_sdk": None,
        "application": None,
        "permissions": [],
        "components": collections.defaultdict(list),
    }
    if not manifest.exists():
        return out
    try:
        tree = ET.parse(manifest)
        root = tree.getroot()
        out["package"] = root.attrib.get("package")
        out["version_name"] = root.attrib.get(ANDROID_NS + "versionName")
        out["version_code"] = root.attrib.get(ANDROID_NS + "versionCode")
        uses_sdk = root.find("uses-sdk")
        if uses_sdk is not None:
            out["min_sdk"] = uses_sdk.attrib.get(ANDROID_NS + "minSdkVersion")
            out["target_sdk"] = uses_sdk.attrib.get(ANDROID_NS + "targetSdkVersion")
        for node in root.findall("uses-permission") + root.findall("uses-permission-sdk-23"):
            name = node.attrib.get(ANDROID_NS + "name")
            if name:
                out["permissions"].append(name)
        app = root.find("application")
        if app is not None:
            out["application"] = app.attrib.get(ANDROID_NS + "name")
            for tag in ("activity", "activity-alias", "service", "receiver", "provider"):
                for node in app.findall(tag):
                    name = node.attrib.get(ANDROID_NS + "name")
                    exported = node.attrib.get(ANDROID_NS + "exported")
                    permission = node.attrib.get(ANDROID_NS + "permission")
                    actions = []
                    categories = []
                    for intent in node.findall("intent-filter"):
                        for action in intent.findall("action"):
                            a = action.attrib.get(ANDROID_NS + "name")
                            if a:
                                actions.append(a)
                        for category in intent.findall("category"):
                            c = category.attrib.get(ANDROID_NS + "name")
                            if c:
                                categories.append(c)
                    out["components"][tag].append({
                        "name": name,
                        "exported": exported,
                        "permission": permission,
                        "actions": sorted(set(actions)),
                        "categories": sorted(set(categories)),
                    })
    except Exception as exc:
        out["parse_error"] = str(exc)
    out["permissions"] = sorted(set(out["permissions"]))
    out["components"] = dict(out["components"])
    return out


def detect_manifest(root: Path) -> Path:
    candidates = [
        root / "resources" / "AndroidManifest.xml",
        root / "AndroidManifest.xml",
    ]
    for c in candidates:
        if c.exists():
            return c
    found = list(root.rglob("AndroidManifest.xml"))
    return found[0] if found else root / "AndroidManifest.xml"


def package_inventory(source_files: list[Path], source_root: Path) -> tuple[dict, list]:
    counter = collections.Counter()
    classes = []
    for p in source_files:
        text = read_text(p)
        m = PACKAGE_RE.search(text)
        package = m.group(1) if m else "(default)"
        counter[package] += 1
        for cm in CLASS_RE.finditer(text):
            classes.append({"name": cm.group(2), "kind": cm.group(1), "package": package, "file": rel(p, source_root)})
    return dict(counter.most_common()), classes


def detect_libraries(text_files: list[Path], root: Path) -> dict:
    hits = {name: [] for name in LIBRARIES}
    for p in text_files:
        text = read_text(p)
        low_path = rel(p, root).replace("\\", "/")
        for name, markers in LIBRARIES.items():
            if any(marker in text or marker in low_path for marker in markers):
                if len(hits[name]) < 12:
                    hits[name].append(low_path)
    return {k: sorted(set(v)) for k, v in hits.items() if v}


def architecture_signals(classes: list, libraries: dict, text_files: list[Path]) -> dict:
    names = [c["name"] for c in classes]
    packages = [c["package"] for c in classes]
    joined_names = "\n".join(names)
    joined_packages = "\n".join(packages)
    signals = {
        "viewmodels": sorted({n for n in names if n.endswith("ViewModel")}),
        "repositories": sorted({n for n in names if n.endswith("Repository") or "Repository" in n}),
        "use_cases": sorted({n for n in names if n.endswith("UseCase") or n.endswith("Interactor")}),
        "presenters": sorted({n for n in names if n.endswith("Presenter")}),
        "controllers": sorted({n for n in names if n.endswith("Controller")}),
        "activities": sorted({n for n in names if n.endswith("Activity")}),
        "fragments": sorted({n for n in names if n.endswith("Fragment")}),
        "services": sorted({n for n in names if n.endswith("Service")}),
        "workers": sorted({n for n in names if n.endswith("Worker")}),
    }
    patterns = []
    if signals["viewmodels"] and signals["repositories"]:
        patterns.append("MVVM-like layering")
    if signals["presenters"]:
        patterns.append("MVP signals")
    if signals["use_cases"] and any(x in joined_packages.lower() for x in ["domain", "data", "presentation"]):
        patterns.append("Clean Architecture / domain-use-case signals")
    if "Jetpack Compose" in libraries:
        patterns.append("Jetpack Compose UI")
    elif signals["activities"] or signals["fragments"]:
        patterns.append("View-system Android UI")
    if "Flutter" in libraries:
        patterns.append("Flutter-host Android shell")
    if "React Native" in libraries:
        patterns.append("React Native-host Android shell")
    signals["inferred_patterns"] = patterns or ["No strong named architecture pattern inferred automatically"]
    return signals


def scan_network_data(text_files: list[Path], root: Path) -> dict:
    urls = set()
    endpoints = []
    network_files = []
    data_files = []
    secret_counts = collections.Counter()
    for p in text_files:
        text = read_text(p)
        r = rel(p, root)
        if any(marker in text for marker in NETWORK_MARKERS):
            network_files.append(r)
        if any(marker in text for marker in DATA_MARKERS):
            data_files.append(r)
        for u in URL_RE.findall(text):
            if len(urls) < 250:
                urls.add(u.rstrip("),.;"))
        for method, endpoint in ENDPOINT_RE.findall(text):
            if len(endpoints) < 500:
                endpoints.append({"method": method, "path": endpoint, "file": r})
        for label, pattern in SECRET_PATTERNS.items():
            secret_counts[label] += len(pattern.findall(text))
    return {
        "urls": sorted(urls),
        "retrofit_endpoints": endpoints,
        "network_files": sorted(set(network_files))[:300],
        "data_files": sorted(set(data_files))[:300],
        "possible_secret_literal_counts": dict(secret_counts),
        "secret_values_included": False,
    }


def resource_inventory(root: Path) -> dict:
    resources = root / "resources"
    layout_count = len(list(resources.rglob("layout*/**/*.xml"))) if resources.exists() else 0
    xml_count = len(list(resources.rglob("*.xml"))) if resources.exists() else 0
    image_exts = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
    images = [p for p in resources.rglob("*") if p.is_file() and p.suffix.lower() in image_exts] if resources.exists() else []
    native = [p for p in root.rglob("*.so")]
    return {
        "xml_resources": xml_count,
        "layout_xml_files": layout_count,
        "image_assets": len(images),
        "native_libraries": [rel(p, root) for p in native],
    }


def write_md(path: Path, title: str, sections: list[tuple[str, str]]) -> None:
    body = [f"# {title}", ""]
    for heading, content in sections:
        body += [f"## {heading}", "", content.rstrip(), ""]
    path.write_text("\n".join(body), encoding="utf-8")


def bullet(items: Iterable[str], empty: str = "None detected") -> str:
    items = list(items)
    return "\n".join(f"- `{x}`" for x in items) if items else empty


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jadx-output", required=True)
    ap.add_argument("--input-file", required=True)
    ap.add_argument("--reports", required=True)
    args = ap.parse_args()

    root = Path(args.jadx_output).resolve()
    input_file = Path(args.input_file).resolve()
    reports = Path(args.reports).resolve()
    reports.mkdir(parents=True, exist_ok=True)

    source_root = root / "sources"
    source_files = list(iter_source_files(source_root if source_root.exists() else root))
    text_files = list(iter_text_files(root))
    manifest_path = detect_manifest(root)
    manifest = parse_manifest(manifest_path)
    packages, classes = package_inventory(source_files, source_root if source_root.exists() else root)
    libraries = detect_libraries(text_files, root)
    arch = architecture_signals(classes, libraries, text_files)
    network_data = scan_network_data(text_files, root)
    resources = resource_inventory(root)

    screen_candidates = sorted({
        c["name"] for c in classes
        if c["name"].endswith(("Activity", "Fragment", "Screen", "Page", "Dialog", "BottomSheet"))
    })

    analysis = {
        "input": {
            "name": input_file.name,
            "size_bytes": input_file.stat().st_size,
            "sha256": sha256_file(input_file),
        },
        "manifest_path": rel(manifest_path, root),
        "manifest": manifest,
        "source_file_count": len(source_files),
        "class_count": len(classes),
        "packages": packages,
        "libraries": libraries,
        "architecture": arch,
        "screen_candidates": screen_candidates,
        "network_and_data": network_data,
        "resources": resources,
    }
    (reports / "analysis.json").write_text(json.dumps(analysis, indent=2, sort_keys=True), encoding="utf-8")

    component_counts = {k: len(v) for k, v in manifest.get("components", {}).items()}
    summary_lines = [
        f"- Input: `{input_file.name}`",
        f"- SHA-256: `{analysis['input']['sha256']}`",
        f"- Package: `{manifest.get('package') or 'unknown'}`",
        f"- Version: `{manifest.get('version_name') or 'unknown'}` (code `{manifest.get('version_code') or 'unknown'}`)",
        f"- SDK: min `{manifest.get('min_sdk') or 'unknown'}`, target `{manifest.get('target_sdk') or 'unknown'}`",
        f"- Decompiled source files: **{len(source_files):,}**",
        f"- Detected classes/interfaces/enums: **{len(classes):,}**",
        f"- Permissions: **{len(manifest.get('permissions', []))}**",
        f"- Native libraries: **{len(resources.get('native_libraries', []))}**",
    ]
    write_md(reports / "APP_SUMMARY.md", "App Summary", [
        ("Identity", "\n".join(summary_lines)),
        ("Detected architecture", bullet(arch.get("inferred_patterns", []))),
        ("Android components", "\n".join(f"- {k}: **{v}**" for k, v in sorted(component_counts.items())) or "None parsed"),
        ("Screen candidates", bullet(screen_candidates[:150])),
    ])

    package_top = list(packages.items())[:120]
    package_body = "\n".join(f"- `{p}` — {count} source file(s)" for p, count in package_top) or "No source packages found"
    write_md(reports / "ARCHITECTURE_MAP.md", "Architecture Map", [
        ("Inferred patterns", bullet(arch.get("inferred_patterns", []))),
        ("ViewModels", bullet(arch.get("viewmodels", [])[:150])),
        ("Repositories", bullet(arch.get("repositories", [])[:150])),
        ("Use cases / interactors", bullet(arch.get("use_cases", [])[:150])),
        ("Activities", bullet(arch.get("activities", [])[:150])),
        ("Fragments", bullet(arch.get("fragments", [])[:150])),
        ("Workers / services", bullet((arch.get("workers", []) + arch.get("services", []))[:150])),
        ("Top source packages", package_body),
    ])

    component_sections = []
    for ctype, items in sorted(manifest.get("components", {}).items()):
        rows = []
        for item in items:
            rows.append(
                f"- `{item.get('name')}` — exported=`{item.get('exported')}`"
                + (f", permission=`{item.get('permission')}`" if item.get("permission") else "")
                + (f", actions={', '.join(item.get('actions', []))}" if item.get("actions") else "")
            )
        component_sections.append((ctype, "\n".join(rows) or "None"))
    component_sections.append(("Permissions", bullet(manifest.get("permissions", []))))
    write_md(reports / "ANDROID_COMPONENTS.md", "Android Components", component_sections)

    lib_sections = [(name, bullet(files[:30])) for name, files in sorted(libraries.items())]
    write_md(reports / "LIBRARY_INVENTORY.md", "Library Inventory", lib_sections or [("Detected libraries", "None detected automatically")])

    endpoint_lines = [f"- `{e['method']} {e['path']}` — `{e['file']}`" for e in network_data["retrofit_endpoints"][:250]]
    secret_counts = network_data["possible_secret_literal_counts"]
    secret_note = "Potential hard-coded credential-like literals are counted only; values are intentionally not copied into the report."
    secret_note += "\n" + ("\n".join(f"- {k}: **{v}**" for k, v in secret_counts.items()) if secret_counts else "- No configured credential-like patterns matched.")
    write_md(reports / "NETWORK_AND_DATA_LAYER.md", "Network and Data Layer", [
        ("HTTP / API endpoint annotations", "\n".join(endpoint_lines) or "No Retrofit-style endpoint annotations detected"),
        ("Observed URL literals", bullet(network_data["urls"][:150])),
        ("Network-related files", bullet(network_data["network_files"][:150])),
        ("Local data / persistence files", bullet(network_data["data_files"][:150])),
        ("Credential hygiene scan", secret_note),
    ])

    index_lines = []
    for c in classes[:10000]:
        index_lines.append(f"CLASS\t{c['package']}.{c['name']}\t{c['file']}")
    for lib, files in sorted(libraries.items()):
        for f in files:
            index_lines.append(f"LIB\t{lib}\t{f}")
    for u in network_data["urls"][:250]:
        index_lines.append(f"URL\t{u}")
    (reports / "SEARCH_INDEX.txt").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "package": manifest.get("package"),
        "source_files": len(source_files),
        "classes": len(classes),
        "libraries": sorted(libraries),
        "reports": str(reports),
    }, indent=2))


if __name__ == "__main__":
    main()
