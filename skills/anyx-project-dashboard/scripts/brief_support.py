"""Shared renderer contract, copied locally so each skill is independently installable."""
from __future__ import annotations
from datetime import datetime
import base64
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlparse

SECTIONS = ("summary", "actions", "decisions", "risks")

HEBREW_UI = {
    "Data as of": "המידע נכון ל־",
    "to": "עד",
    "Actions": "פעולות",
    "Action": "פעולה",
    "Status": "מצב",
    "all": "הכול",
    "ID": "מזהה",
    "Owner": "אחראי",
    "Due": "מועד",
    "Evidence": "מקורות",
    "Decisions": "החלטות",
    "Risks and missing checks": "סיכונים ובדיקות חסרות",
    "Sources": "מקורות",
    "actions in this brief": "פעולות בתמצית",
    "risks recorded": "סיכונים שתועדו",
    "source references": "הפניות למקורות",
    "This file is a snapshot and has no live data connection.": "הקובץ מציג תמונת מצב למועד המצוין, ללא חיבור חי למידע.",
    "Prepared with": "הוכן באמצעות",
    "Sharing and publishing require an approved destination.": "שיתוף ופרסום דורשים יעד שאושר.",
    "Project summary": "תמצית הפרויקט",
    "Slide navigation": "ניווט בשקופיות",
    "Previous": "הקודם",
    "Next": "הבא",
    "presentation": "מצגת",
    "Project update": "עדכון פרויקט",
    "Current picture": "תמונת המצב",
    "Decisions and conditions": "החלטות ותנאים",
    "Actions for review": "פעולות לבדיקה",
    "Evidence and coverage": "מקורות וכיסוי המידע",
    "Source registry travels with this video": "רשימת המקורות מצורפת לסרטון",
    "Synthetic demo": "הדגמה בדויה",
    "Private project snapshot": "תמונת מצב פרטית של הפרויקט",
    "Private snapshot": "תמונת מצב פרטית",
    "Captured context, review required": "מידע שנקלט בקבוצה, נדרשת בדיקה",
    "Unassigned": "ללא אחראי",
    "Unknown": "לא ידוע",
    "System": "מערכת",
    "Group ID": "מזהה קבוצה",
    "Record ID": "מזהה רשומה",
    "Timestamp": "חותמת זמן",
    "Open source": "פתיחת המקור",
}

HEBREW_STATUSES = {
    "unknown": "לא ידוע",
    "unassigned": "ללא אחראי",
    "proposed": "הוצע",
    "accepted": "התקבל",
    "confirmed": "אושר",
    "approved": "אושר",
    "conditional": "מותנה",
    "withdrawn": "בוטל",
    "cancelled": "בוטל",
    "canceled": "בוטל",
    "blocked": "חסום",
    "open": "פתוח",
    "resolved": "נפתר",
    "pending": "ממתין",
    "in progress": "בתהליך",
    "completed": "הושלם",
    "reported completed": "דווח כהושלם",
    "authority unconfirmed": "סמכות האישור לא אומתה",
    "disputed": "במחלוקת",
    "superseded": "הוחלף",
    "on hold": "בהשהיה",
    "hold": "בהשהיה",
    "submitted": "הוגש",
    "outcome unknown": "התוצאה אינה ידועה",
    "verified": "אומת",
}


def ui(data, phrase):
    return HEBREW_UI.get(phrase, phrase) if data["language"] == "he" else phrase


def status_label(data, value):
    status = value.strip() if isinstance(value, str) and value.strip() else "unknown"
    if data["language"] == "he":
        key = status.casefold().replace("_", " ").replace("-", " ")
        return HEBREW_STATUSES.get(key, status)
    return status


def item_details(data, item, action=False):
    details = []
    if "status" in item or action:
        details.append(f'{ui(data, "Status")} {status_label(data, item.get("status"))}')
    if action:
        details.append(f'{ui(data, "Owner")} {item.get("owner") or ui(data, "Unassigned")}')
        details.append(f'{ui(data, "Due")} {item.get("due") or ui(data, "Unknown")}')
    return " · ".join(details)


def validate_source_url(value):
    if value is None or value == "":
        return
    if not isinstance(value, str):
        raise ValueError("Source URL must be a string or null")
    url = urlparse(value)
    if url.scheme not in ("https", "http") or not url.netloc or url.username or url.password:
        raise ValueError("Source URL must be ordinary http(s) without credentials")
    credential_keys = {
        "token", "accesstoken", "idtoken", "refreshtoken", "apikey", "signature",
        "authorization", "password", "secret", "clientsecret", "xamzsignature",
        "xamzcredential", "sig",
    }
    fragment = unquote(url.fragment)
    fragment_query = fragment.partition("?")[2] if "?" in fragment else fragment
    for fields in (url.query, fragment_query):
        for key, _ in parse_qsl(fields, keep_blank_values=True):
            normalized = re.sub(r"[^a-z0-9]", "", unquote(key).casefold())
            if normalized in credential_keys:
                raise ValueError("Do not embed credential-bearing URLs")


def timestamp(value, field):
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"{field} needs a timezone")
    return parsed


def validate_brief(data):
    """Validate JSON types and return a normalized brief without mutating input.

    data_as_of is the evidence cutoff, not a promise of capture completeness.
    A requested window extending beyond that cutoff must be explicitly partial.
    """
    # Validate the complete JSON value, including unknown metadata and keys,
    # before any renderer can create a file or output directory.
    try:
        json.dumps(data, ensure_ascii=False).encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        raise ValueError("Brief must contain valid UTF-8 text; unpaired Unicode surrogates are invalid") from None
    except (TypeError, ValueError, RecursionError):
        raise ValueError("Brief must be JSON-serializable") from None

    def object_value(value, field):
        if not isinstance(value, dict):
            raise ValueError(f"{field} must be a JSON object")
        return value

    def nonempty_text(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a nonempty string")
        return value

    object_value(data, "Brief")
    normalized = dict(data)
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1 or type(data.get("synthetic")) is not bool:
        raise ValueError("schema_version=1 and explicit synthetic boolean are required")
    if data.get("language") not in ("en", "he"):
        raise ValueError("language must be en or he")
    project = object_value(data.get("project"), "project")
    nonempty_text(project.get("id"), "project.id")
    title = nonempty_text(project.get("title"), "project.title")
    if len(title) > 120:
        raise ValueError("project.title must be 1..120 characters")
    period = object_value(project.get("period"), "project.period")
    start = timestamp(period.get("start"), "period.start")
    end = timestamp(period.get("end"), "period.end")
    as_of = timestamp(project.get("data_as_of"), "project.data_as_of")
    nonempty_text(period.get("timezone"), "period.timezone")
    if end <= start:
        raise ValueError("Positive bounded period required")
    if as_of < start:
        raise ValueError("project.data_as_of cannot precede period.start")
    coverage = object_value(data.get("coverage"), "coverage")
    if coverage.get("status") not in ("partial", "complete_capture_not_asserted"):
        raise ValueError("Explicit coverage status required")
    nonempty_text(coverage.get("note"), "coverage.note")
    if as_of < end and coverage["status"] != "partial":
        raise ValueError("A window beyond project.data_as_of requires coverage.status=partial")
    sources = data.get("sources", [])
    if not isinstance(sources, list) or any(not isinstance(s, dict) for s in sources):
        raise ValueError("sources must be a list of JSON objects")
    ids = []
    for source in sources:
        source_id = source.get("id")
        if not isinstance(source_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", source_id):
            raise ValueError("Unique safe source IDs required")
        ids.append(source_id)
        nonempty_text(source.get("label"), "source.label")
        nonempty_text(source.get("system"), "source.system")
        for key in ("group_id", "record_id"):
            if source.get(key) is not None and not isinstance(source[key], str):
                raise ValueError(f"source.{key} must be a string or null")
        if source.get("timestamp") is not None:
            source_time = timestamp(source["timestamp"], "source.timestamp")
            if source_time > as_of:
                raise ValueError("source.timestamp cannot follow project.data_as_of")
        validate_source_url(source.get("url"))
    if len(ids) != len(set(ids)):
        raise ValueError("Unique safe source IDs required")
    normalized["sources"] = sources
    known_ids = set(ids)
    for section in SECTIONS:
        rows = data.get(section, [])
        if not isinstance(rows, list) or len(rows) > 40:
            raise ValueError(f"{section} must be a bounded list, maximum 40")
        normalized_rows = []
        for item in rows:
            object_value(item, f"{section} row")
            row = dict(item)
            text = row.get("title" if section == "actions" else "text")
            if not isinstance(text, str) or not text.strip() or len(text) > 280:
                raise ValueError(f"{section} text must be 1..280 characters")
            if section == "actions" and "text" in row and row["text"] != text:
                raise ValueError("actions.title is canonical; an optional text alias must exactly match title")
            refs = row.get("source_ids")
            if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in known_ids for ref in refs):
                raise ValueError("Every factual row needs a list of resolvable source_ids")
            if section != "summary":
                row.setdefault("status", "unknown")
                nonempty_text(row["status"], f"{section}.status")
            if section in ("actions", "decisions"):
                nonempty_text(row.get("id"), f"{section}.id")
            if section == "actions":
                row.setdefault("owner", None)
                row.setdefault("due", None)
                if row["owner"] is not None:
                    nonempty_text(row["owner"], "action.owner")
                if row["due"] is not None:
                    timestamp(row["due"], "action.due")
            normalized_rows.append(row)
        normalized[section] = normalized_rows
    return normalized


def read_brief(path):
    path = Path(path)
    if path.stat().st_size > 1024 * 1024:
        raise ValueError("Brief exceeds 1 MiB")
    return validate_brief(json.loads(path.read_text(encoding="utf-8")))


def h(value):
    return escape(str(value), quote=True)


def refs(item):
    return " ".join(f'<a href="#source-{h(i)}">[{h(i)}]</a>' for i in item["source_ids"])


def source_list(data):
    return "".join(f'<li id="source-{h(source["id"])}">{source_markup(data, source)}</li>'
                   for source in data["sources"])


def source_markup(data, source):
    fields = (("system", "System"), ("group_id", "Group ID"),
              ("record_id", "Record ID"), ("timestamp", "Timestamp"))
    metadata = " · ".join(f'{h(ui(data, label))} <bdi>{h(source[key])}</bdi>'
                          for key, label in fields if source.get(key) is not None)
    link = ""
    if source.get("url"):
        validate_source_url(source["url"])
        link = f' <a href="{h(source["url"])}" target="_blank" rel="noreferrer noopener">{h(ui(data, "Open source"))}</a>'
    return f'<b>{h(source["id"])}</b> {h(source["label"])}<br><small>{metadata}</small>{link}'


def source_registry(data):
    # JSON remains lossless while no untrusted closing tag can escape the inert element.
    payload = json.dumps(data["sources"], ensure_ascii=False, separators=(",", ":"))
    for character, escaped in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                               ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        payload = payload.replace(character, escaped)
    return f'<script type="application/json" id="source-registry">{payload}</script>'


def save_text(path, text):
    path = Path(path)
    if path.exists():
        raise ValueError(f"Output exists; choose a new output path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path.resolve())


def disclosures(data):
    phrase = "Synthetic demo" if data["synthetic"] else "Private project snapshot"
    return ui(data, phrase) + ". " + data["coverage"]["note"]



def brand_logo():
    """Embed the bundled original PNG unchanged; no network or image conversion."""
    asset = Path(__file__).resolve().parent.parent / "assets" / "brand" / "anyx-logo.png"
    encoded = base64.b64encode(asset.read_bytes()).decode("ascii")
    return f'<img class="brand-logo" src="data:image/png;base64,{encoded}" alt="Anyx" width="56" height="56">'


def run_cli(main):
    """Emit machine-readable local input/file errors instead of a traceback."""
    try:
        main()
    except (ValueError, OSError, RecursionError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)]}, ensure_ascii=False))
        raise SystemExit(1) from None
