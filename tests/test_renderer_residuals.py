"""Actual artifact/API regressions for canonical action text and valid UTF-8."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import test_renderers as existing

ROOT = existing.ROOT
SKILLS = existing.SKILLS


def load_renderer(kind):
    skill, filename = SKILLS[kind]
    scripts = ROOT / "skills" / skill / "scripts"
    previous = sys.modules.pop("brief_support", None)
    sys.path.insert(0, str(scripts))
    try:
        spec = importlib.util.spec_from_file_location("residual_" + kind, scripts / filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)
        sys.modules.pop("brief_support", None)
        if previous is not None:
            sys.modules["brief_support"] = previous


class RendererResidualChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="anyx-residuals-")
        self.directory = Path(self.temp.name)
        self.counter = 0

    def tearDown(self):
        self.temp.cleanup()

    def call_cli(self, kind, data, ensure_ascii=True):
        self.counter += 1
        folder = self.directory / f"case-{self.counter}"
        folder.mkdir()
        source = folder / "brief.json"
        source.write_text(json.dumps(data, ensure_ascii=ensure_ascii), encoding="utf-8")
        output = folder / ("video" if kind == "video" else "artifact.html")
        skill, filename = SKILLS[kind]
        process = subprocess.run(
            [sys.executable, "-B", "-X", "utf8",
             str(ROOT / "skills" / skill / "scripts" / filename),
             "--input", str(source), "--output", str(output)],
            cwd=folder, capture_output=True, text=True, encoding="utf-8", timeout=30)
        return process, output, source

    def assert_rejected_without_output(self, process, output):
        self.assertNotEqual(process.returncode, 0, process.stdout)
        self.assertNotIn("Traceback", process.stdout + process.stderr)
        response = json.loads(process.stdout)
        self.assertIs(response["valid"], False)
        self.assertTrue(response["errors"])
        # A zero-byte HTML file or a partial video directory would fail here.
        self.assertFalse(output.exists(), str(output))
        return response

    def html(self, kind, output):
        path = output / "index.html" if kind == "video" else output
        return path.read_text(encoding="utf-8")

    def test_action_alias_validation_requires_title_and_exact_matching_text(self):
        for skill, _ in SKILLS.values():
            check = existing.validator(skill)
            for alias in (None, "", False, {}, "Approve immediately without the condition."):
                with self.subTest(skill=skill, alias=alias):
                    data = existing.brief()
                    data["actions"][0]["title"] = "Approve only after the revised signed scope."
                    data["actions"][0]["text"] = alias
                    with self.assertRaises(ValueError):
                        check(data)
            data = existing.brief()
            data["actions"][0]["text"] = data["actions"][0]["title"]
            self.assertEqual(check(copy.deepcopy(data)), data)
            del data["actions"][0]["title"]
            with self.assertRaises(ValueError):
                check(data)

    def test_null_and_conflicting_aliases_fail_cleanly_before_any_of_three_outputs(self):
        for kind in SKILLS:
            for alias in (None, "Start now; omit the approval condition."):
                with self.subTest(kind=kind, alias=alias):
                    data = existing.brief()
                    data["actions"][0]["title"] = "Start only after a new signed approval."
                    data["actions"][0]["text"] = alias
                    process, output, _ = self.call_cli(kind, data)
                    self.assert_rejected_without_output(process, output)

    def test_matching_alias_produces_identical_html_and_retains_canonical_condition(self):
        for kind in SKILLS:
            with self.subTest(kind=kind):
                data = existing.brief()
                title = "Start only after the revised signed scope is approved."
                data["actions"][0]["title"] = title
                first, first_output, _ = self.call_cli(kind, data)
                self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
                data["actions"][0]["text"] = title
                second, second_output, _ = self.call_cli(kind, data)
                self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
                self.assertEqual(self.html(kind, first_output), self.html(kind, second_output))
                self.assertIn(title, self.html(kind, second_output))

    def test_lone_surrogates_anywhere_in_json_fail_before_output_creation(self):
        malformed = []
        for value in ("\ud800", "\udfff"):
            data = existing.brief()
            data["project"]["title"] = value
            malformed.append(data)
        data = existing.brief()
        data["sources"][0]["label"] = "label\ud800"
        malformed.append(data)
        data = existing.brief()
        data["metadata"] = {"history": ["valid", {"note": "\udfff"}]}
        malformed.append(data)
        data = existing.brief()
        data["metadata"] = {"\ud800": "valid value"}
        malformed.append(data)
        data = existing.brief()
        data["actions"][0]["metadata"] = [{"\udfff": "valid value"}]
        malformed.append(data)
        for kind in SKILLS:
            for index, data in enumerate(malformed):
                with self.subTest(kind=kind, placement=index):
                    process, output, _ = self.call_cli(kind, data)
                    result = self.assert_rejected_without_output(process, output)
                    self.assertIn("UTF-8", result["errors"][0])

    def test_valid_hebrew_and_literal_or_escaped_paired_emoji_are_preserved(self):
        data = existing.brief()
        data["project"]["title"] = "בדיקת פרויקט 🙂"
        data["summary"][0]["text"] = "האישור עדיין מותנה בבדיקה 🙂"
        data["actions"][0]["title"] = "לאשר רק לאחר בדיקה 🙂"
        data["actions"][0]["text"] = data["actions"][0]["title"]
        for kind in SKILLS:
            with self.subTest(kind=kind):
                literal, literal_output, _ = self.call_cli(kind, data, ensure_ascii=False)
                escaped, escaped_output, source = self.call_cli(kind, data, ensure_ascii=True)
                self.assertIn(r"\ud83d\ude42", source.read_text(encoding="utf-8"))
                self.assertEqual(literal.returncode, 0, literal.stdout + literal.stderr)
                self.assertEqual(escaped.returncode, 0, escaped.stdout + escaped.stderr)
                self.assertEqual(self.html(kind, literal_output), self.html(kind, escaped_output))
                self.assertIn(data["project"]["title"], self.html(kind, escaped_output))
                self.assertIn(data["actions"][0]["title"], self.html(kind, escaped_output))

    def test_direct_artifact_apis_also_validate_before_creating_output(self):
        for kind in SKILLS:
            module = load_renderer(kind)
            for invalid in ("alias", "unicode"):
                with self.subTest(kind=kind, invalid=invalid):
                    data = existing.brief()
                    if invalid == "alias":
                        data["actions"][0]["text"] = None
                    else:
                        data["metadata"] = {"unrecognized": ["\ud800"]}
                    target = self.directory / f"direct-{kind}-{invalid}"
                    with self.assertRaises(ValueError):
                        if kind == "video":
                            module.build(data, target)
                        else:
                            module.render(data)
                    self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
