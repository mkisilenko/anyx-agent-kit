"""Render an offline HTML slide deck. This helper does not create a PPTX."""
import argparse
from brief_support import disclosures, h, item_details, read_brief, save_text, source_markup, source_registry, ui

def render(data):
    project=data["project"]
    pages=[(project["title"],f'<p class="intro"><bdi>{h(project["id"])}</bdi></p><p>{h(disclosures(data))}</p><p>{h(ui(data,"Data as of"))} <bdi>{h(project["data_as_of"])}</bdi></p>')]
    for section,label in [("summary","Project summary"),("decisions","Decisions"),("actions","Actions"),("risks","Risks and missing checks")]:
        entries=[]
        characters=0
        for row in data[section]:
            title=row.get("text",row.get("title",""))
            detail=item_details(data,row,action=section=="actions")
            markers=" ".join("["+source_id+"]" for source_id in row["source_ids"])
            size=len(title)+len(detail)+len(markers)
            if size>520:
                raise ValueError("Slide entry is too long. Prepare a shorter reviewed entry without dropping conditions.")
            if entries and (len(entries)>=2 or characters+size>520):
                pages.append((ui(data,label),"".join(entries)))
                entries=[]
                characters=0
            entries.append(f'<div class="entry"><p>{h(title)}</p><small>{h(detail)} {h(markers)}</small></div>')
            characters+=size
        if entries:
            pages.append((ui(data,label),"".join(entries)))
    for start in range(0,len(data["sources"]),2):
        body="".join(f'<p class="source" id="source-{h(source["id"])}">{source_markup(data,source)}</p>'
                     for source in data["sources"][start:start+2])
        pages.append((ui(data,"Sources"),body))
    period=project["period"]
    footer=f'<bdi>{h(period["start"])}</bdi> {h(ui(data,"to"))} <bdi>{h(period["end"])}</bdi> · <bdi>{h(period["timezone"])}</bdi>'
    sections="".join(f'<section class="slide" id="slide-{i}"><div class="brand">ANYX AGENT KIT</div><h1>{h(title)}</h1>{body}<footer>{footer} · {i+1}/{len(pages)}</footer></section>' for i,(title,body) in enumerate(pages))
    direction="rtl" if data["language"]=="he" else "ltr"
    script="let i=0;const s=[...document.querySelectorAll('.slide')];function show(n){i=Math.max(0,Math.min(s.length-1,n));s.forEach((e,j)=>e.hidden=j!==i);document.getElementById('page').textContent=(i+1)+' / '+s.length}document.getElementById('next').onclick=()=>show(i+1);document.getElementById('previous').onclick=()=>show(i-1);document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1)});show(0);"
    return f"""<!doctype html><html lang="{data["language"]}" dir="{direction}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(project["title"])} | Anyx {h(ui(data,"presentation"))}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#06100c;color:#f5faf4;font:26px/1.35 system-ui,sans-serif}}
.slide{{position:relative;max-width:1280px;min-height:720px;margin:auto;padding:54px 72px 82px;background:#10251a}}.slide[hidden]{{display:none}}
.brand{{font-size:17px;letter-spacing:.18em;color:#b1f5bc;font-weight:800}}h1{{font-size:48px;line-height:1.08;max-width:1000px;margin:34px 0}}
.intro{{font-size:34px;color:#b1f5bc}}.entry{{border-top:1px solid #4c6953;margin-top:23px;padding-top:12px}}p{{max-width:1050px;margin:14px 0}}
small{{font-size:18px;color:#bed1c0}}.source{{font-size:22px;overflow-wrap:anywhere}}a{{color:#b1f5bc}}footer{{position:absolute;bottom:24px;font-size:14px;color:#bed1c0}}
nav{{display:flex;justify-content:center;align-items:center;gap:18px;padding:16px}}button{{font:18px system-ui;padding:9px 18px;background:#b1f5bc;border:0;border-radius:6px;cursor:pointer}}
@media(max-width:800px){{.slide{{padding:32px 24px 80px;min-height:100vh}}h1{{font-size:36px}}body{{font-size:21px}}}}
@media print{{@page{{size:16in 9in;margin:0}}nav{{display:none}}.slide,.slide[hidden]{{display:block!important;break-after:page;width:1280px;height:720px;margin:0}}}}
</style>{sections}<nav aria-label="{h(ui(data,"Slide navigation"))}"><button id="previous">{h(ui(data,"Previous"))}</button><span id="page"></span><button id="next">{h(ui(data,"Next"))}</button></nav>{source_registry(data)}<script>{script}</script></html>"""

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    print(save_text(args.output,render(read_brief(args.input))))

