"""Offline synthetic fixture replay, not an MCP transport or Anyx API client."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path


class FixtureError(ValueError):
    pass


class ReplaySession:
    def __init__(self, scenario: Path | str, state: Path | str):
        self.scenario = json.loads(Path(scenario).read_text(encoding="utf-8"))
        if self.scenario.get("synthetic") is not True:
            raise FixtureError("Only explicitly synthetic scenarios are allowed")
        self.state_path = Path(state)
        self.state = (
            json.loads(self.state_path.read_text(encoding="utf-8"))
            if self.state_path.exists()
            else {"case_id": self.scenario["case_id"], "status_read": False,
                  "seen_groups": [], "calls": []}
        )
        if self.state["case_id"] != self.scenario["case_id"]:
            raise FixtureError("State belongs to a different scenario")

    def call(self, tool: str, arguments: dict | None = None) -> dict:
        args = arguments or {}
        try:
            result = self._read(tool, args)
            response = {"fixture_only": True, "isError": False,
                        "structuredContent": copy.deepcopy(result)}
        except FixtureError as error:
            response = {"fixture_only": True, "isError": True,
                        "structuredContent": {"error": "fixture_contract_error",
                                              "message": str(error)}}
        self.state["calls"].append({"tool": tool, "arguments": args,
                                    "isError": response["isError"]})
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
        return response

    def _read(self, tool: str, args: dict) -> dict:
        schema = self.scenario["available_tools"]
        if tool not in schema:
            raise FixtureError("Tool is not exposed by this fixture client")
        if set(args) - set(schema[tool]):
            raise FixtureError("Argument is not exposed by this fixture client")
        if tool == "get_status":
            self.state["status_read"] = True
            return self.scenario["status"]
        if not self.state["status_read"]:
            raise FixtureError("Call get_status first")
        if tool == "list_groups":
            for page in self.scenario["group_pages"]:
                if page["cursor"] == args.get("cursor"):
                    result = page["result"]
                    seen = set(self.state["seen_groups"])
                    seen.update(group["group_id"] for group in result["groups"])
                    self.state["seen_groups"] = sorted(seen)
                    return result
            raise FixtureError("Unknown group cursor")
        group_id = args.get("group_id")
        if group_id not in self.state["seen_groups"]:
            raise FixtureError("Use a group_id actually returned by list_groups")
        if tool == "get_group_messages":
            for page in self.scenario["message_pages"]:
                if page["group_id"] == group_id and page["cursor"] == args.get("cursor"):
                    return page["result"]
            raise FixtureError("Unknown message cursor or group")
        if tool == "get_message_content":
            ref = self.scenario["references"].get(args.get("reference"))
            if not ref or ref["group_id"] != group_id or ref["record_id"] != args.get("record_id"):
                raise FixtureError("Reference must match its group and stored record")
            raw = ref["text"].encode("utf-8")
            offset, limit = args.get("offset", 0), args.get("limit", 65536)
            if type(offset) is not int or offset < 0 or offset > len(raw):
                raise FixtureError("Invalid UTF-8 byte offset")
            if type(limit) is not int or not 4 <= limit <= 65536:
                raise FixtureError("Chunk limit must be 4..65536")
            try:
                raw[:offset].decode("utf-8")
            except UnicodeDecodeError:
                raise FixtureError("Offset splits a UTF-8 character") from None
            end = min(len(raw), offset + min(limit, ref.get("chunk_bytes", limit)))
            text = raw[offset:end].decode("utf-8", errors="ignore")
            next_offset = offset + len(text.encode("utf-8"))
            if next_offset == offset and offset < len(raw):
                raise FixtureError("Chunk cannot advance")
            complete = next_offset == len(raw)
            return {"text": text, "offset": offset,
                    "next_offset": None if complete else next_offset,
                    "complete": complete, "total_utf8_bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest()}
        raise FixtureError("Unsupported fixture tool")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--tool")
    parser.add_argument("--arguments", default="{}")
    parser.add_argument("--arguments-file", type=Path)
    parser.add_argument("--describe", action="store_true")
    options = parser.parse_args()
    session = ReplaySession(options.scenario, options.state)
    if options.describe:
        print(json.dumps({key: session.scenario[key] for key in
                          ("case_id", "synthetic", "description", "skill",
                           "user_request", "timezone", "available_tools")},
                         ensure_ascii=False, indent=2))
        return
    if not options.tool:
        parser.error("--tool is required unless --describe is used")
    args = json.loads(options.arguments_file.read_text(encoding="utf-8")
                      if options.arguments_file else options.arguments)
    result = session.call(options.tool, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result["isError"] else 0)


if __name__ == "__main__":
    main()

