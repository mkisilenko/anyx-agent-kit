"""Validate portable skill packaging and internal references without a network call."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"anyx-team-catchup", "anyx-materials-review", "anyx-decision-log", "anyx-project-dashboard", "anyx-project-presentation", "anyx-project-video", "anyx-project-control", "anyx-workspace-sync"}


def validate(root: Path = ROOT) -> list[str]:
    errors = []
    skills = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    if skills != EXPECTED:
        errors.append(f"Expected exactly {sorted(EXPECTED)}, found {sorted(skills)}")
    for name in sorted(skills):
        skill_root = (root / "skills" / name).resolve()
        path = skill_root / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append(f"{path.relative_to(root)}: missing YAML frontmatter")
            continue
        front = text.split("---\n", 2)[1]
        declared = re.search(r"^name:\s*['\"]?([a-z0-9-]+)", front, re.M)
        description = re.search(r"^description:\s*(.+)", front, re.M)
        if not declared or declared.group(1) != name or len(name) > 64 or "--" in name:
            errors.append(f"{name}: invalid or mismatched name")
        if not description or not 1 <= len(description.group(1).strip()) <= 1024:
            errors.append(f"{name}: missing or oversized description")
        for resource in skill_root.rglob("*"):
            if resource.is_symlink():
                errors.append(f"{name}: symlink is not portable: {resource.name}")
            if resource.is_file() and (resource.name.startswith(".env") or resource.suffix in {".pem", ".key"}):
                errors.append(f"{name}: secret-bearing file type in skill")
        for document in skill_root.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                destination = (document.parent / target.split("#")[0]).resolve()
                if not destination.is_relative_to(skill_root):
                    errors.append(f"{name}: reference escapes installable skill: {target}")
                elif not destination.exists():
                    errors.append(f"{name}: missing reference: {target}")
    for document in [root / "README.md", *(root / "docs").glob("*.md")]:
        if not document.exists():
            errors.append(f"Missing document: {document}")
            continue
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith(("#", "mailto:")) or "<" in target:
                continue
            if not (document.parent / target.split("#")[0]).exists():
                errors.append(f"{document.relative_to(root)}: missing local link {target}")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        for error in errors:
            print("FAIL:", error)
        raise SystemExit(1)
    print("PASS: 8 portable skills, frontmatter names and self-contained references")


if __name__ == "__main__":
    main()

