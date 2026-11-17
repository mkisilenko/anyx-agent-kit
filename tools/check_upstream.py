"""Opt-in public documentation drift check. Never rewrites skills or publishes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "mcp-tools": "https://raw.githubusercontent.com/mkisilenko/docs/main/developers/mcp-tools.mdx",
    "mcp-quickstart": "https://raw.githubusercontent.com/mkisilenko/docs/main/developers/mcp-quickstart.mdx",
}


def check() -> tuple[list[dict], int]:
    baseline = json.loads((ROOT / "docs/upstream-sources.json").read_text(encoding="utf-8"))
    results, code = [], 0
    for source in baseline["sources"]:
        expected_url = ALLOWED.get(source["id"])
        if expected_url != source["url"]:
            raise ValueError("Unexpected upstream URL; review source configuration")
        try:
            request = Request(expected_url, headers={"User-Agent": "AnyxAgentKit-source-check/0.1"})
            with urlopen(request, timeout=20) as response:
                content = response.read(1024 * 1024 + 1)
            if len(content) > 1024 * 1024:
                raise ValueError("Source exceeds 1 MiB read budget")
            digest = hashlib.sha256(content).hexdigest()
            changed = digest != source["sha256"]
            results.append({"source": source["id"], "changed": changed,
                            "current_sha256": digest, "action": "review" if changed else "none"})
            if changed:
                code = max(code, 2)
        except Exception as error:
            results.append({"source": source["id"], "status": "unverified",
                            "error_type": type(error).__name__})
            code = max(code, 3)
    return results, code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Perform two bounded public HTTP reads")
    options = parser.parse_args()
    if not options.check:
        parser.error("Pass --check to enable network reads")
    results, code = check()
    print(json.dumps({"public_sources": results, "changed_files_written": 0}, indent=2))
    raise SystemExit(code)

