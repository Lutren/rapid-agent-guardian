from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rapid_agent_guardian.readiness import REQUIRED_PUBLIC_FILES, check_submission_readiness


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def default_output(root: Path) -> Path:
    return root.parents[1] / "publish_staging" / "hackathons" / f"{root.name}-public-safe"


def ensure_safe_output(root: Path, output: Path) -> Path:
    root_resolved = root.resolve()
    output_resolved = output.resolve()
    if output_resolved == root_resolved or output_resolved in root_resolved.parents:
        raise ValueError(f"refusing unsafe output path: {output_resolved}")
    if root_resolved in output_resolved.parents:
        raise ValueError("output path must be outside the source tree")
    return output_resolved


def export_public_repo(root: Path | str, output: Path | str | None = None) -> dict[str, Any]:
    project_root = Path(root).resolve()
    out_root = ensure_safe_output(project_root, Path(output).resolve() if output else default_output(project_root))
    readiness = check_submission_readiness(project_root)
    if not readiness["localPublicationCandidate"]:
        raise RuntimeError("readiness gate blocked public export")

    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    exported: list[dict[str, Any]] = []
    for rel in REQUIRED_PUBLIC_FILES:
        source = project_root / rel
        target = out_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        exported.append(
            {
                "path": rel,
                "bytes": target.stat().st_size,
                "sha256": sha256_file(target),
            }
        )

    manifest = {
        "schemaVersion": "rapid_agent_guardian.public_export_manifest.v1",
        "sourceRoot": str(project_root),
        "outputRoot": str(out_root),
        "decision": "PUBLIC_EXPORT_STAGED",
        "readinessDecision": readiness["decision"],
        "cloudDemoReady": readiness["cloudDemoReady"],
        "files": exported,
        "excluded": readiness["publicExportExclude"],
    }
    manifest_path = out_root / "PUBLIC_EXPORT_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["manifestPath"] = str(manifest_path)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage a clean public-safe hackathon repo export.")
    parser.add_argument("--root", default=".", help="Hackathon project root.")
    parser.add_argument("--out", help="Output directory. Defaults to publish_staging/hackathons/<name>-public-safe.")
    args = parser.parse_args()

    manifest = export_public_repo(Path(args.root), Path(args.out) if args.out else None)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
