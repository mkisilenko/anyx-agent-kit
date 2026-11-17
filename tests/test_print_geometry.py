"""Actual local Chromium print geometry, with no network or package installation.

The browser test runs when Node, installed Chrome, existing puppeteer-core and
pypdf are present. An unavailable browser dependency is an explicit skip, not
evidence that PDF geometry passed on that machine.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest

from test_renderers import brief

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "skills/anyx-project-presentation/scripts/render_presentation.py"

BROWSER_CHECK = r"""
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const require=createRequire(import.meta.url);
const puppeteer=require(process.env.ANYX_QA_PUPPETEER);
const directory=process.env.ANYX_QA_DIRECTORY;
let browser;
const report={views:[],blocked_requests:[],stage:'launch',browser_pid:null,error:null};
function note(stage){
  report.stage=stage;
  fs.writeFileSync(path.join(directory,'progress.json'),JSON.stringify({
    stage,browser_pid:report.browser_pid}));
}
async function step(label,operation,milliseconds=10000){
  note(label);
  let timer;
  const forced=process.env.ANYX_QA_FORCE_TIMEOUT_STAGE===label;
  try {
    return await Promise.race([
      forced?new Promise(()=>{}):operation(),
      new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error(
        `Print QA timed out at ${label} after ${forced?200:milliseconds}ms`)),forced?200:milliseconds);})
    ]);
  }finally{clearTimeout(timer);}
}
function killOwnedBrowser(){
  const child=browser?.process();
  if(!child || child.exitCode!==null)return;
  // The PID comes only from this Puppeteer launch, never from a global lookup.
  if(process.platform==='win32'){
    const killed=spawnSync('taskkill.exe',['/PID',String(child.pid),'/T','/F'],
      {windowsHide:true,timeout:5000,encoding:'utf8'});
    report.forced_browser_cleanup={pid:child.pid,status:killed.status,error:killed.error?.message};
  }else{
    try{child.kill('SIGKILL');}catch(error){report.cleanup_error=error.message;}
  }
}
const watchdog=setTimeout(()=>{
  report.error=`Print QA exceeded 45s total budget at ${report.stage}`;
  killOwnedBrowser();
  // If launch has not returned, leave Node alive for the Python process-tree
  // watchdog; killing Node alone at that point could orphan its Chrome child.
  if(browser)process.stdout.write(JSON.stringify(report),()=>process.exit(1));
},45000);
try {
  note('launch');
  browser=await puppeteer.launch({executablePath:process.env.ANYX_QA_CHROME,
    userDataDir:path.join(directory,'browser-profile'),headless:true,
    timeout:12000,protocolTimeout:10000,args:[
      '--no-first-run','--no-default-browser-check','--disable-extensions',
      '--disable-background-networking','--disable-component-update','--disable-sync',
      '--no-pings','--force-color-profile=srgb']});
  report.browser_pid=browser.process().pid;
  for(const width of [390,1440]) {
    const page=await step(`${width}:new_page`,()=>browser.newPage());
    page.setDefaultTimeout(10000);page.setDefaultNavigationTimeout(10000);
    await step(`${width}:interception`,()=>page.setRequestInterception(true));
    page.on('request',request=>{
      if(/^(file:|data:|about:)/.test(request.url()))request.continue();
      else{report.blocked_requests.push(request.url());request.abort();}
    });
    await step(`${width}:viewport`,()=>page.setViewport({width,height:900}));
    await step(`${width}:load`,()=>page.goto(pathToFileURL(path.join(directory,'deck.html')).href,{waitUntil:'load'}));
    await step(`${width}:print_media`,()=>page.emulateMediaType('print'));
    await step(`${width}:fonts`,()=>page.evaluate(()=>document.fonts.ready));
    const initialPrint=await step(`${width}:initial_geometry`,()=>page.evaluate(()=>({
      headingFont:getComputedStyle(document.querySelector('h1')).fontSize,
      slideHeight:document.querySelector('.slide').getBoundingClientRect().height})));
    // Inspect coordinates on the print page's CSS canvas, rather than on the
    // narrow screen viewport where an overflowing RTL box is right aligned.
    // The PDF MediaBox below independently verifies this canvas's physical size.
    await step(`${width}:print_canvas`,()=>page.setViewport({width:1280,height:720}));
    const geometry=await step(`${width}:geometry`,()=>page.evaluate(()=>{
      const rect=element=>{const r=element.getBoundingClientRect();
        return{x:r.x,y:r.y,width:r.width,height:r.height};};
      const logo=document.querySelector('.brand-logo');
      return{slides:[...document.querySelectorAll('.slide')].map(slide=>({
        box:rect(slide),heading:rect(slide.querySelector('h1')),
        footer:rect(slide.querySelector('footer')),
        hidden:getComputedStyle(slide).display==='none'})),
        brand:rect(document.querySelector('.brand')),logo:{...rect(logo),
          naturalWidth:logo.naturalWidth,objectFit:getComputedStyle(logo).objectFit},
        headingFont:getComputedStyle(document.querySelector('h1')).fontSize};
    }));
    const pdf=path.join(directory,`deck-${width}.pdf`);
    await step(`${width}:pdf`,()=>page.pdf({path:pdf,preferCSSPageSize:true,printBackground:true,timeout:15000}),16000);
    report.views.push({width,pdf,initialPrint,...geometry});
    await step(`${width}:close_page`,()=>page.close(),3000);
  }
}catch(error){report.error=error.stack || error.message;}
finally{
  const failedStage=report.stage;
  if(browser){
    try{await step('close_browser',()=>browser.close(),3000);}
    catch(error){report.close_error=error.message;}
    finally{killOwnedBrowser();}
  }
  report.stage=failedStage;clearTimeout(watchdog);
}
process.stdout.write(JSON.stringify(report),()=>process.exit(report.error || report.close_error?1:0));
"""


def kill_owned_tree(process):
    """Terminate only this still-running test subprocess and its descendants."""
    if process.poll() is not None:
        return
    if os.name == "nt":
        result = subprocess.run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
                                capture_output=True, text=True, timeout=8)
        if result.returncode and process.poll() is None:
            raise RuntimeError(f"Could not stop owned test process tree {process.pid}: {result.stderr}")
    else:
        os.killpg(process.pid, signal.SIGKILL)


def run_browser(node, script, temporary, environment):
    """A Python backstop also covers a hung launch before Puppeteer returns."""
    options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
               else {"start_new_session": True})
    process = subprocess.Popen([node, str(script)], cwd=temporary, env=environment,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", **options)
    try:
        stdout, stderr = process.communicate(timeout=55)
    except subprocess.TimeoutExpired:
        progress = temporary / "progress.json"
        stage = progress.read_text(encoding="utf-8") if progress.exists() else "launch not reported"
        kill_owned_tree(process)
        stdout, stderr = process.communicate(timeout=5)
        raise AssertionError(f"Print QA process exceeded 55s; last progress={stage}; "
                             f"owned profile={temporary / 'browser-profile'}; stderr={stderr}") from None
    finally:
        if process.poll() is None:
            kill_owned_tree(process)
    return subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr)


class PrintGeometryChecks(unittest.TestCase):
    def browser_inputs(self, temporary):
        node = shutil.which("node")
        chrome = Path(os.environ.get("ANYX_PRINT_CHROME", "C:/Program Files/Google/Chrome/Application/chrome.exe"))
        puppeteer = Path(os.environ.get("ANYX_PRINT_PUPPETEER", str(
            ROOT / ".validation/hyperframes-runtime/node_modules/puppeteer-core")))
        if not node or not chrome.is_file() or not (puppeteer / "package.json").is_file():
            self.skipTest("Local Node/Chrome/puppeteer-core unavailable; no installation attempted")
        if importlib.util.find_spec("pypdf") is None:
            self.skipTest("Local pypdf unavailable; no installation attempted")
        source = temporary / "brief.json"
        source.write_text(json.dumps(brief(), ensure_ascii=False), encoding="utf-8")
        process = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(RENDERER), "--input", str(source),
             "--output", str(temporary / "deck.html")], cwd=temporary,
            capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        script = temporary / "check.mjs"
        script.write_text(BROWSER_CHECK, encoding="utf-8")
        environment = dict(os.environ, ANYX_QA_DIRECTORY=str(temporary),
                           ANYX_QA_CHROME=str(chrome), ANYX_QA_PUPPETEER=str(puppeteer))
        environment.pop("ANYX_QA_FORCE_TIMEOUT_STAGE", None)
        return node, script, environment

    def test_actual_print_pages_match_slide_boxes_and_brand_inset(self):
        # Cleanup must not hide the useful browser failure if a profile remains
        # locked. The owned-process watchdog runs before this context exits.
        with tempfile.TemporaryDirectory(prefix="anyx-print-geometry-", ignore_cleanup_errors=True) as directory:
            temporary = Path(directory)
            node, script, environment = self.browser_inputs(temporary)
            from pypdf import PdfReader
            checked = run_browser(node, script, temporary, environment)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertEqual(report["blocked_requests"], [])
            for view in report["views"]:
                with self.subTest(viewport=view["width"]):
                    self.assertEqual(view["initialPrint"]["headingFont"], "48px")
                    self.assertAlmostEqual(view["initialPrint"]["slideHeight"], 720, delta=0.1)
                    self.assertEqual(len(view["slides"]), 6)
                    pdf = PdfReader(view["pdf"])
                    self.assertEqual(len(pdf.pages), len(view["slides"]))
                    for index, (page, slide) in enumerate(zip(pdf.pages, view["slides"])):
                        self.assertAlmostEqual(float(page.mediabox.width), 960, delta=0.1)
                        self.assertAlmostEqual(float(page.mediabox.height), 540, delta=0.1)
                        self.assertEqual(len(page.images), 1)
                        self.assertFalse(slide["hidden"])
                        self.assertAlmostEqual(slide["box"]["width"], 1280, delta=0.1)
                        self.assertAlmostEqual(slide["box"]["height"], 720, delta=0.1)
                        self.assertAlmostEqual(slide["box"]["x"], 0, delta=0.1)
                        self.assertAlmostEqual(slide["box"]["y"], index * 720, delta=0.1)
                        self.assertGreater(slide["heading"]["y"], slide["box"]["y"] + 76)
                        footer = slide["footer"]
                        self.assertLessEqual(footer["y"] + footer["height"], (index + 1) * 720)
                    self.assertEqual(view["headingFont"], "48px")
                    self.assertAlmostEqual(view["brand"]["x"], 72, delta=0.1)
                    self.assertAlmostEqual(view["brand"]["y"], 20, delta=0.1)
                    self.assertGreater(view["logo"]["naturalWidth"], 0)
                    self.assertEqual(view["logo"]["objectFit"], "contain")
        self.assertFalse(temporary.exists(), f"Owned browser profile was not released: {temporary}")

    def test_browser_timeout_reports_stage_and_releases_its_own_profile(self):
        with tempfile.TemporaryDirectory(prefix="anyx-print-geometry-", ignore_cleanup_errors=True) as directory:
            temporary = Path(directory)
            node, script, environment = self.browser_inputs(temporary)
            environment["ANYX_QA_FORCE_TIMEOUT_STAGE"] = "390:pdf"
            checked = run_browser(node, script, temporary, environment)
            self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertIsInstance(report["browser_pid"], int)
            self.assertIn("timed out at 390:pdf", report["error"])
            self.assertEqual(report["stage"], "390:pdf")
            self.assertEqual(report["views"], [])
            self.assertFalse((temporary / "deck-390.pdf").exists())
        self.assertFalse(temporary.exists(), f"Timed-out browser left its profile locked: {temporary}")


if __name__ == "__main__":
    unittest.main()
