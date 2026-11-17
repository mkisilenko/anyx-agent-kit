"""Contract checks for the offline fixture adapter, not live Anyx integration tests."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from replay_mcp import ReplaySession


class ReplayChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.case = ROOT / "evals/scenarios/team-catchup.json"
        self.session = ReplaySession(self.case, Path(self.temp.name) / "state.json")

    def tearDown(self):
        self.temp.cleanup()

    def ready(self):
        self.session.call("get_status")
        first = self.session.call("list_groups")["structuredContent"]
        second = self.session.call("list_groups", {"cursor": first["next_cursor"]})["structuredContent"]
        return second["groups"][0]["group_id"]

    def test_status_and_returned_group_required(self):
        self.assertTrue(self.session.call("list_groups")["isError"])
        self.session.call("get_status")
        self.assertTrue(self.session.call("get_group_messages", {"group_id": "invented"})["isError"])

    def test_short_group_page_is_not_completion(self):
        self.session.call("get_status")
        first = self.session.call("list_groups")["structuredContent"]
        self.assertEqual(len(first["groups"]), 1)
        self.assertIsNotNone(first["next_cursor"])
        second = self.session.call("list_groups", {"cursor": first["next_cursor"]})["structuredContent"]
        self.assertIsNone(second["next_cursor"])

    def test_text_recovery_uses_utf8_byte_offsets_and_matching_reference(self):
        group = self.ready()
        ref_key, ref = next(iter(self.session.scenario["references"].items()))
        args = {"group_id": group, "record_id": ref["record_id"], "reference": ref_key, "limit": 17}
        chunks, offset = [], 0
        for _ in range(100):
            response = self.session.call("get_message_content", {**args, "offset": offset})
            self.assertFalse(response["isError"])
            data = response["structuredContent"]
            chunks.append(data["text"])
            if data["complete"]:
                break
            self.assertGreater(data["next_offset"], offset)
            offset = data["next_offset"]
        else:
            self.fail("Text recovery did not complete")
        actual = "".join(chunks)
        self.assertEqual(actual, ref["text"])
        self.assertEqual(data["sha256"], hashlib.sha256(actual.encode()).hexdigest())
        self.assertTrue(self.session.call("get_message_content", {**args, "record_id": "wrong"})["isError"])

    def test_invalid_utf8_offset_and_unexposed_argument_rejected(self):
        group = self.ready()
        ref_key, ref = next(iter(self.session.scenario["references"].items()))
        self.assertTrue(self.session.call("get_message_content", {
            "group_id": group, "record_id": ref["record_id"], "reference": ref_key,
            "offset": 1})["isError"])
        self.assertTrue(self.session.call("get_group_messages", {
            "group_id": group, "send_to": "external"})["isError"])

    def test_fixture_restart_keeps_call_state_and_case_binding(self):
        self.ready()
        reloaded = ReplaySession(self.case, self.session.state_path)
        self.assertEqual(len(reloaded.state["calls"]), 3)
        other = ROOT / "evals/scenarios/materials-review.json"
        with self.assertRaises(ValueError):
            ReplaySession(other, self.session.state_path)

    def test_message_cursor_and_reference_content_are_retained(self):
        group = self.ready()
        first = self.session.call("get_group_messages", {"group_id": group})["structuredContent"]
        self.assertIsNotNone(first["next_cursor"])
        last = self.session.call("get_group_messages", {"group_id": group,
                                 "cursor": first["next_cursor"]})["structuredContent"]
        self.assertIsNone(last["next_cursor"])
        self.assertIn("content_reference", last["messages"][-1])


if __name__ == "__main__":
    unittest.main()

