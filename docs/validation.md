# Validation evidence

**TLDR:** Alpha.3 passes 63 local tests and eight portable skill checks. A fresh 124-second MP4 uses the revised text timeline, original logo and clarified synthetic group scope; ten scene-midpoint frames were inspected. Real Chrome checks cover PDF geometry and desktop/mobile artifacts. Live MCP evidence is a separate pilot record.

Reviewed on 17 November 2026, Asia/Jerusalem. All conversations, projects, external records and media demos are synthetic.



## Current alpha.3 integration checks

This local revision integrates the independent review fixes onto branded source `8387975a5a45f5053afe1702fa8f8a16559424f5`. The original PNG, all four byte-identical asset copies, eight-skill structure and binary ZIP packaging are preserved.

| Layer | Observed result |
| --- | --- |
| Automated suite | 63 tests passed without skips: the 36 alpha.2 cases plus 27 new regressions. The original replay scenarios were not edited. |
| Input and time bounds | Malformed containers, rows and excessively nested JSON produce clean errors. Missing optional arrays normalize consistently. Evidence cutoff cannot precede the window start; known source timestamps cannot exceed it. A requested end after cutoff requires partial coverage. |
| Sync structure | Approved state requires an authorization reference in either mode. Exact identifier, business-key, receipt and ledger-reference types and SHA-256 base format are checked. Validation still performs zero remote writes and does not authenticate grants or receipts. |
| Independent batches | The full ledger retains unknown outcomes. A separate independent execute batch preserves operation IDs, keys, bases and provenance; unresolved or unverified dependencies remain blocked. Live freshness and reconciliation remain executor responsibilities. |
| Video pacing | Visible text, including repeated brand/footer, receives a heuristic 20 Unicode codepoints per second with a four-second minimum. Default total limit is 180 seconds; an explicit 60-second limit rejects the 124-second demo before creating output. Rows, statuses, owners, deadlines, conditions and source markers are retained. |
| Actual PDF geometry | Existing local Chrome printed the independent Hebrew brief at initial viewports 390 and 1440. Six pages per run matched 1280×720 CSS pixels / 960×540 PDF points, with one logo image on each page. A deliberately stalled browser operation verified named timeouts and cleanup limited to its own test process tree. |
| New actual video | Hyperframes 0.9.61 rendered 124.000 seconds, 1280×720 H.264, 24 fps, 2,976 frames and no audio. This is a new alpha.3 render, rather than evidence reused from an earlier 40-second MP4. |
| Visual inspection | All ten actual video midpoint frames, dashboard at desktop/mobile and all ten deck slides at desktop/mobile were inspected. Original image bytes, visible branding, conditions and per-job material distinctions were retained, with no blocking clipping. Browser inspection observed no script errors or outbound attempts. |
| Current-source binding | Regeneration with the final validators produced byte-identical dashboard, deck and video composition HTML to the reviewed render inputs. |
| Imported tools | All eight reading references and installation guidance distinguish useful legacy core reads from long-text recovery requiring actually imported tools and returned references. Any truncation flag makes the affected field incomplete. |

The shipped demonstration is a synthetic group briefing: J42 decisions and scope are separate from J21/J22/J25 materials. Its three portable skill copies share that clarified example. Independent replay fixtures retain their separate scenario contexts. No live group identity, customer content, credentials or private pilot result was copied into public code or examples.

These automated and rendering checks are local. The browser check explicitly skips on a machine without its existing Node/Chrome/puppeteer-core/pypdf dependencies; it actually executed in this run. The pacing budget aids review and does not prove human reading speed. Sampling ten video frames is narrower than checking every frame. Native live MCP, clean-host discovery and destination writes require their own evidence; the local validator cannot establish them.

## Historical alpha.2 branding checks

Version `0.1.0-alpha.2` was a branding update. The validation and timing changes below were not included in that earlier version.

| Layer | Observed result |
| --- | --- |
| Automated suite | 36 tests passed: 32 existing cases plus four dedicated branding tests. |
| Original asset | Canonical PNG and all three skill copies match SHA-256 `4b898fa294753d522b6a5c39475f0a430e01b5127cb0bfb39e208d29b80d3f43`, 1,303,035 bytes each. |
| Actual output image | Each skill was unpacked from its ZIP and run from an unrelated working directory. Independently decoded PNG data URIs match the original bytes. There is one persistent logo in each HTML document, with proportional contain sizing. |
| Binary packaging | Extracted PNGs from three skill ZIPs and the full-kit ZIP match the original. Full-kit branding guidance is included. Existing archive reproducibility and private-state exclusion checks passed. |
| Image policy | Dashboard CSP permits `data:` images without remote image origins. Existing escaping and source-registry checks passed with only the trusted logo image allowed. |
| Portable structure | Eight skills passed frontmatter and self-contained-reference checks. |
| Regenerated public examples | Dashboard and all ten HTML slides opened in local Chrome at desktop and mobile widths. The original image loaded and remained visible with contain sizing. A local Chrome print produced ten PDF pages with the logo on every page, also inspected after rasterization. |
| Branded MP4 | The public video example was rendered again: H.264, 1280x720, 24fps, 40 seconds, no audio. Ten frames sampled at each scene midpoint showed the original logo without cropping or distortion. |

All examples are synthetic and English. This branding QA used local Chrome and sampled video frames. It does not establish other browser behavior, every video frame, general caption readability or live MCP behavior. The pre-existing four-second scene timing is unchanged in this branding-only release. No live Anyx or destination records were read for these checks.

## Historical alpha.1 evidence

The evidence below predates the original-logo integration. Its 32-test count, five workflow cases and rendering observations describe alpha.1, rather than extra alpha.2 checks.

| Layer | Observed result |
| --- | --- |
| Portable skills | Eight self-contained folders passed skill-creator validation and package reference checks. |
| Automated suite | 32 tests passed, covering replay, UTF-8, archives, source-backed briefs, escaping, credential URLs, provenance, rendering limits and sync-plan preconditions. |
| Independent workflows | Five reviewed Hebrew results: catch-up, materials, decision log, project control and workspace sync. |
| Dashboard | Generated offline HTML opened in Chrome. Layout, evidence and status filtering were observed. |
| Presentation | Ten-slide HTML deck opened in Chrome. Cover, content navigation and source readability were observed. No PPTX was produced. |
| Video | Hyperframes 0.9.61 rendered H.264 at 1280x720, 24fps, 40 seconds, without audio. FFprobe verified the stream. Opening, middle and closing frames were inspected. |
| Hebrew | UI labels, unknown fields and lossless source-registry round-trip passed focused checks. A Hebrew composition was generated. The MP4 inspected here is English. |
| Public source baseline | Two reviewed MCP documentation files are pinned by hashes in upstream-sources.json. |

The video runtime used Node 22.17.0, Hyperframes 0.9.61, Chrome and private FFmpeg/FFprobe paths. Runtime executables and node_modules are excluded from source control and archives. No paid media generation was used. External tools keep their own licenses.

Hyperframes lint reported zero errors and 11 nonblocking editor-structure warnings. These recommend more sub-compositions for editing. The render used strict errors and no best-effort capture fallback. Every new real brief still needs its own visual inspection.

## Behavioral checks

Catch-up completed pages and three UTF-8 chunks, retaining the difference between a reported reassignment and an accepted commitment. Materials kept corrections, cancellations, exact units and missing fields. Decision log preserved conditional and withdrawn approvals.

Project control completed an empty continuation page and kept the work hold, CRM signature evidence, accepted supplier check, failing CI and missing deployment distinct. Sync reconciled a prior timeout from an operation-specific simulated audit receipt without retrying, then held a proposal affected by a concurrent human edit. The existing scoped policy remained valid.

The five cases used 26 simulated Anyx calls. No live Anyx account or customer records were read. Destination observations were fictional supplied records. Fixed fixtures do not establish actual transport, expiry, capture completeness, transaction or server-idempotency behavior.

## Remaining verification

- Clean-host skill discovery, live MCP authentication and an authorized synthetic group pilot.
- Actual destination connections. The 15 systems in systems-compatibility.md are API/mapping candidates, not fifteen implemented authenticated integrations.
- Native presentation formats. The portable helper creates HTML slides; other formats require a real host backend.
- Fresh remote versions and user authority. The sync helper validates plan structure and performs no remote writes.
- New real output quality. A prepared composition is not an MP4, and local HTML has no live data connection.
- Search indexing, traffic, useful customer activation and model recommendations.

## Reproduce

Run `python tools/validate_kit.py`, `python -m unittest discover -s tests` and `python tools/build_skill_zips.py`. The generated manifest records per-artifact SHA-256 values. Archives normalize text line endings and exclude private validation state and runtime dependencies.

Optional `python tools/check_upstream.py --check` reads bounded public sources and never rewrites instructions. Original test traces remain in ignored .validation folders. Public examples are labeled synthetic.

