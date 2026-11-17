"""Build deterministic local ZIP artifacts. Does not upload, install or publish."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from validate_kit import ROOT, validate

SKIP = {".git", ".validation", "__pycache__", "dist", ".venv", "node_modules", ".hyperframes", "renders", ".pytest_cache"}
SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".html", ".js", ".mjs", ".css", ".svg", ".mp4", ".png"}
BINARY_SUFFIXES = {".mp4", ".png"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def add_file(archive: ZipFile, path: Path, arcname: str) -> None:
    info = ZipInfo(arcname, FIXED_TIME)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    data = path.read_bytes()
    if path.suffix in SUFFIXES - BINARY_SUFFIXES or path.name in {"LICENSE", ".gitignore", ".gitattributes"}:
        data = data.replace(b"\r\n", b"\n")
    archive.writestr(info, data)


def build(root: Path = ROOT) -> dict:
    errors = validate(root)
    if errors:
        raise ValueError("; ".join(errors))
    output = root / "dist"
    output.mkdir(exist_ok=True)
    artifacts = []
    for skill in sorted((root / "skills").iterdir()):
        if not skill.is_dir():
            continue
        path = output / f"{skill.name}.zip"
        with ZipFile(path, "w") as archive:
            for resource in sorted(skill.rglob("*")):
                if resource.is_file() and not any(part in SKIP for part in resource.relative_to(skill).parts):
                    add_file(archive, resource, f"{skill.name}/{resource.relative_to(skill).as_posix()}")
        artifacts.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    path = output / "anyx-agent-kit-prepared.zip"
    with ZipFile(path, "w") as archive:
        for resource in sorted(root.rglob("*")):
            rel = resource.relative_to(root)
            if not resource.is_file() or any(part in SKIP for part in rel.parts):
                continue
            if resource.is_symlink() or resource.name.startswith(".env"):
                raise ValueError(f"Refusing to package secret/symlink {rel}")
            if resource.suffix in SUFFIXES or resource.name in {"LICENSE", ".gitignore", ".gitattributes"}:
                add_file(archive, resource, f"anyx-agent-kit/{rel.as_posix()}")
    artifacts.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {"status": "packaged", "publication_verified_by_builder": False, "artifacts": artifacts}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))

