"""Brand integrity from installed archives to actual output; synthetic context only."""
from __future__ import annotations

import base64
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

import test_renderers as render_checks

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_skill_zips import build

LOGO_SHA256 = "4b898fa294753d522b6a5c39475f0a430e01b5127cb0bfb39e208d29b80d3f43"
VISUAL = render_checks.SKILLS


class ImageHTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.csp = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "meta" and attrs.get("http-equiv", "").casefold() == "content-security-policy":
            self.csp = attrs.get("content", "")


class BrandingChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="anyx-branding-")
        self.directory = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def make_archives(self):
        kit = self.directory / "kit"
        shutil.copytree(ROOT, kit, ignore=shutil.ignore_patterns(
            ".git", ".validation", "dist", "node_modules", "__pycache__", ".venv",
            ".hyperframes", "renders", ".pytest_cache"))
        build(kit)
        return kit / "dist"

    def run_installed(self, kind, skill_root):
        _, filename = VISUAL[kind]
        source = self.directory / (kind + "-brief.json")
        source.write_text(json.dumps(render_checks.brief(), ensure_ascii=False), encoding="utf-8")
        output = self.directory / (kind + "-output")
        environment = {key: value for key, value in os.environ.items()
                       if key.upper() not in ("PYTHONPATH", "PYTHONHOME")}
        process = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(skill_root / "scripts" / filename),
             "--input", str(source), "--output", str(output)],
            cwd=self.directory, env=environment, capture_output=True, text=True,
            encoding="utf-8", timeout=30)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        artifact = output / "index.html" if kind == "video" else output
        return artifact.read_text(encoding="utf-8")

    def assert_original_image(self, attributes):
        self.assertEqual(attributes.get("class"), "brand-logo")
        self.assertEqual(attributes.get("alt"), "Anyx")
        self.assertEqual(attributes.get("width"), attributes.get("height"))
        self.assertGreaterEqual(int(attributes["width"]), 48)
        prefix, encoded = attributes["src"].split(",", 1)
        self.assertEqual(prefix, "data:image/png;base64")
        decoded = base64.b64decode(encoded, validate=True)
        self.assertEqual(hashlib.sha256(decoded).hexdigest(), LOGO_SHA256)
        self.assertEqual(decoded, (ROOT / "assets/brand/anyx-logo.png").read_bytes())

    def test_canonical_and_three_skill_assets_are_exact_original_bytes(self):
        original = (ROOT / "assets/brand/anyx-logo.png").read_bytes()
        self.assertEqual(len(original), 1303035)
        self.assertEqual(hashlib.sha256(original).hexdigest(), LOGO_SHA256)
        self.assertTrue(original.startswith(b"\x89PNG\r\n\x1a\n"))
        for skill, _ in VISUAL.values():
            with self.subTest(skill=skill):
                self.assertEqual((ROOT / "skills" / skill / "assets/brand/anyx-logo.png").read_bytes(), original)

    def test_skill_and_full_kit_zips_preserve_binary_assets_and_brand_guidance(self):
        archives = self.make_archives()
        original = (ROOT / "assets/brand/anyx-logo.png").read_bytes()
        for skill, _ in VISUAL.values():
            with self.subTest(skill=skill), ZipFile(archives / (skill + ".zip")) as archive:
                self.assertEqual(archive.read(skill + "/assets/brand/anyx-logo.png"), original)
        with ZipFile(archives / "anyx-agent-kit-prepared.zip") as archive:
            self.assertEqual(archive.read("anyx-agent-kit/assets/brand/anyx-logo.png"), original)
            for skill, _ in VISUAL.values():
                self.assertEqual(archive.read("anyx-agent-kit/skills/" + skill + "/assets/brand/anyx-logo.png"), original)
            for document in ("AGENTS.md", "CLAUDE.md", "BRANDING.md"):
                self.assertEqual(archive.read("anyx-agent-kit/" + document),
                                 (ROOT / document).read_bytes().replace(b"\r\n", b"\n"))

    def test_each_unpacked_skill_embeds_original_image_without_repository_or_network(self):
        archives = self.make_archives()
        for kind, (skill, _) in VISUAL.items():
            with self.subTest(kind=kind):
                installed = self.directory / (kind + "-installed")
                with ZipFile(archives / (skill + ".zip")) as archive:
                    archive.extractall(installed)
                html = self.run_installed(kind, installed / skill)
                parsed = ImageHTML(html)
                self.assertEqual(len(parsed.images), 1)
                self.assert_original_image(parsed.images[0])
                self.assertIn("object-fit:contain", html)
                if kind == "presentation":
                    self.assertIn("position:fixed", html)
                    self.assertLess(html.index('class="brand"'), html.index('class="slide"'))
                elif kind == "video":
                    self.assertGreater(html.index('class="brand"'), html.rindex("</section>"))

    def test_dashboard_csp_allows_local_data_images_without_remote_image_origins(self):
        skill, _ = VISUAL["dashboard"]
        installed = self.directory / "dashboard-installed"
        shutil.copytree(ROOT / "skills" / skill, installed)
        parsed = ImageHTML(self.run_installed("dashboard", installed))
        self.assertIsNotNone(parsed.csp)
        directives = {parts[0]: parts[1:] for directive in parsed.csp.split(";")
                      if (parts := directive.strip().split())}
        self.assertEqual(directives.get("default-src"), ["'none'"])
        self.assertEqual(directives.get("img-src"), ["data:"])
        self.assertEqual(len(parsed.images), 1)
        self.assert_original_image(parsed.images[0])


if __name__ == "__main__":
    unittest.main()
