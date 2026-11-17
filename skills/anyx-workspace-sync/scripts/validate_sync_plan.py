"""Validate a source-backed sync plan. This helper never writes to a remote system."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def stable_identifier(value):
    """Destination IDs/business-key values are exact strings or integers."""
    return nonempty_text(value) or type(value) is int


def validate_plan(plan):
    """Return structural errors for any parsed JSON value, never execute it."""
    if not isinstance(plan, dict):
        return ["Plan must be a JSON object"]
    errors = []
    if type(plan.get("schema_version")) is not int or plan["schema_version"] != 1 or plan.get("mode") not in ("propose", "execute"):
        errors.append("schema_version=1 and mode propose|execute required")
    scope = plan.get("scope")
    if not isinstance(scope, dict) or not nonempty_text(scope.get("project_id")):
        errors.append("Explicit project scope object required")
    if plan.get("ledger_reference") is not None and not nonempty_text(plan["ledger_reference"]):
        errors.append("ledger_reference must be a nonempty string or null")
    sources = plan.get("sources", [])
    source_ids = set()
    if not isinstance(sources, list):
        errors.append("sources must be a list of JSON objects")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"sources[{index}] must be a JSON object")
                continue
            source_id = source.get("id")
            if not nonempty_text(source_id) or not re.fullmatch(r"[A-Za-z0-9_-]+", source_id):
                errors.append(f"sources[{index}] needs a safe string id")
            elif source_id in source_ids:
                errors.append("Source IDs must be unique")
            else:
                source_ids.add(source_id)
            if not nonempty_text(source.get("system")) or not nonempty_text(source.get("reference")):
                errors.append(f"sources[{index}] needs system and reference strings")
    operations = plan.get("operations", [])
    if not isinstance(operations, list) or not 1 <= len(operations) <= 100 or any(not isinstance(op, dict) for op in operations):
        return errors + ["Operations must be a list of 1..100 objects"]
    ids = [op.get("operation_id") for op in operations]
    valid_ids = [value for value in ids if isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]+", value)]
    if len(valid_ids) != len(ids) or len(valid_ids) != len(set(valid_ids)):
        errors.append("Bounded unique safe operation IDs required")
    keys = [op.get("idempotency_key") for op in operations]
    valid_keys = [value for value in keys if nonempty_text(value)]
    if len(valid_keys) != len(keys) or len(valid_keys) != len(set(valid_keys)):
        errors.append("Every operation needs a distinct stable idempotency key")
    known = set(valid_ids)
    edges = {}
    by_id = {op["operation_id"]: op for op in operations if isinstance(op.get("operation_id"), str)}
    for index, op in enumerate(operations):
        prefix = op["operation_id"] if isinstance(op.get("operation_id"), str) else f"operations[{index}]"
        for key in ("system", "account_identifier", "object_type", "authority"):
            if not nonempty_text(op.get(key)):
                errors.append(f"{prefix}: missing string {key}")
        action = op.get("action")
        if action not in ("create", "update"):
            errors.append(f"{prefix}: only scoped create/update plans supported")
        object_id = op.get("object_id")
        if object_id is not None and not stable_identifier(object_id):
            errors.append(f"{prefix}: object_id must be an exact string or integer")
        if action == "update" and not stable_identifier(object_id):
            errors.append(f"{prefix}: updates need exact external object_id")
        for key in ("external_business_key", "business_key"):
            if op.get(key) is not None and not stable_identifier(op[key]):
                errors.append(f"{prefix}: {key} must be an exact string or integer")
        before, after = op.get("before"), op.get("after")
        if not isinstance(before, dict) or not isinstance(after, dict):
            errors.append(f"{prefix}: before/after fields must be JSON objects")
        else:
            if before == after:
                errors.append(f"{prefix}: no-op should be omitted")
            if after.get("external_business_key") is not None and not stable_identifier(after["external_business_key"]):
                errors.append(f"{prefix}: after.external_business_key must be an exact string or integer")
            if action == "create" and not any(stable_identifier(value) for value in
                    (object_id, op.get("external_business_key"), op.get("business_key"), after.get("external_business_key"))):
                errors.append(f"{prefix}: create needs stable external_business_key")
        base = op.get("base")
        if not isinstance(base, dict):
            errors.append(f"{prefix}: base must be a JSON object")
        else:
            present = False
            for key in ("version", "etag", "snapshot_sha256"):
                value = base.get(key)
                if value is None or value == "":
                    continue
                valid = stable_identifier(value) if key == "version" else nonempty_text(value)
                if key == "snapshot_sha256":
                    valid = isinstance(value, str) and re.fullmatch(r"[a-fA-F0-9]{64}", value) is not None
                if not valid:
                    errors.append(f"{prefix}: invalid base.{key} type or format")
                else:
                    present = True
            if not present:
                errors.append(f"{prefix}: stale-write guard missing")
        refs = op.get("source_ids")
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in source_ids for ref in refs):
            errors.append(f"{prefix}: source_ids must be a list of resolved IDs")
        deps = op.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(dep, str) for dep in deps):
            errors.append(f"{prefix}: depends_on must be a list of operation IDs")
            deps = []
        edges[prefix] = deps
        if any(dep not in known or dep == prefix for dep in deps):
            errors.append(f"{prefix}: invalid dependency")
        state = op.get("state")
        if state not in ("proposed", "approved", "submitted", "outcome_unknown", "verified"):
            errors.append(f"{prefix}: invalid reconciliation state")
        authorization = op.get("authorization_reference")
        if authorization is not None and not nonempty_text(authorization):
            errors.append(f"{prefix}: authorization_reference must be a nonempty string or null")
        if state == "approved" and not nonempty_text(authorization):
            errors.append(f"{prefix}: approved state requires authorization_reference in every mode")
        if op.get("external_receipt") is not None and not isinstance(op["external_receipt"], dict):
            errors.append(f"{prefix}: external_receipt must be an object or null")
        if state in ("submitted", "verified") and (not isinstance(op.get("external_receipt"), dict) or not op["external_receipt"]):
            errors.append(f"{prefix}: submitted/verified needs a nonempty receipt object")
        if plan.get("mode") == "execute":
            if state != "verified" and (state != "approved" or not nonempty_text(authorization)):
                errors.append(f"{prefix}: execute requires approved state and authorization_reference")
            if state == "outcome_unknown":
                errors.append(f"{prefix}: unknown prior outcome blocks retry")
            for dep in deps:
                if by_id.get(dep, {}).get("state") != "verified":
                    errors.append(f"{prefix}: dependency has no verified outcome")
    visiting, visited = set(), set()
    def walk(node):
        if node in visiting:
            errors.append("Dependency cycle blocks ordered execution")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in edges.get(node, []):
            walk(dep)
        visiting.remove(node)
        visited.add(node)
    for node in edges:
        walk(node)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 1024 * 1024:
            raise ValueError("Plan exceeds 1 MiB")
        errors = validate_plan(json.loads(path.read_text(encoding="utf-8")))
    except (ValueError, OSError, RecursionError) as error:
        errors = [str(error)]
    print(json.dumps({"valid": not errors, "errors": errors, "remote_writes": 0,
                      "authorization_verified_by_helper": False}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
