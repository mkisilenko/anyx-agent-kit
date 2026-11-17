"""Offline video timing checks. No rendering runtime, browser or network is used."""
from __future__ import annotations

import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def load_video_helper():
    scripts = ROOT / "skills" / "anyx-project-video" / "scripts"
    previous_support = sys.modules.pop("brief_support", None)
    sys.path.insert(0, str(scripts))
    try:
        spec = importlib.util.spec_from_file_location("video_readability_helper", scripts / "build_video.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)
        sys.modules.pop("brief_support", None)
        if previous_support is not None:
            sys.modules["brief_support"] = previous_support


VIDEO = load_video_helper()


def small_brief():
    return {
        "schema_version": 1,
        "synthetic": True,
        "language": "en",
        "project": {
            "id": "DEMO-1", "title": "Demo",
            "period": {"start": "2026-11-17T09:00:00Z", "end": "2026-11-17T10:00:00Z", "timezone": "UTC"},
            "data_as_of": "2026-11-17T10:00:00Z",
        },
        "coverage": {"status": "partial", "note": "Selected captured messages only."},
        "summary": [{"text": "Scope on hold.", "source_ids": ["V1"]}],
        "actions": [{"id": "A1", "title": "Check supplier.", "owner": "Demo reviewer", "status": "accepted",
                     "due": "2026-11-18T12:30:00Z", "source_ids": ["V1"]}],
        "decisions": [{"id": "D1", "text": "Start requires signed scope.", "status": "conditional", "source_ids": ["V1"]}],
        "risks": [{"text": "Signature unconfirmed.", "status": "open", "source_ids": ["V1"]}],
        "sources": [{"id": "V1", "system": "synthetic-anyx", "group_id": "demo-group", "record_id": "demo-record",
                     "timestamp": "2026-11-17T09:15:00Z", "label": "Fictional scope discussion", "url": None}],
    }


class CompositionHTML(HTMLParser):
    """Read the emitted timing and displayed text independently of its calculation."""
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.scenes = []
        self.current_scene = None
        self.persistent = []
        self.reading_persistent = False
        self.root_duration = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id") == "root":
            self.root_duration = int(values["data-duration"])
        if tag == "section" and "scene" in values.get("class", "").split():
            self.current_scene = {
                "id": values["id"], "start": int(values["data-start"]),
                "duration": int(values["data-duration"]), "text": [],
            }
            self.scenes.append(self.current_scene)
        if tag == "div" and values.get("class") in ("brand", "footer"):
            self.reading_persistent = True

    def handle_endtag(self, tag):
        if tag == "section":
            self.current_scene = None
        if tag == "div":
            self.reading_persistent = False

    def handle_data(self, text):
        if self.current_scene is not None:
            self.current_scene["text"].append(text)
        elif self.reading_persistent:
            self.persistent.append(text)

    def reading_characters(self, scene):
        return len(" ".join(" ".join(scene["text"] + self.persistent).split()))


class VideoReadabilityChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="anyx-video-readability-")
        self.workspace = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def build(self, data, name):
        input_path = self.workspace / (name + ".json")
        input_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        output, result = VIDEO.build(VIDEO.read_brief(input_path), self.workspace / name)
        parsed = CompositionHTML((output / "index.html").read_text(encoding="utf-8"))
        return output, result, parsed

    def assert_reading_budget(self, result, parsed):
        policy = result["reading_budget"]
        self.assertIs(policy["heuristic"], True)
        self.assertEqual(policy["characters_per_second"], 20)
        self.assertIn("footer", policy["scope"])
        self.assertTrue(parsed.persistent)
        self.assertEqual(len(parsed.scenes), len(policy["scenes"]))
        for scene, timing in zip(parsed.scenes, policy["scenes"]):
            characters = parsed.reading_characters(scene)
            self.assertLessEqual(characters / scene["duration"], 20)
            self.assertEqual(timing["reading_characters"], characters)
            self.assertGreaterEqual(scene["duration"], 4)

    def test_each_scene_budgets_actual_visible_text_and_persistent_footer(self):
        _, result, parsed = self.build(small_brief(), "paced")
        self.assert_reading_budget(result, parsed)
        self.assertTrue(any(scene["duration"] > 4 for scene in parsed.scenes))

    def test_longer_text_receives_more_time_without_truncation(self):
        short = small_brief()
        short.update(actions=[], decisions=[], risks=[])
        long = copy.deepcopy(short)
        long["summary"][0]["text"] = "Review the signed scope and retain each stated condition. " * 4
        _, short_result, _ = self.build(short, "short")
        _, long_result, parsed = self.build(long, "long")
        self.assertGreater(long_result["duration_seconds"], short_result["duration_seconds"])
        self.assertIn(long["summary"][0]["text"].strip(), " ".join(" ".join(scene["text"]) for scene in parsed.scenes))
        self.assert_reading_budget(long_result, parsed)

    def test_timeline_is_contiguous_and_matches_declared_duration(self):
        _, result, parsed = self.build(small_brief(), "timeline")
        end = 0
        for index, scene in enumerate(parsed.scenes):
            self.assertEqual(scene["id"], f"scene-{index}")
            self.assertEqual(scene["start"], end)
            end += scene["duration"]
        self.assertEqual(end, parsed.root_duration)
        self.assertEqual(end, result["duration_seconds"])
        self.assertLessEqual(end, result["reading_budget"]["maximum_video_seconds"])
        self.assertIs(result["rendered"], False)
        self.assertIs(result["verified"], False)

    def test_supported_rows_conditions_sources_and_coverage_are_retained(self):
        data = small_brief()
        data.update(summary=[], risks=[])
        data["actions"] = [dict(data["actions"][0], id=f"A{index}", title=f"Check item {index}.", owner=f"Reviewer {index}") for index in range(2)]
        data["decisions"] = [dict(data["decisions"][0], id=f"D{index}", text=f"Choice {index} remains conditional.") for index in range(2)]
        output, result, parsed = self.build(data, "retained")
        visible = " ".join(" ".join(scene["text"]) for scene in parsed.scenes)
        for action in data["actions"]:
            for field in ("title", "owner", "status", "due"):
                self.assertIn(action[field], visible)
        for decision in data["decisions"]:
            self.assertIn(decision["text"], visible)
            self.assertIn(decision["status"], visible)
        self.assertIn(data["coverage"]["note"], visible)
        self.assertIn("[V1]", visible)
        self.assertEqual(json.loads((output / "brief.json").read_text(encoding="utf-8")), data)
        self.assertFalse(list(output.glob("*.mp4")))
        self.assert_reading_budget(result, parsed)

    def test_over_time_budget_fails_before_creating_output(self):
        data = small_brief()
        data["actions"] = [dict(data["actions"][0], id=f"A{index}", title=(f"Item {index}. " + "Keep the scope and approval conditions visible. " * 5)) for index in range(3)]
        destination = self.workspace / "over-budget"
        with self.assertRaisesRegex(ValueError, "reading budget requires.*60-second maximum"):
            VIDEO.build(data, destination, max_duration_seconds=60)
        self.assertFalse(destination.exists())

    def test_hebrew_and_html_entities_use_displayed_codepoints(self):
        data = small_brief()
        data["language"] = "he"
        data["project"]["title"] = "דוגמה & בדיקה <טקסט>"
        data["summary"][0]["text"] = "יש לבדוק אישור לפני התחלה."
        _, result, parsed = self.build(data, "unicode")
        self.assertIn(data["project"]["title"], " ".join(parsed.scenes[0]["text"]))
        self.assert_reading_budget(result, parsed)

    def test_bundled_demo_prepares_completely_under_default_budget(self):
        source = ROOT / "skills/anyx-project-video/examples/demo-brief.json"
        data = VIDEO.read_brief(source)
        output, result = VIDEO.build(data, self.workspace / "bundled-demo")
        parsed = CompositionHTML((output / "index.html").read_text(encoding="utf-8"))
        self.assertGreater(result["duration_seconds"], 60)
        self.assertLessEqual(result["duration_seconds"], 180)
        self.assertEqual(result["reading_budget"]["maximum_video_seconds"], 180)
        self.assertEqual(json.loads((output / "brief.json").read_text(encoding="utf-8")), data)
        self.assertIs(result["rendered"], False)
        self.assert_reading_budget(result, parsed)

    def test_cli_applies_explicit_cap_and_rejects_sixty_seconds_without_output(self):
        script = ROOT / "skills/anyx-project-video/scripts/build_video.py"
        source = ROOT / "skills/anyx-project-video/examples/demo-brief.json"
        for maximum in (180, 60):
            with self.subTest(maximum=maximum):
                destination = self.workspace / f"cli-cap-{maximum}"
                result = subprocess.run(
                    [sys.executable, "-B", "-X", "utf8", str(script), "--input", str(source),
                     "--output", str(destination), "--max-duration-seconds", str(maximum)],
                    cwd=self.workspace, capture_output=True, text=True, encoding="utf-8", timeout=30,
                )
                payload = json.loads(result.stdout)
                if maximum == 60:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIs(payload["valid"], False)
                    self.assertIn("exceeding the 60-second maximum", payload["errors"][0])
                    self.assertFalse(destination.exists())
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertGreater(payload["duration_seconds"], 60)
                    self.assertLessEqual(payload["duration_seconds"], maximum)
                    self.assertEqual(payload["reading_budget"]["maximum_video_seconds"], maximum)
                    self.assertFalse(list(destination.glob("*.mp4")))

    def test_invalid_duration_configuration_is_rejected_before_output(self):
        for maximum in (0, -1, True, 12.5):
            with self.subTest(maximum=maximum):
                destination = self.workspace / f"invalid-cap-{maximum}"
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    VIDEO.build(small_brief(), destination, max_duration_seconds=maximum)
                self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
