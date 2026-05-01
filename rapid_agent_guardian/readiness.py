from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


REQUIRED_PUBLIC_FILES = [
    "README.md",
    ".github/FUNDING.yml",
    "LICENSE",
    "pyproject.toml",
    "rapid_agent_guardian/__init__.py",
    "rapid_agent_guardian/agent.py",
    "rapid_agent_guardian/cli.py",
    "rapid_agent_guardian/mcp_client.py",
    "rapid_agent_guardian/models.py",
    "rapid_agent_guardian/readiness.py",
    "scripts/export_public_repo.py",
    "examples/release_goal.json",
    "tests/test_agent.py",
    "docs/HACKATHON_PLAN.md",
    "docs/SUBMISSION_DRAFT.md",
]

PUBLICATION_EXCLUDES = [
    "runtime",
    ".venv",
    "__pycache__",
    ".pytest_cache",
]

SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{16,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"bearer\s+[A-Za-z0-9._-]{16,}", re.I),
    re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*[\"']?[^\s\"']{12,}", re.I),
]

FORBIDDEN_CLAIMS = [
    "guaranteed safety",
    "eliminates hallucinations",
    "elimina alucinaciones",
    "garantiza seguridad",
    "seguridad garantizada",
]

CLAIM_SCAN_EXCLUDED_FILES = {
    "rapid_agent_guardian/readiness.py",  # contains the guardrail phrases as data, not public claims.
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _iter_public_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(rel == item or rel.startswith(f"{item}/") for item in PUBLICATION_EXCLUDES):
            continue
        if path.suffix.lower() in {".py", ".md", ".toml", ".json", ".txt"} or path.name in {"LICENSE"}:
            files.append(path)
    return files


def check_submission_readiness(root: Path | str) -> dict[str, Any]:
    project_root = Path(root).resolve()
    checks: list[dict[str, Any]] = []
    blockers: list[str] = []

    missing = [rel for rel in REQUIRED_PUBLIC_FILES if not (project_root / rel).exists()]
    checks.append({"id": "required_public_files", "ok": not missing, "missing": missing})
    if missing:
        blockers.append("missing required public files")

    secret_hits: list[str] = []
    claim_hits: list[str] = []
    for path in _iter_public_text_files(project_root):
        text = _read_text(path)
        rel = path.relative_to(project_root).as_posix()
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            secret_hits.append(rel)
        lowered = text.lower()
        if rel not in CLAIM_SCAN_EXCLUDED_FILES and any(claim in lowered for claim in FORBIDDEN_CLAIMS):
            claim_hits.append(rel)

    checks.append({"id": "secret_like_markers", "ok": not secret_hits, "files": secret_hits})
    if secret_hits:
        blockers.append("secret-like markers in public candidate files")

    checks.append({"id": "forbidden_claims", "ok": not claim_hits, "files": claim_hits})
    if claim_hits:
        blockers.append("forbidden safety claims in public copy")

    runtime_exists = (project_root / "runtime").exists()
    checks.append(
        {
            "id": "runtime_exclusion",
            "ok": True,
            "runtimeExists": runtime_exists,
            "decision": "exclude runtime from public repo export",
        }
    )

    gcloud_available = shutil.which("gcloud") is not None
    checks.append(
        {
            "id": "google_cloud_cli",
            "ok": gcloud_available,
            "blockingForLocal": False,
            "blockingForCloudDemo": True,
        }
    )

    partner_endpoint_configured = bool((project_root / "runtime" / "partner_mcp_endpoint.txt").exists())
    checks.append(
        {
            "id": "partner_mcp_real_endpoint",
            "ok": partner_endpoint_configured,
            "blockingForLocal": False,
            "blockingForCloudDemo": True,
        }
    )

    local_publication_candidate = not blockers
    cloud_demo_ready = local_publication_candidate and gcloud_available and partner_endpoint_configured
    cloud_blockers: list[str] = []
    if not gcloud_available:
        cloud_blockers.append("gcloud CLI not installed")
    if not partner_endpoint_configured:
        cloud_blockers.append("real partner MCP endpoint not configured")

    return {
        "schemaVersion": "rapid_agent_guardian.submission_readiness.v1",
        "projectRoot": str(project_root),
        "localPublicationCandidate": local_publication_candidate,
        "cloudDemoReady": cloud_demo_ready,
        "checks": checks,
        "blockers": blockers,
        "cloudBlockers": cloud_blockers,
        "publicExportInclude": REQUIRED_PUBLIC_FILES,
        "publicExportExclude": PUBLICATION_EXCLUDES,
        "decision": "LOCAL_PUBLIC_SAFE" if local_publication_candidate else "BLOCK_LOCAL_PUBLICATION",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public-safe hackathon submission readiness.")
    parser.add_argument("--root", default=".", help="Hackathon project root.")
    parser.add_argument("--out", help="Optional JSON output path.")
    args = parser.parse_args()

    report = check_submission_readiness(args.root)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0 if report["localPublicationCandidate"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
