"""Plan guard tests only; this validator has no live connector or write authority."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "anyx-workspace-sync" / "scripts" / "validate_sync_plan.py"
spec = importlib.util.spec_from_file_location("sync_plan_under_test", SCRIPT)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def plan():
    return {
        "schema_version": 1, "mode": "propose",
        "scope": {"project_id": "QA-9", "description": "Review one synthetic project note."},
        "sources": [{"id": "Q1", "system": "Anyx synthetic replay",
                     "reference": "demo-group / demo-record-9 / 2026-11-17T10:00:00Z"}],
        "operations": [{
            "operation_id": "OP1", "system": "Synthetic PM", "account_identifier": "demo-tenant",
            "object_type": "project", "object_id": "demo-project-9", "action": "update",
            "before": {"internal_note": "Scope awaiting review."},
            "after": {"internal_note": "Scope withdrawn pending a new approval."},
            "source_ids": ["Q1"], "authority": "Synthetic project approver's captured withdrawal.",
            "base": {"etag": '"demo-v3"'}, "authorization_reference": None,
            "idempotency_key": "demo-QA9-note-revision1", "depends_on": [],
            "state": "proposed", "external_receipt": None,
        }],
    }


def add_second_operation(data):
    second = copy.deepcopy(data["operations"][0])
    second.update(operation_id="OP2", object_id="demo-project-10",
                  idempotency_key="demo-QA9-note-revision2")
    data["operations"].append(second)
    return second


class SyncPlanChecks(unittest.TestCase):
    def test_proposal_needs_no_execution_grant_and_validation_is_repeatable(self):
        data = plan()
        original = copy.deepcopy(data)
        self.assertEqual(sync.validate_plan(data), [])
        self.assertEqual(sync.validate_plan(data), [])
        self.assertEqual(data, original)

    def test_execute_requires_approved_state_and_authorization_reference(self):
        data = plan()
        data["mode"] = "execute"
        self.assertTrue(sync.validate_plan(data))
        data["operations"][0]["state"] = "approved"
        self.assertTrue(sync.validate_plan(data))
        data["operations"][0]["authorization_reference"] = "synthetic-user-grant-for-OP1"
        self.assertEqual(sync.validate_plan(data), [])

    def test_uncertain_or_submitted_operation_cannot_be_replayed_by_execute(self):
        for state in ("outcome_unknown", "submitted"):
            with self.subTest(state=state):
                data = plan()
                data["mode"] = "execute"
                data["operations"][0].update(
                    state=state, authorization_reference="synthetic-user-grant-for-OP1",
                    external_receipt={"request_id": "demo-request-1", "outcome": "not-yet-verified"},
                )
                self.assertTrue(sync.validate_plan(data))

    def test_stable_idempotency_keys_are_required_and_distinct_per_operation(self):
        data = plan()
        data["operations"][0]["idempotency_key"] = None
        self.assertTrue(sync.validate_plan(data))
        data = plan()
        second = add_second_operation(data)
        second["idempotency_key"] = data["operations"][0]["idempotency_key"]
        self.assertTrue(sync.validate_plan(data))
        second["idempotency_key"] = "demo-OP2-intention-1"
        self.assertEqual(sync.validate_plan(data), [])

    def test_dependency_must_exist_be_acyclic_and_be_verified_before_execution(self):
        data = plan()
        second = add_second_operation(data)
        second["depends_on"] = ["does-not-exist"]
        self.assertTrue(sync.validate_plan(data))
        second["depends_on"] = ["OP1"]
        data["operations"][0]["depends_on"] = ["OP2"]
        self.assertTrue(sync.validate_plan(data))
        data["operations"][0]["depends_on"] = []
        data["mode"] = "execute"
        for operation in data["operations"]:
            operation.update(state="approved", authorization_reference="synthetic-scoped-user-grant")
        self.assertTrue(sync.validate_plan(data))
        data["operations"][0].update(
            state="verified", external_receipt={"object_id": "demo-project-9", "request_id": "demo-write-1",
                                                "verified_at": "2026-11-17T12:00:00Z"},
        )
        self.assertEqual(sync.validate_plan(data), [])

    def test_self_dependency_is_rejected(self):
        data = plan()
        data["operations"][0]["depends_on"] = ["OP1"]
        self.assertTrue(sync.validate_plan(data))

    def test_stale_write_guard_requires_a_recorded_base_not_just_target_id(self):
        for base in ({}, {"version": None, "etag": "", "snapshot_sha256": None}):
            with self.subTest(base=base):
                data = plan()
                data["operations"][0]["base"] = base
                self.assertTrue(sync.validate_plan(data))
        for base in ({"version": 0}, {"etag": '"demo-v1"'}, {"snapshot_sha256": "a" * 64}):
            with self.subTest(base=base):
                data = plan()
                data["operations"][0]["base"] = base
                self.assertEqual(sync.validate_plan(data), [])

    def test_verified_state_requires_an_evidence_object_not_a_truthy_placeholder(self):
        for receipt in (None, True, "looks done"):
            with self.subTest(receipt=receipt):
                data = plan()
                data["operations"][0].update(state="verified", external_receipt=receipt)
                self.assertTrue(sync.validate_plan(data))

    def test_updates_require_exact_ids_and_creates_require_a_stable_business_key(self):
        data = plan()
        operation = data["operations"][0]
        operation["object_id"] = None
        self.assertTrue(sync.validate_plan(data))
        operation["action"] = "create"
        self.assertTrue(sync.validate_plan(data))
        operation["after"]["external_business_key"] = "demo-QA9-project-note"
        self.assertEqual(sync.validate_plan(data), [])

    def test_unresolved_evidence_noops_and_unsupported_mutations_are_rejected(self):
        for change in ("unknown-source", "no-op", "delete"):
            with self.subTest(change=change):
                data = plan()
                operation = data["operations"][0]
                if change == "unknown-source":
                    operation["source_ids"] = ["unknown"]
                elif change == "no-op":
                    operation["after"] = copy.deepcopy(operation["before"])
                else:
                    operation["action"] = "delete"
                self.assertTrue(sync.validate_plan(data))

    def test_cli_validation_never_claims_authority_or_modifies_the_plan(self):
        data = plan()
        data["mode"] = "execute"
        data["operations"][0].update(state="approved", authorization_reference="synthetic-user-grant")
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "plan.json"
            source.write_text(json.dumps(data), encoding="utf-8")
            original = source.read_bytes()
            process = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(SCRIPT), "--input", str(source)],
                cwd=temporary, capture_output=True, text=True, encoding="utf-8", timeout=15,
            )
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            result = json.loads(process.stdout)
            self.assertIs(result["valid"], True)
            self.assertEqual(result["remote_writes"], 0)
            self.assertIs(result["authorization_verified_by_helper"], False)
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
