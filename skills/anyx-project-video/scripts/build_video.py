"""Prepare a local Hyperframes composition and optionally render/verify a real MP4."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
from brief_support import disclosures, h, item_details, read_brief, ui


def append_scenes(scenes, label, headline, lines):
    page = []
    characters = 0
    for line in lines:
        if len(line) > 420:
            raise ValueError("Video caption is too long. Prepare a shorter reviewed caption without dropping conditions.")
        if page and (len(page) >= 2 or characters + len(line) > 420):
            scenes.append((label, headline, page))
            page = []
            characters = 0
        page.append(line)
        characters += len(line)
    if page:
        scenes.append((label, headline, page))

def build(data, output):
    output=Path(output)
    if output.exists():
        raise ValueError("Choose a new output directory; existing output is not overwritten")
    title=data["project"]["title"]
    scenes=[]
    append_scenes(scenes,ui(data,"Project update"),title,[disclosures(data)])
    for key,label in [("summary","Current picture"),("decisions","Decisions and conditions"),("actions","Actions for review"),("risks","Risks and missing checks")]:
        lines=[]
        for item in data[key]:
            text=item.get("text",item.get("title",""))
            detail=item_details(data,item,action=key=="actions")
            markers=" ".join("["+source_id+"]" for source_id in item["source_ids"])
            line=(detail+" · " if detail else "")+text+" "+markers
            lines.append(line)
        append_scenes(scenes,ui(data,label),ui(data,label),lines)
    source_lines=[ui(data,"Sources")+" · ["+source["id"]+"]" for source in data["sources"]]
    append_scenes(scenes,ui(data,"Evidence and coverage"),ui(data,"Source registry travels with this video"),[data["coverage"]["note"]]+source_lines)
    if len(scenes)>15:
        raise ValueError("Video exceeds 60 seconds. Prepare a shorter reviewed brief without dropping conditions.")
    duration=len(scenes)*4
    output.mkdir(parents=True)
    cards=""
    for i,(label,headline,lines) in enumerate(scenes):
        cards+=f'<section class="clip scene" id="scene-{i}" data-start="{i*4}" data-duration="4" data-track-index="{i}"><div class="label">{h(label)}</div><h1>{h(headline)}</h1>'
        cards+="".join(f'<p>{h(line)}</p>' for line in lines)
        cards+="</section>"
    direction="rtl" if data["language"]=="he" else "ltr"
    content=f"""<!doctype html><html lang="{data["language"]}" dir="{direction}"><head><meta charset="utf-8"><title>{h(title)}</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:1280px;height:720px;background:#091812;color:#f0faef;overflow:hidden;font-family:Arial,sans-serif}}
#root{{position:relative;width:1280px;height:720px;overflow:hidden}}.scene{{position:absolute;inset:0;padding:110px 86px 100px;background:#10291b}}
.label{{font-size:24px;color:#aaf3b6;letter-spacing:.08em}}h1{{font-size:53px;line-height:1.08;max-width:1050px;margin:28px 0 35px;overflow-wrap:anywhere}}
p{{font-size:28px;line-height:1.35;max-width:1050px;margin:18px 0;overflow-wrap:anywhere}}.brand{{position:absolute;top:36px;left:86px;font-size:20px;letter-spacing:.16em;color:#aaf3b6;z-index:20}}
.footer{{position:absolute;bottom:25px;left:86px;right:60px;font-size:16px;color:#bad2c0;z-index:20}}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1280" data-height="720" data-fps="24" data-no-timeline>
{cards}<div class="brand">ANYX AGENT KIT</div><div class="footer">{h(data["project"]["data_as_of"])} · {h(ui(data,"Synthetic demo" if data["synthetic"] else "Private snapshot"))} · {h(ui(data,"Captured context, review required"))} · anyx.app</div></div></body></html>"""
    (output/"index.html").write_text(content,encoding="utf-8")
    (output/"brief.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result={"artifact_kind":"composition","rendered":False,"verified":False,"duration_seconds":duration,
            "width":1280,"height":720,"audio":"none","source_registry":"brief.json",
            "render_command":["hyperframes","render",".","--output","project-update.mp4","--fps","24","--quality","draft","--workers","1","--strict","--no-best-effort"]}
    (output/"result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return output,result

def render_project(output,result,cli,node,runtime_bin=None,browser_path=None):
    cli=Path(cli).resolve()
    if not cli.is_file():
        raise ValueError("Provide the actual installed official Hyperframes CLI .mjs path")
    env=os.environ.copy()
    env.update({"HYPERFRAMES_NO_TELEMETRY":"1","DO_NOT_TRACK":"1",
                "HYPERFRAMES_NO_UPDATE_CHECK":"1","HYPERFRAMES_SKIP_SKILLS":"1"})
    if runtime_bin:
        old_path=next((v for k,v in env.items() if k.upper()=="PATH"),"")
        for key in list(env):
            if key.upper()=="PATH":del env[key]
        env["PATH"]=str(Path(runtime_bin).resolve())+os.pathsep+old_path
    if browser_path:
        env["HYPERFRAMES_BROWSER_PATH"]=str(Path(browser_path).resolve())
    if not shutil.which("ffmpeg",path=env.get("PATH")) or not shutil.which("ffprobe",path=env.get("PATH")):
        raise ValueError("Local rendering requires FFmpeg and FFprobe on the supplied runtime PATH")
    env["HYPERFRAMES_FFMPEG_PATH"]=shutil.which("ffmpeg",path=env.get("PATH"))
    env["HYPERFRAMES_FFPROBE_PATH"]=shutil.which("ffprobe",path=env.get("PATH"))
    destination=output/"project-update.mp4"
    command=[node,str(cli),"render",str(output),"--output",str(destination),"--fps","24",
             "--quality","draft","--workers","1","--strict","--no-best-effort"]
    process=subprocess.run(command,cwd=output,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=process.stdout.decode("utf-8",errors="replace")
    (output/"render.log").write_text(log,encoding="utf-8")
    if process.returncode or not destination.exists():
        raise RuntimeError("Hyperframes did not produce a verified video; inspect render.log")
    probe=subprocess.run([shutil.which("ffprobe",path=env.get("PATH")),"-v","error",
                          "-show_entries","stream=width,height,codec_name","-show_entries","format=duration",
                          "-of","json",str(destination)],capture_output=True,check=True)
    metadata=json.loads(probe.stdout)
    stream=next(s for s in metadata["streams"] if "width" in s)
    duration=float(metadata["format"]["duration"])
    if stream["width"]!=1280 or stream["height"]!=720 or not result["duration_seconds"]-0.2<=duration<=result["duration_seconds"]+0.2:
        raise ValueError("Rendered video geometry/duration mismatch")
    result.update({"artifact_kind":"mp4","rendered":True,"verified":True,
                   "file":"project-update.mp4","duration_seconds":duration,"codec":stream["codec_name"]})
    (output/"result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True,help="New project directory")
    parser.add_argument("--render",action="store_true")
    parser.add_argument("--hyperframes-cli",help="Trusted installed hyperframes/bin/hyperframes.mjs")
    parser.add_argument("--node",default="node")
    parser.add_argument("--runtime-bin",help="Optional directory containing FFmpeg/FFprobe")
    parser.add_argument("--browser-path",help="Optional trusted installed Chrome executable")
    args=parser.parse_args()
    output,result=build(read_brief(args.input),Path(args.output).resolve())
    if args.render:
        if not args.hyperframes_cli:
            parser.error("--render requires --hyperframes-cli")
        result=render_project(output,result,args.hyperframes_cli,args.node,args.runtime_bin,args.browser_path)
    print(json.dumps(result,indent=2))

