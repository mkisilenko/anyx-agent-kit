"""Portable archives must preserve references and exclude local/private artifacts."""
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_skill_zips import build
from validate_kit import validate


class PackagingChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            "dist", ".validation", "__pycache__", ".git", ".venv", "node_modules", "renders", ".hyperframes"))

    def tearDown(self):
        self.temp.cleanup()

    def test_archives_self_contained_reproducible_and_private_state_excluded(self):
        private = self.root / ".validation" / "local-session.json"
        private.parent.mkdir()
        private.write_text('{"private":true}', encoding="utf-8")
        dependency = self.root / "node_modules" / "vendor.js"
        dependency.parent.mkdir()
        dependency.write_text("vendor code is not redistributed", encoding="utf-8")
        first = build(self.root)
        first_bytes = {row["file"]: (self.root / "dist" / row["file"]).read_bytes()
                       for row in first["artifacts"]}
        second = build(self.root)
        for row in second["artifacts"]:
            actual = (self.root / "dist" / row["file"]).read_bytes()
            self.assertEqual(actual, first_bytes[row["file"]])
            self.assertEqual(hashlib.sha256(actual).hexdigest(), row["sha256"])
            with ZipFile(self.root / "dist" / row["file"]) as archive:
                self.assertFalse(any(".validation" in n or "__pycache__" in n or "node_modules" in n
                                     for n in archive.namelist()))
                if row["file"] != "anyx-agent-kit-prepared.zip":
                    skill = row["file"][:-4]
                    self.assertIn(f"{skill}/SKILL.md", archive.namelist())
                    self.assertIn(f"{skill}/references/mcp-reading.md", archive.namelist())

    def test_reference_outside_installable_skill_is_rejected(self):
        path = self.root / "skills/anyx-team-catchup/SKILL.md"
        with path.open("a", encoding="utf-8") as output:
            output.write("\n[Not portable](../../README.md)\n")
        self.assertTrue(any("escapes" in error for error in validate(self.root)))

    def test_secret_file_in_skill_prevents_packaging(self):
        path = self.root / "skills/anyx-team-catchup/.env"
        path.write_text("DEMO_ONLY=not-a-secret\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            build(self.root)


if __name__ == "__main__":
    unittest.main()

