"""Validate a source-backed sync plan. This helper never writes to a remote system."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

def validate_plan(plan):
    errors=[]
    if plan.get("schema_version")!=1 or plan.get("mode") not in ("propose","execute"):
        errors.append("schema_version=1 and mode propose|execute required")
    if not plan.get("scope",{}).get("project_id"):
        errors.append("Explicit project scope required")
    source_ids={s.get("id") for s in plan.get("sources",[]) if s.get("id")}
    operations=plan.get("operations",[])
    if not isinstance(operations,list) or not 1<=len(operations)<=100 or any(not isinstance(o,dict) for o in operations):
        return errors+["Operations must be a list of 1..100 objects"]
    ids=[o.get("operation_id") for o in operations]
    if not operations or len(ids)!=len(set(ids)) or any(not isinstance(i,str) or not re.fullmatch(r"[A-Za-z0-9_-]+",i) for i in ids):
        errors.append("Bounded unique safe operation IDs required")
    keys=[o.get("idempotency_key") for o in operations]
    if any(not key for key in keys) or len(keys)!=len(set(keys)):
        errors.append("Every operation needs a distinct stable idempotency key")
    known=set(ids)
    edges={}
    for op in operations:
        prefix=str(op.get("operation_id"))
        for key in ("system","account_identifier","object_type","authority"):
            if not op.get(key):
                errors.append(f"{prefix}: missing {key}")
        action=op.get("action")
        if action not in ("create","update"):
            errors.append(f"{prefix}: only scoped create/update plans supported")
        if action=="update" and not op.get("object_id"):
            errors.append(f"{prefix}: updates need exact external object_id")
        if action=="create" and not op.get("object_id") and not (op.get("external_business_key") or op.get("business_key") or op.get("after",{}).get("external_business_key")):
            errors.append(f"{prefix}: create needs stable external_business_key")
        if not isinstance(op.get("before"),dict) or not isinstance(op.get("after"),dict):
            errors.append(f"{prefix}: before/after fields required")
        if op.get("before")==op.get("after"):
            errors.append(f"{prefix}: no-op should be omitted")
        base=op.get("base",{})
        if not any(base.get(k) is not None and base.get(k)!="" for k in ("version","etag","snapshot_sha256")):
            errors.append(f"{prefix}: stale-write guard missing")
        refs=op.get("source_ids",[])
        if not refs or any(ref not in source_ids for ref in refs):
            errors.append(f"{prefix}: source_ids must resolve")
        deps=op.get("depends_on",[])
        edges[prefix]=deps
        if any(dep not in known or dep==prefix for dep in deps):
            errors.append(f"{prefix}: invalid dependency")
        state=op.get("state")
        if state not in ("proposed","approved","submitted","outcome_unknown","verified"):
            errors.append(f"{prefix}: invalid reconciliation state")
        if state in ("submitted","verified") and (not isinstance(op.get("external_receipt"),dict) or not op["external_receipt"]):
            errors.append(f"{prefix}: submitted/verified needs actual receipt")
        if plan.get("mode")=="execute":
            if state!="verified" and (state!="approved" or not op.get("authorization_reference")):
                errors.append(f"{prefix}: execute requires approved state and matching user grant")
            if state=="outcome_unknown":
                errors.append(f"{prefix}: unknown prior outcome blocks retry")
            for dep in deps:
                parent=next((x for x in operations if x.get("operation_id")==dep),{})
                if parent.get("state")!="verified":
                    errors.append(f"{prefix}: dependency has no verified outcome")
    visiting,visited=set(),set()
    def walk(node):
        if node in visiting:
            errors.append("Dependency cycle blocks ordered execution")
            return
        if node in visited:return
        visiting.add(node)
        for dep in edges.get(node,[]):walk(dep)
        visiting.remove(node);visited.add(node)
    for node in edges:walk(node)
    return errors

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",required=True)
    args=parser.parse_args()
    path=Path(args.input)
    if path.stat().st_size>1024*1024:raise ValueError("Plan exceeds 1 MiB")
    errors=validate_plan(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps({"valid":not errors,"errors":errors,"remote_writes":0,"authorization_verified_by_helper":False},indent=2))
    raise SystemExit(1 if errors else 0)

