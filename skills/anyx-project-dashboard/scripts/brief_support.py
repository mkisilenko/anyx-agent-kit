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
    if data.get("schema_version") != 1 or type(data.get("synthetic")) is not bool:
        raise ValueError("schema_version=1 and explicit synthetic boolean are required")
    if data.get("language") not in ("en", "he"):
        raise ValueError("language must be en or he")
    project = data.get("project", {})
    if not project.get("id") or not isinstance(project.get("title"),str) or not 1<=len(project["title"])<=120:
        raise ValueError("Project id/title required")
    period = project.get("period", {})
    start = timestamp(period.get("start"), "period.start")
    end = timestamp(period.get("end"), "period.end")
    timestamp(project.get("data_as_of"), "project.data_as_of")
    if end <= start or not period.get("timezone"):
        raise ValueError("Positive bounded period and timezone required")
    coverage = data.get("coverage", {})
    if coverage.get("status") not in ("partial", "complete_capture_not_asserted") or not coverage.get("note"):
        raise ValueError("Explicit coverage limitations required")
    sources = data.get("sources", [])
    ids = [s.get("id") for s in sources]
    if len(ids) != len(set(ids)) or any(not isinstance(i, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", i) for i in ids):
        raise ValueError("Unique safe source IDs required")
    for source in sources:
        if not source.get("label") or not source.get("system"):
            raise ValueError("Source system and label required")
        if source.get("timestamp"):
            timestamp(source["timestamp"], "source.timestamp")
        validate_source_url(source.get("url"))
    for section in SECTIONS:
        rows = data.get(section, [])
        if not isinstance(rows, list) or len(rows) > 40:
            raise ValueError(f"{section} must be a bounded list, maximum 40")
        for item in rows:
            text = item.get("title" if section == "actions" else "text")
            if not isinstance(text, str) or not text.strip() or len(text) > 280:
                raise ValueError(f"{section} text must be 1..280 characters")
            refs = item.get("source_ids", [])
            if not refs or any(ref not in ids for ref in refs):
                raise ValueError("Every factual row needs resolvable source_ids")
            if section == "actions" and item.get("due"):
                timestamp(item["due"], "action.due")
    return data


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
