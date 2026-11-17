"""Offline artifact invariants; no browser, Hyperframes render, or remote calls."""
from __future__ import annotations

import copy
from html import unescape
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "dashboard": ("anyx-project-dashboard", "render_dashboard.py"),
    "presentation": ("anyx-project-presentation", "render_presentation.py"),
    "video": ("anyx-project-video", "build_video.py"),
}


def brief():
    """An independent, small synthetic project, not the shipped demonstration."""
    return {
        "schema_version": 1, "synthetic": True, "language": "he",
        "project": {
            "id": "QA-9", "title": "בדיקת פרויקט",
            "period": {"start": "2026-11-17T09:00:00+02:00",
                       "end": "2026-11-17T11:00:00+02:00",
                       "timezone": "Asia/Jerusalem"},
            "data_as_of": "2026-11-17T11:15:00+02:00",
        },
        "coverage": {"status": "partial", "note": "Only the bounded captured discussion was read."},
        "summary": [{"text": "The revised scope is awaiting approval.", "source_ids": ["Q1"]}],
        "actions": [{"id": "A-QA", "title": "Confirm the revised scope", "owner": "Demo reviewer",
                     "status": "accepted-for-check", "due": "2026-11-18T12:30:00+02:00",
                     "source_ids": ["Q1", "Q2"]}],
        "decisions": [{"id": "D-QA", "text": "The earlier start approval was withdrawn.",
                       "status": "withdrawn", "source_ids": ["Q1"]}],
        "risks": [{"text": "The revised signature has not been observed.",
                   "status": "unresolved", "source_ids": ["Q2"]}],
        "sources": [
            {"id": "Q1", "system": "synthetic-anyx", "group_id": "demo-group-qa",
             "record_id": "demo-record-qa-1", "timestamp": "2026-11-17T10:21:00+02:00",
             "label": "Synthetic withdrawal", "url": None},
            {"id": "Q2", "system": "synthetic-document", "record_id": "demo-document-qa-2",
             "timestamp": "2026-11-17T10:32:00+02:00", "label": "Synthetic scope draft",
             "url": "https://evidence.example.test/demo/scope"},
        ],
    }


def validator(skill):
    path = ROOT / "skills" / skill / "scripts" / "brief_support.py"
    spec = importlib.util.spec_from_file_location(skill.replace("-", "_") + "_brief", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_brief


class ParsedHTML(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.visible = []
        self.hidden_depth = 0
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag in ("script", "style"):
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden_depth = max(0, self.hidden_depth - 1)

    def handle_data(self, data):
        if not self.hidden_depth:
            self.visible.append(data)


class BriefValidationChecks(unittest.TestCase):
    def test_sourced_bounded_brief_is_accepted_by_each_portable_copy(self):
        for skill, _ in SKILLS.values():
            with self.subTest(skill=skill):
                data = brief()
                self.assertEqual(validator(skill)(copy.deepcopy(data)), data)

    def test_every_section_rejects_unsourced_or_unresolvable_facts(self):
        for skill, _ in SKILLS.values():
            for section in ("summary", "actions", "decisions", "risks"):
                for refs in ([], ["missing-source"]):
                    with self.subTest(skill=skill, section=section, refs=refs):
                        data = brief()
                        data[section][0]["source_ids"] = refs
                        with self.assertRaises(ValueError):
                            validator(skill)(data)

    def test_script_and_credential_bearing_source_urls_are_rejected(self):
        urls = (
            "javascript:alert('not-executed')",
            "https://demo-user:demo-secret@evidence.example.test/",
            "https://evidence.example.test/?api_key=not-a-real-key",
            "https://evidence.example.test/?api%5Fkey=not-a-real-key",
            "https://evidence.example.test/?token=not-a-real-token",
        )
        for skill, _ in SKILLS.values():
            for url in urls:
                with self.subTest(skill=skill, url=url):
                    data = brief()
                    data["sources"][1]["url"] = url
                    with self.assertRaises(ValueError):
                        validator(skill)(data)

    def test_periods_compare_aware_instants_and_reject_naive_or_reversed_bounds(self):
        for skill, _ in SKILLS.values():
            check = validator(skill)
            with self.subTest(skill=skill, case="different-offsets-valid"):
                data = brief()
                data["project"]["period"].update(start="2026-11-17T10:00:00+02:00",
                                                 end="2026-11-17T08:30:00Z")
                self.assertEqual(check(data), data)
            for start, end in (
                ("2026-11-17T09:00:00", "2026-11-17T11:00:00+02:00"),
                ("2026-11-17T10:00:00+02:00", "2026-11-17T08:00:00Z"),
                ("2026-11-17T10:00:00+02:00", "2026-11-17T07:59:00Z"),
            ):
                with self.subTest(skill=skill, start=start, end=end):
                    data = brief()
                    data["project"]["period"].update(start=start, end=end)
                    with self.assertRaises(ValueError):
                        check(data)

    def test_naive_due_and_duplicate_source_identity_are_rejected(self):
        for skill, _ in SKILLS.values():
            with self.subTest(skill=skill, case="naive-due"):
                data = brief()
                data["actions"][0]["due"] = "2026-11-18T12:30:00"
                with self.assertRaises(ValueError):
                    validator(skill)(data)
            with self.subTest(skill=skill, case="duplicate-source"):
                data = brief()
                data["sources"].append(copy.deepcopy(data["sources"][0]))
                with self.assertRaises(ValueError):
                    validator(skill)(data)


class RendererArtifactChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_renderer(self, kind, data):
        skill, script = SKILLS[kind]
        independent = self.workspace / (kind + "-isolated")
        shutil.copytree(ROOT / "skills" / skill / "scripts", independent / "scripts")
        source = independent / "brief.json"
        source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        output = independent / ("composition" if kind == "video" else "artifact.html")
        env = {key: value for key, value in os.environ.items()
               if key.upper() not in ("PYTHONPATH", "PYTHONHOME")}
        process = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(independent / "scripts" / script),
             "--input", str(source), "--output", str(output)],
            cwd=self.workspace, env=env, capture_output=True, text=True,
            encoding="utf-8", timeout=30,
        )
        return process, output

    def html_output(self, kind, output):
        return (output / "index.html" if kind == "video" else output).read_text(encoding="utf-8")

    def assert_renders(self, process):
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_copied_renderer_scripts_run_without_repo_imports_or_external_assets(self):
        for kind in SKILLS:
            with self.subTest(kind=kind):
                process, output = self.run_renderer(kind, brief())
                self.assert_renders(process)
                parsed = ParsedHTML(self.html_output(kind, output))
                roots = [attrs for tag, attrs in parsed.tags if tag == "html"]
                self.assertEqual(roots[0].get("lang"), "he")
                self.assertEqual(roots[0].get("dir"), "rtl")
                for tag, attrs in parsed.tags:
                    if tag in ("script", "img", "video", "audio", "iframe", "link"):
                        resource = attrs.get("src") or (attrs.get("href") if tag == "link" else None)
                        self.assertFalse(resource and resource.startswith(("http:", "https:", "//")),
                                         (tag, resource))

    def test_untrusted_project_row_and_source_text_cannot_create_executable_markup(self):
        for kind in SKILLS:
            with self.subTest(kind=kind):
                data = brief()
                script_text = "<script>window.__qa_injected=1</script>"
                image_text = '<img src="x" onerror="window.__qa_injected=2">'
                data["project"]["title"] = script_text
                data["summary"][0]["text"] = image_text
                data["actions"][0]["owner"] = image_text
                data["sources"][0]["label"] = script_text
                process, output = self.run_renderer(kind, data)
                self.assert_renders(process)
                html = self.html_output(kind, output)
                parsed = ParsedHTML(html)
                self.assertNotIn(script_text, html)
                self.assertNotIn(image_text, html)
                self.assertIn(script_text, " ".join(parsed.visible))
                self.assertFalse(any("onerror" in attrs for _, attrs in parsed.tags))
                self.assertFalse(any(tag == "img" for tag, _ in parsed.tags))

    def test_provenance_and_requested_period_survive_artifact_generation(self):
        for kind in SKILLS:
            with self.subTest(kind=kind):
                data = brief()
                process, output = self.run_renderer(kind, data)
                self.assert_renders(process)
                if kind == "video":
                    preserved = json.loads((output / "brief.json").read_text(encoding="utf-8"))
                    self.assertEqual(preserved, data)
                else:
                    html = unescape(self.html_output(kind, output))
                    for source in data["sources"]:
                        for field in ("id", "system", "group_id", "record_id", "timestamp", "url"):
                            if source.get(field):
                                self.assertIn(source[field], html, (kind, field))
                    for value in data["project"]["period"].values():
                        self.assertIn(value, html)

    def test_video_retains_all_actions_decisions_statuses_owners_and_due_dates(self):
        data = brief()
        data["actions"] = [
            {"id": f"A-{index}", "title": f"Distinct action {index}", "owner": f"Reviewer {index}",
             "status": f"review-state-{index}", "due": f"2026-11-{18 + index:02d}T12:30:00+02:00",
             "source_ids": ["Q1"]} for index in range(5)
        ]
        data["decisions"] = [
            {"id": f"D-{index}", "text": f"Distinct decision {index} remains conditional.",
             "status": f"decision-state-{index}", "source_ids": ["Q2"]} for index in range(5)
        ]
        process, output = self.run_renderer("video", data)
        self.assert_renders(process)
        visible = " ".join(ParsedHTML(self.html_output("video", output)).visible)
        for action in data["actions"]:
            for key in ("title", "owner", "status", "due"):
                self.assertIn(action[key], visible, (action["id"], key))
        for decision in data["decisions"]:
            self.assertIn(decision["text"], visible)
            self.assertIn(decision["status"], visible)

    def test_video_preparation_does_not_claim_or_create_an_mp4(self):
        process, output = self.run_renderer("video", brief())
        self.assert_renders(process)
        result = json.loads((output / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(result["artifact_kind"], "composition")
        self.assertIs(result["rendered"], False)
        self.assertIs(result["verified"], False)
        self.assertGreater(result["duration_seconds"], 0)
        self.assertFalse(list(output.rglob("*.mp4")))

    def test_video_over_capacity_fails_instead_of_silently_dropping_rows(self):
        data = brief()
        data["actions"] = [
            {"id": f"A-{index}", "title": f"Action {index}: " + "Long accepted scope condition. " * 5,
             "owner": None, "status": "conditional", "due": None, "source_ids": ["Q1"]}
            for index in range(40)
        ]
        process, output = self.run_renderer("video", data)
        self.assertNotEqual(process.returncode, 0)
        self.assertFalse((output / "result.json").exists())
        self.assertFalse(list(output.rglob("*.mp4")))

    def test_existing_output_is_not_overwritten(self):
        data = brief()
        for kind in SKILLS:
            with self.subTest(kind=kind):
                process, output = self.run_renderer(kind, data)
                self.assert_renders(process)
                artifact = output / "index.html" if kind == "video" else output
                before = artifact.read_bytes()
                skill, script = SKILLS[kind]
                second = subprocess.run(
                    [sys.executable, "-B", "-X", "utf8", str(ROOT / "skills" / skill / "scripts" / script),
                     "--input", str(output.parent / "brief.json"), "--output", str(output)],
                    capture_output=True, text=True, encoding="utf-8", timeout=30,
                )
                self.assertNotEqual(second.returncode, 0)
                self.assertEqual(artifact.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
