"""Regressions from the independent review; synthetic inputs, local outputs only."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_renderers import ROOT, SKILLS, brief, validator
from test_sync_plan import SCRIPT as SYNC_SCRIPT, add_second_operation, plan, sync


class ReviewInputRegressions(unittest.TestCase):
    def test_sync_wrong_json_types_return_errors_instead_of_raising(self):
        malformed = [None, [], "not-an-object", 7]
        for field, value in (("scope", "not-an-object"), ("sources", {}),
                             ("sources", ["not-an-object"]), ("operations", [None])):
            item = plan()
            item[field] = value
            malformed.append(item)
        for field, value in (("base", "not-an-object"), ("after", []),
                             ("source_ids", [{}]), ("depends_on", [{}]),
                             ("operation_id", []), ("idempotency_key", {})):
            item = plan()
            item["operations"][0][field] = value
            if field == "after":
                item["operations"][0]["action"] = "create"
                item["operations"][0]["object_id"] = None
            malformed.append(item)
        item = plan()
        item["sources"][0]["id"] = []
        malformed.append(item)
        for index, item in enumerate(malformed):
            with self.subTest(index=index):
                errors = sync.validate_plan(item)
                self.assertIsInstance(errors, list)
                self.assertTrue(errors)
                self.assertTrue(all(isinstance(error, str) for error in errors))

    def test_brief_nested_wrong_types_are_validation_errors_in_every_copy(self):
        malformed = [None, [], "not-an-object", 7]
        for field, value in (("project", "bad"), ("coverage", []),
                             ("sources", {}), ("sources", ["bad"]),
                             ("decisions", ["bad"]), ("risks", None)):
            item = brief()
            item[field] = value
            malformed.append(item)
        item = brief()
        item["project"]["period"] = "bad"
        malformed.append(item)
        for field, value in (("source_ids", [{}]), ("status", []), ("owner", {}),
                             ("due", 0), ("id", [])):
            item = brief()
            item["actions"][0][field] = value
            malformed.append(item)
        item = brief()
        item["sources"][0]["id"] = []
        malformed.append(item)
        for skill, _ in SKILLS.values():
            for index, item in enumerate(malformed):
                with self.subTest(skill=skill, index=index):
                    with self.assertRaises(ValueError):
                        validator(skill)(copy.deepcopy(item))

    def test_missing_optional_sections_are_normalized_without_mutating_input(self):
        for skill, _ in SKILLS.values():
            for absent in ("summary", "actions", "decisions", "risks"):
                with self.subTest(skill=skill, absent=absent):
                    data = brief()
                    del data[absent]
                    original = copy.deepcopy(data)
                    normalized = validator(skill)(data)
                    self.assertEqual(normalized[absent], [])
                    self.assertEqual(data, original)
            data = brief()
            for section in ("summary", "actions", "decisions", "risks", "sources"):
                del data[section]
            normalized = validator(skill)(data)
            self.assertTrue(all(normalized[section] == [] for section in
                                ("summary", "actions", "decisions", "risks", "sources")))

    def test_omitted_optional_row_fields_have_consistent_unknown_defaults(self):
        for skill, _ in SKILLS.values():
            with self.subTest(skill=skill):
                data = brief()
                for section in ("actions", "decisions", "risks"):
                    del data[section][0]["status"]
                del data["actions"][0]["owner"]
                del data["actions"][0]["due"]
                original = copy.deepcopy(data)
                normalized = validator(skill)(data)
                for section in ("actions", "decisions", "risks"):
                    self.assertEqual(normalized[section][0]["status"], "unknown")
                self.assertIsNone(normalized["actions"][0]["owner"])
                self.assertIsNone(normalized["actions"][0]["due"])
                self.assertEqual(data, original)

    def test_explicit_null_optional_sections_are_rejected_consistently(self):
        for skill, _ in SKILLS.values():
            for section in ("summary", "actions", "decisions", "risks", "sources"):
                with self.subTest(skill=skill, section=section):
                    data = brief()
                    data[section] = None
                    with self.assertRaises(ValueError):
                        validator(skill)(data)

    def test_as_of_before_window_is_rejected_in_every_copy(self):
        for skill, _ in SKILLS.values():
            with self.subTest(skill=skill):
                data = brief()
                data["project"]["data_as_of"] = "2026-11-17T08:59:59+02:00"
                with self.assertRaises(ValueError):
                    validator(skill)(data)

    def test_source_time_cannot_exceed_evidence_cutoff_but_older_context_is_valid(self):
        for skill, _ in SKILLS.values():
            with self.subTest(skill=skill):
                data = brief()
                data["sources"][0]["timestamp"] = "2026-11-17T09:15:01Z"
                with self.assertRaises(ValueError):
                    validator(skill)(data)
                data["sources"][0]["timestamp"] = "2026-11-17T09:15:00Z"
                self.assertEqual(validator(skill)(copy.deepcopy(data)), data)
                data["sources"][0]["timestamp"] = "2026-11-16T09:00:00+02:00"
                self.assertEqual(validator(skill)(copy.deepcopy(data)), data)
                data["sources"][0]["timestamp"] = None
                self.assertEqual(validator(skill)(copy.deepcopy(data)), data)

    def test_partial_window_requires_partial_coverage_but_can_render_known_context(self):
        for skill, _ in SKILLS.values():
            with self.subTest(skill=skill):
                data = brief()
                data["project"]["data_as_of"] = "2026-11-17T10:45:00+02:00"
                data["coverage"]["note"] = "Read through 10:45; the requested 10:45-11:00 tail is not covered."
                self.assertEqual(validator(skill)(copy.deepcopy(data)), data)
                data["coverage"]["status"] = "complete_capture_not_asserted"
                with self.assertRaises(ValueError):
                    validator(skill)(data)

    def test_approved_always_requires_a_real_reference_field_even_in_propose(self):
        for mode in ("propose", "execute"):
            for authorization in (None, "", "   ", True, {}):
                with self.subTest(mode=mode, authorization=authorization):
                    data = plan()
                    data["mode"] = mode
                    data["operations"][0].update(state="approved", authorization_reference=authorization)
                    self.assertTrue(sync.validate_plan(data))
            data = plan()
            data["mode"] = mode
            data["operations"][0].update(state="approved", authorization_reference="synthetic-scoped-user-request")
            self.assertEqual(sync.validate_plan(data), [])

    def test_exact_identity_receipt_and_ledger_types_cannot_pass_as_executable_structure(self):
        for field, value in (("object_id", 1.5), ("object_id", True),
                             ("external_receipt", "not-an-object"),
                             ("external_business_key", {"unresolved": "mapping"})):
            with self.subTest(field=field, value=value):
                data = plan()
                data["mode"] = "execute"
                data["operations"][0].update(state="approved", authorization_reference="synthetic-grant")
                data["operations"][0][field] = value
                self.assertTrue(sync.validate_plan(data))
        data = plan()
        data["operations"][0].update(action="create", object_id=None)
        data["operations"][0]["after"]["external_business_key"] = {"missing": "resolved-value"}
        self.assertTrue(sync.validate_plan(data))
        data = plan()
        data["ledger_reference"] = {}
        self.assertTrue(sync.validate_plan(data))
        data["ledger_reference"] = "synthetic-ledger@revision-2"
        self.assertEqual(sync.validate_plan(data), [])

    def test_stale_base_fields_need_real_types_and_sha256_format(self):
        for base in ({"version": "   "}, {"etag": 3}, {"snapshot_sha256": "not-a-fingerprint"},
                     {"snapshot_sha256": True}, {"snapshot_sha256": "g" * 64}):
            with self.subTest(base=base):
                data = plan()
                data["operations"][0]["base"] = base
                self.assertTrue(sync.validate_plan(data))
        for base in ({"version": 0}, {"etag": '"synthetic-v4"'}, {"snapshot_sha256": "A" * 64}):
            data = plan()
            data["operations"][0]["base"] = base
            self.assertEqual(sync.validate_plan(data), [])

    def test_independent_execution_batch_preserves_full_unknown_outcome_ledger(self):
        ledger = plan()
        ledger["operations"][0].update(
            state="outcome_unknown", external_receipt={"request_id": "demo-uncertain-write"})
        independent = add_second_operation(ledger)
        independent.update(state="approved", authorization_reference="synthetic-user-grant-OP2")
        original = json.dumps(ledger, sort_keys=True)
        self.assertEqual(sync.validate_plan(ledger), [])
        mixed_execution = copy.deepcopy(ledger)
        mixed_execution["mode"] = "execute"
        self.assertTrue(sync.validate_plan(mixed_execution))
        batch = copy.deepcopy(ledger)
        batch.update(mode="execute", ledger_reference="demo-ledger.json@revision-3")
        batch["operations"] = [copy.deepcopy(independent)]
        self.assertEqual(sync.validate_plan(batch), [])
        self.assertEqual(batch["operations"][0]["operation_id"], independent["operation_id"])
        self.assertEqual(batch["operations"][0]["idempotency_key"], independent["idempotency_key"])
        self.assertEqual(json.dumps(ledger, sort_keys=True), original)
        self.assertEqual(ledger["operations"][0]["state"], "outcome_unknown")
        batch["operations"][0]["depends_on"] = ["OP1"]
        self.assertTrue(sync.validate_plan(batch))


class ReviewCLIRegressions(unittest.TestCase):
    def call_helper(self, script, data, syntax_error=False, raw_text=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        source = directory / "input.json"
        source.write_text(raw_text if raw_text is not None else ("{" if syntax_error else json.dumps(data, ensure_ascii=False)), encoding="utf-8")
        command = [sys.executable, "-B", "-X", "utf8", str(script), "--input", str(source)]
        if script != SYNC_SCRIPT:
            command += ["--output", str(directory / ("video" if script.name == "build_video.py" else "artifact.html"))]
        process = subprocess.run(command, cwd=directory, capture_output=True, text=True,
                                 encoding="utf-8", timeout=30)
        return process, directory

    def assert_clean_error(self, process):
        self.assertNotEqual(process.returncode, 0)
        self.assertNotIn("Traceback", process.stdout + process.stderr)
        response = json.loads(process.stdout)
        self.assertIs(response["valid"], False)
        self.assertIsInstance(response["errors"], list)
        self.assertTrue(response["errors"])

    def test_sync_cli_returns_json_errors_for_malformed_syntax_and_types(self):
        for data, syntax_error in ((None, True), (None, False), ({"scope": "bad"}, False)):
            with self.subTest(data=data, syntax_error=syntax_error):
                process, _ = self.call_helper(SYNC_SCRIPT, data, syntax_error)
                self.assert_clean_error(process)
                self.assertEqual(json.loads(process.stdout)["remote_writes"], 0)

    def test_renderer_clis_return_json_errors_without_creating_an_artifact(self):
        for skill, filename in SKILLS.values():
            script = ROOT / "skills" / skill / "scripts" / filename
            for data, syntax_error in ((None, True), (None, False), ({"project": "bad"}, False)):
                with self.subTest(skill=skill, data=data, syntax_error=syntax_error):
                    process, directory = self.call_helper(script, data, syntax_error)
                    self.assert_clean_error(process)
                    self.assertFalse((directory / "artifact.html").exists())
                    self.assertFalse((directory / "video").exists())

    def test_excessively_nested_json_is_a_clean_cli_error(self):
        deep = "[" * 2000 + "0" + "]" * 2000
        scripts = [SYNC_SCRIPT] + [ROOT / "skills" / skill / "scripts" / filename
                                  for skill, filename in SKILLS.values()]
        for script in scripts:
            with self.subTest(script=script):
                process, directory = self.call_helper(script, None, raw_text=deep)
                self.assert_clean_error(process)
                self.assertFalse((directory / "artifact.html").exists())
                self.assertFalse((directory / "video").exists())

    def test_missing_risks_is_safe_in_actual_dashboard_deck_and_video_clis(self):
        data = brief()
        del data["risks"]
        for skill, filename in SKILLS.values():
            with self.subTest(skill=skill):
                process, directory = self.call_helper(ROOT / "skills" / skill / "scripts" / filename, data)
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                artifact = directory / ("video/index.html" if filename == "build_video.py" else "artifact.html")
                self.assertTrue(artifact.is_file())
                if filename == "build_video.py":
                    normalized = json.loads((directory / "video/brief.json").read_text(encoding="utf-8"))
                    self.assertEqual(normalized["risks"], [])


if __name__ == "__main__":
    unittest.main()
