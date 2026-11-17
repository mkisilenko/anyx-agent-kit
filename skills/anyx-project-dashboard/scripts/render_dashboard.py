"""Render a source-backed local dashboard. No network, publication or live connection."""
import argparse
import hashlib
from brief_support import brand_logo, disclosures, h, read_brief, refs, save_text, source_list, source_registry, status_label, ui

def render(data):
    project = data["project"]
    cards = "".join(f'<article><h2>{h(x["text"])}</h2><p>{refs(x)}</p></article>' for x in data["summary"])
    rows = "".join(f'<tr data-status="{h(x.get("status") or "unknown")}"><td>{h(x["id"])}</td><td>{h(x["title"])}</td>'
                   f'<td>{h(x.get("owner") or ui(data,"Unassigned"))}</td><td>{h(status_label(data,x.get("status")))}</td>'
                   f'<td>{h(x.get("due") or ui(data,"Unknown"))}</td><td>{refs(x)}</td></tr>' for x in data["actions"])
    decisions = "".join(f'<li><b>{h(status_label(data,x.get("status")))}</b> {h(x["text"])} {refs(x)}</li>' for x in data["decisions"])
    risks = "".join(f'<li><b>{h(status_label(data,x.get("status")))}</b> {h(x["text"])} {refs(x)}</li>' for x in data["risks"])
    script = "document.getElementById('status').addEventListener('change',function(){document.querySelectorAll('tbody tr').forEach(r=>r.hidden=this.value!=='all'&&r.dataset.status!==this.value);});"
    import base64
    digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
    options = "".join(f'<option value="{h(status)}">{h(status_label(data,status))}</option>'
                      for status in sorted({str(action.get("status") or "unknown") for action in data["actions"]}))
    direction = "rtl" if data["language"] == "he" else "ltr"
    return f"""<!doctype html><html lang="{data["language"]}" dir="{direction}"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'sha256-{digest}'">
<title>{h(project["title"])} | Anyx</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#091512;color:#eff8f1;font:17px/1.5 system-ui,sans-serif}}
main{{max-width:1120px;margin:auto;padding:42px 28px}}a{{color:#a8fac3}}header{{border-bottom:1px solid #395145;padding-bottom:24px}}
.brand{{display:flex;align-items:center;gap:12px;direction:ltr;font-weight:800;letter-spacing:.12em;color:#a8fac3}}h1{{font-size:clamp(32px,5vw,54px);line-height:1.08;margin:18px 0}}
.brand-logo{{display:block;width:56px;height:56px;object-fit:contain;flex-shrink:0}}
.meta,small{{color:#b7cbbd}}.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin:28px 0}}
article{{background:#15291f;padding:22px;border-radius:12px;border:1px solid #36563d}}article h2{{font-size:23px;line-height:1.3;margin:0}}
.stats{{display:flex;gap:30px;flex-wrap:wrap;margin:28px 0}}.stats b{{font-size:34px;color:#a8fac3}}
table{{border-collapse:collapse;width:100%;font-size:15px}}th,td{{text-align:start;border-bottom:1px solid #36513d;padding:12px 8px;vertical-align:top}}
.scroll{{overflow:auto}}select{{padding:8px;color:#e5fbe9;background:#173423;border:1px solid #688d73}}section{{margin-top:34px}}
.notice{{border-inline-start:3px solid #a8fac3;padding:12px 18px;background:#14241b}}li{{margin:12px 0;overflow-wrap:anywhere}}footer{{margin-top:40px;color:#b7cbbd}}
</style><main><header><div class="brand">{brand_logo()}<span>ANYX AGENT KIT</span></div><h1>{h(project["title"])}</h1>
<p class="meta"><bdi>{h(project["id"])}</bdi> · {h(ui(data,"Data as of"))} <bdi>{h(project["data_as_of"])}</bdi></p>
<p class="meta"><bdi>{h(project["period"]["start"])}</bdi> {h(ui(data,"to"))} <bdi>{h(project["period"]["end"])}</bdi> · <bdi>{h(project["period"]["timezone"])}</bdi></p></header>
<p class="notice">{h(disclosures(data))} {h(ui(data,"This file is a snapshot and has no live data connection."))}</p>
<div class="stats"><div><b>{len(data["actions"])}</b><br>{h(ui(data,"actions in this brief"))}</div><div><b>{len(data["risks"])}</b><br>{h(ui(data,"risks recorded"))}</div><div><b>{len(data["sources"])}</b><br>{h(ui(data,"source references"))}</div></div>
<div class="summary">{cards}</div><section><h2>{h(ui(data,"Actions"))}</h2><label>{h(ui(data,"Status"))} <select id="status"><option value="all">{h(ui(data,"all"))}</option>{options}</select></label>
<div class="scroll"><table><thead><tr><th>{h(ui(data,"ID"))}</th><th>{h(ui(data,"Action"))}</th><th>{h(ui(data,"Owner"))}</th><th>{h(ui(data,"Status"))}</th><th>{h(ui(data,"Due"))}</th><th>{h(ui(data,"Evidence"))}</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>{h(ui(data,"Decisions"))}</h2><ul>{decisions}</ul></section><section><h2>{h(ui(data,"Risks and missing checks"))}</h2><ul>{risks}</ul></section>
<section><h2>{h(ui(data,"Sources"))}</h2><ol>{source_list(data)}</ol></section><footer>{h(ui(data,"Prepared with"))} <a href="https://anyx.app">Anyx</a>. {h(ui(data,"Sharing and publishing require an approved destination."))}</footer>
</main>{source_registry(data)}<script>{script}</script></html>"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(save_text(args.output, render(read_brief(args.input))))

